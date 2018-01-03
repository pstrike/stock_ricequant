import uuid
import position

class Order(object):

    def __init__(self, stockId, amount, time, price, isBuy, refPositionId):
        self.stockId = stockId
        self.amount = amount
        self.time = time
        self.price = price
        self.isBuy = isBuy
        self.refPositionId = refPositionId

        # Initialize property
        self.id = uuid.uuid1()

    def convertToPosition(self):
        return position.Position(self.stockId,self.amount,self.time,self.price,0,0,self.price,0.05)
