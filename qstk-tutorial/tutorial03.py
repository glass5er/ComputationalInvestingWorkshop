import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

na_portfolio = np.loadtxt('./portfolio03.csv', dtype='S5,f4', delimiter=',', comments="#", skiprows=1)

#  Raw portofolio
print na_portfolio

#  Sorted portofolio
na_portfolio = sorted(na_portfolio, key=lambda x: x[0])
print na_portfolio

#  Copy portofolio data into two lists.
ls_port_syms = []
lf_port_alloc = []
for port in na_portfolio:
	ls_port_syms.append(port[0])
	lf_port_alloc.append(port[1])

#  Detect invalid symbols, which are not in the market.
c_dataobj = da.DataAccess('Yahoo')
ls_all_syms = c_dataobj.get_all_symbols()
ls_bad_syms = list(set(ls_port_syms) - set(ls_all_syms))

if len(ls_bad_syms) != 0:
	print "Portfolio contains bad symbols : ", ls_bad_syms

#  Remove data corresponding to invalid symbols.
for s_sym in ls_bad_syms:
	i_index = ls_port_syms.index(s_sym)
	ls_port_syms.pop(i_index)
	lf_port_alloc.pop(i_index)

#  Read data of valid portfolio.
dt_end = dt.datetime(2011, 1, 1)
dt_start = dt_end - dt.timedelta(days = 1095)  #  Three years
dt_timeofday = dt.timedelta(hours=16)

ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)

ls_keys = ["open", "high", "low", "close", "volume", "actual_close"]

ldf_data = c_dataobj.get_data(ldt_timestamps, ls_port_syms, ls_keys)
d_data = dict(zip(ls_keys, ldf_data))

#  Apply a quick and dirty back test.
df_rets = d_data["close"].copy()
df_rets = df_rets.fillna(method="ffill")
df_rets = df_rets.fillna(method="bfill")

na_rets = df_rets.values
tsu.returnize0(na_rets)

#  Calculate total return of the portfolio.
na_portrets = np.sum(na_rets * lf_port_alloc, axis=1)
na_port_total = np.cumprod(na_portrets + 1)

#  Calculate total return of each component.
na_component_total = np.cumprod(na_rets + 1, axis=0)

#  Plot returns.
plt.clf()
fig = plt.figure()
fig.add_subplot(111)
plt.plot(ldt_timestamps, na_component_total, alpha=0.4)
plt.plot(ldt_timestamps, na_port_total)
ls_names = ls_port_syms
ls_names.append("Portfolio")
plt.legend(ls_names)
plt.ylabel("Cumulative returns")
plt.xlabel("Date")
fig.autofmt_xdate(rotation=45)
plt.savefig("graph03.pdf", format="pdf")
