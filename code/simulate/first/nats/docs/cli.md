# Start Hopf simulation
python modular_client.py start-hopf hopf_1 --params '{"mu": 0.5, "omega": 2.0}'

# Start predator-prey simulation  
python modular_client.py start-pp pp_1 --params '{"alpha": 1.5, "beta": 0.5}'

# Stop simulation
python modular_client.py stop hopf_1

# Check status
python modular_client.py status hopf_1

# Update parameters
python modular_client.py update hopf_1 --params '{"mu": 0.8}'

# Pause/resume
python modular_client.py pause pp_1
python modular_client.py resume pp_1