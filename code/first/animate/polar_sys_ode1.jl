import DifferentialEquations as DE

import Plots
using Plots; plotlyjs()
using Printf

function bifurk!(du,u,p,t)
    a,b,c = p
    du[1] = (1 + b*u[2]^2)
    du[2] = c*u[2] + a*u[2]^1
end



for i in 0:200
  tspan = (0.0, 200.0)
  p = [-0.001,1,0.1]
  u0 = [-200,2.0+i/100]
  prob = DE.ODEProblem(bifurk!,u0,tspan,p)
  sol = DE.solve(prob)
  p = plot(sol, idxs=(1,2), denseplot=false,
        xlimits=(-200,400),
        ylimits=(0,10)
          )
  savefig(p, "$(@sprintf("%04d",i)).png")
end
