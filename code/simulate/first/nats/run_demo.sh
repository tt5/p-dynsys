#!/bin/bash

# Demo script for NATS simulation project
# Similar to myscript.sh in parent directory

echo "=== NATS Dynamic Systems Simulation Demo ==="

# Check if NATS server is running
if ! pgrep -f "nats-server" > /dev/null; then
    echo "Starting NATS server with Docker..."
    docker run -d --name nats-demo -p 4222:4222 nats:latest
    sleep 3
else
    echo "NATS server is already running"
fi

# Install dependencies if needed
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    echo "Virtual environment exists"
    source venv/bin/activate
fi

echo ""
echo "Starting simulation publisher..."
echo "This will run predator-prey and Hopf simulations for 30 seconds each"
echo ""

# Run publisher in background
python nats_publisher.py &
PUBLISHER_PID=$!

# Wait a moment for publisher to start
sleep 2

echo ""
echo "Starting subscriber with live plotting..."
echo "Plots will be updated every 2 seconds"
echo ""

# Run subscriber
python nats_subscriber.py

# Clean up
echo ""
echo "Cleaning up..."
kill $PUBLISHER_PID 2>/dev/null
docker stop nats-demo 2>/dev/null
docker rm nats-demo 2>/dev/null

echo "Demo completed! Check the generated PNG files."
