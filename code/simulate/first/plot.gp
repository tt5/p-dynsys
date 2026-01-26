set title "Predator-Prey Dynamics"
set xlabel "Time Step"
set ylabel "Population"
set logscale y
set yrange [1e-20:100]

# Use line numbers as time steps
plot "< jq -r '.[] | [.value1, .value2] | @tsv' predator_prey.dat" \
     using 0:1 with lines title "Prey", \
     "" using 0:2 with lines title "Predator"