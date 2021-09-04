import pyupbit
import numpy as np

df = pyupbit.get_ohlcv("KRW-BTC", interval="day", count=7)
# KRW-BTC 일봉 데이터
df['range'] = (df['high'] - df['low']) * 0.5
# 마지막 열이 자동으로 추가됨
df['target'] = df['open'] + df['range'].shift(1)
# 목표가는 전날 데이터를 이용하기 때문에 shift를 이용해 다음 행으로 이행
df['ror'] = np.where(df['high'] > df['target'],  df['close']/df['target'], 1)
# 각 행마다 고가가 목표가를 넘었으면 수익률인 종가와 목표가의 나눈 값을, 아닌 경우 매수하지 않았으므로 수익률은 1
ror = df['ror'].cumprod()[-2]
# 기간수익률은 모든 수익률의 곱과 동일
print(df.tail())
print(ror)
