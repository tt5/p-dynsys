#!/usr/bin/env python3
"""
Bridge simulation output to input for feedback loops
"""
import asyncio
import json
import nats
from nats.js.api import ConsumerConfig
import time

class SimulationBridge:
    def __init__(self, server="nats://localhost:4222", sim_id="hopf_2"):
        self.server = server
        self.sim_id = sim_id
        self.nc = None
        self.js = None
        
        # Configuration
        self.output_subject = f"sim.hopf.{sim_id}.>"
        self.input_subject = f"sim.input.{sim_id}"
        
        # Feedback parameters
        self.feedback_strength = 0.1  # How much of output affects input
        self.delay_steps = 5  # Number of steps to delay feedback
        self.output_buffer = []
        
    async def connect(self):
        """Connect to NATS"""
        self.nc = await nats.connect(self.server)
        self.js = self.nc.jetstream()
        print(f"Connected to NATS at {self.server}")
        
    async def setup_output_subscription(self):
        """Subscribe to simulation output"""
        async def output_handler(msg):
            try:
                data = json.loads(msg.data.decode())
                
                # Extract x, y from simulation output
                if "x" in data and "y" in data:
                    step = data.get("step", 0)
                    
                    # Store in buffer with delay
                    self.output_buffer.append({
                        "step": step,
                        "x": data["x"],
                        "y": data["y"],
                        "timestamp": data.get("timestamp", time.time())
                    })
                    
                    # Keep only recent data for delay
                    if len(self.output_buffer) > self.delay_steps * 2:
                        self.output_buffer = self.output_buffer[-self.delay_steps * 2:]
                    
                    print(f"Received output step {step}: x={data['x']:.3f}, y={data['y']:.3f}")
                    
            except Exception as e:
                print(f"Error processing output: {e}")
        
        # Subscribe to simulation output
        await self.js.subscribe(
            subject=self.output_subject,
            stream="SIMULATION",
            cb=output_handler,
            deliver_policy="new_only"
        )
        print(f"Subscribed to output: {self.output_subject}")
    
    async def send_feedback(self):
        """Send delayed feedback to input"""
        while True:
            await asyncio.sleep(0.1)  # Check every 100ms
            
            if not self.output_buffer:
                continue
                
            # Find data that's old enough for feedback delay
            current_time = time.time()
            feedback_data = None
            
            for data in self.output_buffer:
                if current_time - data["timestamp"] > (self.delay_steps * 0.01):  # Assuming dt=0.01
                    feedback_data = data
                    break
            
            if feedback_data:
                # Apply feedback transformation
                x_feedback = feedback_data["x"] * self.feedback_strength
                y_feedback = feedback_data["y"] * self.feedback_strength
                
                # Create input message
                input_data = {
                    "x": x_feedback,
                    "y": y_feedback,
                    "source": "feedback",
                    "original_step": feedback_data["step"]
                }
                
                # Send to input stream
                await self.js.publish(
                    self.input_subject,
                    json.dumps(input_data).encode()
                )
                
                print(f"Sent feedback: x={x_feedback:.3f}, y={y_feedback:.3f} (from step {feedback_data['step']})")
                
                # Remove used data from buffer
                self.output_buffer.remove(feedback_data)
    
    async def run(self):
        """Run the bridge"""
        await self.connect()
        await self.setup_output_subscription()
        
        print(f"Bridge running for {self.sim_id}")
        print(f"Feedback strength: {self.feedback_strength}")
        print(f"Delay steps: {self.delay_steps}")
        print(f"Output -> {self.output_subject}")
        print(f"Input -> {self.input_subject}")
        
        # Start feedback loop
        feedback_task = asyncio.create_task(self.send_feedback())
        
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping bridge...")
            feedback_task.cancel()
        finally:
            await self.nc.close()

async def main():
    import sys
    sim_id = sys.argv[1] if len(sys.argv) > 1 else "hopf_2"
    strength = float(sys.argv[2]) if len(sys.argv) > 2 else 0.1
    delay = int(sys.argv[3]) if len(sys.argv) > 3 else 5
    
    bridge = SimulationBridge(sim_id=sim_id)
    bridge.feedback_strength = strength
    bridge.delay_steps = delay
    
    await bridge.run()

if __name__ == "__main__":
    asyncio.run(main())
