#!/usr/bin/env python3
"""
Minimal NATS publisher for dynamic systems simulation
Similar to the Lua simulation scripts but using Python + NATS
"""

import asyncio
import json
import time
import nats
from nats.js.api import StreamConfig, ConsumerConfig
import numpy as np


class NatsSimulationPublisher:
    def __init__(self, server="nats://localhost:4222", stream_name="SIMULATION"):
        self.server = server
        self.stream_name = stream_name
        self.nc = None
        self.js = None
        
    async def connect(self):
        """Connect to NATS server and setup JetStream"""
        self.nc = await nats.connect(self.server)
        self.js = self.nc.jetstream()
        
        # Create stream if it doesn't exist
        try:
            await self.js.add_stream(StreamConfig(
                name=self.stream_name,
                subjects=["sim.>"],
                description="Dynamic systems simulation data"
            ))
            print(f"Created stream: {self.stream_name}")
        except Exception as e:
            print(f"Stream might already exist: {e}")
    
    async def publish_predator_prey(self, duration=60, dt=0.1):
        """
        Publish predator-prey simulation data
        Similar to n1-predprey.lua
        """
        # Lotka-Volterra parameters
        alpha = 1.1    # prey growth rate
        beta = 0.4     # predation rate
        delta = 0.1    # predator efficiency
        gamma = 0.4    # predator death rate
        
        # Initial conditions
        x = 10.0  # prey population
        y = 5.0   # predator population
        
        print(f"Starting predator-prey simulation for {duration}s...")
        
        start_time = time.time()
        step = 0
        
        while time.time() - start_time < duration:
            # Lotka-Volterra equations
            dx_dt = alpha * x - beta * x * y
            dy_dt = delta * x * y - gamma * y
            
            # Euler integration
            x = x + dx_dt * dt
            y = y + dy_dt * dt
            
            # Prepare data message
            data = {
                "timestamp": time.time(),
                "step": step,
                "prey": x,
                "predator": y,
                "dx_dt": dx_dt,
                "dy_dt": dy_dt,
                "parameters": {
                    "alpha": alpha,
                    "beta": beta,
                    "delta": delta,
                    "gamma": gamma
                }
            }
            
            # Publish to NATS
            await self.js.publish(
                f"sim.predator_prey.{step}",
                json.dumps(data).encode()
            )
            
            if step % 10 == 0:
                print(f"Step {step}: prey={x:.2f}, predator={y:.2f}")
            
            step += 1
            await asyncio.sleep(dt)
    
    async def publish_hopf(self, duration=60, dt=0.01):
        """
        Publish Hopf bifurcation simulation data
        Similar to the Hopf normal form data generation
        """
        # Hopf normal form parameters
        mu = 0.5    # bifurcation parameter
        omega = 2.0  # natural frequency
        
        # Initial conditions
        x = 0.1
        y = 0.1
        
        print(f"Starting Hopf bifurcation simulation for {duration}s...")
        
        start_time = time.time()
        step = 0
        
        while time.time() - start_time < duration:
            # Hopf normal form equations
            dx_dt = mu * x - omega * y - x * (x**2 + y**2)
            dy_dt = mu * y + omega * x - y * (x**2 + y**2)
            
            # Euler integration
            x = x + dx_dt * dt
            y = y + dy_dt * dt
            
            # Prepare data message
            data = {
                "timestamp": time.time(),
                "step": step,
                "x": x,
                "y": y,
                "r": np.sqrt(x**2 + y**2),  # radius
                "theta": np.arctan2(y, x),  # angle
                "dx_dt": dx_dt,
                "dy_dt": dy_dt,
                "parameters": {
                    "mu": mu,
                    "omega": omega
                }
            }
            
            # Publish to NATS
            await self.js.publish(
                f"sim.hopf.{step}",
                json.dumps(data).encode()
            )
            
            if step % 100 == 0:
                print(f"Step {step}: r={np.sqrt(x**2 + y**2):.3f}, theta={np.arctan2(y, x):.3f}")
            
            step += 1
            await asyncio.sleep(dt)
    
    async def close(self):
        """Close NATS connection"""
        if self.nc:
            await self.nc.close()


async def main():
    publisher = NatsSimulationPublisher()
    
    try:
        await publisher.connect()
        
        # Run predator-prey simulation
        await publisher.publish_predator_prey(duration=30, dt=0.1)
        
        # Run Hopf bifurcation simulation  
        await publisher.publish_hopf(duration=30, dt=0.01)
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await publisher.close()


if __name__ == "__main__":
    asyncio.run(main())
