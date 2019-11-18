#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This trading strategy each day calculates the 50-day and 200-day moving average
of the stock price. If the 50-day average is higher than the 200-day one, buy
50 units of stock. If the 50-day average is below the 200-day average, sell
50 units of stock. It calculates the number of stocks held and tracks wealth 
and profit.
We use the open price, so only adjust portfolio in the morning as the 
markets open.
"""

"""
To make more efficiient, retrieve length of data 2070,
What do we do for dates before 200?
Make a program to update moving averages 
        
#  You don't need to calculate the moving average completely for each day
#  average50+=(newDayStockPrice - (day50-1))/50

"""

import pandas_datareader as web
"""    
symbol = 'WIKI/AAPL'

df = web.DataReader(symbol, 'quandl', '2010-01-01', '2018-10-04', \
                    api_key='ppa2TFFUfPyLxGQmwDuT')
# Returns apple data from quandl
# Does not return recent data eg. only up to 2018
Increasing stock prices
"""
"""
# Returns disney stock prices: 590 terms
df = web.DataReader('EOD/DIS', 'quandl', '2015-08-01', '2017-12-01', \
                    api_key='ppa2TFFUfPyLxGQmwDuT')
Relatively constant stock price
"""
# Returns IBM stock prices (falling): 377 terms
df = web.DataReader('EOD/IBM', 'quandl', '2014-09-01', '2016-03-01', \
                    api_key='ppa2TFFUfPyLxGQmwDuT')

class Account():
    def __init__(self):
        self.funds = 0 
        self.noStocks = 0
    
    def buyStocks(self, num, price):
        self.noStocks += num #Gain stocks
        self.funds -= (price*num)
        #print("\n{} stocks bought for price {}.".format(num, price))
        
    def sellStocks(self, num, price):
        self.noStocks -= num #Sell stocks
        self.funds += (price*num)
        #print("\n{} stocks sold for price {}.".format(num, price))
        
    def statement(self):
        print("\nFunds: {}\nNumber of stocks: {}.\n"\
              .format(self.funds, self.noStocks))
   

# Defines trading strategy     
def adjustPortfolio(account_name, currentPrice, average50, average200):
    if (average50 > average200) and (account_name.funds > -100000):
        # Your funds can only fall so low
        account_name.buyStocks(1, currentPrice)
    elif (average50 < average200) and (account_name.noStocks > -1000):
        # You can only short sell so many stocks
        account_name.sellStocks(1, currentPrice)
    else:
        pass # Do nothing
        
def getMovingAverage(currentDay):
    day50 = currentDay-49
    day200 = currentDay-149

    # Calculate 50-day moving average (including current day)  
    sumStocks = 0
    for i in range(day50,currentDay+1):
            # Finds open price of each day
            item = df.index[i]
            stockPrice = df.loc[item][0]
            sumStocks += stockPrice
            
            
    average50 = sumStocks/50
    
    # Calculate 200-day moving average
    sumStocks2 = 0
    for i in range(day200,currentDay+1):
            # Finds open price of each day
            item = df.index[i]
            stockPrice = df.loc[item][0]
            sumStocks2 += stockPrice
            
    average200 = sumStocks2/200
    
    # print("The 50-day moving average is {}".format(average50))
    # print("The 200-day moving average is {}".format(average200))
    
    return average50, average200


def getCurrentPrice(currentDay):
    item = df.index[currentDay]
    return df.loc[item][0]
    
def sellAll(account_name, currentPrice):
    account_name.sellStocks(account_name.noStocks, currentPrice)
    
    
# Main code space

trader = Account()

#  Lets run the investment program for dates 250 to 2070
startDate = 201
endDate = 370
for i in range(startDate, endDate+1):
    currentDay = i
    average50, average200 = getMovingAverage(i)
    currentPrice = getCurrentPrice(i)
    
    adjustPortfolio(trader, currentPrice, average50, average200)
    
    #if (i % 100 ==0):
        #trader.statement() #Only shows statement at some intervals

print("\nFinal statement:")
trader.statement()

# At the end you must sell all your stocks
# End price is  already the current price
sellAll(trader, currentPrice)
trader.statement()
print("The profit is: {}".format(trader.funds))

#  I don't understand why I get these results.. if the stock price is falling
#  why do I still end up with positive stocks?




