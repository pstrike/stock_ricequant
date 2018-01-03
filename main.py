import bardata
import buyDecision
import sellDecision
import tradeAgent
import position
import datetime

# in context
positions = {}
# initial position
preposition = position.Position("000001.XSHE",500,datetime.datetime(2017,12,01,14,0,0),15.01,0,0,15.01,0.98)
positions[preposition.id] = preposition

# in every bar
orders = []

buyOrders = buyDecision.buy(bardata.bar)
if buyOrders:
    orders = orders + buyOrders

sellOrders = sellDecision.sell(bardata.bar, positions)
if sellOrders:
    orders = orders + sellOrders

for item in orders:
    result = tradeAgent.execute(item)

    if result:
        if item.isBuy:
            position = item.convertToPosition()
            positions[position.id] = position
        else:
            positions[item.refPositionId].sellTime = item.time
            positions[item.refPositionId].sellPrice = item.price
    else:
        print("order error")

print("done")

