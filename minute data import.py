# Read in the minute data
BTC = pd.read_csv('Equity data/Binance_BTCUSDT_2022_minute_short.csv', sep=',')
BTC['date'] = pd.to_datetime(BTC['date'], format='%m/%d/%Y %H:%M')
BTC= BTC.sort_values(by='date')

BCH = pd.read_csv('Equity data/Binance_BCHUSDT_2022_minute.csv', sep=',')
BTC['date'] = pd.to_datetime(BTC['date'], format='%m/%d/%Y %H:%M')
BCH['date'] = pd.to_datetime(BCH['date'])
BCH= BCH.sort_values(by='date')
#keep only date and close price columns
BCH=BCH.loc[:,['date','close']]

#Merge the 2 datasets into one
merged_data = pd.merge(BTC, BCH, on='date', how='left')
#Rename columns of the merged_dataset
merged_data.rename(columns={'close_x': 'BTC'}, inplace=True)
merged_data.rename(columns={'close_y': 'BCH'}, inplace=True)

#Divide the dataset in half for later testing
#DATASET 1 will be used for optimisation and DATASET 2 will be used for testing the performance
cutoff = '2022-08-31'

# Create a filter before cutoff
before_cutoff = merged_data['date'] < cutoff
# Use .loc to filter the data into two sets
merged_data_1 = merged_data.loc[before_cutoff, :]
merged_data_2 = merged_data.loc[~before_cutoff, :]  
# Check the split datasets
print(f'merged_data_1: {len(merged_data_1)} rows')
print(f'merged_data_2: {len(merged_data_2)} rows')

