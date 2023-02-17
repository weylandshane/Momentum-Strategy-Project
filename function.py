import pandas as pd
import random
import numpy as np


def get_tickers_by_sector(sector):
    #not used, just early thought
    """
    input the sector we want in SP500 and return all tickers in that sector
    """
    df500 = pd.read_csv('sp500.csv')
    df_sector = df500.loc[df500['Sector'] == sector]
    return df_sector['Symbol']

# Get the tickers that we want


def get_tickers(init_date):
    """
    input(str) init_dat: the initial date when we start to 
                         calculate the momentum
    """
    df500 = pd.read_csv('S&P_500_Historical_Components.csv')
    if(pd.to_datetime(init_date) <= pd.to_datetime("1996-01-01")):
        print("Initial date is out of the range, please input a date which is later than 1996-01-01.")
    else:
        x = df500.loc[df500['date'] == init_date]
        # If the initial date is not on the S&P_500_Historical_Componenets.csv, go back one day
        # until the data is found.
        d = init_date
        while(x.empty):
            d = pd.to_datetime(d) - pd.DateOffset(days=1)
            x = df500.loc[df500['date'] == d.strftime("%Y-%m-%d")]
        df500 = x
        df500_ticker = pd.Series(df500['tickers'], dtype="string").tolist()
        df500_ticker = df500_ticker[0].split(",")
        return df500_ticker

def get_random_ticker_dataframe(df500_ticker,df_total,init_date, num_stock, lowest_price, highest_price):
        """
        input(int) num_stock: number of ticker we want to analyze.

        input(int) lowest_price/highest_price: The filter standard. We only want the stock that the open price is
        greater than lowest_price and lower than highest_price.
        input(dataframe) df500_ticker: dataframe of SP500 tickers
        input(str) init_dat: the initial date when we start to calculate the momentum
        """
        # Filter with price of init date
        df = df_total.copy().iloc[0:1]
        bool_list = df > lowest_price
        bool_list = df[bool_list].dropna(
            axis='columns', how='all') < highest_price
        df = df[bool_list].dropna(axis='columns', how='all')
        df500_ticker = list(df)

        # Generate random number list
        n = num_stock
        random_list = random.sample(range(len(df500_ticker)), n)

        # Obtain ticker list using random index
        ticker_list = []
        for i in range(len(random_list)):
            t = df500_ticker[random_list[i]]
            ticker_list.append(t)

        return [ticker_list, df_total[ticker_list]]


def weight_calculation(port):
    port_pct = port.pct_change()[1:]
    port_returns = []
    port_volatility = []
    port_weights = []
    
    num_assets = len(port_pct.columns)
    num_portfolios = 1000
    
    individual_rets = port_pct.mean()
    # Annualized
    individual_rets = (individual_rets + 1) **(252) - 1
    
    var_matrix = port_pct.cov() * 252
    
    for port in range(num_portfolios):
        # Normalized weights
        weights = np.random.random(num_assets)
        weights = weights / np.sum(weights)
        port_weights.append(weights)
        
        # Calculate variance
        var = var_matrix.mul(weights, axis=0).mul(weights, axis=1).sum().sum()
        # get volatility (annualized)
        vol = np.sqrt(var) * np.sqrt(252)
        port_volatility.append(vol)
        
        # Obtain weighted return
        returns = np.dot(weights, individual_rets)
        port_returns.append(returns)
    
    # Create dictionary
    data = {'Returns':port_returns, 'Volatility': port_volatility}
    
    ticker_name = port_pct.columns.tolist()
    for counter, symbol in enumerate(ticker_name):
        data[symbol + ' weight'] = [w[counter] for w in port_weights]
    
    portfolio_V1 = pd.DataFrame(data)

    rf = 0.025  # Average risk free rate    

    b = portfolio_V1
    # using the one with the highest Sharpe Ratio
    opt_risk_port = b.iloc[((b['Returns'] - rf)/b['Volatility']).idxmax()]
    opt_risk_port_w = opt_risk_port.iloc[2:].tolist()
    
    return opt_risk_port_w




def draft_function(ticker, start, port_start, window, holding, sector, wealth_list, weight, df_total):
    """
    input variables:
        ticker: list of the filtered tickers
        start: Lookback window start time
        window: time length of our lookback window
        holding: time length holding the portfolio in each period
        sector: areas of the companies 
        wealth_list: recorded wealth, start with a one element list
        weight: how we distribute our wealth to the stocks in our portfolios
        df_total: dataframe of the filtered stocks
    """

    # momentum calculation end date
    end = pd.to_datetime(start) + window

    # port folio start and end date(difference is 1 month)

    port_end = port_start + holding

    df = df_total[start:end]

    # find annualized return and rank, start building portfolio
    df_annualized_return = df.iloc[-1]/df.iloc[0]-1
    df_annualized_return = df_annualized_return.sort_values()


    # portfolio with top 5 stocks
    portfolio = []
    for i in range(5):
        if(df_annualized_return.tail(5).iloc[i]>0):
            portfolio.append(df_annualized_return.tail(5).index[i])
        
    

    # equal weight
    if(weight == 'equal'):
        num = len(portfolio)
        weight = []
        for i in range(num):
            weight.append(1/num)
            
    elif (weight == "Optimal Portfolio"):
        df_port = df[portfolio]
        print(df_port)
        weight = weight_calculation(df_port)
        print("if 5 weights add to one" + str(sum(weight)))

    # calculate inversed volatility as weight
    elif(weight == 'inverse volatility'):
        df_var = df[portfolio]

        IV_lst = []
        for ticker in portfolio:
            std = df_var[ticker].std()
            temp = 1/std
            IV_lst.append(temp)
        weight = []
        for i in range(len(IV_lst)):
            weight.append(IV_lst[i]/sum(IV_lst))

    # calculate payoff of portfolio with one share of each stock
    df_temp = df_total.copy()[port_start:port_end]
    df_temp = df_temp[portfolio]

    payoff_temp = df_temp.iloc[-1]-df_temp.iloc[0]

    # get latest wealth
    wealth = wealth_list[-1]
    # add weight to each ticker
    i = 0
    for ticker in portfolio:

        weighted_wealth = wealth * weight[i]
        share = weighted_wealth / df_temp[ticker].iloc[0]
    
        payoff_temp[ticker] = payoff_temp[ticker]*share

        # change final df_temp to get the wealth
        df_temp[ticker].iloc[-1] = df_temp[ticker].iloc[-1]*share

        i += 1

    # update wealth
    temp_wealth = sum(df_temp.iloc[-1])
    wealth_list.append(temp_wealth)

    final_df = pd.DataFrame()
    final_df['Wealth Before'] = [wealth_list[-2]]
    final_df['Window Start'] = [start]
    final_df['Window End'] = [end]
    final_df['Portfolio Start'] = [port_start]
    final_df['Portfolio End'] = [port_end]
    final_df['Portfolio'] = [portfolio]
    final_df['Portfolio Payoff'] = sum(payoff_temp)
    final_df['Wealth After'] = wealth_list[-1]
    return final_df
