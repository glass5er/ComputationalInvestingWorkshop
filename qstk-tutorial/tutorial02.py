import numpy as np
import pandas as pd
import datetime as dt

na_data = np.loadtxt("./data02.csv", delimiter=",", skiprows=1)

na_price = na_data[:, 3:]
na_dates = np.int_(na_data[:, 0:3])
ls_symbols = ["$SPX", "XOM", "GOOG", "GLD"]

print "First 5 rows of Price Data:"
print na_price[:5, :]
print "First 5 rows of Dates:"
print na_dates[:5, :]

ldt_timestamps = []
for i in range(0, na_dates.shape[0]):
	ldt_timestamps.append(dt.date(na_dates[i, 0], na_dates[i, 1], na_dates[i, 2]))

import matplotlib.pyplot as plt
plt.clf()
plt.plot(ldt_timestamps, na_price)
plt.legend(ls_symbols)
plt.ylabel("Adjusted Close")
plt.xlabel("Date")
plt.savefig("adjusteclose.pdf", format="pdf")
