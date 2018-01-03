import order
import datetime

def buy(bar):
    print("buy decision")
    orders = []
    date = datetime.datetime(2017,12,11,14,30,0)
    orders.append(order.Order("000001.XSHE",100,date,11.34,True,0))

    return orders