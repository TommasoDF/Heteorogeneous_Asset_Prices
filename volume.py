import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import yfinance as yf
import numpy as np


df = pd.read_csv("Bitcoin_from_2021-12-22_23-59-49_to_2021-10-04_18-01-43.csv")
df = df.set_index('Datetime')
df.index = pd.to_datetime(df.index)

daily_counts = df.groupby(df.index.date).count().Text


start = daily_counts.index[0]
end = daily_counts.index[-1]

# Getting data
data = yf.download('BTC-USD', start=start, end=end)

Volume = pd.DataFrame(data.Volume)
daily_counts = np.log(daily_counts[0:-1])
daily_counts = pd.DataFrame(daily_counts)
daily_counts['Volume'] = np.log(Volume)

### Plotting

t = daily_counts.index
data1 = daily_counts.Volume
data2 = daily_counts.Text

fig, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_xlabel('Date')
ax1.xaxis.set_minor_locator(matplotlib.dates.MonthLocator([10,11,12]))
ax1.xaxis.set_minor_formatter(matplotlib.dates.DateFormatter('%b'))
ax1.xaxis.set_major_locator(matplotlib.dates.YearLocator())
ax1.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%Y'))
ax1.set_ylabel('Volume (log scale)', color=color)
ax1.plot(t, data1, color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:blue'
ax2.set_ylabel('# of tweets (log scale)', color=color )  # we already handled the x-label with ax1
ax2.plot(t, data2, color=color, alpha = 0.7, linestyle = 'dashed')
ax2.tick_params(axis='y', labelcolor=color)
plt.title('BTC volume and number of tweets per day containing the word "Bitcoin"')

fig.tight_layout()

fig.savefig('graph.png')

