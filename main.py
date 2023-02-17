import function as d
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import numpy as np
#variables that we need for the function
num_stock = 300 # number of stock we need in our stock universe
lowest_price = 10 #we only keep the stock with price greater than lowest price in our universe
highest_price = 500000 #we only keep the stock with price lower than highest price in our universe
init_date = "2010-01-01"  #must be a date later than 1996/01/01

sector = 'Industrials' #The area that we want to investigate

weight='equal' # weight how we want to divide our wealth to buy the stocks in our portfolio



#download data of 3 years for training and back testing
df500_ticker = d.get_tickers(init_date)
df_total = yf.download(df500_ticker, start=init_date, end=pd.to_datetime(
    init_date)+pd.DateOffset(years=2))['Adj Close'].dropna(how='all')
df_total = df_total.dropna(axis='columns',how = 'all')
df_check = df_total.isnull()
for row in range(len(df_total.index)) :
    for col in range(len(df_total.columns)):
        if(df_check.iloc[row,col] == True):
            df_total.iloc[row,col] = df_total.iloc[row-1,col]
            
vol = []
for j in range(100):
    print(j)
    #test eight different strategies with different frequncy n times
    #list contains 10 outcomes of the same frequency
    big_data1 = []
    big_data2 = []
    big_data3 = []
    big_data4 = []
    big_data5 = []
    big_data6 = []
    big_data7 = []
    big_data8 = []
    payoff_final1_lst = []
    payoff_final2_lst = []
    payoff_final3_lst = []
    payoff_final4_lst = []
    payoff_final5_lst = []
    payoff_final6_lst = []
    payoff_final7_lst = []
    payoff_final8_lst = []
    
    
    for i in range(j+1):
        
        #trying 30 different universe
        ticker_dataframe = d.get_random_ticker_dataframe(df500_ticker,df_total,init_date, num_stock,lowest_price,highest_price)
        ticker = ticker_dataframe[0]#selected tickers
        df = ticker_dataframe[1]#two years data of selected tickers 
            
        #window = 12 M, holding = 1 M, start date = init_date, length =  1Y
        start1 = pd.to_datetime(init_date) # momentum calculation start time
        window1 = pd.DateOffset(months=12)
        holding1 = pd.DateOffset(months=1)
        port_start1 = start1 + window1
        wealth_list1=[1000000]#wealth start from 1 million and record each update
        data1 = []
        for i in range(12):
            data1.append(d.draft_function(ticker, start1, port_start1, window1, holding1, sector, wealth_list1, weight, df))
            start1 += holding1
            port_start1 += holding1
            
        data1 = pd.concat(data1)
        payoff_final1 = sum(data1['Portfolio Payoff'])
    
        #window = 12 M, holding = 2 M, start date = init_date, length = 1 Y
        start2 = pd.to_datetime(init_date) # momentum calculation start time
        window2 = pd.DateOffset(months=12)
        holding2 = pd.DateOffset(months=2)
        port_start2 = start2 + window2
        wealth_list2=[1000000]#wealth start from 1 million and record each update
        data2 = []
        for i in range(6):
            data2.append(d.draft_function(ticker, start2, port_start2, window2, holding2, sector, wealth_list2, weight,df))
            start2 += holding2
            port_start2 += holding2
            
        data2 = pd.concat(data2)
        payoff_final2 = sum(data2['Portfolio Payoff'])
    
        #window = 12 M, holding = 3 M, start date = init_date, length = 1 Y
        start3 = pd.to_datetime(init_date) # momentum calculation start time
        window3 = pd.DateOffset(months=12)
        holding3 = pd.DateOffset(months=3)
        port_start3 = start3 + window3
        wealth_list3=[1000000]#wealth start from 1 million and record each update
        data3 = []
        for i in range(4):  #range(12 M mod holding)
            data3.append(d.draft_function(ticker, start3, port_start3, window3, holding3, sector, wealth_list3, weight, df))
            start3 += holding3
            port_start3 += holding3
            
        data3 = pd.concat(data3)
        payoff_final3 = sum(data3['Portfolio Payoff'])
        
        #window = 12 M, holding = 4 M, start date = init_date, length = 1 Y
        start4 = pd.to_datetime(init_date)  # momentum calculation start time
        window4 = pd.DateOffset(months=12)
        holding4 = pd.DateOffset(months=4)
        port_start4 = start4 + window4
        wealth_list4 = [1000000]  # wealth start from 1 million and record each update
        data4 = []
        for i in range(3):
            data4.append(d.draft_function(ticker, start4, port_start4, window4, holding4, sector, wealth_list4, weight, df))
            start4 += holding4
            port_start4 += holding4
    
        data4 = pd.concat(data4)
        payoff_final4 = sum(data4['Portfolio Payoff'])
    
        #window = 12 M, holding = 6 M, start date = init_date, length = 1 Y
        start5 = pd.to_datetime(init_date)  # momentum calculation start time
        window5 = pd.DateOffset(months=12)
        holding5 = pd.DateOffset(months=6)
        port_start5 = start5 + window5
        wealth_list5 = [1000000]  # wealth start from 1 million and record each update
        data5 = []
        for i in range(2):
            data5.append(d.draft_function(ticker, start5, port_start5, window5, holding5, sector, wealth_list5, weight, df))
            start5 += holding5
            port_start5 += holding5
    
        data5 = pd.concat(data5)
        payoff_final5 = sum(data5['Portfolio Payoff'])
    
        #window = 1 M, holding = 1 M, start date = init_date + 11 months date off set, length = 1 Y
        start6 = pd.to_datetime(init_date) + pd.DateOffset(months=11) # momentum calculation start time
        window6 = pd.DateOffset(months=1)
        holding6 = pd.DateOffset(months=1)
        port_start6 = start6 + window6
        wealth_list6 = [1000000]  # wealth start from 1 million and record each update
        data6 = []
        for i in range(12):
            data6.append(d.draft_function(ticker, start6, port_start6, window6, holding6, sector, wealth_list6, weight, df))
            start6 += holding6
            port_start6 += holding6
    
        data6 = pd.concat(data6)
        payoff_final6 = sum(data6['Portfolio Payoff'])
        
        #window = 3 M, holding = 3 M, start date = init_date + 9 months date off set, length = 1 Y
        start7 = pd.to_datetime(init_date) + pd.DateOffset(months=9) # momentum calculation start time
        window7 = pd.DateOffset(months=3)
        holding7 = pd.DateOffset(months=3)
        port_start7 = start7 + window7
        wealth_list7 = [1000000]  # wealth start from 1 million and record each update
        data7 = []
        for i in range(4):
            data7.append(d.draft_function(ticker, start7, port_start7, window7, holding7, sector, wealth_list7, weight, df))
            start7 += holding7
            port_start7 += holding7
    
        data7 = pd.concat(data7)
        payoff_final7 = sum(data7['Portfolio Payoff'])    
    
        #window = 11 M, holding = 3 M, start dtae  = init_date, length = 1 Y
        #Port_start date is still the start date + 12 month, we want to check reversal in this strategy
        start8 = pd.to_datetime(init_date) # momentum calculation start time
        port_start8 = start8 + pd.DateOffset(months=12) 
        window8 = pd.DateOffset(months=11)
        holding8 = pd.DateOffset(months=3)
        wealth_list8=[1000000]#wealth start from 1 million and record each update
        data8 = []
        for i in range(4):
            data8.append(d.draft_function(ticker, start8, port_start8, window8, holding8, sector, wealth_list8, weight, df))
            start8 += holding8
            port_start8 += holding8
            
        data8 = pd.concat(data8)
        payoff_final8 = sum(data8['Portfolio Payoff'])
        
        big_data1.append(data1)
        big_data2.append(data2)
        big_data3.append(data3)
        big_data4.append(data4)
        big_data5.append(data5)
        big_data6.append(data6)
        big_data7.append(data7)
        big_data8.append(data8)
        payoff_final1_lst.append(payoff_final1)
        payoff_final2_lst.append(payoff_final2)
        payoff_final3_lst.append(payoff_final3)
        payoff_final4_lst.append(payoff_final4)
        payoff_final5_lst.append(payoff_final5)
        payoff_final6_lst.append(payoff_final6)
        payoff_final7_lst.append(payoff_final7)
        payoff_final8_lst.append(payoff_final8)
    
    payoff_final_lst =[payoff_final1_lst, payoff_final2_lst, payoff_final3_lst, payoff_final4_lst, payoff_final5_lst, payoff_final6_lst, payoff_final7_lst, payoff_final8_lst]
    

    
    strategy_list = ['strategy 1', 'strategy 2', 'strategy 3', 'strategy 4', 'strategy 5', 'strategy 6', 'strategy 7', 'strategy 8']
    win_list = ["12 Month", "12 Month", "12 Month", "12 Month", "12 Month", "1 Month", "3 Month", "11 Month"]
    hol_list = ["1 Month", "2 Month", "3 Month", "4 Month", "6 Month", "1 Month", "3 Month", "3 Month"]
    avg_list = []
    max_list = []
    min_list = []
    
    for i in range(8):
        lst = payoff_final_lst[i]
        sum_lst = sum(lst)
        avg = sum_lst / len(lst)
        avg_list.append(avg)
        max_list.append(max(lst))
        min_list.append(min(lst))
    
    pd.options.display.float_format = '{:.5f}'.format
    dic = {'Strategy':strategy_list,'Lookback Window':win_list, 'Holding period':hol_list ,'Average':avg_list,'Maximum':max_list,'Minimum':min_list}
    strategy_df = pd.DataFrame(dic)
    strategy_df.to_csv(init_date +" - "+ weight + '.csv')
    
    """
    print(strategy_df) #print the out put of 30 times 
    

    plt.hist(payoff_final1_lst)
    plt.show()
    plt.figure()
    plt.hist(payoff_final2_lst)
    plt.show()
    plt.figure()
    plt.hist(payoff_final3_lst)
    plt.show()
    plt.figure()
    plt.hist(payoff_final4_lst)
    plt.show()
    plt.figure()
    plt.hist(payoff_final5_lst)
    plt.show()
    plt.figure()
    plt.hist(payoff_final6_lst)
    plt.show()
    plt.figure()
    plt.hist(payoff_final7_lst)
    plt.show()
    plt.figure()
    plt.hist(payoff_final8_lst)
    plt.show()
    plt.figure()
    """
    
    payoff_final1_lst = np.array(payoff_final1_lst)
    vol.append(payoff_final1_lst.std())
    
plt.figure()
plt.plot(vol)

    
    
    