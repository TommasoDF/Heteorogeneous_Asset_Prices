import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
import yfinance as yf
import numpy as np
from scipy import stats


df = pd.read_csv("results\Bitcoin_from_2021-12-22_23-59-49_to_2021-10-04_18-01-43.csv")
df1 = pd.read_csv("results\Bitcoin_from_2022-03-24_23-59-56_to_2021-12-23_16-50-03.csv")
df2 = pd.read_csv("results\Bitcoin_from_2022-06-16_23-59-52_to_2022-03-25_22-17-47.csv")
df3 = pd.read_csv("results\Bitcoin_from_2022-09-12_23-59-56_to_2022-06-17_01-16-06.csv")
df4 = pd.read_csv("results\Bitcoin_from_2022-11-22_23-59-51_to_2022-09-13_22-10-38.csv")
final_df = pd.concat([df,df1,df2,df3,df4]).drop_duplicates().reset_index(drop=True)
final_df = final_df.set_index('Datetime')
final_df.index = pd.to_datetime(final_df.index)

daily_counts = final_df.groupby(final_df.index.date).count().Text
daily_counts.to_csv('Daily_count_from_'+ start_day + '_to_'+ end_day + '.csv', index = True, index_label = 'index')

start = daily_counts.index[0]
end = daily_counts.index[-1]
start_day = start.strftime('%Y-%m-%d_%H-%M-%S')
end_day = end.strftime('%Y-%m-%d_%H-%M-%S')

# Getting data
data = yf.download('BTC-USD', start=start, end=end)

daily_counts = pd.read_csv('Daily_count_from_'+ start_day + '_to_'+ end_day + '.csv',index_col = 'index')
Volume = pd.DataFrame(data.Volume)
daily_counts = daily_counts[0:-1]
daily_counts['Volume'] = Volume
daily_counts = np.log(daily_counts)

#Removing outliers for plotting
daily_counts = daily_counts[(daily_counts > 7).all(axis=1)]

### Plotting

t = pd.to_datetime(daily_counts.index)
data1 = daily_counts.Volume
data2 = daily_counts.Text

fig, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_xlabel('Date')
ax1.xaxis.set_minor_locator(matplotlib.dates.MonthLocator([1,4,7,10]))
ax1.xaxis.set_minor_formatter(matplotlib.dates.DateFormatter('%Y-%m'))
ax1.xaxis.set_major_locator(matplotlib.dates.YearLocator())
ax1.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%Y-%m'))
ax1.set_ylabel('Volume (log scale)', color=color)
ax1.plot(t, data1, color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:blue'
ax2.set_ylabel('# of tweets (log scale)', color=color )  # we already handled the x-label with ax1
ax2.plot(t, data2, color=color, alpha = 0.7, linestyle = 'dashed')
ax2.tick_params(axis='y', labelcolor=color)


fig.tight_layout()
plt.show()
fig.savefig('graph.png')

daily_counts.corr()

