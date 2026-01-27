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
        
        # Generic data storage - key: simulation_id, value: deque of data points
        self.simulation_data = {}  # sim_id -> deque of data points
        self.simulation_start_times = {}  # sim_id -> start timestamp
        
        # Track subscription start time to filter old messages
        self.subscription_start_time = None
        
        # Live plot setup
        self.fig = None
        self.ax = None
        self.lines = {}  # sim_id -> line objects
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
    
    async def subscribe_all_simulations(self):
        """Subscribe to all simulation data generically"""
        print("Subscribing to all simulation data...")
        
        async def message_handler(msg):
            try:
                data = json.loads(msg.data.decode())
                print(f"Received message: {data.get('simulation_id', 'unknown')} step {data.get('step', 'unknown')}")
                
                # Only process messages newer than subscription start time
                if self.subscription_start_time and data.get("timestamp", 0) < self.subscription_start_time:
                    return  # Skip old messages
                
                sim_id = data.get("simulation_id", "unknown")
                
                # Initialize data storage for this simulation if needed
                if sim_id not in self.simulation_data:
                    self.simulation_data[sim_id] = deque(maxlen=2000)  # Increased from 500 to 2000
                    self.simulation_start_times[sim_id] = data.get("timestamp", time.time())
                    # Add lines for x and y if plot is initialized
                    if self.plot_initialized:
                        self.lines[sim_id] = {}
                        line_x, = self.ax.plot([], [], label=f"{sim_id}_x", linewidth=2)
                        line_y, = self.ax.plot([], [], label=f"{sim_id}_y", linewidth=2, linestyle='--')
                        self.lines[sim_id]['x'] = line_x
                        self.lines[sim_id]['y'] = line_y
                        self.ax.legend(loc='upper right')
                
                # Store the data point
                self.simulation_data[sim_id].append(data)
                print(f"Added data point for {sim_id}, total: {len(self.simulation_data[sim_id])}")
                
            except Exception as e:
                print(f"Error processing message: {e}")
                import traceback
                traceback.print_exc()
        
        # Subscribe to all simulation subjects
        try:
            await self.js.subscribe(
                subject="sim.>",  # All simulation data
                stream=self.stream_name,
                cb=message_handler,
                deliver_policy="new_only"  # Only get new messages
            )
            print("Successfully subscribed to all simulations (new messages only)")
        except Exception as e:
            print(f"Failed to subscribe to simulations: {e}")
            # Fallback to regular subscription
            try:
                await self.js.subscribe(
                    subject="sim.>",
                    stream=self.stream_name,
                    cb=message_handler
                )
                print("Subscribed to all simulations (all messages)")
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
        
        # Initialize empty lines dictionary
        self.lines = {}  # sim_id -> {'x': line, 'y': line}
        
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
        for sim_lines in self.lines.values():
            for line in sim_lines.values():
                line.set_data([], [])
        
        # Update each simulation's data
        for sim_id, data_deque in self.simulation_data.items():
            if data_deque and sim_id in self.lines:
                # Use relative time from simulation start
                start_time = self.simulation_start_times[sim_id]
                relative_times = [d["timestamp"] - start_time for d in data_deque]
                
                # Extract x and y values
                x_values = [d.get("x", 0) for d in data_deque]
                y_values = [d.get("y", 0) for d in data_deque]
                
                # Only show last N data points (sliding window)
                window_size = min(500, len(data_deque))  # Show last 500 points or all if less
                if len(data_deque) > window_size:
                    relative_times = relative_times[-window_size:]
                    x_values = x_values[-window_size:]
                    y_values = y_values[-window_size:]
                
                # Update x and y lines
                self.lines[sim_id]['x'].set_data(relative_times, x_values)
                self.lines[sim_id]['y'].set_data(relative_times, y_values)
        
        # Always adjust plot limits and force immediate update
        if self.simulation_data:
            self.ax.relim()
            self.ax.autoscale_view()
            # Force a small manual range if autoscale doesn't work
            if not hasattr(self, '_initial_range_set'):
                self.ax.set_xlim(-1, 5)  # Initial 5-second window
                self.ax.set_ylim(-2, 2)   # Initial value range
                self._initial_range_set = True
        
        # Redraw without stealing focus
        self.fig.canvas.draw_idle()
        try:
            self.fig.canvas.flush_events()
            # Remove plt.pause to prevent focus stealing
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
    
    async def run_live_plotting(self, update_interval=0.2):
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
        
        # Subscribe to all simulations generically
        await subscriber.subscribe_all_simulations()
        
        # Run live plotting
        await subscriber.run_live_plotting()
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await subscriber.close()


if __name__ == "__main__":
    asyncio.run(main())
