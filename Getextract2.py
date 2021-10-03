#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 15 14:32:45 2018

@author: mhurtgen
"""

import PyPDF2
import re
import numpy as np

def reader(filename):
    read_pdf = PyPDF2.PdfFileReader(filename)
    return read_pdf

def getyear(filename):
    p=re.compile('-2[0-1][1-9][0-9]-')
    d=p.findall(filename)
    year=d[0][1:5]
    return year

def getNumberOfPages(filename):
    read_pdf=reader(filename)
    npages=read_pdf.getNumPages()
    return npages

def getpagecontent(page,filename):
    read_pdf=reader(filename)
    if (read_pdf.isEncrypted):
        read_pdf.decrypt('')
    page = read_pdf.getPage(page)
    
    page_content = page.extractText()
    return page_content


            
def findPos(j,Transactions,posTransaction,content):

    i=0
    lg=0
    
    while (i<lg):
        word=content[i]
        if (Transactions[j].strip()==word):
            #print(word)
            posTransaction.append(i)
            j=j+1
            break
        i=i+1
    return posTransaction

def GetAmountsDescription(i,j,content,p1,p1red,p2,amounts,year):
    #amounts=list()
    s=str()
    for l in range(i+1,j):
            word=content[l]
            if (p1.match(word)):
                
                if (p2.match(word)):
                    
                    #if (indexMinus>0):
                    DateString=p1.findall(word)                    
                    
                    DateString2=p1red.findall(DateString[0])
                    posred=DateString[0].strip('.').rfind(DateString2[0])
                    lgred=len(DateString[0])
                    fulldate=DateString2[0]+'-'+year                    
                    amounts.append([fulldate,word[posred+5:lgred].strip('.'),s])
                    s=str()
            else:
                s=s+' '+word.strip('.')#content[l]
            
    #print(s)
    
    return amounts


def patterns():
    num_transaction=re.compile('0[1-4][0-9][0-9] ')
    date_transaction=re.compile('.*[0-9][0-9]-[0-9][0-9].*')
    date_transaction_red=re.compile('[0-9][0-9]-[0-9][0-9]')
    amount=re.compile('.*[0-9]?.[0-9]*,[0-9][0-9]+|-')
    return num_transaction, date_transaction, date_transaction_red, amount

def patterns2():
    num_transaction=re.compile('^0[0-4][0-9][0-9]',re.M)
    date_transaction=re.compile('.*[0-9][0-9]-[0-9][0-9].*')
    date_transaction_red=re.compile('[0-9][0-9]-[0-9][0-9]')
    amount=re.compile('.*[0-9]?.[0-9]*,[0-9][0-9](+|-)+')
    return num_transaction, date_transaction, date_transaction_red, amount

def correct(Transactions):
    lg=len(Transactions)
    corrTransactions=list()
    
    corrTransactions.append(Transactions[0])
    
    lastk=int(Transactions[0])
    
    for i in range(1,lg-1):
        k=int(Transactions[i]) 
        
        
        if (k==lastk-1):
                corrTransactions.append(Transactions[i])
                lastk=k
    return corrTransactions

def correct2(Transactions):
    lg=len(Transactions)
    a=np.zeros(shape=(lg,lg))
    
    s2=[]
    seq=0
    for i in range(0,lg):
        for j in range(0,lg):
            a[i][j]=int(Transactions[i])-int(Transactions[j])
            if (i!=j):
                if abs(a[i][j])<lg:
                    seq=seq+1
        if seq>0:
                    s2.append(Transactions[i])
                    seq=0
    return s2

def getTransactions(filename):
    num_transaction, date_transaction, date_transaction_red, amount=patterns()
    page=0
    page_content=getpagecontent(page,filename)
    #print(content)
    content=page_content.split(' ')
    lg=len(content)
    for i in range(0,lg-2):
        s=content[i]
        snum=content[i+2]
        #print('ok')
        #print(s)
        if (date_transaction.match(s) and snum!='' and snum.isdigit()):
           # print(content[i+1])
            return snum
    #s3=correct3(s2)
    #return s2
def getNTransactions(page,filename):
    page_content=getpagecontent(page,filename)
    #print(content)
    content=page_content.split(' ')
    #print(content)
    lg=len(content)
    n=0
    num_transaction, date_transaction, date_transaction_red, amount=patterns()
    for i in range(0,lg):
        s=content[i]
        #snum=content[i+2]
        spre=content[i-2]
        #print('ok')
        #print(s)
        lg2=len(s)
        if (amount.match(s)
        and (date_transaction.match(s))
        
        #',' in s 
        and (('+' in s) or ('-' in s)) 
        and ('*' not in s)
        and (':' not in s)
        and ('EUR' not in s)
        and spre !='précédent' 
        and spre !='actuel'
        and spre!='incluse)'): 
        #(s.endswith('+') or s.endswith('-') or s.endswith('.')):
            #print(s)
            
            #print(content[i-2])
            #print(s)
           # print('ok')
            n=n+1
    print (n)   
    return n

def getTransactionsTotal(filename):
    lg=getNumberOfPages(filename)
    T=getTransactions(filename)
    
    startnum=T
    firstTransactionNum=startnum
    
    TransactionsTotal=list()
    
    for i in range(0,lg-1):
        N=getNTransactions(i,filename)
        Transaction=list()
        currTransaction=firstTransactionNum
        for j in range(0,N):
            j=int(currTransaction)
            Transaction.append(str(j).zfill(4))
            k=j-1
            currTransaction=str(k).zfill(4)
        firstTransactionNum=currTransaction    
        
        TransactionsTotal.append(Transaction)
        
    return TransactionsTotal

def getTransactionsPos(Transactions,content):
    j=0
    i=0
    lg=len(content)
    posTransaction=list()
    lgT=len(Transactions)
   
    """find list of posTransactions"""
    while(j<lgT):      
        
        """find index of Transaction num corresponding to j index"""
      
        while (i<lg):
            word=content[i]
            if (Transactions[j].strip()==word):
                #print(word)
                posTransaction.append(i)
                j=j+1
                break
            i=i+1
        
        j=j+1

    return posTransaction

def getAmounts(content,p1,p1red,p2, posTransaction,lgT,year):
    amounts=list()
    lgPT=len(posTransaction) 
    k=0   
    
    
    LastNum = posTransaction[lgPT-1]
    
    while (k<lgPT-1):
        i=posTransaction[k]
        j=posTransaction[k+1]
        
        """get amounts"""
       
        amounts=GetAmountsDescription(i,j,content,p1,p1red,p2,amounts,year)
        
        
        
        k=k+1
    
    

    
    lastdesc=LastNum+1
    delta=0
    lg=len(content)-delta
    s=str()
    lgA=len(amounts)
    while (lastdesc<lg):
        word=content[lastdesc]
    
   
        if (p1.match(word)):
            
            
            if (p2.match(word)):
                DateString=p1.findall(word)
               
                DateString2=p1red.findall(DateString[0])
                newdate=DateString2[0]+'-'+year
                posred=DateString[0].strip('.').rfind(DateString2[0])
                lgred=len(DateString[0])
                if (lgA<lgT):
                    amounts.append([newdate,word[posred+5:lgred].strip('.'),s])
                lgA=len(amounts)
                s=str()
                
        else:
            s=s+' '+word.strip('.')        #print(word[15:lgw])
        lastdesc=lastdesc+1
    
    return amounts

def getAmountsPage(pagenumber,filename):
    page_content=getpagecontent(pagenumber,filename)
   
    year=getyear(filename)
    
    num_transaction, date_transaction, date_transaction_red, amount=patterns()
    
    content=page_content.split(' ')
    
    TransactionsTotal=getTransactionsTotal(filename)   
    print(pagenumber)
    Transactions=TransactionsTotal[pagenumber]
    print(Transactions)
    
    lgT=len(Transactions)
    if (lgT>0):
        #Transactions=correct(Transactions)
    
        posTransaction=getTransactionsPos(Transactions,content)
    
    
        amounts=list()

        lgT=len(Transactions)    
        amounts=getAmounts(content,date_transaction,date_transaction_red,amount, posTransaction, lgT, year)
        
        return amounts
    else:
            return

def getAmountsPage2(pagenumber,filename):
    page_content=getpagecontent(pagenumber,filename)
   
    year=getyear(filename)
    
    num_transaction, date_transaction, date_transaction_red, amount=patterns()
    
    content=page_content.split(' ')
    
       
    #Transactions=re.findall(num_transaction,page_content)
    
    
    
    lgT=len(Transactions)
    if (lgT>0):
        Transactions=correct2(Transactions)
    
        posTransaction=getTransactionsPos(Transactions,content)
    
    
        amounts=list()

        lgT=len(Transactions)    
       
        amounts=getAmounts(content,date_transaction,date_transaction_red,amount, posTransaction, lgT, year)
    #print(amounts)
        return amounts
    else:
            return
        
def getAmountsAllPages(filename):
    
    n=getNumberOfPages(filename)
    TotalAmounts=list()
    
    for page in range(0,n-1):
        
        amounts=getAmountsPage(page,filename)
        TotalAmounts.append(amounts)
    
    return TotalAmounts

def getAmountsAllPages2(filename):
    
    n=getNumberOfPages(filename)
    TotalAmounts=list()
    
    for page in range(0,n-2):
        
        amounts=getAmountsPage2(page,filename)
        TotalAmounts.append(amounts)
    
    return TotalAmounts

def getAmountsAllPagesTest(filename):
    
    n=getNumberOfPages(filename)
    TotalAmounts=list()
    page=3
    
    
    amounts=getAmountsPage(page,filename)
    TotalAmounts.append(amounts)
    
    return TotalAmounts    
    
#