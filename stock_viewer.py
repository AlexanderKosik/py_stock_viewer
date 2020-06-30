import yfinance as yf
import seaborn as sns
from matplotlib import rcParams
import matplotlib.pyplot as plt
import pandas as pd

ticker = "ARL.F"
data = yf.download(ticker, period="3y", interval="1d")
# data = yf.download(ticker, period="6mo", interval="1d")

sns.set(style="darkgrid")
rcParams['figure.figsize'] = 13, 5
rcParams['figure.subplot.bottom'] = 0.2

closing = data.get("Close")
closing_avg_short = closing.rolling(window=10).mean()
closing_avg_long = closing.rolling(window=50).mean()
ax = sns.lineplot(hue="Events", dashes=False, markers=True, data=closing, label="Closing price")
ay = sns.lineplot(hue="Events", dashes=False, markers=True, data=closing_avg_short, label="Rolling avg 10")
az = sns.lineplot(hue="Events", dashes=False, markers=True, data=closing_avg_long, label="Rolling avg 100")
ax.set_title(f"Aktie: {ticker}")

plt.xticks(
    rotation=45,
    horizontalalignment='right',
    fontweight='light',
    fontsize='medium'
)
plt.show()
plt.get