import datetime
import pyupbit
import time


class Core():

    def __init__(self, access_key, secret_key, ticker):
        self.access_key = access_key
        self.secret_key = secret_key
        # api 발급받은 키
        self.ticker = ticker
        # 기준통화-암호화폐
        self.account = pyupbit.Upbit(access_key, secret_key)
        # 계정 정보를 저장

    def get_target_price(self):
        df = pyupbit.get_ohlcv(self.ticker)

        yesterday = df.iloc[-2]
        # -1이 마지막행==당일을 불러오므로 -2==어제
        today_open = yesterday['close']
        # 금일 시가는 전일 종가로 잡음
        yesterday_high = yesterday['high']
        # 전일 고가
        yesterday_low = yesterday['low']
        # 전일 저가
        target_price = today_open + (yesterday_high - yesterday_low) * 0.5
        # 매수가 = 시가 + 변동폭의 절반값
        return target_price
        # 매수가 반환

    def buy_crypto_currency(self):
        # krw = self.account.get_balance('KRW')
        orderbook = pyupbit.get_orderbook(self.ticker)
        sell_price = (orderbook[0]['ask_price'])
        # unit = krw/(sell_price*0.9995)
        self.account.buy_market_order(self.ticker, sell_price)

    def sell_crypto_currency(self):
        unit = self.account.get_balance(self.ticker)
        self.account.sell.market_order(self.ticker, unit)


now = datetime.datetime.now()  # 현재 시각
mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
core = Core(None, None, 'KRW-XRP')

while True:
    try:
        now = datetime.datetime.now()
        if mid < now < mid + datetime.delta(seconds=10):
            target_price = core.get_target_price()
            mid = datetime.datetime(now.year, now.month, now.day)
            +datetime.timedelta(1)
            core.sell_crypto_currency()

        current_price = pyupbit.get_current_price('KRW-XRP')
        if current_price > target_price:
            core.buy_crypto_currency()
    except Exception:
        print("error")

    time.sleep(1)
