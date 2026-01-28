./nats-server -js -sd /tmp/nats-data -m 8222

python3 cleanup_nats.py
python3 setup_nats_streams.py
