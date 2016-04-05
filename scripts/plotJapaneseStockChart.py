# coding: utf-8

#  This is a char plotting script for Japanese stocks.
#  See:
#  http://sinhrks.hatenablog.com/entry/2015/02/04/002258

from __future__ import unicode_literals
import numpy as np
import pandas as pd
import pandas.io.data as web
import pandas.tools.plotting as plotting
import lxml.html

def get_quote_yahoojp(code, start=None, end=None, interval='d'):
	base = 'http://info.finance.yahoo.co.jp/history/?code={0}.T&{1}&{2}&tm={3}&p={4}'
	start, end = web._sanitize_dates(start, end)
	start = 'sy={0}&sm={1}&sd={2}'.format(start.year, start.month, start.day)
	end = 'ey={0}&em={1}&ed={2}'.format(end.year, end.month, end.day)
	p = 1
	results = []

	if interval not in ['d', 'w', 'm', 'v']:
		raise ValueError("Invalid interval: valid values are 'd', 'w', 'm' and 'v'")

	while True:
		url = base.format(code, start, end, interval, p)
		print url

		title = lxml.html.parse(url).find(".//title").text
		tables = pd.read_html(url, header=0)

		if len(tables) < 2 or len(tables[1]) == 0:
			break
		results.append(tables[1])
		p += 1
	result = pd.concat(results, ignore_index=True)

	result.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close']

	#  Use '年月日' to parse Japanese date.
	if interval == 'm':
		result['Date'] = pd.to_datetime(result['Date'], format='%Y年%m月')
	else:
		result['Date'] = pd.to_datetime(result['Date'], format='%Y年%m月%d日')

	result = result.set_index('Date')
	result = result.sort_index()
	return title, result


class OhlcPlot(plotting.LinePlot):
	ohlc_cols = pd.Index(['open', 'high', 'low', 'close'])
	reader_cols = pd.Index(['Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close'])

	def __init__(self, data, **kwargs):
		data = data.copy()
		self.freq = kwargs.pop('freq', 'B')

		if isinstance(data, pd.Series):
			data = data.resample(self.freq, how='ohlc')
		assert isinstance(data, pd.DataFrame)
		assert isinstance(data.index, pd.DatetimeIndex)
		if data.columns.equals(self.ohlc_cols):
			data.columns = [c.title() for c in data.columns]
		elif data.columns.equals(self.reader_cols):
			pass
		else:
			raise ValueError('data is not ohlc-like')
		data = data[['Open', 'Close', 'High', 'Low']]
		plotting.LinePlot.__init__(self, data, **kwargs)

	def _get_plot_function(self):
		#  From matplotlib 1.5, 'candlestick' is no longer available. Use 'candlestick_ohlc'.
		from matplotlib.finance import candlestick_ohlc
		def _plot(data, ax, **kwds):
			candles = candlestick_ohlc(ax, data.values, **kwds)
			return candles
		return _plot

	def _make_plot(self):
		from pandas.tseries.plotting import _decorate_axes, format_dateaxis
		plotf = self._get_plot_function()
		ax = self._get_ax(0)

		data = self.data
		data.index.name = 'Date'
		data = data.to_period(freq=self.freq)
		data = data.reset_index(level=0)

		if self._is_ts_plot():
			data['Date'] = data['Date'].apply(lambda x: x.ordinal)
			_decorate_axes(ax, self.freq, self.kwds)
			candles = plotf(data, ax, **self.kwds)
			format_dateaxis(ax, self.freq)
		else:
			from matplotlib.dates import date2num, AutoDateFormatter, AutoDateLocator
			data['Date'] = data['Date'].apply(lambda x: date2num(x.to_timestamp()))
			candles = plotf(data, ax, **self.kwds)

			locator = AutoDateLocator()
			ax.xaxis.set_major_locator(locator)
			ax.xaxis.set_major_formatter(AutoDateFormatter(locator))


plotting._all_kinds.append('ohlc')
plotting._common_kinds.append('ohlc')
plotting._plot_klass['ohlc'] = OhlcPlot


if __name__ == '__main__':
	import matplotlib
	import matplotlib.font_manager as font_manager
	#  Set Japanese font property for graph plot.
	fontPath = "/usr/share/fonts/truetype/takao-mincho/TakaoExMincho.ttf"
	import os
	if os.path.exists(fontPath):
		prop = font_manager.FontProperties(fname=fontPath)
		matplotlib.rc("font", family=prop.get_name())
	else:
		print "Warning: Font file %s not found." % fontPath

	import matplotlib.pyplot as plt
	start = '2014-10-01'

	import pickle

	stockID = 7203  #  Toyota

	fileTmp = "tmp%d.pkl" % stockID
	if not os.path.exists(fileTmp):
		print "Fetching data of stock %d..." % stockID
		title, result = get_quote_yahoojp(stockID, start=start)
		pickle.dump([title, result], open(fileTmp, "wb"))
	else:
		title, result = pickle.load(open(fileTmp, "rb"))

	#print result[-30:]

	#  Plot candle stick using Open, High, Low, and Close.
	#  Plot only business day.
	result = result.asfreq('B')

	result.plot(kind='ohlc')
	plt.title(title)
	plt.show()
