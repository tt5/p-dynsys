# Complete CLI Commands Reference

## Basic Usage
```bash
python modular_client.py [ACTION] [SIM_ID] [--params '{"param": "value"}'] [--server nats://localhost:4222]
```

## Actions Available
- `start-hopf` - Start Hopf bifurcation simulation
- `start-pp` - Start predator-prey simulation  
- `stop` - Stop running simulation
- `pause` - Pause simulation
- `resume` - Resume paused simulation
- `update` - Update simulation parameters
- `status` - Get simulation status

## Hopf Simulation Parameters
```json
{
  "type": "hopf",
  "duration": 60,           // Simulation duration in seconds
  "dt": 0.001,             // Time step (use 0.001 for high precision)
  "mu": 0.1,               // Bifurcation parameter
  "omega": 1.0,            // Frequency of oscillations
  "alpha": -1.0,           // Negative for stable limit cycle
  "beta": 1.0,             // Frequency shift with amplitude
  "x0": 0.1,               // Initial x coordinate
  "y0": 0.1,               // Initial y coordinate
  
  // Performance optimization parameters
  "integration_method": "rk4",     // "euler", "rk2", "rk4"
  "publish_frequency": 200,        // Publish every N steps
  "status_frequency": 2000,        // Status updates every N steps
  "debug": false,                  // Enable/disable debug prints
  
  // External input (optional)
  "external_input": false,
  "input_subject": "sim.input.>",
  "input_strength": 0.1
}
```

## Predator-Prey Simulation Parameters
```json
{
  "type": "predator_prey",
  "duration": 60,           // Simulation duration in seconds
  "dt": 0.1,               // Time step
  "alpha": 1.1,            // Prey growth rate
  "beta": 0.4,             // Predation rate
  "delta": 0.1,            // Predator efficiency
  "gamma": 0.4,            // Predator death rate
  "prey0": 10.0,           // Initial prey population
  "predator0": 5.0,        // Initial predator population
  
  // Performance optimization parameters
  "integration_method": "rk4",     // "euler", "rk2", "rk4"
  "publish_frequency": 50,         // Publish every N steps
  "status_frequency": 500,         // Status updates every N steps
  "debug": false                   // Enable/disable debug prints
}
```

## Example Commands

### High Precision Hopf (Recommended)
```bash
python modular_client.py start-hopf hopf_high_precision --params '{"dt": 0.001, "integration_method": "rk4", "publish_frequency": 200, "status_frequency": 2000, "debug": false, "mu": 0.5, "omega": 2.0, "duration": 60}'
```

### Standard Hopf
```bash
python modular_client.py start-hopf hopf_1 --params '{"mu": 0.5, "omega": 2.0, "duration": 30}'
```

### Predator-Prey
```bash
python modular_client.py start-pp pp_1 --params '{"alpha": 1.5, "beta": 0.5, "duration": 45}'
```

### Control Commands
```bash
# Stop simulation
python modular_client.py stop hopf_1

# Pause simulation
python modular_client.py pause hopf_1

# Resume simulation
python modular_client.py resume hopf_1

# Check status
python modular_client.py status hopf_1

# Update parameters
python modular_client.py update hopf_1 --params '{"mu": 0.8, "omega": 1.5}'

# Update performance settings
python modular_client.py update hopf_1 --params '{"publish_frequency": 100, "debug": true}'
```

### Custom Server
```bash
python modular_client.py start-hopf hopf_test --params '{"mu": 0.3}' --server nats://192.168.1.100:4222
```

## Performance Profiles

### Maximum Performance
```json
{
  "dt": 0.001,
  "integration_method": "rk4",
  "publish_frequency": 500,
  "status_frequency": 5000,
  "debug": false
}
```

### Balanced Performance
```json
{
  "dt": 0.001,
  "integration_method": "rk2", 
  "publish_frequency": 200,
  "status_frequency": 2000,
  "debug": false
}
```

### Debug Mode
```json
{
  "dt": 0.001,
  "integration_method": "rk4",
  "publish_frequency": 50,
  "status_frequency": 500,
  "debug": true
}
```

## Tips
- Use `integration_method: "rk4"` for best accuracy with `dt: 0.001`
- Increase `publish_frequency` to reduce CPU load (100-500 recommended)
- Set `debug: false` for production runs
- Use `status_frequency` to control console output frequency
- Parameters can be updated on-the-fly with the `update` command
