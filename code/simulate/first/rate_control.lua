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
    local min_interval = 1000000000 / max_rate  -- nanoseconds
    
    -- Calculate when this message should be output
    local scheduled_time = last_output_time + min_interval
    
    if timestamp >= scheduled_time then
        -- Message is late enough, let it through
        kept_count = kept_count + 1
        last_output_time = timestamp
        return 1, timestamp, record
    else
        -- Message is too early, delay it by updating its timestamp
        local delayed_timestamp = scheduled_time
        last_output_time = delayed_timestamp
        return 1, delayed_timestamp, record  -- Return with delayed timestamp
    end
end

return {
    rate_control = rate_control
}
