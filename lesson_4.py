# lesson 4 onwards

import pandas as pd
import os
import time
import datetime as dt

path = 'intraQuarter'

def key_stats(gather='Total Debt/Equity (mrq)'):
	statspath = path + '/_KeyStats'
	stock_list = [x[0] for x in os.walk(statspath)]
	# print stock_list

	for each_dir in stock_list[1:]:
		each_file = os.listdir(each_dir)
		# print each_file, each_dir
		# time.sleep(15)
		ticker = each_dir.split(os.sep)[-1]
		if len(each_file) > 0:
			for filename in each_file:
				date_stamp = dt.datetime.strptime(filename, '%Y%m%d%H%M%S.html')
				unix_time = time.mktime(date_stamp.timetuple())
				# print date_stamp, unix_time
				# time.sleep(15)
				full_file_path = os.path.join(each_dir, filename)
				print full_file_path
				source = open(full_file_path, 'r').read()
				# print source
				# time.sleep(15)

				value = source.split(gather + ':</td><td class="yfnc_tabledata1">')[1].split('</td>')[0]

				print ticker + ' (' + str(date_stamp) + '): ', value
				time.sleep(1)

key_stats()