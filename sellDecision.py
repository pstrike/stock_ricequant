import order

# update position highestPrice
def sell(bar, positions):
    print("sell decision")

    orders = []
    for pid in positions:
        p = positions[pid]
        for b in bar:
            if p.stockId == b["order_book_id"] and p.highestPrice < b["close"]:
                p.highestPrice = b.close
            elif p.stockId == b["order_book_id"] and p.highestPrice * p.lostTolerance > b["close"]:
                orders.append(order.Order(p.stockId,p.amount,b["datetime"],b["close"],False,p.id))

    return orders