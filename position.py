import uuid

class Position(object):

    def __init__(self, stockId, amount, buyTime, buyPrice, sellTime, sellPrice, highestPrice, lostTolerance):
        self.stockId = stockId
        self.amount = amount
        self.buyTime = buyTime
        self.buyPrice = buyPrice
        self.sellTime = sellTime
        self.sellPrice = sellPrice
        self.highestPrice = highestPrice
        self.lostTolerance = lostTolerance

        # Initialize property
        self.id = uuid.uuid1()
