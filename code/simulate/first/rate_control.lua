local counter = 0
local max_rate = 50
local last_message_time = 0

function rate_control(tag, timestamp, record)
    counter = counter + 1
    
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
    
    -- Calculate minimum time between messages (nanoseconds)
    local min_interval = 1000000000 / max_rate  -- 1 second / max_rate
    
    -- Track message times for rate limiting (timestamp is in nanoseconds)
    local current_time_ns = timestamp
    
    -- Drop if too soon since last message
    if last_message_time > 0 and (current_time_ns - last_message_time) < min_interval then
        -- Drop every second message when too close
        if counter % 2 == 0 then
            return -1, timestamp, nil  -- Drop the record
        end
    end
    
    last_message_time = current_time_ns
    
    -- Return code 1 means keep the record
    return 1, timestamp, record
end

return {
    rate_control = rate_control
}
