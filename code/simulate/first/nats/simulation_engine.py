#!/usr/bin/env python3
"""
Independent simulation module that orchestrates the simulation process
Combines input control with core simulation logic
"""

import asyncio
import json
import time
from typing import Dict, Any
from collections import deque
import nats
from core_simulation import HopfNormalForm, PredatorPreyModel
from input_control import SimulationController, SimulationState


class SimulationEngine:
    """
    Independent simulation module that runs the actual simulations
    Similar to the main simulation logic but modularized
    """
    
    def __init__(self, server="nats://localhost:4222", stream_name="SIMULATION"):
        self.server = server
        self.stream_name = stream_name
        self.nc = None
        self.js = None
        
        # Core simulation instances
        self.hopf_simulations = {}  # sim_id -> HopfNormalForm
        self.predator_prey_simulations = {}  # sim_id -> PredatorPreyModel
        
        # Simulation state
        self.simulation_states = {}  # sim_id -> SimulationState
        
        # Setup controller
        self.controller = SimulationController(server)
        self.controller.set_simulation_runner(self._run_simulation)
    
    async def connect(self):
        """Connect to NATS and setup streams"""
        await self.controller.connect()
        self.nc = self.controller.nc
        self.js = self.controller.js
        
        # Create data stream if it doesn't exist
        try:
            from nats.js.api import StreamConfig
            await self.js.add_stream(StreamConfig(
                name=self.stream_name,
                subjects=["sim.>"],
                description="Dynamic systems simulation data"
            ))
            print(f"Created data stream: {self.stream_name}")
        except Exception as e:
            print(f"Data stream might already exist: {e}")
    
    async def _run_simulation(self, sim_id: str, params: Dict[str, Any]):
        """
        Main simulation runner - called by input control module
        This is where the actual simulation logic happens
        """
        sim_type = params.get("type", "hopf")
        duration = params.get("duration", 60)
        dt = params.get("dt", 0.01)
        
        print(f"Starting {sim_type} simulation {sim_id} for {duration}s...")
        print(f"Parameters: {params}")
        external_input_enabled = params.get("external_input", False)
        print(f"External input enabled: {external_input_enabled}")
        if external_input_enabled:
            print(f"Input subject: {params.get('input_subject', 'sim.input.>')}")
        
        # Initialize simulation based on type
        if sim_type == "hopf":
            await self._run_hopf_simulation(sim_id, params, duration, dt)
        elif sim_type == "predator_prey":
            await self._run_predator_prey_simulation(sim_id, params, duration, dt)
        else:
            print(f"Unknown simulation type: {sim_type}")
            return
    
    async def _run_hopf_simulation(self, sim_id: str, params: Dict[str, Any], duration: float, dt: float):
        """Run Hopf bifurcation simulation"""
        print(f"DEBUG: Starting _run_hopf_simulation for {sim_id}")
        
        # Validate parameters for stability
        mu = params.get("mu", 0.1)
        alpha = params.get("alpha", -1.0)
        
        print(f"DEBUG: mu={mu}, alpha={alpha}")
        
        if mu > 0.3:
            print(f"Warning: mu={mu} is high, may cause instability")
        if alpha > 0:
            print(f"Warning: alpha={alpha} is positive, may cause unbounded growth")
        
        # Initialize Hopf simulation
        print(f"DEBUG: Creating HopfNormalForm")
        hopf = HopfNormalForm(
            mu=mu,
            omega=params.get("omega", 1.0),
            alpha=alpha,
            beta=params.get("beta", 1.0),
            dt=dt
        )
        self.hopf_simulations[sim_id] = hopf
        print(f"DEBUG: HopfNormalForm created")
        
        # Setup external input subscription if enabled
        external_input_enabled = params.get("external_input", False)
        input_buffer = deque(maxlen=1000)
        
        if external_input_enabled:
            input_subject = params.get("input_subject", "sim.input.>")
            
            # Create input stream if it doesn't exist
            try:
                from nats.js.api import StreamConfig
                await self.js.add_stream(StreamConfig(
                    name="SIMULATION_INPUT",
                    subjects=["sim.input.>"],
                    description="External input for simulation manipulation"
                ))
                print(f"Created input stream: SIMULATION_INPUT")
            except Exception as e:
                if "already exist" in str(e) or "overlap" in str(e):
                    print(f"Input stream already exists: SIMULATION_INPUT")
                else:
                    print(f"Error creating input stream: {e}")
                    print(f"DEBUG: Continuing without external input subscription")
                    external_input_enabled = False  # Disable external input if stream creation fails
            
            async def input_handler(msg):
                try:
                    input_data = json.loads(msg.data.decode())
                    if "x" in input_data and "y" in input_data:
                        input_buffer.append((input_data["x"], input_data["y"]))
                        print(f"Received external input: x={input_data['x']}, y={input_data['y']}")
                except Exception as e:
                    print(f"Error processing input: {e}")
            
            # Subscribe to external input only if stream creation succeeded
            if external_input_enabled:
                print(f"DEBUG: Attempting to subscribe to {input_subject}")
                try:
                    await self.js.subscribe(
                        subject=input_subject,
                        stream="SIMULATION_INPUT",
                        cb=input_handler
                    )
                    print(f"DEBUG: Successfully subscribed to external input: {input_subject}")
                except Exception as e:
                    print(f"DEBUG: Failed to subscribe to external input: {e}")
                    print(f"DEBUG: Continuing without external input")
                    external_input_enabled = False
        
        # Initial conditions
        print(f"DEBUG: Setting initial conditions")
        x = params.get("x0", 0.1)
        y = params.get("y0", 0.1)
        print(f"DEBUG: Initial x={x}, y={y}")
        
        start_time = time.time()
        step = 0
        print(f"DEBUG: Starting simulation loop")
        
        try:
            while time.time() - start_time < duration:
                # Check if simulation is paused
                if self.controller.simulations.get(sim_id) == SimulationState.PAUSED:
                    await asyncio.sleep(0.1)
                    continue
                
                # Check if simulation is stopped
                if self.controller.simulations.get(sim_id) != SimulationState.RUNNING:
                    print(f"DEBUG: Simulation {sim_id} not running, breaking")
                    break
                
                try:
                    print(f"DEBUG: Step {step} - Current x={x:.4f}, y={y:.4f}")
                    # manipulate x and y using external input if available
                    if external_input_enabled and input_buffer:
                        # Get the next external input value
                        external_x, external_y = input_buffer.popleft()
                        
                        # Apply external input (you can customize how to combine)
                        input_strength = params.get("input_strength", 0.1)
                        x = x * (1 - input_strength) + external_x * input_strength
                        y = y * (1 - input_strength) + external_y * input_strength
                        
                        print(f"Applied external input: new x={x:.4f}, y={y:.4f}")
                    
                    # Perform simulation step
                    x, y = hopf.step(x, y)
                    dx_dt, dy_dt = hopf.get_derivatives(x, y)
                    r, theta = hopf.get_polar_coords(x, y)
                    
                    # Prepare data message
                    data = {
                        "timestamp": time.time(),
                        "simulation_id": sim_id,
                        "step": step,
                        "x": x,
                        "y": y,
                        "r": r,
                        "theta": theta,
                        "dx_dt": dx_dt,
                        "dy_dt": dy_dt,
                        "parameters": hopf.get_params()
                    }
                    
                    # Publish to NATS
                    try:
                        await self.js.publish(
                            f"sim.hopf.{sim_id}.{step}",
                            json.dumps(data).encode()
                        )
                    except Exception as e:
                        print(f"Error publishing to NATS at step {step}: {e}")
                        # Continue simulation even if publishing fails
                    
                    # Status updates
                    if step % 10 == 0:  # Changed from 100 to 10 for more frequent updates
                        print(f"Hopf {sim_id} Step {step}: r={r:.3f}, theta={theta:.3f}")
                        # Output JSON for subscriber
                        print(json.dumps(data))
                    
                    step += 1
                    await asyncio.sleep(dt)
                    
                except Exception as e:
                    print(f"Error in simulation step {step}: {e}")
                    break
                    
        except Exception as e:
            print(f"Simulation loop error: {e}")
        finally:
            # Clean up simulation state
            self.simulation_states.pop(sim_id, None)
            self.hopf_simulations.pop(sim_id, None)
            # Use controller's stop method for proper cleanup
            try:
                await self.controller._stop_simulation(sim_id)
            except Exception as e:
                print(f"Error cleaning up simulation state: {e}")
            print(f"Hopf simulation {sim_id} completed after {step} steps")
    
    async def _run_predator_prey_simulation(self, sim_id: str, params: Dict[str, Any], duration: float, dt: float):
        """Run predator-prey simulation"""
        # Initialize predator-prey simulation
        pp = PredatorPreyModel(
            alpha=params.get("alpha", 1.1),
            beta=params.get("beta", 0.4),
            delta=params.get("delta", 0.1),
            gamma=params.get("gamma", 0.4),
            dt=dt
        )
        self.predator_prey_simulations[sim_id] = pp
        
        # Initial conditions
        prey = params.get("prey0", 10.0)
        predator = params.get("predator0", 5.0)
        
        start_time = time.time()
        step = 0
        
        while time.time() - start_time < duration:
            # Check if simulation is paused
            if self.controller.simulations.get(sim_id) == SimulationState.PAUSED:
                await asyncio.sleep(0.1)
                continue
            
            # Check if simulation is stopped
            if self.controller.simulations.get(sim_id) != SimulationState.RUNNING:
                break
            
            # Perform simulation step
            prey, predator = pp.step(prey, predator)
            dx_dt, dy_dt = pp.get_derivatives(prey, predator)
            
            # Prepare data message
            data = {
                "timestamp": time.time(),
                "simulation_id": sim_id,
                "step": step,
                "prey": prey,
                "predator": predator,
                "dx_dt": dx_dt,
                "dy_dt": dy_dt,
                "parameters": pp.get_params()
            }
            
            # Publish to NATS
            try:
                await self.js.publish(
                    f"sim.predator_prey.{sim_id}.{step}",
                    json.dumps(data).encode()
                )
            except Exception as e:
                print(f"Error publishing to NATS at step {step}: {e}")
                # Continue simulation even if publishing fails
            
            # Status updates
            if step % 5 == 0:  # Changed from 10 to 5 for even more frequent updates
                print(f"Predator-Prey {sim_id} Step {step}: prey={prey:.2f}, predator={predator:.2f}")
                # Output JSON for subscriber
                print(json.dumps(data))
            
            step += 1
            await asyncio.sleep(dt)
        
        print(f"Predator-prey simulation {sim_id} completed")
    
    async def update_simulation_params(self, sim_id: str, params: Dict[str, Any]):
        """Update parameters for a running simulation"""
        if sim_id in self.hopf_simulations:
            self.hopf_simulations[sim_id].update_params(**params)
            print(f"Updated Hopf simulation {sim_id} parameters: {params}")
        elif sim_id in self.predator_prey_simulations:
            self.predator_prey_simulations[sim_id].update_params(**params)
            print(f"Updated predator-prey simulation {sim_id} parameters: {params}")
        else:
            print(f"Simulation {sim_id} not found for parameter update")
    
    async def close(self):
        """Close connections and cleanup"""
        await self.controller.close()


async def main():
    """Main function to run the simulation engine"""
    engine = SimulationEngine()
    
    try:
        await engine.connect()
        print("Simulation engine started. Waiting for control commands...")
        
        # Keep running
        while True:
            await asyncio.sleep(1)
            
    except KeyboardInterrupt:
        print("\nShutting down simulation engine...")
    finally:
        await engine.close()


if __name__ == "__main__":
    asyncio.run(main())
