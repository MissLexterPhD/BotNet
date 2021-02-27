import pandas as pd
replication_file = '/Users/markselden/Work/AI_Research/gym-swarm-sim/swarmsimmaster/outputs/csv/2021-02-27_10-18-3_lonely_agent_velo_move_10/_simple.csv'

def scenario(world):
    #add all the agents with a mapping
    world.replication_data = pd.read_csv(replication_file)
    for agent_id in world.replication_data.columns:
        world.add_agent(world.grid.get_center())

