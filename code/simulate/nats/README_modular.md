# Modular Simulation System

This directory contains a NATS simulation system with a modular architecture similar to fluent-bit (parent directory).

## Architecture

### 1. Core Module (`core_simulation.py`)
- **Purpose**: Contains pure mathematical simulation functions
- **Components**:
  - `HopfNormalForm`: Core Hopf bifurcation mathematics
  - `PredatorPreyModel`: Core Lotka-Volterra mathematics
- **Responsibilities**: 
  - Mathematical computations
  - Parameter management
  - State integration (Euler method)

### 2. Input Control Module (`input_control.py`)
- **Purpose**: Manages simulation lifecycle and control commands
- **Components**:
  - `SimulationController`: Handles start/stop/pause/resume/update
  - `SimulationState`: State enumeration
  - Control command processing
- **Responsibilities**:
  - Receive and process control commands via NATS
  - Manage simulation state
  - Handle parameter updates
  - Coordinate with simulation engine

### 3. Simulation Engine (`simulation_engine.py`)
- **Purpose**: Independent simulation orchestration
- **Components**:
  - `SimulationEngine`: Main simulation coordinator
  - Integration of core + input modules
- **Responsibilities**:
  - Run actual simulations
  - Publish data to NATS streams
  - Handle simulation lifecycle
  - Coordinate between modules

### 4. Client Interface (`modular_client.py`)
- **Purpose**: High-level interface for controlling simulations
- **Components**:
  - `SimulationClient`: Easy-to-use client API
  - Demo functions
- **Responsibilities**:
  - Provide simple API for users
  - Demonstrate system usage
  - Handle communication details

## Usage

### Start the Simulation Engine
```bash
# Make sure NATS server is running with JetStream
./nats-server-v2.10.23-linux-amd64/nats-server -js

# Start the simulation engine
python simulation_engine.py
```

### Control Simulations
```bash
# Run the demo client
python modular_client.py
```

### Or use the client directly
```python
import asyncio
from modular_client import SimulationClient

async def main():
    client = SimulationClient()
    
    # Start a Hopf simulation
    await client.start_hopf_simulation(
        "my_hopf",
        mu=0.5,
        omega=2.0,
        duration=60
    )
    
    # Update parameters while running
    await client.update_simulation("my_hopf", mu=0.8)
    
    # Stop the simulation
    await client.stop_simulation("my_hopf")

asyncio.run(main())
```

## Control Commands

The system responds to control commands on the `sim.control.*` subjects:

### Start Command
```json
{
    "simulation_id": "sim_1",
    "action": "start",
    "parameters": {
        "type": "hopf",
        "duration": 60,
        "mu": 0.1,
        "omega": 1.0,
        "x0": 0.1,
        "y0": 0.1
    }
}
```

### Stop Command
```json
{
    "simulation_id": "sim_1",
    "action": "stop"
}
```

### Update Command
```json
{
    "simulation_id": "sim_1",
    "action": "update",
    "parameters": {
        "mu": 0.5,
        "omega": 2.0
    }
}
```

## Data Streams

Simulation data is published to:
- `sim.hopf.{simulation_id}.{step}` - Hopf bifurcation data
- `sim.predator_prey.{simulation_id}.{step}` - Predator-prey data