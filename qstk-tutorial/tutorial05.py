import QSTK.qstksim as qstksim
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
import datetime as dt
import pandas as pd
import numpy as np
import tradesim_mod

#  We use sample allocation values from pre-generated file.
#  If you have not executed tutorial 04, do it now.

import cPickle
df_alloc = cPickle.load(open("allocations04.pkl", "rb"))

#  Create historical data from Yahoo! finance.
dt_start = dt.datetime(2004, 1, 1)
dt_end = dt.datetime(2009, 12, 31)
dt_timeofday = dt.timedelta(hours=16)

ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)
c_dataobj = da.DataAccess("Yahoo")

ls_symbols = c_dataobj.get_symbols_from_list("sp5002012")
ls_symbols = ls_symbols[:20]

ls_keys = ["close"]

ldf_data = c_dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
d_data = dict(zip(ls_keys, ldf_data))
na_price = d_data["close"].values

df_close = pd.DataFrame(na_price[:1], index=[ldt_timestamps[0]], columns=ls_symbols)

dt_last_date = ldt_timestamps[0]
#  Looping throught all dates and creating monthly allocations.
for i, dt_date in enumerate(ldt_timestamps[1:]):
	if dt_last_date.month != dt_date.month:
		df_new_row = pd.DataFrame(na_price[i:i+1], index=[dt_date], columns=ls_symbols)
		df_close = df_close.append(df_new_row)
	dt_last_date = dt_date

#  Apply a backtest using QSTK.qstksim module.
#(ts_funds, ts_leverage, f_commision, f_slippage, f_borrow_cost) = qstksim.tradesim(df_alloc,
(ts_funds, ts_leverage, f_commision, f_slippage, f_borrow_cost) = tradesim_mod.tradesim(df_alloc,
		df_close, f_start_cash=10000.0, i_leastcount=1, b_followleastcount=True,
		f_slippage=0.0005, f_minimumcommision=5.0, f_commision_share=0.0035,
		i_target_leverage=1, f_rate_borrow=3.5, log="transaction05.csv")

print (ts_funds, ts_leverage, f_commision, f_slippage, f_borrow_cost)
