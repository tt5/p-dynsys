# Usage

`mkfifo fifo`

ports 8000, 8001

`fluent-bit -c n1.conf`
`fluent-bit -c n2.conf`

`echo '{"value1": 1.0, "value2": 0.5}' >> fifo`

`fluent-bit -c n3.conf > predator_prey.dat`

`gnuplot -p plot.gp`

`fluent-bit -c n3.conf | python3 visualization/plot_live.py`

# Lua Script Behavior

Script Loading:
The script is loaded once when Fluent Bit starts
last_sample_time is initialized to 0 at this point
The sample function is registered with Fluent Bit
Log Processing:
For each incoming log, Fluent Bit calls the registered sample function
The last_sample_time variable maintains its value between these function calls
