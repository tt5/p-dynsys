#!/usr/bin/env python3
"""
Optimized simulation configuration for high precision (dt=0.001) with minimal CPU usage
"""

import asyncio
import json
from simulation_engine import SimulationEngine

async def run_optimized_simulation():
    """Run simulation with performance optimizations"""
    engine = SimulationEngine()
    await engine.connect()
    
    # Optimized configuration for dt=0.001 precision
    config = {
        "type": "hopf",
        "dt": 0.001,                    # High precision timestep
        "duration": 60,                 # Run for 60 seconds
        "integration_method": "rk4",    # Use RK4 for better numerical efficiency
        "publish_frequency": 200,       # Publish every 200 steps (reduces NATS overhead)
        "status_frequency": 2000,       # Status updates every 2000 steps
        "debug": False,                 # Disable debug prints
        "mu": 0.1,
        "omega": 1.0,
        "alpha": -1.0,
        "beta": 1.0,
        "x0": 0.1,
        "y0": 0.1
    }
    
    print("Starting optimized simulation with dt=0.001...")
    print(f"Configuration: {json.dumps(config, indent=2)}")
    
    # Start simulation
    sim_id = "optimized_test"
    await engine.controller.start_simulation(sim_id, config)
    
    # Wait for completion
    await asyncio.sleep(config["duration"] + 1)
    
    await engine.close()

if __name__ == "__main__":
    asyncio.run(run_optimized_simulation())
