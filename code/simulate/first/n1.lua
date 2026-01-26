local N = 0  -- prey population
local P = 0  -- predator population
-- Model parameters
local alpha = 1.1  -- prey growth rate
local beta = 0.1   -- predation rate
local delta = 0.1  -- predator growth rate
local gamma = 0.4  -- predator death rate
local dt = 0.1     -- time step

function multiplyby2(tag, timestamp, record)
    if record.value1 ~= nil and record.value2 ~= nil then
        N = record.value1
        P = record.value2
        
        -- Lotka-Volterra equations
        local dN = (alpha * N - beta * N * P) * dt
        local dP = (delta * N * P - gamma * P) * dt
        
        -- Update populations
        record.value1 = N + dN
        record.value2 = P + dP
    end
    return 1, timestamp, record
end