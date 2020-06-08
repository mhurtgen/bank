#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 09:31:30 2020

@author: mhurtgen
"""
import sqlite3
import pandas as pd
from pandas import DataFrame
import numpy as np

def connsql():
    conn = sqlite3.connect('Transactions2')   
    
   # cur=conn.cursor()
    query='''SELECT substr(date_transaction,0,8),category_id, SUM(amount)
FROM transactions
WHERE category_id=4 OR category_id=6 OR category_id=7
GROUP BY substr(date_transaction,0,8),category_id'''
    
    cursor = conn.execute(query)
    
    columnsSQL = [column[0] for column in cursor.description]
    f=cursor.fetchall()
    k=np.asarray(f)


    sql_data=pd.DataFrame(k,columns=columnsSQL)
    return sql_data
    conn.commit()
    conn.close()
    return f

f=connsql()

df=DataFrame(qs)
     