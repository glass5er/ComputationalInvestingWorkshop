# coding: utf-8
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.finance import candlestick_ohlc

pairList = [ "USDJPY", "EURJPY", "EURUSD", "AUDJPY", "AUDUSD", "NZDJPY", "NZDUSD", "CADJPY", "GBPJPY", "TRYJPY", "ZARJPY" ]
pairDict = dict(zip(pairList, list(range(len(pairList))) ))

def downloadCurrencyData(fileOut, tick="d"):
	assert(tick in ["d", "w", "m"])

	import pycurl
	from StringIO import StringIO

	buff = StringIO()
	c = pycurl.Curl()
	c.setopt(c.URL, "http://www.m2j.co.jp/market/histryall_dl.php?type=%s" % tick)
	c.setopt(c.WRITEDATA, buff)
	c.perform()
	c.close()

	fp = open(fileOut, "wt")
	fp.write(buff.getvalue())
	fp.close()

#def toUtf8(fileIn, fileOut):
#	import nkf
#	strIn  = open(fileIn, "rt").read()
#	strOut = nkf.nkf("u", strIn)
#
#	fp = open(fileOut, "wt")
#	fp.write(strOut)
#	fp.close()

if __name__ == '__main__':
	#  Choose target currency exchange in 'pairList' above.
	target = "TRYJPY"
	#  Choose tick in (day, week, month).
	tick = "m"

	fileTmpSjis = "m2j_urrency_%s_sjis.csv" % tick
	fileTmpUtf8 = "m2j_urrency_%s_utf8.csv" % tick

	if not os.path.exists(fileTmpSjis):
		print "Downloading currency data..."
		downloadCurrencyData(fileTmpSjis, tick=tick)

	#if not os.path.exists(fileTmpUtf8):
	#	print "Converting character code..."
	#	toUtf8(fileTmpSjis, fileTmpUtf8)

	colIdx = 6 * pairDict[target]
	df = pd.read_csv(fileTmpSjis, skiprows=1, usecols=[0] + list(range(colIdx+1, colIdx+5)), parse_dates=[0])
	#  Rename colmuns to English.
	df.columns = ["Date", "Open", "High", "Low", "Close"]
	#  @TODO:  Define datetime range. Use last 1000 values for now.
	df = df[-100:]

	dates = df["Date"]
	df["Date"] = dates.values.astype("datetime64[D]").astype(float)

	step = df.shape[0] / 10
	plt.xticks(df["Date"][::step], [x.strftime("%Y/%m/%d") for x in dates[::step]], rotation=20)

	ax = plt.subplot()
	candlestick_ohlc(ax, df.values)
	plt.title(target)
	plt.ylabel(target)
	plt.grid()
	plt.show()

