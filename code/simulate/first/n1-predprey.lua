-- Calculate the next state of the Lotka-Volterra system
-- @param N number: current prey population
-- @param P number: current predator population
-- @param params table: table containing model parameters (alpha, beta, delta, gamma, dt)
-- @return number, number: new prey and predator populations
local function lotka_volterra(N, P, params)
    local alpha = params.alpha or 1.1
    local beta = params.beta or 0.1
    local delta = params.delta or 0.1
    local gamma = params.gamma or 0.4
    local dt = params.dt or 0.1
    
    -- Lotka-Volterra equations
    local dN = (alpha * N - beta * N * P) * dt
    local dP = (delta * N * P - gamma * P) * dt
    
    return N + dN, P + dP
end

function multiplyby2(tag, timestamp, record)
    if record.value1 ~= nil and record.value2 ~= nil then
        N = record.value1
        P = record.value2
        
        -- Update populations using the Lotka-Volterra function
        local params = {
            alpha = alpha,
            beta = beta,
            delta = delta,
            gamma = gamma,
            dt = dt
        }
        record.value1, record.value2 = lotka_volterra(N, P, params)
    end
    return 1, timestamp, record
end