# SwarmCommSim: A Simulator for (Optionally) Networked Multi-Agent Control and Swarm vs. Swarm Games

## Setup:

```
<set up your own virtualenv with conda or whatever>
pip install -r requirements.txt
cd gym-swarm-sim/envs/swarmsimmaster/
```

### SwarmSim: Swarm vs. Swarm
`python swarmsim.py`

### 6TiSCH + Swarm Sim: Networked Multi-Agent Control (No RPC & Real-time Viz)
`python ../../../6tisch-simulator/bin/runSim.py`

Running Google Doc: https://docs.google.com/document/d/1OhyHHBxHN3_bAwsYYcrqfswcTrh-pLQrN6X59aoQMSg/edit?usp=sharing



### SwarmSim RPC server:
To start the rpc server cd into the swarmsimmaster directory and run `python3 rpyc_server.py`
Once the server is started you can connect to the via the following python code in any directory  
`import rpyc`  
`service = rpyc.connect("localhost", 18861).root`  
This will let you remotely control the simulator via the service variable.
