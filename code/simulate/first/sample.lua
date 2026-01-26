local last_sample_time = 0
function sample(tag, timestamp, record)
    local current_time = os.time()

    if current_time - last_sample_time >= 10 then
        last_sample_time = current_time
        -- Return code 1 means keep the record
        return 1, timestamp, record
    end

    -- Return code -1 means drop the record
    return -1, 0, 0
end
-- Register the function
return {
    sample = sample
}
