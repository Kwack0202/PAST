from common_imports import *
from utils.labeling import *
from utils.candlestick_img import *

# ============================================
'''
step 1.data preprocessing
'''
def data_preprocessing(output_dir):
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    # ============================================
    # 1. Data concat
    stock_data = pd.DataFrame()
    for filename in tqdm(sorted(os.listdir('./data/Futures_KOSPI/'))):
        if filename.endswith('.xlsx'):
            file_path = os.path.join('./data/Futures_KOSPI/', filename)
            
            df = pd.concat(pd.read_excel(file_path, sheet_name=None), ignore_index=True)
            
            stock_data = pd.concat([stock_data, df], ignore_index=True)
    stock_data.to_csv(os.path.join(output_dir, f"origin_data.csv"), encoding='utf-8', index=False)

    stock_data['BBAND_UPPER'],stock_data['BBAND_MIDDLE'],stock_data['BBAND_LOWER'] = talib.BBANDS(stock_data['close'],20,2)
    # ============================================
    # 2. Instance selection
    stock_data['time'] = pd.to_datetime(stock_data['time'])

    # 2-1
    date_counts = stock_data['time'].dt.date.value_counts()
    dates_to_remove = date_counts[date_counts.isin([380, 336, 395, 351, 382])].index
    stock_data = stock_data[~stock_data['time'].dt.date.isin(dates_to_remove)].reset_index(drop=True)

    # 2-2
    stock_data = stock_data[stock_data['time'].dt.time < pd.Timestamp('15:30:00').time()].reset_index(drop=True)
    stock_data.to_csv(os.path.join(output_dir, f"stock_data.csv"), encoding='utf-8', index=False)

'''
step 2.numeric data
''' 
def numeric_data(numeric_dir, stock_csv, seq_len, window_len, end_date):
    if not os.path.exists(numeric_dir):
        os.makedirs(numeric_dir)
    
    stock_data = pd.read_csv(stock_csv)
    stock_data['time'] = pd.to_datetime(stock_data['time'])
    
    loop_end = pd.Timestamp(end_date).date()
    
    trading_days = list(stock_data.groupby(stock_data['time'].dt.date))
    
    index = 0
    start_day = 0
    end_day = len(trading_days)
    
    for trading_day in tqdm(range(start_day, end_day)):
        date, group = trading_days[trading_day]
    
        if date >= loop_end:
            break
        
        candle_data = pd.DataFrame(group).reset_index(drop=True)
        
        for start in range(0, len(candle_data) - seq_len + window_len, window_len):
            try:
                end = start + seq_len
                current_data = candle_data.iloc[start:end]
                current_data = current_data.reset_index(drop=True)
                
                current_data.to_csv(os.path.join(numeric_dir, f'{index}-{date}.csv'), encoding='utf-8', index=False)                    
                index += 1
            
            except Exception as e:
                print(f"Error processing {date}: {e}")
                continue  
                
'''
step 3.candlestick image
'''
def candlestick_image(candel_dir, stock_csv, seq_len, window_len, end_date, start_idx, end_idx):
    if not os.path.exists(candel_dir):
        os.makedirs(candel_dir)
    
    stock_data = pd.read_csv(stock_csv)
    stock_data['time'] = pd.to_datetime(stock_data['time'])
    
    loop_end = pd.Timestamp(end_date).date()
    trading_days = list(stock_data.groupby(stock_data['time'].dt.date))
    image_index = start_idx * ((len(stock_data) - seq_len + window_len) // window_len)
    
    for trading_day in tqdm(range(start_idx, end_idx)):
        date, group = trading_days[trading_day]
    
        if date >= loop_end:
            break
        
        candle_data = pd.DataFrame(group).reset_index(drop=True)
        
        for start in range(0, len(candle_data) - seq_len + window_len, window_len):
            try:
                end = start + seq_len
                current_data = candle_data.iloc[start:end].reset_index(drop=True)
                
                fig = plot_candles(current_data, title=None, trend_line=False, volume_bars=False, color_function=None, technicals=None)
                current_image_path = os.path.join(candel_dir, f'{image_index}-{date}.png')
                fig.savefig(current_image_path, dpi=150)
                plt.close(fig)
                image_index += 1
            
            except Exception as e:
                print(f"Error processing {date}: {e}")
                continue

'''
step 4.bollinger band area image
''' 
def bollinger_band(bband_dir, stock_csv, seq_len, window_len, end_date, start_idx, end_idx):
    if not os.path.exists(bband_dir):
        os.makedirs(bband_dir)

    stock_data = pd.read_csv(stock_csv)
    stock_data['time'] = pd.to_datetime(stock_data['time'])
    
    loop_end = pd.Timestamp(end_date).date()
    trading_days = list(stock_data.groupby(stock_data['time'].dt.date))
    image_index = start_idx * ((len(stock_data) - seq_len + window_len) // window_len)
    
    for trading_day in tqdm(range(start_idx, end_idx)):
        date, group = trading_days[trading_day]
    
        if date >= loop_end:
            break
        
        candle_data = pd.DataFrame(group).reset_index(drop=True)
        
        for start in range(0, len(candle_data) - seq_len + window_len, window_len):
            try:
                end = start + seq_len
                current_data = candle_data.iloc[start:end].reset_index(drop=True)
                
                plt.figure(facecolor='black')
                plt.fill_between(current_data.index, current_data['BBAND_LOWER'], current_data['BBAND_UPPER'], color='white')
                plt.plot(current_data['BBAND_UPPER'], label='Upper Bollinger Band', color='white')
                plt.plot(current_data['BBAND_MIDDLE'], label='Middle Bollinger Band', color='white')
                plt.plot(current_data['BBAND_LOWER'], label='Lower Bollinger Band', color='white')
                plt.axis('off')
                plt.savefig(os.path.join(bband_dir, f'{image_index}-{date}.png'), dpi=150)
                plt.close()
                image_index += 1
            
            except Exception as e:
                print(f"Error processing {date}: {e}")
                continue

'''
step 5.stock movement labeling
'''  
def label_data(output_dir, stock_csv, seq_len, window_len, future_points, end_date):
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    stock_data = pd.read_csv(stock_csv)
    stock_data['time'] = pd.to_datetime(stock_data['time'])
    
    loop_end = pd.Timestamp(end_date).date()
    
    trading_days = list(stock_data.groupby(stock_data['time'].dt.date))
    
    for future_point in future_points:       
        image_index = 0
        results = []
        for trading_day in tqdm(range(len(trading_days))): 
            date, group = trading_days[trading_day]
            
            if date >= loop_end:
                break

            candle_data = pd.DataFrame(group).reset_index(drop=True)
                   
            for start in range(0, len(candle_data) - seq_len + window_len, window_len):
                end = start + seq_len
                
                current_data = candle_data.iloc[start:end]
                
                available_future = candle_data.iloc[end:]
                
                if len(available_future) >= future_point:
                    future_data = candle_data.iloc[end:end+future_point]
                
                else:
                    future_data_current = available_future
                    remaining = future_point - len(future_data_current)
                    if trading_day < len(trading_days) - 1:
                        _, next_day_group = trading_days[trading_day + 1]
                        next_day_data = pd.DataFrame(next_day_group).reset_index(drop=True)
                        future_data_next = next_day_data.iloc[0:remaining]
                        future_data = pd.concat([future_data_current, future_data_next], ignore_index=True)
                    else:
                        future_data = future_data_current
                
                # ===========================================================================
                current_result = analyze_trend(current_data, 'current', image_index)
                future_result = analyze_trend(future_data, 'future', image_index, current_data['close'].iloc[-1] if future_point == 1 else None)    
                
                if current_result:
                    results.append(current_result)    
                if future_result:
                    results.append(future_result)
                    
                image_index += 1
        
        result_df = pd.DataFrame(results)
        current_df = result_df[result_df['phase'] == 'current'].reset_index(drop=True)
        future_df = result_df[result_df['phase'] == 'future'].reset_index(drop=True)
        
        current_df['date'] = pd.to_datetime(current_df['date'])
        current_df.to_csv(os.path.join(output_dir, f"{future_point}_current.csv"), encoding='utf-8', index=False)

        future_df['date'] = pd.to_datetime(future_df['date'])
        future_df.to_csv(os.path.join(output_dir, f"{future_point}_future.csv"), encoding='utf-8', index=False)