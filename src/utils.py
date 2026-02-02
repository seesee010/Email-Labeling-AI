def utilsBatchList(items, batchSize):
    # batch list into chunks
    for i in range(0, len(items), batchSize):
        yield items[i:i + batchSize]
