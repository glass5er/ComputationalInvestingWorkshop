import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
import datetime as dt
import pandas as pd
import numpy as np

dt_start = dt.datetime(2004, 1, 1)
dt_end = dt.datetime(2009, 12, 31)
dt_timeofday = dt.timedelta(hours=16)

ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)
c_dataobj = da.DataAccess("Yahoo")

ls_symbols = c_dataobj.get_symbols_from_list("sp5002012")
ls_symbols = ls_symbols[:20]
ls_symbols.append("_CASH")

na_vals = np.random.randint(0, 1000, len(ls_symbols))
#  Normalize the row - Typecasting as everything is int.
na_vals = na_vals / float(sum(na_vals))
#  Reshape to a 2D matrix to append into dataframe.
na_vals = na_vals.reshape(1, -1)

#  Create a dataframe with pandas module.
df_alloc = pd.DataFrame(na_vals, index=[ldt_timestamps[0]], columns=ls_symbols)

dt_last_date = ldt_timestamps[0]

#  Looping throught all dates and creating monthly allocations.
for dt_date in ldt_timestamps[1:]:
	if dt_last_date.month != dt_date.month:
		#  Create allonation.
		na_vals = np.random.randint(0, 1000, len(ls_symbols))
		na_vals = na_vals / float(sum(na_vals))
		na_vals = na_vals.reshape(1, -1)
		#  Append to the dataframe.
		df_new_row = pd.DataFrame(na_vals, index=[dt_date], columns=ls_symbols)
		df_alloc = df_alloc.append(df_new_row)
	dt_last_date = dt_date

#  If you want to use the dataframe later, store it with pkl format.
import cPickle
output = open("allocations04.pkl", "wb")
cPickle.dump(df_alloc, output)
output.close()  #  Do not forget to close the file!

#  If you want to load the stored dataframe, do like this:
df_loaded = cPickle.load(open("allocations04.pkl", "rb"))

print "Two dataframes are equal ? ->", df_alloc.equals(df_loaded)
