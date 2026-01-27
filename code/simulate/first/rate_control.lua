local counter = 0
local max_rate = 50

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
    
    -- Drop if we exceed the rate limit
    if counter % (max_rate + 1) == 0 then
        return -1, timestamp, nil  -- Drop the record
    end
    
    -- Return code 1 means keep the record
    return 1, timestamp, record
end

return {
    rate_control = rate_control
}
