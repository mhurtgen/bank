#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  2 05:52:12 2019

@author: mhurtgen
"""
#import sqlite3
def reset(conn):
    query='DELETE FROM transactions'
    cur=conn.cursor()
    cur.execute(query)
    conn.commit()
    
def insertinfo(transactions,conn):
    
    cur=conn.cursor()
    for transaction in transactions:
         cur.execute('INSERT INTO transactions values(?,?,?,?)',(transaction[0],transaction[1],transaction[2],transaction[3]))
    conn.commit()
     
#        id int,
#                                        date_transaction text,
#                                        description text,
#                                        category_id int