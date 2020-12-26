#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 10:44:35 2019

@author: mhurtgen
"""

def datetransform(datestr):
    t1=datestr.find('-')
    t2=datestr.rfind('-')
    year=datestr[t2+1:11]
    month=datestr[t1+1:t2]
    day=datestr[0:t1]
    output=year+'-'+month+'-'+day
    return output

def getAmount(amountstr):
    loss=amountstr.find('-')
    
    
    #gain=amountstr.find('+')
    #amount=amountstr.replace(',','.')
    amount1=amountstr.replace('.','')
    amount=amount1.replace(',','.')
    
    index_min=amount.find('-')
    index_plus=amount.find('+')
    while True:
        try:
            if loss==-1:
                return float(amount[0:index_plus])
            else:
                return -float(amount[0:index_min])
        except Exception:
            break

def descriptionCategory(description):
    #Logement
    if ('BE19 3400 4130' in description)|('crédit habitation' in description):
        output=1
    elif ('Electrabel' in description)|('MEGA'  in description)|('Eneco' in description):
        output=2
    elif ('CPAS' in description):
        output=3
    elif (('COMPTOIR DES MER' in description)|
            ('ORIGIN' in description)|
            ('BINET' in description)|
            ('PETITS PRODUCTEURS' in description)|
            ('EKIMAN' in description)|
            ('DELHAIZE' in description)|
            ('BIOPLANET' in description)|
            ('LIDL' in description)|
            ('ALDI' in description)|
            ('CORA' in description)|
            ('MAKRO' in description)
            ):
        output=4
    elif ('épargne' in description):
        output=5
    elif ('EAUX' in description):
        output=6    
    elif ('AUTO' in description):
        output=7    
    elif (('NIV-VET' in description)|
            ('TOM & CO' in description)):
        output=8    
    else:
        output=9
    return output

def prepareForSql(Transactions):
    lg=len(Transactions)
    i=1
    TransactionsTot=list()
    
    for a in Transactions:
        #print(a)
        
        if (a is not None):
            lg=len(a)
            for j in range(0,lg):
         #       print(a[j])
                id=i
                
                date_transaction=a[j][0]
                
                amount_transaction=a[j][1]
               
                description=a[j][2]
           
                date=datetransform(date_transaction)
                amount=getAmount(amount_transaction)
                category=descriptionCategory(description)
                
                TransactionsTot.append([date, amount, description, category])
                i=i+1
    return TransactionsTot
        
        
def prepareForSqlUnique(Transaction):
    #lg=len(Transactions)
    i=1
    #TransactionsTot=list()
    
    
    id=i
            
    date_transaction=Transaction[0]
            
    amount_transaction=Transaction[1]
        
    description=Transaction[2]
       
    date=datetransform(date_transaction)
    amount=getAmount(amount_transaction)
    category=descriptionCategory(description)
            
    vec=[date, amount, description, category]
    i=i+1
    return vec       
        
        
        
        
        
    