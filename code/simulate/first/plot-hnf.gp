set title "Hopf Normal Form Dynamics"
set xlabel "Time Step"
set ylabel "Value"
set yrange [*:*]  # Auto-scale y-axis
set key top right

# Use line numbers as time steps
plot "< jq -r '.[] | [.value1, .value2] | @tsv' hopf_normal_form.dat" \
     using 0:1 with lines lw 2 title "x (Real part)", \
     "" using 0:2 with lines lw 2 title "y (Imaginary part)"
