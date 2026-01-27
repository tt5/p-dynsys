local counter = 0
function sample(tag, timestamp, record)
    counter = counter + 1
    
    return 1, timestamp, record

end
-- Register the function
return {
    sample = sample
}
