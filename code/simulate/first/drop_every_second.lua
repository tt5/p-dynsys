local counter = 0
local drop_enabled = false
local drop_next = 0

function drop_every_second(tag, timestamp, record)
    counter = counter + 1
    
    -- Check for toggle command
    if record.toggle_drop ~= nil then
        drop_enabled = record.toggle_drop
        print("Drop toggled to:", drop_enabled)
        return -1, timestamp, nil  -- Drop the control message
    end
    
    -- Check for drop commands
    if record.drop_one == true then
        print("Dropping one message")
        return -1, timestamp, nil  -- Drop this message only
    end
    
    if record.drop_two == true then
        print("Dropping two messages")
        drop_next = 1  -- Set counter to drop next 2 messages
        return -1, timestamp, nil  -- Drop this message too
    end
    
    -- Drop if we have pending drops
    if drop_next > 0 then
        drop_next = drop_next - 1
        print("Dropping message, remaining:", drop_next)
        return -1, timestamp, nil
    end
    
    -- Drop every second message if enabled
    if drop_enabled and counter % 2 == 0 then
        return -1, timestamp, nil  -- Drop the record
    end
    
    -- Keep the record
    return 1, timestamp, record
end

return {
    drop_every_second = drop_every_second
}
