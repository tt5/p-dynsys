#!/usr/bin/env python3
"""
Minimal NATS subscriber for dynamic systems simulation
Receives and processes simulation data from NATS
"""

import asyncio
import json
import nats
from nats.js.api import ConsumerConfig
import matplotlib.pyplot as plt
import numpy as np
from collections import deque
import time


class NatsSimulationSubscriber:
    def __init__(self, server="nats://localhost:4222", stream_name="SIMULATION"):
        self.server = server
        self.stream_name = stream_name
        self.nc = None
        self.js = None
        
        # Data storage for live plotting
        self.hopf_data = deque(maxlen=500)  # Keep last 500 points
        self.predator_prey_data = deque(maxlen=500)
        
        # Track subscription start time to filter old messages
        self.subscription_start_time = None
        
        # Live plot setup
        self.fig = None
        self.ax = None
        self.lines = {}
        self.plot_initialized = False
        
    async def connect(self):
        """Connect to NATS server and setup JetStream"""
        try:
            self.nc = await nats.connect(self.server)
            self.js = self.nc.jetstream()
            print(f"Connected to NATS at {self.server}")
            
            # Set subscription start time to filter old messages
            self.subscription_start_time = time.time()
            
            # Clear old data to ensure only new messages
            try:
                stream_info = await self.js.stream_info(self.stream_name)
                print(f"Stream {self.stream_name} has {stream_info.state.messages} messages")
                # Don't delete stream, just note it exists
            except Exception as e:
                print(f"Stream info not available: {e}")
                
        except Exception as e:
            print(f"Failed to connect to NATS: {e}")
            raise
    
    async def subscribe_predator_prey(self):
        """Subscribe to predator-prey simulation data"""
        print("Subscribing to predator-prey simulation...")
        
        async def message_handler(msg):
            try:
                data = json.loads(msg.data.decode())
                
                # Only process messages newer than subscription start time
                if self.subscription_start_time and data.get("timestamp", 0) < self.subscription_start_time:
                    return  # Skip old messages
                
                self.predator_prey_data.append(data)
                
                # Print status updates
                if data["step"] % 50 == 0:
                    print(f"Predator-Prey Step {data['step']}: "
                          f"prey={data['prey']:.2f}, predator={data['predator']:.2f}")
                
            except Exception as e:
                print(f"Error processing message: {e}")
        
        # Subscribe to messages directly (only new messages)
        try:
            await self.js.subscribe(
                subject="sim.predator_prey.>",
                stream=self.stream_name,
                cb=message_handler,
                deliver_policy="new_only"  # Only get new messages
            )
            print("Successfully subscribed to Predator-Prey simulations (new messages only)")
        except Exception as e:
            print(f"Failed to subscribe to Predator-Prey simulations: {e}")
            # Fallback to regular subscription
            try:
                await self.js.subscribe(
                    subject="sim.predator_prey.>",
                    stream=self.stream_name,
                    cb=message_handler
                )
                print("Subscribed to Predator-Prey simulations (all messages)")
            except Exception as e2:
                print(f"Fallback subscription also failed: {e2}")
                raise
    
    async def subscribe_hopf(self):
        """Subscribe to Hopf bifurcation simulation data"""
        print("Subscribing to Hopf bifurcation simulation...")
        
        async def message_handler(msg):
            try:
                data = json.loads(msg.data.decode())
                print(f"Received message: step={data.get('step')}, sim_id={data.get('simulation_id')}")
                
                # Only process messages newer than subscription start time
                if self.subscription_start_time and data.get("timestamp", 0) < self.subscription_start_time:
                    print(f"Skipping old message from {data.get('timestamp')}")
                    return  # Skip old messages
                
                self.hopf_data.append(data)
                print(f"Added data point, total: {len(self.hopf_data)}")
                
                # Print status updates
                if data["step"] % 200 == 0:
                    print(f"Hopf Step {data['step']}: "
                          f"r={data['r']:.3f}, theta={data['theta']:.3f}")
                
            except Exception as e:
                print(f"Error processing message: {e}")
                import traceback
                traceback.print_exc()
        
        # Subscribe to messages directly (only new messages)
        try:
            await self.js.subscribe(
                subject="sim.hopf.>",
                stream=self.stream_name,
                cb=message_handler,
                deliver_policy="new_only"  # Only get new messages
            )
            print("Successfully subscribed to Hopf simulations (new messages only)")
        except Exception as e:
            print(f"Failed to subscribe to Hopf simulations: {e}")
            # Fallback to regular subscription
            try:
                await self.js.subscribe(
                    subject="sim.hopf.>",
                    stream=self.stream_name,
                    cb=message_handler
                )
                print("Subscribed to Hopf simulations (all messages)")
            except Exception as e2:
                print(f"Fallback subscription also failed: {e2}")
                raise
    
    def setup_live_plot(self):
        """Setup live plot for real-time visualization"""
        plt.ion()  # Turn on interactive mode
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel('Values')
        self.ax.set_title('Live Simulation Data')
        self.ax.grid(True, alpha=0.3)
        
        # Initialize empty lines for different data types
        self.lines['hopf_r'], = self.ax.plot([], [], 'r-', label='Hopf Radius', linewidth=2)
        self.lines['hopf_theta'], = self.ax.plot([], [], 'b-', label='Hopf Angle', linewidth=2)
        self.lines['prey'], = self.ax.plot([], [], 'g-', label='Prey', linewidth=2)
        self.lines['predator'], = self.ax.plot([], [], 'orange', label='Predator', linewidth=2)
        
        self.ax.legend(loc='upper right')
        self.plot_initialized = True
        print("Live plot initialized")
        
        # Make plot window not steal focus
        if plt.get_backend() == 'TkAgg':
            self.fig.canvas.manager.window.attributes('-topmost', False)
        plt.show(block=False)
    
    def update_live_plot(self):
        """Update the live plot with current data"""
        if not self.plot_initialized:
            return
        
        # Clear all lines first
        for line in self.lines.values():
            line.set_data([], [])
        
        # Update Hopf data
        if self.hopf_data:
            hopf_times = [d["timestamp"] for d in self.hopf_data]
            hopf_r = [d["r"] for d in self.hopf_data]
            hopf_theta = [d["theta"] for d in self.hopf_data]
            
            self.lines['hopf_r'].set_data(hopf_times, hopf_r)
            self.lines['hopf_theta'].set_data(hopf_times, hopf_theta)
        
        # Update Predator-Prey data
        if self.predator_prey_data:
            pp_times = [d["timestamp"] for d in self.predator_prey_data]
            prey = [d["prey"] for d in self.predator_prey_data]
            predator = [d["predator"] for d in self.predator_prey_data]
            
            self.lines['prey'].set_data(pp_times, prey)
            self.lines['predator'].set_data(pp_times, predator)
        
        # Only adjust plot limits if we have data
        if self.hopf_data or self.predator_prey_data:
            self.ax.relim()
            self.ax.autoscale_view()
        
        # Redraw without stealing focus
        self.fig.canvas.draw_idle()
        try:
            self.fig.canvas.flush_events()
        except:
            pass  # Ignore if window is closed
    
    def plot_predator_prey(self):
        if not self.predator_prey_data:
            print("No predator-prey data to plot")
            return
        
        # Extract data
        prey = [d["prey"] for d in self.predator_prey_data]
        predator = [d["predator"] for d in self.predator_prey_data]
        timestamps = [d["timestamp"] for d in self.predator_prey_data]
        
        # Create subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Phase space plot
        ax1.plot(prey, predator, 'b-', alpha=0.7)
        ax1.scatter(prey[0], predator[0], c='green', s=100, label='Start')
        ax1.scatter(prey[-1], predator[-1], c='red', s=100, label='End')
        ax1.set_xlabel('Prey Population')
        ax1.set_ylabel('Predator Population')
        ax1.set_title('Predator-Prey Phase Space')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # Time series plot
        time_relative = [t - timestamps[0] for t in timestamps]
        ax2.plot(time_relative, prey, 'g-', label='Prey', alpha=0.7)
        ax2.plot(time_relative, predator, 'r-', label='Predator', alpha=0.7)
        ax2.set_xlabel('Time (s)')
        ax2.set_ylabel('Population')
        ax2.set_title('Population Time Series')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        plt.tight_layout()
        plt.savefig('/home/n/data/p/dynsys/code/simulate/first/nats/predator_prey_plot.png', dpi=150)
        plt.close()  # Close plot to continue live updates
    
    def plot_hopf(self):
        """Plot Hopf bifurcation data"""
        if not self.hopf_data:
            print("No Hopf data to plot")
            return
        
        # Extract data
        x = [d["x"] for d in self.hopf_data]
        y = [d["y"] for d in self.hopf_data]
        r = [d["r"] for d in self.hopf_data]
        theta = [d["theta"] for d in self.hopf_data]
        timestamps = [d["timestamp"] for d in self.hopf_data]
        
        # Create subplots
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
        
        # Phase space plot
        ax1.plot(x, y, 'b-', alpha=0.5)
        ax1.set_xlabel('x')
        ax1.set_ylabel('y')
        ax1.set_title('Hopf Phase Space')
        ax1.grid(True, alpha=0.3)
        ax1.set_aspect('equal')
        
        # Radius over time
        time_relative = [t - timestamps[0] for t in timestamps]
        ax2.plot(time_relative, r, 'r-', alpha=0.7)
        ax2.set_xlabel('Time (s)')
        ax2.set_ylabel('Radius r')
        ax2.set_title('Limit Cycle Radius')
        ax2.grid(True, alpha=0.3)
        
        # Angle over time
        ax3.plot(time_relative, theta, 'g-', alpha=0.7)
        ax3.set_xlabel('Time (s)')
        ax3.set_ylabel('Angle θ')
        ax3.set_title('Phase Angle')
        ax3.grid(True, alpha=0.3)
        
        # Polar plot
        ax4.plot(theta, r, 'b-', alpha=0.5)
        ax4.set_xlabel('θ')
        ax4.set_ylabel('r')
        ax4.set_title('Polar Representation')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('/home/n/data/p/dynsys/code/simulate/first/nats/hopf_plot.png', dpi=150)
        plt.close()  # Close plot to continue live updates
    
    async def run_live_plotting(self, update_interval=0.5):
        """Run live plotting while receiving data"""
        print("Starting live plotting...")
        
        # Setup the live plot
        self.setup_live_plot()
        
        async def plot_loop():
            while True:
                await asyncio.sleep(update_interval)
                
                # Update live plot with current data
                self.update_live_plot()
        
        # Start plotting loop
        plot_task = asyncio.create_task(plot_loop())
        
        try:
            # Keep running
            while True:
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            pass
        finally:
            plot_task.cancel()
            plt.close('all')
    
    async def close(self):
        """Close NATS connection"""
        if self.nc:
            await self.nc.close()


async def main():
    subscriber = NatsSimulationSubscriber()
    
    try:
        await subscriber.connect()
        
        # Subscribe to both simulations
        await subscriber.subscribe_predator_prey()
        await subscriber.subscribe_hopf()
        
        # Run live plotting
        await subscriber.run_live_plotting()
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await subscriber.close()


if __name__ == "__main__":
    asyncio.run(main())
