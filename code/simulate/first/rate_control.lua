local counter = 0
local max_rate = 50
local message_times = {}

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
    
    -- Track message times for rate limiting
    local current_time = os.time()
    table.insert(message_times, current_time)
    
    -- Remove messages older than 1 second
    local i = 1
    while i <= #message_times do
        if current_time - message_times[i] >= 1 then
            table.remove(message_times, i)
        else
            i = i + 1
        end
    end
    
    -- Drop if we exceed the rate limit per second
    if #message_times > max_rate then
        return -1, timestamp, nil  -- Drop the record
    end
    
    -- Return code 1 means keep the record
    return 1, timestamp, record
end

return {
    rate_control = rate_control
}
