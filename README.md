# MF-703-Project Proposal

Momentum investing is a well-known trading strategy that suggests investors first compare and rank the historical performances among various stocks, then purchase the past winner stocks and short the past loser stocks to maximize their profits. In 1993, Jegadeesh and Titman(1993) used this strategy and generated significant positive returns over 3- to 12-month holding periods. In our project, we will use Python to replicate this system and backtest it to see whether momentum investing is a robust trading strategy or not. 

To replicate this system, we will first select our “tracking universe.” There are numerous stocks in the financial market; therefore, to improve the efficiency of the project, we have to select some stocks (probably 50-100 stocks) as candidates for our momentum portfolio. We will call those candidates the “tracking universe.” Once the “tracking universe” is determined, we will collect stock price data. And we think that Yahoo Finance will be the major source of our data. Next, we need to calculate the returns of all candidates and rank them accordingly from the best return to the worst return. Returns on different time frequencies can have a serious effect on momentum investing. We may try several returns (monthly return, weekly return, etc.) to see which works the best in our strategy. Based on the ranking, we select winners and losers to form the momentum portfolio. As Jegadeesh and Titman(1933) mentioned in their paper, “the longer-term performances of these winners and losers reveal that half of their excess returns in the year following the portfolio formation date dissipate within the following 2 years.” This implied that the momentum portfolio needs to be rebalanced after a certain period (1 month, 3 months, etc.). Therefore, we will repeat the previous steps to rebalance our portfolio. We may also compare several holding periods to see which one generates the best result.
