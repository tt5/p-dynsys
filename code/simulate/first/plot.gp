set title "Predator-Prey Dynamics"
set xlabel "Time Step"
set ylabel "Population"
set logscale y
set yrange [1e-20:100]

# Use jq to extract data with line numbers
plot "< jq -r 'to_entries[] | [.key, .value.value1, .value.value2] | @tsv' predator_prey.dat" \
     using 1:2 with lines title "Prey", \
     "" using 1:3 with lines title "Predator"