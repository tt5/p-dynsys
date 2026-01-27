#!/usr/bin/env python3
"""
Input control module for managing simulation lifecycle
Handles start/stop/update commands and parameter management
"""

import asyncio
import json
import time
from typing import Dict, Any, Optional, Callable
from enum import Enum
import nats
from nats.js.api import StreamConfig


class SimulationState(Enum):
    STOPPED = "stopped"
    RUNNING = "running"
    PAUSED = "paused"
    UPDATING = "updating"


class SimulationController:
    """
    Input module that controls simulation lifecycle
    Similar to fluent-bit's input management
    """
    
    def __init__(self, server="nats://localhost:4222", control_subject="sim.control"):
        self.server = server
        self.control_subject = control_subject
        self.nc = None
        self.js = None
        
        # Simulation state management
        self.simulations = {}  # simulation_id -> SimulationState
        self.simulation_tasks = {}  # simulation_id -> asyncio.Task
        self.simulation_params = {}  # simulation_id -> parameters
        
        # Callback for running actual simulation
        self.simulation_runner: Optional[Callable] = None
    
    async def connect(self):
        """Connect to NATS server and setup control stream"""
        self.nc = await nats.connect(self.server)
        self.js = self.nc.jetstream()
        
        # Create control stream if it doesn't exist
        try:
            await self.js.add_stream(StreamConfig(
                name="SIMULATION_CONTROL",
                subjects=["sim.control.>"],
                description="Simulation control commands"
            ))
            print("Created control stream: SIMULATION_CONTROL")
        except Exception as e:
            print(f"Control stream might already exist: {e}")
        
        # Subscribe to control commands
        await self.nc.subscribe(
            subject="sim.control.>",
            cb=self._handle_control_command
        )
        
        print(f"Simulation controller listening on {self.control_subject}")
    
    def set_simulation_runner(self, runner: Callable):
        """Set the callback function for running simulations"""
        self.simulation_runner = runner
    
    async def _handle_control_command(self, msg):
        """Handle incoming control commands"""
        try:
            command = json.loads(msg.data.decode())
            sim_id = command.get("simulation_id")
            action = command.get("action")
            params = command.get("parameters", {})
            
            print(f"Received command: {action} for simulation {sim_id}")
            
            response = {"simulation_id": sim_id, "action": action, "status": "unknown"}
            
            if action == "start":
                response = await self._start_simulation(sim_id, params)
            elif action == "stop":
                response = await self._stop_simulation(sim_id)
            elif action == "pause":
                response = await self._pause_simulation(sim_id)
            elif action == "resume":
                response = await self._resume_simulation(sim_id)
            elif action == "update":
                response = await self._update_simulation(sim_id, params)
            elif action == "status":
                response = await self._get_status(sim_id)
            else:
                response["status"] = "error"
                response["message"] = f"Unknown action: {action}"
            
            # Send response
            await msg.respond(json.dumps(response).encode())
            
        except Exception as e:
            error_response = {
                "status": "error",
                "message": str(e)
            }
            await msg.respond(json.dumps(error_response).encode())
    
    async def _start_simulation(self, sim_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Start a new simulation"""
        if sim_id in self.simulations and self.simulations[sim_id] == SimulationState.RUNNING:
            return {
                "simulation_id": sim_id,
                "action": "start",
                "status": "error",
                "message": "Simulation already running"
            }
        
        # Store parameters
        self.simulation_params[sim_id] = params
        
        # Create and start simulation task
        if self.simulation_runner:
            task = asyncio.create_task(self.simulation_runner(sim_id, params))
            self.simulation_tasks[sim_id] = task
            self.simulations[sim_id] = SimulationState.RUNNING
            
            return {
                "simulation_id": sim_id,
                "action": "start",
                "status": "started",
                "message": f"Simulation {sim_id} started"
            }
        else:
            return {
                "simulation_id": sim_id,
                "action": "start",
                "status": "error",
                "message": "No simulation runner configured"
            }
    
    async def _stop_simulation(self, sim_id: str) -> Dict[str, Any]:
        """Stop a running simulation"""
        if sim_id not in self.simulations:
            return {
                "simulation_id": sim_id,
                "action": "stop",
                "status": "error",
                "message": "Simulation not found"
            }
        
        # Cancel the task if it exists
        if sim_id in self.simulation_tasks:
            self.simulation_tasks[sim_id].cancel()
            del self.simulation_tasks[sim_id]
        
        self.simulations[sim_id] = SimulationState.STOPPED
        
        return {
            "simulation_id": sim_id,
            "action": "stop",
            "status": "stopped",
            "message": f"Simulation {sim_id} stopped"
        }
    
    async def _pause_simulation(self, sim_id: str) -> Dict[str, Any]:
        """Pause a running simulation"""
        if sim_id not in self.simulations:
            return {
                "simulation_id": sim_id,
                "action": "pause",
                "status": "error",
                "message": "Simulation not found"
            }
        
        if self.simulations[sim_id] != SimulationState.RUNNING:
            return {
                "simulation_id": sim_id,
                "action": "pause",
                "status": "error",
                "message": "Simulation not running"
            }
        
        self.simulations[sim_id] = SimulationState.PAUSED
        
        return {
            "simulation_id": sim_id,
            "action": "pause",
            "status": "paused",
            "message": f"Simulation {sim_id} paused"
        }
    
    async def _resume_simulation(self, sim_id: str) -> Dict[str, Any]:
        """Resume a paused simulation"""
        if sim_id not in self.simulations:
            return {
                "simulation_id": sim_id,
                "action": "resume",
                "status": "error",
                "message": "Simulation not found"
            }
        
        if self.simulations[sim_id] != SimulationState.PAUSED:
            return {
                "simulation_id": sim_id,
                "action": "resume",
                "status": "error",
                "message": "Simulation not paused"
            }
        
        self.simulations[sim_id] = SimulationState.RUNNING
        
        return {
            "simulation_id": sim_id,
            "action": "resume",
            "status": "resumed",
            "message": f"Simulation {sim_id} resumed"
        }
    
    async def _update_simulation(self, sim_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Update simulation parameters"""
        if sim_id not in self.simulations:
            return {
                "simulation_id": sim_id,
                "action": "update",
                "status": "error",
                "message": "Simulation not found"
            }
        
        # Update parameters
        self.simulation_params[sim_id].update(params)
        
        return {
            "simulation_id": sim_id,
            "action": "update",
            "status": "updated",
            "message": f"Simulation {sim_id} parameters updated",
            "parameters": self.simulation_params[sim_id]
        }
    
    async def _get_status(self, sim_id: str) -> Dict[str, Any]:
        """Get simulation status"""
        if sim_id not in self.simulations:
            return {
                "simulation_id": sim_id,
                "action": "status",
                "status": "not_found",
                "message": "Simulation not found"
            }
        
        return {
            "simulation_id": sim_id,
            "action": "status",
            "status": self.simulations[sim_id].value,
            "parameters": self.simulation_params.get(sim_id, {})
        }
    
    async def get_all_status(self) -> Dict[str, Any]:
        """Get status of all simulations"""
        return {
            "simulations": {
                sim_id: {
                    "state": state.value,
                    "parameters": self.simulation_params.get(sim_id, {})
                }
                for sim_id, state in self.simulations.items()
            }
        }
    
    async def close(self):
        """Close NATS connection and cleanup"""
        # Cancel all running tasks
        for task in self.simulation_tasks.values():
            task.cancel()
        
        if self.nc:
            await self.nc.close()


# Utility functions for sending control commands
async def send_control_command(server: str, sim_id: str, action: str, parameters: Dict[str, Any] = None):
    """Send a control command to the simulation controller"""
    nc = await nats.connect(server)
    
    command = {
        "simulation_id": sim_id,
        "action": action,
        "parameters": parameters or {}
    }
    
    try:
        response = await nc.request(
            f"sim.control.{action}",
            json.dumps(command).encode(),
            timeout=5.0
        )
        return json.loads(response.data.decode())
    finally:
        await nc.close()
