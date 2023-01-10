import yfinance as yf
import pandas as pd
import numpy as np
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima_process import ArmaProcess
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

# Getting data
start = '2022-01-01'
end = '2023-01-01'
data = yf.download('BTC-USD', start=start, end=end,interval = "1h")



#Plotting ACF
plot_acf(data.Close)
plt.show()

#AR(1)
# Estimating an AR(1) model
mod = ARIMA(np.log(data.Close), order=(1,0,0), trend = 'n')
res = mod.fit()
print(res.summary(), res.rsquared)



const = 9.5802
phi = 0.9989

y_actual = np.log(data.Close[2:])
y_pred = np.log(data.Close[1:-1])
y_pred2 = np.log(data.Close[0:-2])
r2_score(y_actual, y_pred), r2_score(y_actual, y_pred2)


### Plotting
t = data.index[1:]

plt.plot(t,y_actual)
plt.plot(t, y_pred[0:-1])
plt.show()


MSE_Naive = np.mean((np.array(data.Close[1:]) - np.array(data.Close[0:-1]))**2)
MSE_Mean_Rev = np.mean((np.array(data.Close[1:]) - 0.7*np.array(data.Close[0:-1]))**2)
MSE_Explosive = np.mean((np.array(data.Close[1:]) - 1.3*np.array(data.Close[0:-1]))**2)
MSE_trend_follower = np.mean((np.array(data.Close[2:]) - (2*np.array(data.Close[1:-1]) - np.array(data.Close[0:-2])))**2)
MSE_trend_follower_parsimonious = np.mean((np.array(data.Close[2:]) - (1.5*np.array(data.Close[1:-1]) - 0.5*np.array(data.Close[0:-2])))**2)
MSE_trend_contrarian = np.mean((np.array(data.Close[2:])  - np.array(data.Close[0:-2]))**2)
MSE_trend_contrarian_parsimonious = np.mean((np.array(data.Close[2:]) - (0.5*np.array(data.Close[1:-1]) + 0.5*np.array(data.Close[0:-2])))**2)

np.log([np.var((np.array(data.Close[1:]) - np.array(data.Close[0:-1]))) , np.var(np.array(data.Close[1:]))])

Naive_R_squared = 1 - np.sum((np.array(data.Close[1:]) - np.array(data.Close[0:-1]))**2)/np.sum((np.array(data.Close[1:]) - np.mean(np.array(data.Close[1:])))**2)
print(Naive_R_squared)
np.log([MSE, MSE_Mean_Rev, MSE_Explosive, MSE_trend_follower,MSE_trend_follower_parsimonious,MSE_trend_contrarian,MSE_trend_contrarian_parsimonious])




