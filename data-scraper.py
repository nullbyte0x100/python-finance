from cProfile import label
from curses import window
from turtle import color
import pandas as pd
import pandas_datareader as pdr
import matplotlib.pyplot as plt
import datetime as dt
plt.style.use("dark_background")
ma_1=30
ma_2=100
start=dt.datetime.now()-dt.timedelta(days=365*5)
end=dt.datetime.now()
data=pdr.DataReader('BA','yahoo',start,end)
#data.to_csv("boeing.csv")
data=data.iloc[ma_2:]
data[f'SMA_{ma_1}']=data['Adj Close'].rolling(window=ma_1).mean()
data[f'SMA_{ma_2}']=data['Adj Close'].rolling(window=ma_2).mean()
plt.plot(data['Adj Close'],label="Share Price",color="lightgray")
plt.plot(data[f'SMA_{ma_1}'],label=f"SMA_{ma_1}",color="orange")
plt.plot(data[f"SMA_{ma_2}"],label=f"SMA_{ma_2}",color="purple")
plt.legend(loc="upper left")
buy=[]
sell=[]
trigger=0
for x in range(len(data)):
    if data[f'SMA_{ma_1}'].iloc[x]>data[f'SMA_{ma_2}'].iloc[x] and trigger!=1:
        buy.append(data['Adj Close'].iloc[x])
        sell.append(float('nan'))
        trigger=1
    elif data[f'SMA_{ma_1}'].iloc[x]<data[f'SMA_{ma_2}'].iloc[x] and trigger!=-1:
        buy.append(float('nan'))
        sell.append(data['Adj Close'].iloc[x])
        trigger=-1
    else:
        buy.append(float('nan'))
        sell.append(float('nan'))
    
data['Buy']=buy
data['Sell']=sell
print(data)
plt.plot(data['Adj Close'],label="Share Price",alpha=0.5)
plt.plot(data[f'SMA_{ma_1}'],label=f"SMA_{ma_1}",color="orange",linestyle="--")
plt.plot(data[f"SMA_{ma_2}"],label=f"SMA_{ma_2}",color="pink",linestyle="--")
plt.scatter(data.index,data['Buy'],label="Buy signal",marker='^',color="#00ff00",lw=3)
plt.scatter(data.index,data['Sell'],label="Sell signal",marker='v',color="#ff0000",lw=3)
plt.legend(loc="upper left")
plt.show()