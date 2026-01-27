local counter = 0
local max_rate = 50
local start_time = 0
local last_output_time = 0

function rate_control(tag, timestamp, record)
    counter = counter + 1
    
    -- Initialize start time on first message
    if start_time == 0 then
        start_time = timestamp
        last_output_time = timestamp
    end
    
    -- Check for external control signals every 10 messages
    if counter % 10 == 1 then
        local file = io.open("rate_control", "r")
        if file then
            local content = file:read("*all")
            file:close()
            local new_rate = tonumber(content)
            if new_rate and new_rate >= 0 then
                max_rate = new_rate
            end
        end
    end
    
    -- Calculate minimum interval between outputs
    local min_interval = 1 / max_rate  -- nanoseconds (1 second / rate)
    
    -- Check if enough time has passed since last output
    local time_since_last = timestamp - last_output_time
    
    if time_since_last >= min_interval then
        -- Let this message through
        last_output_time = timestamp
        return 1, timestamp, record
    else
        -- Too soon, but let 1 out of 5 through to keep feedback alive
        if counter % 2 == 0 then
            last_output_time = timestamp
            return 1, timestamp, record
        else
            return -1, timestamp, nil
        end
    end
end

return {
    rate_control = rate_control
}
