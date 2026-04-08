#!/usr/bin/env python3
import asyncio
import nats
 
async def clean():
    nc = await nats.connect('nats://localhost:4222')
    js = nc.jetstream()
    try:
        await js.delete_stream('SIMULATION')
        print('Deleted SIMULATION stream')
    except Exception as e:
        print(f'Stream might not exist: {e}')
    await nc.close()
 
if __name__ == "__main__":
    asyncio.run(clean())