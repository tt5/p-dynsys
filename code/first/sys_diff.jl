import DifferentialEquations as DE

import Plots
using Plots; plotlyjs()

function lorenz!(du,u,p,t)
    a,b,c,d,e,f,g,h,i = p
    du[1] = u[1] - a*cos(u[1])*u[1] - b*cos(u[3])*u[3] - c*cos(u[2])*u[2]
    du[2] = u[2] - d*cos(u[2])*u[2] - e*cos(u[1])*u[1] - f*cos(u[3])*u[3]
    du[3] = u[3] - g*cos(u[3])*u[3] - h*cos(u[1])*u[1] - i*cos(u[2])*u[2]
end

u0 = [1.0,1.0,1.0]
p = [0.1,0.1,0.1,0.2,0.2,0.2,0.4,0.4,0.4]

tspan = (0.0, 80.0)
prob = DE.ODEProblem(lorenz!,u0,tspan,p)

sol = DE.solve(prob)

p = plot(sol, idxs=(1,2,3), denseplot=false)
savefig(p, "out.pdf")
