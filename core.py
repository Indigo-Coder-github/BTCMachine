import datetime
import pyupbit
import time
import backtesting as bt


class Core():

    def __init__(self, access_key, secret_key, ticker, k):
        self.access_key = access_key
        self.secret_key = secret_key
        # api 발급받은 키
        self.ticker = ticker
        # 기준통화-암호화폐
        self.account = pyupbit.Upbit(access_key, secret_key)
        # 계정 정보를 저장
        self.k = k

    def get_target_price(self):
        target_price = []
        for i, j in zip(self.ticker, self.k):
            df = pyupbit.get_ohlcv(i, count=3)
            yesterday = df.iloc[-2]
            # -1이 마지막행==당일을 불러오므로 -2==어제
            today_open = yesterday['close']
            # 금일 시가는 전일 종가로 잡음
            yesterday_high = yesterday['high']
            # 전일 고가
            yesterday_low = yesterday['low']
            # 전일 저가
            target_price += today_open + (yesterday_high - yesterday_low) * j
            # 매수목표가 = 시가 + 변동폭의 절반값
        return target_price

    def buy_crypto_currency(self, i):
        krw = self.account.get_balance('KRW')  # 잔고의 krw 조회
        orderbook = pyupbit.get_orderbook(self.ticker[i])  # 호가 조회
        sell_price = (orderbook[0]['ask_price'])  # 최우선 호가를 기준으로 unit 계산
        unit = krw/(sell_price*0.9995)  # 수수료 고려
        self.account.buy_market_order(self.ticker[i], unit)  # 시장가로 unit만큼 매수

    def sell_crypto_currency(self):
        for i in self.ticker:
            unit = self.account.get_balance(i)  # 해당하는 암호화폐의 잔량
            self.account.sell_market_order(i, unit)  # 시장가로 unit만큼 매도


now = datetime.datetime.now()  # 현재 날짜와 시각
mid = datetime.datetime(now.year, now.month, now.day, 9, 0, 0)
+ datetime.timedelta(days=1)
# 다음날 아침 9시가 업비트 종가 기준
invest_ticker, ticker_k = bt.instance.calc_noise()
core = Core(None, None, invest_ticker, ticker_k)
# api key와 가져올 화폐를 인자로 객체 생성

while True:
    try:
        now = datetime.datetime.now()
        if mid < now < mid + datetime.delta(seconds=10):  # 종시와 종시 10초 후 사이일 경우
            target_price = core.get_target_price()  # 매수목표가 호출
            mid = datetime.datetime(now.year, now.month, now.day)
            +datetime.timedelta(1)
            core.sell_crypto_currency()  # 종시에 판매

        current_price = list(pyupbit.get_current_price(
            bt.instance.get_invest_ticker()).values())
        # 현재가 조회
        for i in range(0, len(current_price)):
            if current_price[i] >= target_price[i]:  # 현재가가 매수 목표가 이상이면
                core.buy_crypto_currency(i)  # 해당 가격에 구매
    except Exception:
        print("error")  # 오류시 프로그램 종료 방지

    time.sleep(1)  # 1초뒤 반복
