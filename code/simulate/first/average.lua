local values = {}
local window_size = 10  -- Average over last 10 values

function average_values(tag, timestamp, record)
    -- Initialize storage for this source if needed
    local source = record.source or "default"
    if not values[source] then
        values[source] = {}
    end
    
    -- Add current values to the window
    if record.value1 then
        table.insert(values[source].v1, record.value1)
    end
    if record.value2 then
        table.insert(values[source].v2, record.value2)
    end
    
    -- Keep only the last window_size values
    if #values[source].v1 > window_size then
        table.remove(values[source].v1, 1)
    end
    if #values[source].v2 > window_size then
        table.remove(values[source].v2, 1)
    end
    
    -- Calculate averages
    local sum1 = 0
    local sum2 = 0
    for i, v in ipairs(values[source].v1) do
        sum1 = sum1 + v
    end
    for i, v in ipairs(values[source].v2) do
        sum2 = sum2 + v
    end
    
    record.avg_value1 = sum1 / #values[source].v1
    record.avg_value2 = sum2 / #values[source].v2
    
    -- Return code 1 means keep the modified record
    return 1, timestamp, record
end

return {
    average_values = average_values
}
