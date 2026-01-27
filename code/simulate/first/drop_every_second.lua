local counter = 0
local drop_enabled = false

function drop_every_second(tag, timestamp, record)
    counter = counter + 1
    
    -- Check for toggle command
    if record.toggle_drop ~= nil then
        drop_enabled = record.toggle_drop
        print("Drop toggled to:", drop_enabled)
        return -1, timestamp, nil  -- Drop the control message
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
