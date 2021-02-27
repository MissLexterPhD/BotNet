import pandas as pd

#AGENT RANDOM ORDER SHOULD BE FALSE WHEN USING THIS
def solution(world):
    round = world.get_actual_round()
    round_data = list(world.replication_data.iloc[round])
    print(round_data)
    i = 1
    for agent in world.get_agent_list():
        agent.coordinates = eval(round_data[i])
        i += 1