#!/usr/bin/env python3
"""
Modular client for controlling simulations
Demonstrates how to use the new modular architecture
"""

import asyncio
import json
from input_control import send_control_command


class SimulationClient:
    """Client for interacting with the modular simulation system"""
    
    def __init__(self, server="nats://localhost:4222"):
        self.server = server
    
    async def start_hopf_simulation(self, sim_id: str, **params):
        """Start a Hopf bifurcation simulation"""
        default_params = {
            "type": "hopf",
            "duration": 60,
            "dt": 0.01,
            "mu": 0.1,
            "omega": 1.0,
            "alpha": -1.0,
            "beta": 1.0,
            "x0": 0.1,
            "y0": 0.1
        }
        default_params.update(params)
        
        response = await send_control_command(
            self.server, sim_id, "start", default_params
        )
        print(f"Start response: {response}")
        return response
    
    async def start_predator_prey_simulation(self, sim_id: str, **params):
        """Start a predator-prey simulation"""
        default_params = {
            "type": "predator_prey",
            "duration": 60,
            "dt": 0.1,
            "alpha": 1.1,
            "beta": 0.4,
            "delta": 0.1,
            "gamma": 0.4,
            "prey0": 10.0,
            "predator0": 5.0
        }
        default_params.update(params)
        
        response = await send_control_command(
            self.server, sim_id, "start", default_params
        )
        print(f"Start response: {response}")
        return response
    
    async def stop_simulation(self, sim_id: str):
        """Stop a simulation"""
        response = await send_control_command(self.server, sim_id, "stop")
        print(f"Stop response: {response}")
        return response
    
    async def pause_simulation(self, sim_id: str):
        """Pause a simulation"""
        response = await send_control_command(self.server, sim_id, "pause")
        print(f"Pause response: {response}")
        return response
    
    async def resume_simulation(self, sim_id: str):
        """Resume a simulation"""
        response = await send_control_command(self.server, sim_id, "resume")
        print(f"Resume response: {response}")
        return response
    
    async def update_simulation(self, sim_id: str, **params):
        """Update simulation parameters"""
        response = await send_control_command(self.server, sim_id, "update", params)
        print(f"Update response: {response}")
        return response
    
    async def get_status(self, sim_id: str):
        """Get simulation status"""
        response = await send_control_command(self.server, sim_id, "status")
        print(f"Status response: {response}")
        return response


async def demo_modular_system():
    """Demonstrate the modular simulation system"""
    client = SimulationClient()
    
    print("=== Modular Simulation System Demo ===\n")
    
    # Start a Hopf simulation
    print("1. Starting Hopf simulation...")
    await client.start_hopf_simulation(
        "hopf_1",
        mu=0.5,
        omega=2.0,
        duration=30
    )
    
    await asyncio.sleep(2)
    
    # Start a predator-prey simulation
    print("\n2. Starting predator-prey simulation...")
    await client.start_predator_prey_simulation(
        "pp_1",
        alpha=1.5,
        beta=0.5,
        duration=30
    )
    
    await asyncio.sleep(5)
    
    # Check status
    print("\n3. Checking simulation status...")
    await client.get_status("hopf_1")
    await client.get_status("pp_1")
    
    await asyncio.sleep(5)
    
    # Update parameters
    print("\n4. Updating Hopf simulation parameters...")
    await client.update_simulation("hopf_1", mu=0.8, omega=3.0)
    
    await asyncio.sleep(5)
    
    # Pause simulation
    print("\n5. Pausing predator-prey simulation...")
    await client.pause_simulation("pp_1")
    
    await asyncio.sleep(2)
    
    # Resume simulation
    print("\n6. Resuming predator-prey simulation...")
    await client.resume_simulation("pp_1")
    
    await asyncio.sleep(10)
    
    # Stop simulations
    print("\n7. Stopping simulations...")
    await client.stop_simulation("hopf_1")
    await client.stop_simulation("pp_1")
    
    print("\n=== Demo completed ===")


if __name__ == "__main__":
    asyncio.run(demo_modular_system())
