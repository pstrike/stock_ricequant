# 可以自己import我们平台支持的第三方python模块，比如pandas、numpy等。
import uuid
import talib
import datetime


class Position(object):
    def __init__(self, stock_id, amount, buy_datetime, buy_price, sell_datetime, sell_price, highest_price,
                 lost_tolerance):
        self.id = uuid.uuid1()
        self.stock_id = stock_id
        self.amount = amount
        self.buy_datetime = buy_datetime
        self.buy_price = buy_price
        self.sell_datetime = sell_datetime
        self.sell_price = sell_price
        self.highest_price = highest_price
        self.lost_tolerance = lost_tolerance


class Order(object):
    def __init__(self, stock_id, amount, datetime, price, is_buy, ref_position_id):
        self.id = uuid.uuid1()
        self.stock_id = stock_id
        self.amount = amount
        self.datetime = datetime
        self.price = price
        self.is_buy = is_buy
        self.ref_position_id = ref_position_id

    def convertToPosition(self, context):
        return Position(self.stock_id, self.amount, self.datetime, self.price, 0, 0, self.price, context.LOSTTOLERANCE)


# 在这个方法中编写任何的初始化逻辑。context对象将会在你的算法策略的任何方法之间做传递。
def init(context):
    # 在context中保存全局变量
    context.stocks = [
        "000001.XSHE"
    ]

    context.LOSTTOLERANCE = 0.95

    # 使用MACD需要设置长短均线和macd平均线的参数
    context.SHORTPERIOD = 12
    context.LONGPERIOD = 26
    context.SMOOTHPERIOD = 9
    context.OBSERVATION = 100
    context.positions = {}
    context.BUYAMOUNT = 100

    # 实时打印日志
    logger.info("RunInfo: {}".format(context.run_info))


# before_trading此函数会在每天策略交易开始前被调用，当天只会被调用一次
def before_trading(context):
    pass


# 你选择的证券的数据更新将会触发此段逻辑，例如日或分钟历史数据切片或者是实时数据切片更新
def handle_bar(context, bar_dict):
    # 开始编写你的主要的算法逻辑

    # bar_dict[order_book_id] 可以拿到某个证券的bar信息
    # context.portfolio 可以拿到现在的投资组合信息

    # 使用order_shares(id_or_ins, amount)方法进行落单

    # TODO: 开始编写你的算法吧！
    orders = []
    buy_orders = []
    sell_orders = []

    for stock_id in context.stocks:
        buy_order_result = buy_decision(context, bar_dict, stock_id)
        if buy_order_result:
            buy_orders.append(buy_order_result)

    for position_id in context.positions:
        if context.positions[position_id].sell_price == 0:
            sell_order_result = sell_decision(context, bar_dict, context.positions[position_id])
            if sell_order_result:
                sell_orders.append(sell_order_result)

    orders = buy_orders + sell_orders

    for order in orders:
        result = trade_agent(order)
        if result:
            if order.is_buy:
                position = order.convertToPosition(context)
                context.positions[position.id] = position
            else:
                context.positions[order.ref_position_id].sell_datetime = order.datetime
                context.positions[order.ref_position_id].sell_price = order.price
        else:
            print("order error")

    pass


# after_trading函数会在每天交易结束后被调用，当天只会被调用一次
def after_trading(context):
    for position_id in context.positions:
        print_position(context.positions[position_id])

    pass


def buy_decision(context, bar_dict, stock_id):
    result = None
    # 读取历史数据，使用sma方式计算均线准确度和数据长度无关，但是在使用ema方式计算均线时建议将历史数据窗口适当放大，结果会更加准确
    prices = history_bars(stock_id, context.OBSERVATION, '1d', 'close')

    # 用Talib计算MACD取值，得到三个时间序列数组，分别为macd, signal 和 hist
    macd, signal, hist = talib.MACD(prices, context.SHORTPERIOD,
                                    context.LONGPERIOD, context.SMOOTHPERIOD)

    plot("macd", macd[-1])
    plot("macd signal", signal[-1])

    # macd 是长短均线的差值，signal是macd的均线，使用macd策略有几种不同的方法，我们这里采用macd线突破signal线的判断方法

    # 如果短均线从下往上突破长均线，为入场信号
    if macd[-1] - signal[-1] > 0 and macd[-2] - signal[-2] < 0:
        result = Order(stock_id, context.BUYAMOUNT, datetime.datetime.now(), bar_dict[stock_id].close, True, 0)

    return result


def sell_decision(context, bar_dict, position):
    result = None

    if position.highest_price < bar_dict[position.stock_id].close:
        position.highest_price = bar_dict[position.stock_id].close
    elif position.highest_price * position.lost_tolerance > bar_dict[position.stock_id].close:
        result = Order(position.stock_id, position.amount, datetime.datetime.now(), bar_dict[position.stock_id].close,
                       False, position.id)

    return result


def trade_agent(order):
    if order.is_buy:
        order_shares(order.stock_id, order.amount, style=LimitOrder(order.price))
    else:
        order_shares(order.stock_id, -1 * order.amount, style=LimitOrder(order.price))
    return True


def print_position(position):
    logger.info("stock:%s;buy:%f;sell:%f;percentage:%.2f pct" % (
    position.stock_id, position.buy_price, position.sell_price,
    100 * (position.sell_price - position.buy_price) / position.buy_price))
    pass