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
        self.last_processed_counts = {}  # sim_id -> last processed count
        
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
                
                # Debug: print full message structure if step is missing
                if 'step' not in data:
                    print(f"DEBUG: Full message data: {data}")
                
                # Only process messages newer than subscription start time
                if self.subscription_start_time and data.get("timestamp", 0) < self.subscription_start_time:
                    return  # Skip old messages
                
                sim_id = data.get("simulation_id", "unknown")
                
                # Initialize data storage for this simulation if needed
                if sim_id not in self.simulation_data:
                    self.simulation_data[sim_id] = deque(maxlen=2000)
                    self.simulation_start_times[sim_id] = data.get("timestamp", time.time())
                    self.last_processed_counts[sim_id] = 0  # Reset processed count for new simulation
                    print(f"Initialized new simulation: {sim_id}")
                
                # Store the data point
                self.simulation_data[sim_id].append(data)
                print(f"Added data point for {sim_id}, total: {len(self.simulation_data[sim_id])}")
                
            except Exception as e:
                print(f"Error processing message: {e}")
                import traceback
                traceback.print_exc()
        
        # Subscribe to simulation data only (not control commands)
        try:
            # First try to get stream info to make sure SIMULATION stream exists
            try:
                stream_info = await self.js.stream_info(self.stream_name)
                print(f"Found stream {self.stream_name} with {stream_info.state.messages} messages")
            except Exception as e:
                print(f"Stream {self.stream_name} not found: {e}")
                return
            
            # Subscribe to Hopf simulation data
            await self.js.subscribe(
                subject="sim.hopf.>",  # Hopf simulation data
                stream=self.stream_name,
                cb=message_handler,
                deliver_policy="new_only"  # Only get new messages
            )
            print("Successfully subscribed to Hopf simulation data (new messages only)")
            
            # Subscribe to predator-prey simulation data
            await self.js.subscribe(
                subject="sim.predator_prey.>",  # Predator-prey simulation data
                stream=self.stream_name,
                cb=message_handler,
                deliver_policy="new_only"  # Only get new messages
            )
            print("Successfully subscribed to predator-prey simulation data (new messages only)")
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
    
    def reset_plot(self):
        """Reset the plot completely - useful after crashes"""
        if self.plot_initialized and self.fig:
            # Clear all lines
            for line in self.lines.values():
                line.remove()
            self.lines.clear()
            self.buffers.clear()
            
            # Clear data
            self.simulation_data.clear()
            self.simulation_start_times.clear()
            self.last_processed_counts.clear()
            
            # Reset plot limits
            self.ax.clear()
            self.ax.set_title('Live Simulation Data')
            self.ax.set_xlabel('Time Step')
            self.ax.set_ylabel('Value')
            self.ax.grid(True, alpha=0.3)
            
            print("Plot reset complete")
    
    def setup_live_plot(self):
        """Setup live plot for real-time visualization"""
        plt.ion()  # Turn on interactive mode
        self.fig, self.ax = plt.subplots(figsize=(12, 6))
        self.ax.set_title('Live Simulation Data')
        self.ax.set_xlabel('Time Step')
        self.ax.set_ylabel('Value')
        self.ax.grid(True, alpha=0.3)
        
        # Initialize empty lines dictionary - like plot_live.py
        self.lines = {}  # key -> line
        self.buffers = {}  # key -> deque
        self.timesteps = deque(maxlen=1000)
        
        self.plot_initialized = True
        print("Live plot initialized")
        
        # Make plot window not steal focus
        if plt.get_backend() == 'TkAgg':
            self.fig.canvas.manager.window.attributes('-topmost', False)
            
            # Add keyboard shortcut for reset
            def on_key(event):
                if event.key == 'r':  # Press 'r' to reset plot
                    print("Resetting plot...")
                    self.reset_plot()
                elif event.key == 'c':  # Press 'c' to clear data only
                    print("Clearing data...")
                    self.simulation_data.clear()
                    self.simulation_start_times.clear()
                    self.last_processed_counts.clear()
                    
            self.fig.canvas.mpl_connect('key_press_event', on_key)
        
        plt.show(block=False)
    
    def update_live_plot(self):
        """Update the live plot with current data - simple and reliable"""
        if not self.plot_initialized:
            return
        
        # Clean up stale simulations (no data for more than 5 seconds)
        current_time = time.time()
        stale_sims = []
        for sim_id, start_time in self.simulation_start_times.items():
            if current_time - start_time > 5 and sim_id in self.simulation_data:
                if len(self.simulation_data[sim_id]) == 0 or \
                   current_time - self.simulation_data[sim_id][-1].get('timestamp', 0) > 5:
                    stale_sims.append(sim_id)
        
        # Clean up stale simulation data and plot lines
        for sim_id in stale_sims:
            print(f"Cleaning up stale simulation: {sim_id}")
            # Remove data
            self.simulation_data.pop(sim_id, None)
            self.simulation_start_times.pop(sim_id, None)
            # Remove plot lines and buffers
            keys_to_remove = [k for k in self.buffers.keys() if k.startswith(f"{sim_id}_")]
            for key in keys_to_remove:
                if key in self.lines:
                    self.lines[key].remove()
                    del self.lines[key]
                if key in self.buffers:
                    del self.buffers[key]
            # Update legend
            if self.lines:
                self.ax.legend(loc='upper right')
        
        # Process each simulation
        for sim_id, data_deque in self.simulation_data.items():
            if not data_deque:
                continue
            
            # Get all data points for this simulation
            all_data = list(data_deque)
            
            # Check for overflow values and skip them
            has_overflow = False
            for data in all_data:
                for key in ['x', 'y']:
                    if key in data and isinstance(data[key], (int, float)):
                        if abs(data[key]) > 1e6:
                            has_overflow = True
                            print(f"Skipping overflow data for {sim_id}: {key}={data[key]}")
                            break
                if has_overflow:
                    break
            
            if has_overflow:
                continue  # Skip this simulation entirely if it has overflow data
            
            # Process each key in the data
            for key in ['x', 'y']:
                buffer_key = f"{sim_id}_{key}"
                
                # Create buffer if it doesn't exist
                if buffer_key not in self.buffers:
                    self.buffers[buffer_key] = deque(maxlen=1000)
                    # Create line for this key
                    self.lines[buffer_key], = self.ax.plot([], [], label=buffer_key, alpha=0.8, linewidth=2)
                    if 'y' in key:
                        self.lines[buffer_key].set_linestyle('--')
                    self.ax.legend(loc='upper right')
                
                # Extract all values for this key (skip overflow values)
                values = []
                for data in all_data:
                    if key in data and isinstance(data[key], (int, float)):
                        if abs(data[key]) < 1e6:  # Only add non-overflow values
                            values.append(data[key])
                
                # Update buffer with all values
                self.buffers[buffer_key].clear()
                self.buffers[buffer_key].extend(values)
        
        # Update each line
        for key, line in self.lines.items():
            if key in self.buffers and self.buffers[key]:
                line.set_data(range(len(self.buffers[key])), list(self.buffers[key]))
        
        # Adjust plot limits
        if any(self.buffers.values()):
            max_len = max(len(buf) for buf in self.buffers.values())
            self.ax.set_xlim(0, max_len + 1)
            
            # Find the overall y-range (skip empty buffers)
            all_values = []
            for buf in self.buffers.values():
                if buf:  # Only add values from non-empty buffers
                    all_values.extend(buf)
            
            if all_values:
                min_val = min(all_values)
                max_val = max(all_values)
                padding = (max_val - min_val) * 0.1 if max_val != min_val else 1.0
                self.ax.set_ylim(min_val - padding, max_val + padding)
            else:
                # No valid data, set default limits
                self.ax.set_ylim(-1, 1)
        else:
            # No data at all, set default limits
            self.ax.set_xlim(0, 100)
            self.ax.set_ylim(-1, 1)
        
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
