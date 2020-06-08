#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  7 15:47:08 2019

@author: mhurtgen
"""

#from Getextract2 import textread

#from Getextract import *
from Getextract2 import getAmountsAllPages
import os
import sqlprepare as sp
import transactionsqlite2 as sqlize
#import pandas as pd
import sqlite3

#directory = '/home/mhurtgen/Documents/BNPCC/extraits_toread/'
directory = '/home/mhurtgen/Documents/BNPCC/extraitsrecent/'
#amounts=getAmountsPage(pagenumber,filename)
TotalAmountsAll=list()

for r,d,f in os.walk(directory):
    for file in f:
        if ('-EX-' in file):
            filename=directory+file
            print(filename)
            TotalAmounts=getAmountsAllPages(filename)
            Ta=sp.prepareForSql(TotalAmounts)
            TotalAmountsAll.append(Ta)
            #TotalAmountsAll.append(TotalAmounts)
            #print(filename)
conn = sqlite3.connect('Transactions2')     
##Ta=sp.prepareForSql(TotalAmounts)
##sqlize.insertinfo(Ta)
sqlize.reset(conn)

for el in TotalAmountsAll:
    sqlize.insertinfo(el,conn)
    
conn.close()
#sqlize.insertinfo(TotalAmountsAll)
#for el in TotalAmountsAll:
#    print(el)
#    SQLel=sp.prepareForSql(el)
#    sqlize.insertinfo(SQLel)
#for el in list_transactions:
#    print(el)
#pdfName = 'BE07001268844266-EX-2018-5.pdf'



