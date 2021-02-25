from comms_env import SwarmSimCommsEnv
import rpyc

class MyService(rpyc.Service):
    def on_connect(self, conn):
        # code that runs when a connection is created
        # (to init the service, if needed)
        pass

    def exposed_initialize_simulation(self, goons=None):
        self.simulation = SwarmSimCommsEnv(goons)


    def on_disconnect(self, conn):
        # code that runs after the connection has already closed
        # (to finalize the service, if needed)
        pass



    def exposed_main_loop(self, iterations=1):

        return self.simulation.main_loop(iterations)

    def exposed_end(self):
        return self.simulation.end()



    def exposed_do_reset(self):
        self.simulation.do_reset()

    def exposed_assign_velos(self, new_velos):
        self.simulation.assign_velos(new_velos)

    def exposed_set_all_mote_neighbors(self, agent_neighbor_dict):
        self.simulation.set_all_mote_neighbors(agent_neighbor_dict)

    def exposed_get_all_mote_states(self):
        return self.simulation.get_all_mote_states()

if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    t = ThreadedServer(MyService, port=18861)
    t.start()
