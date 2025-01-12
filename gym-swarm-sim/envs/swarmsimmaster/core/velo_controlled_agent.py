
import importlib
import logging
from core import matter
from core.swarm_sim_header import *
from core import agent
import numpy as np

DEFAULTS = {"flock_rad" : 20, "flock_vel" : 5, "collision_rad" : 0.8, "csv_mid" : "custom"}
VELOCITY_CAP = 30
CAPPED_VELS = True

class VeloAgent(agent.Agent):
    def __init__(self, world, coordinates, color, agent_counter=0, velocities = None):
        super().__init__(world, coordinates, color)
        self.velocities = (0.0,) * 3 # self.world.grid.get_dimension_count()
        self.neighbors = []

    # change in time is one round
    # function adds the velo to the position

    # TODO: Refactor with the parent class to remove the code written twice.
    def move(self):
        #check to make sure that this doesnt throw an error and conforms to grid types.
        direction_coord = tuple(np.add(np.array(self.velocities) * self.world.timestep, self.coordinates))
        direction_coord = self.check_within_border(self.velocities, direction_coord)
        if self.world.grid.are_valid_coordinates(direction_coord) \
                and direction_coord not in self.world.agent_map_coordinates \
                and not self._Agent__isCarried: # this is a little jank IK
            if self.coordinates in self.world.agent_map_coordinates:
                del self.world.agent_map_coordinates[self.coordinates]
            self.coordinates = direction_coord
            self.world.agent_map_coordinates[self.coordinates] = self
            if self.world.vis is not None:
                self.world.vis.agent_changed(self)
            logging.info("Agent %s successfully moved to %s", str(self.get_id()), self.coordinates)
            self.world.csv_round.update_metrics(steps=1)
            self.csv_agent_writer.write_agent(steps=1)
            self.check_for_carried_matter()
            return True

        return False

    def move_coord(self, coordinates):
        if self.world.grid.are_valid_coordinates(coordinates) \
                and not self._Agent__isCarried: # this is a little jank IK
            if self.coordinates in self.world.agent_map_coordinates:
                del self.world.agent_map_coordinates[self.coordinates]
            self.coordinates = coordinates
            self.world.agent_map_coordinates[self.coordinates] = self
            if self.world.vis is not None:
                self.world.vis.agent_changed(self)
            logging.info("Agent %s successfully moved to %s", str(self.get_id()), self.coordinates)
            self.world.csv_round.update_metrics(steps=1)
            self.csv_agent_writer.write_agent(steps=1)
            self.check_for_carried_matter()
            return True

        return False

    # updates the velocities
    def set_velocities(self, new_velocities):
        if CAPPED_VELS:
            new_velocities = tuple([np.sign(vel) * min(abs(vel), VELOCITY_CAP) for vel in new_velocities])
        self.velocities = tuple(np.hstack([np.array(new_velocities), np.zeros(1)])[:3])

    # adds to the velocities.
    def add_velocities(self, dv):
        self.velocities = tuple(np.add(self.velocities, dv))

    def control_update(self, net_id_map, inv_net_id_map):
        set_vel = net_id_map[0] == self.id
        follow = self._leader_agent_move(set_vel=set_vel)
        if set_vel and follow:
            return

        R_COLLISION, R_CONNECTION = .8, self.world.config_data.flock_rad
        R1, R2 = R_COLLISION, R_CONNECTION
        k_col, k_conn = R1*R1 + R2, R2

        # set agent control inputs
        vx, vy, vz = 0, 0, 0
        for (net_id, neighbor) in self.neighbors.items(): # NOTE: currently updated at the end of each slotframe
            agent_id = net_id_map[net_id]
            if agent_id == self.id:
                continue

            x1, y1, _ = self.coordinates
            x2, y2 = neighbor

            dist = np.sqrt((x2-x1)**2 + (y2-y1)**2)

            scaling = 1
            if net_id == 0:
                scaling = float(max(1, len(self.world.get_agent_list()) / 10))  # NOTE: magic number boo

            vx += 2 * scaling * (x1 - x2) * (
                        k_conn * np.exp((dist) / (R2 * R2)) / (R2 * R2) -
                        k_col * np.exp(-(dist) / (R1 * R1)) / (R1 * R1)
            )
            vy += 2 * scaling * (y1 - y2) * (
                        k_conn * np.exp((dist) / (R2 * R2)) / (R2 * R2) -
                        k_col * np.exp(-(dist) / (R1 * R1)) / (R1 * R1)
            )
            vz += 0

            if not self.world.config_data.follow_the_leader:
                vx1, vy1, _ = self.velocities
                vx2, vy2, _ = self.world.agent_map_id[agent_id].velocities

                vx += (vx1 - vx2)
                vy += (vy1 - vy2)
            
        print(f"[Mote {inv_net_id_map[self.id]}] {self.neighbors} new vels {vx} {vy}", end="\r")
        self.set_velocities((-vx, -vy, -vz))
        self.neighbors = []

    def _leader_agent_move(self, set_vel=True): # TODO: how to do follow the leader without a path bias???
        # round = self.world.get_actual_round()
        scale = self.world.config_data.flock_vel
        set_velocities = lambda vels: self.set_velocities(vels) if set_vel else None
        set_velocities((scale, 0, 0)) # TODO: iterate over different angles rather than just straight
        return True