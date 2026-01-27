"""
Configuration for NATS simulation project
Similar to the .conf files in the parent directory
"""

# NATS server configuration
NATS_SERVER = "nats://localhost:4222"
NATS_STREAM = "SIMULATION"

# Simulation parameters
PREDATOR_PREY = {
    "duration": 60,
    "dt": 0.1,
    "alpha": 1.1,    # prey growth rate
    "beta": 0.4,     # predation rate
    "delta": 0.1,    # predator efficiency
    "gamma": 0.4,    # predator death rate
    "initial_prey": 10.0,
    "initial_predator": 5.0
}

HOPF = {
    "duration": 60,
    "dt": 0.01,
    "mu": 0.5,       # bifurcation parameter
    "omega": 2.0,    # natural frequency
    "initial_x": 0.1,
    "initial_y": 0.1
}

# Plotting configuration
PLOTTING = {
    "update_interval": 2.0,
    "max_data_points": 1000,
    "save_plots": True,
    "plot_dir": "/home/n/data/p/dynsys/code/simulate/first/nats"
}

# Data storage
DATA_FILES = {
    "predator_prey": "predator_prey_data.json",
    "hopf": "hopf_data.json"
}
