# lesson 9 onwards

import pandas as pd
import os
import time
import datetime as dt

import matplotlib
import matplotlib.pyplot as plt
matplotlib.style.use('dark_background')

import re

path = 'intraQuarter'

def key_stats(gather='Total Debt/Equity (mrq)'):
	statspath = path + '/_KeyStats'
	stock_list = [x[0] for x in os.walk(statspath)]
	# print stock_list
	df = pd.DataFrame(columns = ['Date',
								 'Unix',
								 'Ticker',
								 'DE Ratio',
								 'Price',
								 'stock_p_change',
								 'SP500',
								 'sp500_p_change',
								 'Difference',
								 'Status'])

	sp500_df = pd.DataFrame.from_csv('YAHOO-INDEX_GSPC.csv')

	ticket_list = []

	for each_dir in stock_list[1:25]:
		each_file = os.listdir(each_dir)

		ticker = each_dir.split(os.sep)[-1]
		ticket_list.append(ticker)

		starting_stock_value = False
		starting_sp500_value = False

		if len(each_file) > 0:
			for filename in each_file:
				date_stamp = dt.datetime.strptime(filename, '%Y%m%d%H%M%S.html')
				unix_time = time.mktime(date_stamp.timetuple())
				full_file_path = os.path.join(each_dir, filename)
				source = open(full_file_path, 'r').read()

				try:
					try:
						value = float(source.split(gather + ':</td><td class="yfnc_tabledata1">')[1].split('</td>')[0])
					except Exception as e:
						value = float(source.split(gather + ':</td>\n<td class="yfnc_tabledata1">')[1].split('</td>')[0])
						# print str(e), ticker, filename


					try:
						sp500_date = dt.datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d')
						row = sp500_df[(sp500_df.index == sp500_date)]
						sp500_value = float(row['Adj Close'])
					except:
						three_days_in_sec = 24*3600*3
						sp500_date = dt.datetime.fromtimestamp(unix_time-three_days_in_sec).strftime('%Y-%m-%d')
						row = sp500_df[(sp500_df.index == sp500_date)]
						sp500_value = float(row['Adj Close'])

					try:
						stock_price = float(source.split('</small><big><b>')[1].split('</b></big>')[0])
					except Exception as e:
						try:
							stock_price = (source.split('</small><big><b>')[1].split('</b></big>')[0])
							stock_price = re.search(r'(\d{1,8}\.\d{1,8})', stock_price)
							stock_price = float(stock_price.group(1))
							print stock_price
							# time.sleep(3)
							# print str(e), ticker, filename
						except Exception as e:
							stock_price = (source.split('<span class="time_rtq_ticker">')[1].split('</span>')[0])

							stock_price = re.search(r'(\d{1,8}\.\d{1,8})', stock_price)
							stock_price = float(stock_price.group(1))
							print 'Latest: ', stock_price

							print 'stock_price: ', str(e), filename
							# time.sleep(3)
					# print 'stock_price: ', stock_price, 'ticker: ', ticker

					if not starting_stock_value:
						starting_stock_value = stock_price
					if not starting_sp500_value:
						starting_sp500_value = sp500_value

					stock_p_change = ((stock_price - starting_stock_value) / starting_stock_value) * 100
					sp500_p_change = ((sp500_value - starting_sp500_value) / starting_sp500_value) * 100

					difference = stock_p_change - sp500_p_change

					if difference > 0:
						status = 'outperform'
					else:
						status = 'underperform'


					df = df.append({'Date': date_stamp,
									'Unix': unix_time,
									'Ticker': ticker,
									'DE Ratio': value,
									'Price': stock_price,
									'stock_p_change': stock_p_change,
									'SP500': sp500_value,
									'sp500_p_change': sp500_p_change,
									'Difference': difference,
									'Status': status},
									ignore_index=True)

				except Exception as e:
					pass

		# time.sleep(1)

	for each_ticker in ticket_list:
		try:
			plot_df = df[(df['Ticker'] == each_ticker)]
			plot_df = plot_df.set_index(['Date'])

			plot_df['Difference'].plot(label=each_ticker)
			plt.legend()
		except:
			pass

	plt.show()

	savefile = gather.replace(' ','').replace(')','').replace('(','').replace('/','') + '.csv'
	print savefile
	df.to_csv(savefile)


key_stats()