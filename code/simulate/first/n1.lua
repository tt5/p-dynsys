-- Calculate the next state of the Hopf normal form
-- @param x number: current x coordinate
-- @param y number: current y coordinate
-- @param params table: table containing model parameters (mu, omega, alpha, beta, dt)
-- @return number, number: new x and y coordinates
local function hopf_normal_form(x, y, params)
    -- Default parameters for Hopf normal form
    local mu = params.mu or 0.1      -- bifurcation parameter (positive for supercritical, negative for subcritical)
    local omega = params.omega or 1.0 -- frequency of oscillations
    local alpha = params.alpha or -1.0 -- controls amplitude of limit cycle (negative for stable limit cycle)
    local beta = params.beta or 1.0   -- controls frequency shift with amplitude
    local dt = params.dt or 0.01      -- time step
    
    -- Calculate r² = x² + y²
    local r_squared = x*x + y*y
    
    -- Hopf normal form equations
    local dx = (mu * x - omega * y + (alpha * x - beta * y) * r_squared) * dt
    local dy = (omega * x + mu * y + (beta * x + alpha * y) * r_squared) * dt
    
    return x + dx, y + dy
end

function multiplyby2(tag, timestamp, record)
    if record.value1 ~= nil and record.value2 ~= nil then
        local x = record.value1
        local y = record.value2
        
        -- Update state using the Hopf normal form
        local params = {
            mu = 0.1,      -- bifurcation parameter (try values around 0)
            omega = 1.0,   -- frequency of oscillations
            alpha = -1.0,  -- negative for stable limit cycle
            beta = 1.0,    -- frequency shift with amplitude
            dt = 0.01      -- smaller time step for better stability
        }
        record.value1, record.value2 = hopf_normal_form(x, y, params)
    end
    return 1, timestamp, record
end