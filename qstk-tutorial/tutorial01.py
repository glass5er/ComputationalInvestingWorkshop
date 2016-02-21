#  Setup required modules.
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def tutorial01():
	#  Define the company list to get the stock prices.
	ls_symbols = ["AAPL", "GLD", "GOOG", "$SPX", "XOM"]
	#  Define the date range of stock data.
	dt_start = dt.datetime(2006,  1,  1)
	dt_end   = dt.datetime(2010, 12, 31)
	#  Define the time of date as 4:00 PM, when it is the close of the day.
	dt_timeofday = dt.timedelta(hours=16)
	#  Create a timestamp list object for QSTK.
	ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)

	#  Define the data repository as Yahoo Finance.
	c_dataobj = da.DataAccess("Yahoo")
	#  Define data keys.
	ls_keys = ["open", "high", "low", "close", "volume", "actual_close"]
	#  Retrieve data.
	ldf_data = c_dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
	#  Create a dictionary (like std::map in C++).
	d_data = dict(zip(ls_keys, ldf_data))

	#  Choose a set of data to plot.
	na_price = d_data["close"].values
	#  Clear the figure canvas.
	plt.clf()
	#  Plot the data.
	plt.plot(ldt_timestamps, na_price)
	#  Arrange the apprearance of the figure.
	plt.legend(ls_symbols)
	plt.ylabel("Adjusted Close")
	plt.xlabel("Date")
	#  Save the figure in PDF format.
	plt.savefig("adjustedclose.pdf", format="pdf")

	#  Normalize the price data so that data.begin = 1.0.
	na_normalized_price = na_price / na_price[0, :]
	#  Draw another figure and save it.
	plt.clf()
	plt.plot(ldt_timestamps, na_normalized_price)
	plt.legend(ls_symbols)
	plt.ylabel("Normalized Close")
	plt.xlabel("Date")
	plt.savefig("normalizedclose.pdf", format="pdf")

	#  Calculate daily returns.
	na_rets = na_normalized_price.copy()
	tsu.returnize0(na_rets)
	#  Draw another figure and save it.
	plt.clf()
	plt.plot(ldt_timestamps, na_rets)
	plt.legend(ls_symbols)
	plt.ylabel("Daily Returns")
	plt.xlabel("Date")
	plt.savefig("dailyreturns.pdf", format="pdf")

	#  Check the correlation between '$SPX' and 'XOM' using scatter plots.
	plt.clf()
	plt.scatter(na_rets[:, 3], na_rets[:, 1], c='blue')
	plt.xlabel("$SPX")
	plt.ylabel("XOM")
	plt.savefig("correlationscatter.pdf", format="pdf")

	#  Calculate cumulative returns.
	daily_cum_ret = np.empty(na_rets.shape)
	daily_cum_ret[0, :] = 1.0
	for t in range(1, na_rets.shape[0]):
		daily_cum_ret[t] = daily_cum_ret[t - 1] * (1.0 + na_rets[t, :])
	plt.clf()
	plt.plot(ldt_timestamps, daily_cum_ret)
	plt.legend(ls_symbols)
	plt.ylabel("Cumulative Returns")
	plt.xlabel("Date")
	plt.savefig("cumulativereturns.pdf", format="pdf")

if __name__ == '__main__':
	tutorial01()
