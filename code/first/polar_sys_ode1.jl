import DifferentialEquations as DE

import Plots
using Plots; plotlyjs()

function bifurk!(du,u,p,t)
    a,b,c = p
    du[1] = (1 + b*u[2]^2)
    du[2] = c*u[2] + a*u[2]^3
end

u0 = [0.1,3.2]
p = [-0.01,1,-0.1]

tspan = (0.0, 100.0)
prob = DE.ODEProblem(bifurk!,u0,tspan,p)

sol = DE.solve(prob)

p = plot(sol, idxs=(1,2), denseplot=false)
savefig(p, "out2.png")
