# Minimal NATS Dynamic Systems Simulation

A minimal Python project that demonstrates using NATS for real-time dynamic systems simulation, similar to the Lua simulation scripts in the parent directory.

## Features

- **Predator-Prey Simulation**: Lotka-Volterra equations published via NATS
- **Hopf Bifurcation Simulation**: Limit cycle dynamics published via NATS  
- **Real-time Visualization**: Live plotting of simulation data
- **JetStream Support**: Persistent streams and durable consumers

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Start NATS server (if not already running)
docker run -d --name nats -p 4222:4222 nats:latest
```

## Usage

### 1. Start the Publisher

```bash
python nats_publisher.py
```

This will:
- Connect to NATS server at `localhost:4222`
- Create JetStream stream `SIMULATION`
- Publish predator-prey simulation data for 30 seconds
- Publish Hopf bifurcation data for 30 seconds

### 2. Start the Subscriber

```bash
python nats_subscriber.py
```

This will:
- Subscribe to both simulation data streams
- Collect data in memory
- Generate live plots every 2 seconds
- Save plots as PNG files

### 3. Configuration

Edit `config.py` to modify:
- NATS server connection
- Simulation parameters
- Plotting settings

## Architecture

```
nats_publisher.py ──┐
                    ├── NATS JetStream ─── nats_subscriber.py ─── Live Plots
nats_publisher.py ──┘
```

- **Publisher**: Runs simulations and publishes data to NATS subjects:
  - `sim.predator_prey.{step}` - Predator-prey data
  - `sim.hopf.{step}` - Hopf bifurcation data
- **Subscriber**: Consumes data and creates visualizations
- **JetStream**: Provides persistence and guaranteed delivery

## Data Format

### Predator-Prey Messages
```json
{
  "timestamp": 1234567890.123,
  "step": 100,
  "prey": 12.34,
  "predator": 5.67,
  "dx_dt": 0.123,
  "dy_dt": -0.456,
  "parameters": {"alpha": 1.1, "beta": 0.4, "delta": 0.1, "gamma": 0.4}
}
```

### Hopf Bifurcation Messages
```json
{
  "timestamp": 1234567890.123,
  "step": 1000,
  "x": 0.123,
  "y": 0.456,
  "r": 0.473,
  "theta": 1.308,
  "dx_dt": 0.001,
  "dy_dt": 0.002,
  "parameters": {"mu": 0.5, "omega": 2.0}
}
```

## Comparison with Lua Project

This Python/NATS version provides similar functionality to the Lua simulation scripts:

| Lua Script | Python Equivalent |
|------------|-------------------|
| `n1-predprey.lua` | `nats_publisher.py` (predator_prey method) |
| `hopf_normal_form.dat` | `nats_publisher.py` (hopf method) |
| `visualization/plot_live.py` | `nats_subscriber.py` (live plotting) |
| `.conf` files | `config.py` |

## Output Files

- `predator_prey_plot.png` - Phase space and time series plots
- `hopf_plot.png` - Hopf bifurcation visualizations
- Console output showing real-time simulation progress

## Dependencies

- `nats-py` - NATS client for Python
- `matplotlib` - Plotting and visualization
- `numpy` - Numerical computations
- `asyncio` - Asynchronous programming

## Troubleshooting

1. **Connection Error**: Ensure NATS server is running on `localhost:4222`
2. **No Data**: Check that publisher is running before subscriber
3. **Missing Plots**: Verify matplotlib backend and permissions for output directory
