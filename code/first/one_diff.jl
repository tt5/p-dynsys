import DifferentialEquations as DE
f(u, p, t) = 1.01 * u
u0 = 0
tspan = (0.0, 1.0)
prob = DE.ODEProblem(f, u0, tspan)
sol = DE.solve(prob, DE.Tsit5(), reltol = 1e-8, abstol = 1e-8)

import Plots
using Plots; plotlyjs()
p = plot(sol, linewidth = 5, title = "Solution to the linear ODE with a thick line",
    xaxis = "Time (t)", yaxis = "u(t) (in μm)", label = "My Thick Line!") # legend=false
savefig(p, "out.pdf")
