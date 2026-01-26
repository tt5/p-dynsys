set title "Hopf Normal Form Phase Portrait"
set xlabel "x (Real part)"
set ylabel "y (Imaginary part)"
set key off
set size square
set xrange [-1.5:1.5]  # Adjust based on your data range
set yrange [-1.5:1.5]  # Adjust based on your data range

plot "< jq -r '.[] | [.value1, .value2] | @tsv' hopf_normal_form.dat" \
     using 1:2 with lines lw 2