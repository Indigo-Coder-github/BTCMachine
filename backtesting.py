import datetime
import pyupbit
import numpy as np


class Backtesting():

    def __init__(self, tickers, yesterday):
        self.tickers = tickers
        self.yesterday = yesterday

    def calc_noise(self):
        
        invest_ticker = []
        ticker_k = []

        for ticker in self.tickers:
            df = pyupbit.get_ohlcv(ticker, count=30, interval="day",
                                   to=self.yesterday)
            # KRW-BTC 일봉 데이터
            df['noise'] = 1 - abs((df['open']-df['close'])
                                  / (df['high']-df['low']))
            noise = df['noise'].sum()/30
            # 30일 전체 noise에 대한 평균 noise 산출
            df['range'] = (df['high'] - df['low']) * noise
            # 마지막 열이 자동으로 추가됨
            df['target'] = df['open'] + df['range'].shift(1)
            # 목표가는 전날 데이터를 이용하기 때문에 shift를 이용해 다음 행으로 이행
            df['ror'] = np.where(df['high'] > df['target'],
                                 df['close']/df['target'] * 0.99900025, 1)
            # 각 행마다 고가가 목표가를 넘었으면 수익률인 종가와 목표가의 나눈 값을, 아닌 경우 매수하지 않았으므로 수익률은 1
            # ror = df['ror'].cumprod()[-2]
            # 기간수익률은 모든 수익률의 곱과 동일
            invest_ticker.append([noise, ticker])
        invest_ticker.sort()
        invest_ticker = invest_ticker[:5]
        for i, j in zip(invest_ticker, range(0, len(invest_ticker))):
            invest_ticker[j] = i[1]
            ticker_k.append(i[0])
            
        return invest_ticker, ticker_k


instance = Backtesting(
    pyupbit.get_tickers(fiat='KRW'),
    (datetime.datetime.now()-datetime.timedelta(days=1)).strftime('%Y%m%d'))
print(instance.calc_noise())