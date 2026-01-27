#!/usr/bin/env python3
"""
Live visualization for Fluent Bit output from n3.conf
Usage: fluent-bit -c n3.conf | python3 plot_live.py
"""
import sys
import json
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import deque
import numpy as np
import os
import time
import asyncio
import threading

class LivePlot:
    def __init__(self, max_points=1000):
        self.max_points = max_points
        self.fig, self.ax = plt.subplots(figsize=(12, 6))
        self.lines = {}
        self.buffers = {}
        self.timesteps = deque(maxlen=max_points)
        
        # Set up the plot
        self.ax.set_title('Live Simulation Data')
        self.ax.set_xlabel('Time Step')
        self.ax.set_ylabel('Value')
        self.ax.grid(True)
        self.line_count = 0
        
        # Start the async event loop in a thread
        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=self._run_event_loop, daemon=True)
        self.thread.start()
        
    def _run_event_loop(self):
        """Run the event loop in a separate thread"""
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()
        
    async def async_write_to_fifo(self, record):
        """Async version of write_to_fifo"""
        try:
            fifo_path = "/home/n/data/p/dynsys/code/simulate/first/fifo"
            if os.path.exists(fifo_path):
                await asyncio.sleep(4)  # 0.5 second delay
                # Use subprocess instead of os.system for better control
                import subprocess
                json_str = json.dumps(record)  # Convert dict to JSON string
                #subprocess.run(['echo', json_str], stdout=open(fifo_path, 'w'), check=True)
        except Exception as e:
            pass  # Silently ignore fifo write errors
        
    def write_to_fifo(self, record):
        """Write JSON record to fifo - runs asynchronously"""
        if not self.loop.is_running():
            return
        asyncio.run_coroutine_threadsafe(self.async_write_to_fifo(record), self.loop)
        
    def update(self, frame):
        # Read a line from stdin
        line = sys.stdin.readline()
        if not line:
            return list(self.lines.values())
            
        try:
            # Parse the JSON data
            records = json.loads(line.strip())
            if not records or not isinstance(records, list):
                return list(self.lines.values())
                
            # Process each record in the array
            for record in records:
                if not isinstance(record, dict):
                    continue
                
                # Write to fifo
                self.write_to_fifo(record)
                    
                # Get or create data buffers for each key
                for key, value in record.items():
                    if not isinstance(value, (int, float)):
                        continue
                        
                    if key not in self.buffers:
                        self.buffers[key] = deque(maxlen=self.max_points)
                        # Create a new line for this key
                        self.lines[key], = self.ax.plot([], [], label=key, alpha=0.8)
                        self.ax.legend()
                    
                    self.buffers[key].append(value)
                
                # Update x-axis (time steps)
                self.timesteps.append(len(self.timesteps) + 1)
                
                # Update each line
                for key, line in self.lines.items():
                    if key in self.buffers and self.buffers[key]:
                        line.set_data(range(len(self.buffers[key])), self.buffers[key])
                
                # Adjust the plot limits
                if self.timesteps:
                    self.ax.set_xlim(0, max(len(buf) for buf in self.buffers.values()) + 1)
                    
                    # Find the overall y-range
                    all_values = []
                    for buf in self.buffers.values():
                        if buf:
                            all_values.extend(buf)
                    
                    if all_values:
                        min_val = min(all_values)
                        max_val = max(all_values)
                        padding = (max_val - min_val) * 0.1  # 10% padding
                        self.ax.set_ylim(min_val - padding, max_val + padding)
            
        except json.JSONDecodeError:
            print(f"Warning: Could not parse line: {line}", file=sys.stderr)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            
        return list(self.lines.values())

def main():
    plot = LivePlot(max_points=1000)
    ani = FuncAnimation(plot.fig, plot.update, interval=50, blit=False, cache_frame_data=False)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()