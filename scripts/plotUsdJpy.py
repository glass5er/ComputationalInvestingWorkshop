import pandas.io.data as web
import datetime
import matplotlib.pyplot as plt

def setJapaneseFont():
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

if __name__ == "__main__":
	setJapaneseFont()

	dateStart = datetime.datetime(2016, 1, 1)
	dateEnd   = None  #  Latest
	#dateEnd   = datetime.datetime(2016, 3, 31)

	print "Fetching data..."
	df = web.DataReader("DEXJPUS", "fred", dateStart, dateEnd)

	df.plot(kind="line")
	plt.title("USD/JPY")
	plt.show()
