import csv
import re
import sys
from datetime import date
from decimal import Decimal
from pyquery import PyQuery as pq
import pprint

GOOGLE_FINANCE_REPORT_TYPES = {
	"inc": "Income Statement",
	"bal": "Balance Sheet",
	"cas": "Cash Flow"
}
DATE = re.compile(".*(\d{4})-(\d{2})-(\d{2}).*")

class GoogleFinance(object):
	"""
	Get financial data from Google Finance.
	aapl = GoogleFinance("NASDAQ", "AAPL")
	print aapl.cash_flow()
	"""
	GOOGLE_FINANCE_URL = "https://www.google.com/finance?q={}:{}&fstype=ii"

	def __init__(self, market, symbol):
		self.market = market.upper()
		self.symbol = symbol.upper()
		self._financial = None

	@staticmethod
	def _parse_number(s):
		"""
		Return decimal object if the given string is parseable as number.
		Return None if the string is '-'.
		Otherwise return the string as is.
		"""
		if s == '-':
			return None
		try:
			return Decimal(s.replace(",", ""))
		except Exception, _:
			pass
		return s

	@staticmethod
	def _parse_data(s):
		"""
		Return datetime object if the given string contains YYYY-MM-DD string.
		Otherwise return the string as is.
		"""
		m = DATE.match(s)
		if m:
			return date(*[int(e) for e in m.groups()])
		return s

	@staticmethod
	def to_csv(csv_file_name, report):
		with open(csv_file_name, "wt") as fp:
			writer = csv.writer(fp, delimiter=",", quotechar='"', quoting = csv.QUOTE_NONNUMERIC)
			for row in report:
				writer.writerow(row)

	def _get_from_google(self):
		url = self.GOOGLE_FINANCE_URL.format(self.market, self.symbol)
		print "Get data from ", url
		return pq(url)

	def _get_table(self, report_type, term):
		"""
		Get the sheet table from html.
		"""
		#  Check if the request format is correct.
		assert term in ("interim", "annual")
		assert report_type in ("inc", "bal", "cas")

		if not self._financial:
			#  Create query at the first time.
			self._financial = self._get_from_google()

		div_id = report_type + term + "div"

		return self._financial("div#{} table#fs-table".format(div_id))

	def _statement(self, stmt_type, term):
		tbl = self._get_table(stmt_type, term)
		ret = []
		for row in tbl.items("tr"):
			data = [self._parse_number(i.text()) for i in row.items("th, td")]
			if not ret:
				#  The first row is date.
				data = [self._parse_data(e) for e in data]
			ret.append(data)
		#  Flip data matrix.
		#pprint.pprint(ret)
		return zip(*ret)

	def income_statement(self, term="annual"):
		return self._statement("inc", term)
	def balance_sheet(self, term="annual"):
		return self._statement("bal", term)
	def cash_flow(self, term="annual"):
		return self._statement("cas", term)

def main():
	google_finance = GoogleFinance("NASDAQ", "AAPL")
	#  Fail with Japanese corporation.
	#google_finance = GoogleFinance("TYO", "7203")

	report = google_finance.balance_sheet("annual")
	#print report
	google_finance.to_csv("AAPL.csv", report)

if __name__ == '__main__':
	main()
