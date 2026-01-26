function multiplyby2(tag, timestamp, record)
    record.exec = record.exec * 2
    return 1, timestamp, record
end
