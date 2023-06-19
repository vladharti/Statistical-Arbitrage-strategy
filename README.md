# Statistical-Arbitrage-strategy

# Data
https://www.cryptodatadownload.com/data/binance/
For this project, the daily and minute prices of crypto coins were used. After testing the cointegration property of the pairs, Bitcoin and Bitcoin Cash were found to exhibit cointegrating properties. Thus the Statistical arbitrage (Pair trading) strategy will be tested on this pair.

# Finding the pairs
In order to run statistical arbitrage strategies on two assets, these need to possess specific statistical features, defined by cointegration. 
Cointegration is a statistical concept that deals with the long-term relationship between two or more non-stationary time series. It is used extensively in econometrics and finance to identify and test for the presence of such relationships among series that exhibit non-stationary behaviour, such as stock prices, currency exchange rates or cryptocurrencies. 
In simple terms, two or more time series are said to be cointegrated if:
1.	They are individually non-stationary, meaning they have a time-dependent structure, and their means and variances change over time. In practice, this often means that each time series has a unit root, which is a common cause of non-stationarity.
2.	There exists a linear combination of these time series that is stationary, meaning it has a constant mean and variance over time with no long-term persistent trend or seasonality.

It allows us to identify the long-term equilibrium relationships among non-stationary time series. 
In this project the prices of cryptocurrencies will be tested for cointegration. The data will be fitted into a linear regression model and the residuals will be stored separately. After this, an Augmented Dickey–Fuller test will be performed on the residuals to identify if there is a unit root present. In other words, this will test if the residuals are stationary. If this is the case, it can be assumed that the time series are cointegrated, thus exhibit a long-term equilibrium relationship.
Once there is proof of cointegration between 2 asset prices, these can be used as an underlying pair for statistical arbitrage trading strategies.

# Strategy description 

The statistical arbitrage is a High-Frequency trading strategy aiming to exploit the temporary mispricing of two related securities. Assuming these have a long-term equilibrium relationship, the strategy implies buying the undervalued asset and selling the overvalued one, with the expectation that the prices will return to the long-term equilibrium in the nearest future. 
Advantages of a statistical arbitrage trading strategy:
Market-neutral: Statistical arbitrage is designed to be market-neutral, meaning it aims to generate positive returns regardless of the overall market direction. This is achieved by holding both long and short positions in related securities. As a result, the strategy has the potential to deliver consistent returns in both bullish and bearish market conditions.
Limited exposure to systematic risk: Since statistical arbitrage strategies involve a combination of long and short positions, they usually have limited exposure to overall market risk. This means their returns are less influenced by broader market events, which can be beneficial in times of increased market volatility or economic uncertainty.
Relatively small initial capital requirements: As statistical arbitrage strategies open positions with offsetting cash flows, it doesn’t require a big initial capital. However, trading costs should be taking into account as transaction fees can add up quickly.
High-frequency trading potential: Many statistical arbitrage strategies are built for high-frequency trading, enabling traders to capitalize on numerous small profit opportunities throughout the day. By acting on price inefficiencies faster than other market participants, high-frequency traders can realize substantial benefits from statistical arbitrage strategies.

# Strategy pseudocode

Calculate “hedge_ratio” by fitting OLS regression on the entire dataset.

Calculate the portfolio value (also known as the spread) at each point in time using the asset prices and the constant hedge_ratio.

Calculate the Z score at each point in time, by computing the mean and standard deviation of the “lookback_period”, where lookback_period will define the number of previous observations we take into account. Example, if the lookback_period is 20, then we calculate the mean and standard deviation based on the last 20 minutes for each iteration.

Open positions:
If z<-2 buy 1 BTC and sell hedge_ratio worth of BCH;
	Close by opening an offsetting one when z>=0;
	
If z>2 sell 1 BTC and buy hedge_ratio worth of BCH;
	Close by opening an offsetting one when z<=0;

Record all opened positions by storing the trade timestamp, trade type, traded price for BTC, traded price for BCH in a dataset called “trades”.

Calculate the pnl of each trade based on the last price from the dataset and the stored prices from “trades” data frame.

Sum up the pnl

# Strategy optimisation

The statistical arbitrage strategy can be optimised on various parameters, including Z-score thresholds for entering and exiting a position and lookback period. Because of the processing power limitations, in this project, the optimisation will be done only on the lookback period. The optimisation function “optimize_lookback_period” aims execute the strategy for each instance of lookback period from 10 minutes to 60 minutes with a step of 5 minutes and to find the instance that maximise the strategy pnl. This will output the optimal lookback period as well as the maximised pnl.
In this project, the strategy was optimised based on the data from January to August 2022. The results indicate that the optimal lookback period is 10 minutes and the maximum pnl that was achieved for this period was $210,615.60.

# Testing the strategy
 
Once optimised, the strategy was tested on unseen data from September 2022 to December 2022. It has opened 17,162 trades(including the offsetting ones to close positions) and generated $89,995.26 in pnl by the end of December 2022. 
It is important to note that this performance results assume zero transaction fees as well as no spread between bid and ask prices. 

# Possible improvements

1.	Implement rolling hedge ratio – currently the above strategy uses a constant hedge ratio calculated on a previous 8 months’ worth of data. Ideally we want it to calculate the hedge ratio on the lookback period. However because of the performance power limitations, optimising a strategy with rolling hedge ratio is very time consuming.
2.	Consider fees and spreads- currently the data contains the close mid price of each minute and there is no visibility on the bid-ask spread. Using data containing bid and ask prices would allow to adjust the performance to the price spread. Moreover, taking into account exchange fees would improve the accuracy of the resulting pnl.
3.	Optimise multiple parameters – The optimisation function in this project only looks at the lookback period and does not optimise other parameters. By optimising other parameters such as Z score entering and exiting thresholds, the strategy can generate a better performance. 





