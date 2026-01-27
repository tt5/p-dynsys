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
    
    -- Check if we should drop this message
    local should_drop = false
    
    if last_message_time > 0 and (current_time_ns - last_message_time) < min_interval then
        -- Too soon - drop every second message
        if counter % 6 == 0 then
            should_drop = true
        end
    end
    
    -- Update last_message_time only for kept messages
    if not should_drop then
        last_message_time = current_time_ns
    end
    
    if should_drop then
        return -1, timestamp, nil  -- Drop the record
    end
    
    -- Return code 1 means keep the record
    return 1, timestamp, record
end

return {
    rate_control = rate_control
}
