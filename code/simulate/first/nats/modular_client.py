#!/usr/bin/env python3
"""
Modular client for controlling simulations
CLI interface for the modular architecture
"""

import asyncio
import json
import argparse
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


async def main():
    """CLI interface for simulation control"""
    parser = argparse.ArgumentParser(description="Control modular simulations")
    parser.add_argument("--server", default="nats://localhost:4222", help="NATS server URL")
    parser.add_argument("action", choices=["start-hopf", "start-pp", "stop", "pause", "resume", "update", "status"], help="Action to perform")
    parser.add_argument("sim_id", help="Simulation ID")
    parser.add_argument("--params", help="Parameters as JSON string")
    
    args = parser.parse_args()
    
    client = SimulationClient(args.server)
    
    # Parse parameters if provided
    params = {}
    if args.params:
        params = json.loads(args.params)
    
    # Execute action
    if args.action == "start-hopf":
        await client.start_hopf_simulation(args.sim_id, **params)
    elif args.action == "start-pp":
        await client.start_predator_prey_simulation(args.sim_id, **params)
    elif args.action == "stop":
        await client.stop_simulation(args.sim_id)
    elif args.action == "pause":
        await client.pause_simulation(args.sim_id)
    elif args.action == "resume":
        await client.resume_simulation(args.sim_id)
    elif args.action == "update":
        await client.update_simulation(args.sim_id, **params)
    elif args.action == "status":
        await client.get_status(args.sim_id)


if __name__ == "__main__":
    asyncio.run(main())


