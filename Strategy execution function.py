
##################################################################################
############### Constant hedge ratio version  ####################################
##################################################################################

# Function to estimate the cointegrating relationship
def estimate_cointegrating_relationship(prices_1, prices_2):
    model = sm.OLS(prices_1, prices_2).fit()
    return model.params[0]

# Function to calculate z-score
def calculate_zscore(series):
    return (series - np.mean(series)) / np.std(series)

lookback_period=30
# Define the trading signal threshold
entry_threshold = 2
exit_threshold = 0


# Calculate hedge ratio by fitting OLS regression on the entire dataset
hedge_ratio = estimate_cointegrating_relationship(merged_data_1['BTC'], merged_data_1['BCH'])

def trading_strategy(dataset,lookback_period):
    final_price_BTC = dataset['BTC'].iloc[-1]
    final_price_BCH = dataset['BCH'].iloc[-1]
   
   
    # Calculate the spread using the calculated hedge ratio
    dataset.loc[:, 'portfolio_value'] = dataset['BTC']-hedge_ratio * dataset['BCH']

    # Calculate the rolling hedge ratio

    # Calculate the z-score
    dataset.loc[:, 'rolling_z_score'] = dataset['portfolio_value'].rolling(lookback_period).apply(lambda x: calculate_zscore(x).tail(1).iloc[0], raw=False)

    #There will be 2 types of trades
    #Type='Buy' if z<-2 buy 1 BTC and sell hedge_ratio worth of BCH
    #Type='Sell' if z>2 sell 1 BTC and buy hedge_ratio worth of BCH
    final_price_BTC = dataset['BTC'].iloc[-1]
    final_price_BCH = dataset['BCH'].iloc[-1]
    trade_type=''
    #set up a flag, "open_position" to know if the position is open
    open_position = 0
    trades=pd.DataFrame(columns=['date','trade_type','price_BTC','price_BCH'])
    for i, row in dataset.iterrows():
        if open_position==0:
            if row['rolling_z_score'] >= entry_threshold:
                trade_type='Sell'
                pnl= row['BTC'] - final_price_BTC + hedge_ratio*(final_price_BCH- row['BCH'])
                trades = trades.append({"date": row['date'], "trade_type": trade_type,"price_BTC": row['BTC'],"price_BCH": row['BCH'],"PNL": pnl }, ignore_index=True)
                open_position=1
            elif row['rolling_z_score']<-entry_threshold:
                trade_type='Buy'
                pnl= -(row['BTC'] - final_price_BTC) + hedge_ratio*-(final_price_BCH- row['BCH'])
                trades = trades.append({"date": row['date'], "trade_type": trade_type,"price_BTC": row['BTC'],"price_BCH": row['BCH'],"PNL": pnl}, ignore_index=True)
                open_position=1
            else: continue;
            #We are going to close a position by opening an offseting off
        elif open_position==1:
            if trade_type=='Sell':
                if row['rolling_z_score']<=exit_threshold:
                    pnl= -(row['BTC'] - final_price_BTC) + hedge_ratio*-(final_price_BCH- row['BCH'])
                    trades = trades.append({"date": row['date'], "trade_type": 'Buy',"price_BTC": row['BTC'],"price_BCH": row['BCH'],"PNL": pnl}, ignore_index=True)
                    trade_type=''
                    open_position=0
                else: continue;
            elif trade_type=='Buy':
                if row['rolling_z_score']>=exit_threshold:
                    pnl= row['BTC'] - final_price_BTC + hedge_ratio*(final_price_BCH- row['BCH'])
                    trades = trades.append({"date": row['date'], "trade_type": 'Sell',"price_BTC": row['BTC'],"price_BCH": row['BCH'],"PNL": pnl}, ignore_index=True)
                    trade_type=''
                    open_position=0
                else: continue;
            else: continue;
       
    total_pnl=trades['PNL'].sum()
    return total_pnl, trades
result=trading_strategy(merged_data_1,lookback_period)
print(result[0])