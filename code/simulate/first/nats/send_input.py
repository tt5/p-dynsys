#!/usr/bin/env python3
"""
Send external input to running simulation
"""
import asyncio
import json
import nats
import time
import math

async def send_input(server="nats://localhost:4222", sim_id="hopf_2"):
    nc = await nats.connect(server)
    js = nc.jetstream()
    
    step = 0
    try:
        while True:
            # Generate some interesting input patterns
            t = step * 0.1
            
            # Example 1: Sinusoidal input
            x = 0.3 * math.sin(t)
            y = 0.3 * math.cos(t)
            
            # Example 2: Random perturbation
            # import random
            # x = random.uniform(-0.5, 0.5)
            # y = random.uniform(-0.5, 0.5)
            
            # Example 3: Step function
            # if step % 20 < 10:
            #     x, y = 0.5, 0.5
            # else:
            #     x, y = -0.5, -0.5
            
            data = {"x": x, "y": y}
            
            await js.publish(
                f"sim.input.{sim_id}",
                json.dumps(data).encode()
            )
            
            print(f"Sent input {step}: x={x:.3f}, y={y:.3f}")
            
            step += 1
            await asyncio.sleep(0.5)  # Send input every 0.5 seconds
            
    except KeyboardInterrupt:
        print("\nStopping input sender...")
    finally:
        await nc.close()

if __name__ == "__main__":
    import sys
    sim_id = sys.argv[1] if len(sys.argv) > 1 else "hopf_2"
    asyncio.run(send_input(sim_id=sim_id))
