local counter = 0
local max_rate = 50
local message_times = {}
local last_second = 0
local messages_this_second = 0

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
    
    -- Track message times for rate limiting (timestamp is in nanoseconds)
    local current_time_ns = timestamp
    local current_second = math.floor(current_time_ns / 1000000000)
    
    -- Reset counter every second
    if current_second ~= last_second then
        last_second = current_second
        messages_this_second = 0
    end
    
    messages_this_second = messages_this_second + 1
    
    -- Drop if we exceed the rate limit for this second
    if messages_this_second > max_rate then
        -- Drop every second message when over limit
        if messages_this_second % 2 == 0 then
            return -1, timestamp, nil  -- Drop the record
        end
    end
    
    -- Return code 1 means keep the record
    return 1, timestamp, record
end

return {
    rate_control = rate_control
}
