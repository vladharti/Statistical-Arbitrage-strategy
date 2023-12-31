#########################################################################################
###################### Cointegration test on daily prices ###############################
#########################################################################################

#Due to processing power limitation we will be using daily returns to check for cointegration

BTC_Daily = pd.read_csv('Equity data/Binance_BTCUSDT_d.csv', sep=',')
BTC_Daily['Date'] = pd.to_datetime(BTC_Daily['Date'], format='%m/%d/%Y')
BTC_Daily= BTC_Daily.sort_values(by='Date')
BTC_Daily=BTC_Daily.loc[:,['Date','Close']]


BCH_Daily = pd.read_csv('Equity data/Binance_BCHUSDT_d.csv', sep=',')
BCH_Daily['Date'] = pd.to_datetime(BCH_Daily['Date'], format='%m/%d/%Y')
BCH_Daily= BCH_Daily.sort_values(by='Date')
BCH_Daily=BCH_Daily.loc[:,['Date','Close']]

#Merge the 2 datasets into one
merged_daily = pd.merge(BTC_Daily, BCH_Daily, on='Date', how='left')
#Rename columns of the merged_dataset
merged_daily.rename(columns={'Close_x': 'BTC'}, inplace=True)
merged_daily.rename(columns={'Close_y': 'BCH'}, inplace=True)

# Filter the dataset only for 2022
start_date = '2022-01-01'
end_date = '2022-12-31'
daily_2022 = merged_daily[(merged_daily['Date'] >= start_date) & (merged_daily['Date'] <= end_date)]

#fit the data into a linear regression model store the results in the "result" variable
result = linregress(daily_2022['BCH'], daily_2022['BTC'])

#calculate the residuals and store them as a series
residuals= daily_2022['BTC']- result.slope*daily_2022['BCH']

#perform the Augmented Dickey–Fuller test
adf = ts.adfuller(residuals)
print(adf)

#interpreting the result
if adf[1]<0.01:
    test_result='The pair has a cointegrating relationship with 99% confidence'
elif adf[1]<0.05:
    test_result='The pair has a cointegrating relationship with 95% confidence'
elif adf[1]<0.1:
    test_result='The pair has a cointegrating relationship with 90% confidence'
else: test_result='The pair has not enough evidence of a cointegrating relationship'
print(test_result)
print(result)