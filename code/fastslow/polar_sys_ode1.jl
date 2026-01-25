import DifferentialEquations as DE

import Plots
using Plots; plotlyjs()
using Printf

function bifurk!(du,u,p,t)
    a,b,c,d,e = p
    du[1] = d * u[1] - u[1]^2 - (a * u[1] * u[2]) / (c + u[1] + u[2])
    du[2] = e * ((b * u[1] * u[2]) / (c + u[1] + u[2]) - c * u[2])
end

# a capture rate
# b consumption rate
# c predator death rate
# d birth rate of prey
# e slow

for i in 0:800
  tspan = (0.0, 400.0)
  p = [1.6, 0.5, 0.0207, 1.3, 1]
  u0 = [0.0001+i/1000, 0.1]
  prob = DE.ODEProblem(bifurk!,u0,tspan,p)
  sol = DE.solve(prob)
  p = plot(sol, idxs=(1,2), denseplot=false,
        xlimits=(0,4),
        ylimits=(0,4)
          )
  savefig(p, "$(@sprintf("%04d",i)).png")
end
