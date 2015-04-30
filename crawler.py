#-*-coding: utf-8 -*-

import pandas.io.data as web
import datetime

start = datetime.datetime(2014, 1, 2)
end = datetime.datetime(2015, 3, 31)
gs = web.DataReader("078930.KS", "yahoo", start, end)

fileName = 'StockData.txt'

"""
f = open(fileName, 'w+')
f.write(gs)
"""

gs.to_csv(fileName, sep='\t', encoding='utf-8')