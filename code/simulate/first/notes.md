# Usage

`mkfifo fifo`

ports 8000, 8001

different terminals:

`fluent-bit -c n1.conf`
`fluent-bit -c n2.conf`
`fluent-bit -c n3.conf`

then start it with `echo "1" >> fifo`

# Sample Script

Script Loading:
The script is loaded once when Fluent Bit starts
last_sample_time is initialized to 0 at this point
The sample function is registered with Fluent Bit
Log Processing:
For each incoming log, Fluent Bit calls the registered sample function
The last_sample_time variable maintains its value between these function calls
