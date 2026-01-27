local counter = 0
local last_time = 0

function clock_generator(tag, timestamp, record)
    counter = counter + 1
    
    -- Generate a clock message every 100ms
    local current_time = os.clock()
    if current_time - last_time >= 0.1 then
        last_time = current_time
        
        -- Create a clock message with current timestamp
        local clock_record = {
            value1 = 0,
            value2 = 0,
            source = "clock",
            timestamp = current_time
        }
        
        -- Return with current time in nanoseconds
        return 1, current_time * 1000000000, clock_record
    end
    
    -- Don't pass through the original record
    return -1, timestamp, nil
end

return {
    clock_generator = clock_generator
}
