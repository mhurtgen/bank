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
import matplotlib.pyplot as plt
import seaborn as sns
def getamount():
    conn = sqlite3.connect('Transactions2')   
    
   # cur=conn.cursor()
    query='''SELECT substr(date_transaction,0,8), SUM(amount)
FROM transactions
WHERE category_id=2 OR category_id=4 OR category_id=6 OR category_id=7 OR category_id=8
GROUP BY substr(date_transaction,0,8)'''
    
    cursor = conn.execute(query)
    
    columnsSQL = [column[0] for column in cursor.description]
    f=cursor.fetchall()
    k=np.asarray(f)


    sql_data=pd.DataFrame(k,columns=columnsSQL)

    conn.commit()
    conn.close()
    return sql_data

def getdetail(i):
    conn = sqlite3.connect('Transactions2')   
    
   # cur=conn.cursor()
    query='''SELECT substr(date_transaction,0,8) AS month, SUM(amount) AS amount
FROM transactions
WHERE category_id=?
GROUP BY substr(date_transaction,0,8)'''
    
    cursor = conn.execute(query,[i])
    
    columnsSQL = [column[0] for column in cursor.description]
    f=cursor.fetchall()
    k=np.asarray(f)



    sql_data=pd.DataFrame(k,columns=columnsSQL)
    
    conn.commit()
    conn.close()
    return sql_data

def getdetail_category(database):
    conn = sqlite3.connect(database)   
    
   # cur=conn.cursor()
    query='''SELECT substr(date_transaction,0,8) AS month, category_id, SUM(amount) AS amount
FROM transactions
GROUP BY substr(date_transaction,0,8),category_id'''
    
    cursor = conn.execute(query)
    
    columnsSQL = [column[0] for column in cursor.description]
    f=cursor.fetchall()
    k=np.asarray(f)



    sql_data=pd.DataFrame(k,columns=columnsSQL)
    
    conn.commit()
    conn.close()
    return sql_data

def getgraph(i):
    a=str(i)
    account=getdetail(a)
    #account.pivot_table(index='month',)
    month=account.iloc[:,0]
    amount=-pd.to_numeric(account.iloc[:,1])
    
    fig = plt.figure(figsize=(10,10))

    sns.barplot(data=account, x=month, y=amount, dodge = False)

def getpivot():
    
    conn=sqlite3.connect('Transactionstot')
    sql_data1=getdetail_category('Transactions2')
    sql_data2=getdetail_category('Transactions_mno')
    sql_data=pd.concat([sql_data1,sql_data2])
    
   # sql_data.to_sql(name='sql_data',con=conn)
    
    query='''SELECT month,category_id,CAST(SUM(amount) AS NUMERIC) AS amount
FROM sql_data
GROUP BY month,category_id
ORDER BY month, CAST(category_id AS INTEGER)'''
    cursor = conn.execute(query)
    columnsSQL = [column[0] for column in cursor.description]
    f=cursor.fetchall()
    k=np.asarray(f)



    sqltot=pd.DataFrame(k,columns=columnsSQL)
    print (sqltot)
    sqltot.to_csv('tot.csv')
    #sqltot.amount.to_numeric
    df=pd.pivot_table(sqltot,values='amount',index=['month'],columns=['category_id'])
    
    df.to_csv('ptable.csv')
    
    conn.commit()
    conn.close()
    return sql_data
    
#    sqltot=sqlt.groupby(['month','category_id'])['amount'].sum()
#    sqltot.to_csv('fulldata2.csv')
#    #pd.to_numeric(sqltot.iloc[:,2])
#    df=pd.pivot_table(sqltot,values='amount',index=['month'],columns=['category_id'])
#    df.to_csv('ptable.csv')
#    print(df)
##   
#    
#    
#    month=sql_data.iloc[:,0]
#    categoryid=sql_data.iloc[:,1]
#    amount=pd.to_numeric(sql_data.iloc[:,2])
#    d={'month':month,'category_id':categoryid,'amount':amount}
#    sqlt=pd.DataFrame(data=d)
#    
#    
    #sql_data.to_csv('fulldata.csv')
    
    # sqltot.set_index('month','category_id').unstack('month')
#    ptable=pd.pivot(sqltot,index='category_id',columns='month',values='amount')
##    ptable.to_csv('pivottable.csv')
#    #return ptable
##getgraph(9)
getpivot()
#f=connsql()


     