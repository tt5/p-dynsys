#!/usr/bin/env python3
import asyncio
import nats
from nats.js.api import StreamConfig

async def setup_streams():
    nc = await nats.connect("nats://localhost:4222")
    js = nc.jetstream()
    
    streams = [
        StreamConfig(
            name="SIMULATION",
            subjects=["sim.>"],
            description="Dynamic systems simulation data"
        ),
        StreamConfig(
            name="SIMULATION_CONTROL", 
            subjects=["sim.control.>"],
            description="Simulation control commands"
        ),
        StreamConfig(
            name="SIMULATION_INPUT",
            subjects=["sim.input.>"],
            description="External input for simulation manipulation"
        )
    ]
    
    for stream_config in streams:
        try:
            await js.add_stream(stream_config)
            print(f"Created stream: {stream_config.name}")
        except Exception as e:
            print(f"Stream {stream_config.name} might already exist: {e}")
    
    await nc.close()

if __name__ == "__main__":
    asyncio.run(setup_streams())