from common_imports import *

def simplify_trend(trend):
    if isinstance(trend, str) and 'sideway' in trend:
        return 'sideway'
    return trend

def predict_trend_single(merged_path, label_dir, stock_csv, top_n, seq_len, window_len, future_point, sim_col):
    # 단일 top_n 처리
    files = [f for f in os.listdir(merged_path) if f.endswith('.csv')]
    sorted_files = sorted(files, key=lambda x: int(x.split('-')[0]))
    first_index = int(sorted_files[0].split('-')[0])
    last_index = int(sorted_files[-1].split('-')[0])

    stock_data = pd.read_csv(stock_csv)
    stock_data['time'] = pd.to_datetime(stock_data['time'])
    stock_data = stock_data[['time', 'open', 'high', 'low', 'close', 'volume']]
    
    trading_days = list(stock_data.groupby(stock_data['time'].dt.date))
    indexed_data = []
    current_idx = 0
    for date, day_data in trading_days:
        day_data = day_data.reset_index(drop=True)
        for i in range(0, len(day_data) - seq_len + window_len, window_len):
            window = day_data.iloc[i:i + seq_len]
            if len(window) == seq_len:
                indexed_data.append([current_idx, window['time'].iloc[-1]])
                current_idx += 1
    indexed_df = pd.DataFrame(indexed_data, columns=['index', 'time'])
    stock_data = stock_data.merge(indexed_df, on='time', how='left')

    pred_df = stock_data[stock_data['index'] >= first_index].copy()

    label_file = os.path.join(label_dir, f'{future_point}_future.csv')
    label_df = pd.read_csv(label_file)[['index', 'trend']]
    label_df['trend'] = label_df['trend'].apply(simplify_trend)

    os.makedirs('./Backtesting/pred', exist_ok=True)
    
    pred_df['real_trend'] = np.nan
    pred_df['pred_trend'] = np.nan
    
    # 단일 top_n에 대해 예측 수행 (tqdm 추가)
    for idx in tqdm(range(first_index, last_index + 1), desc=f"Predicting for top_n={top_n}, future={future_point}, sim={sim_col}"):
        file_name = f'{idx}-*.csv'
        file_path = os.path.join(merged_path, next(f for f in sorted_files if f.startswith(str(idx))))
        sim_data = pd.read_csv(file_path)
        
        real_trend = label_df[label_df['index'] == idx]['trend'].values
        if len(real_trend) > 0:
            pred_df.loc[pred_df['index'] == idx, 'real_trend'] = real_trend[0]
        
        top_similar = sim_data.sort_values(sim_col, ascending=False).head(top_n)
        top_indices = top_similar['index'].values
        top_trends = label_df[label_df['index'].isin(top_indices)]['trend'].value_counts()
        
        if not top_trends.empty:
            pred_trend = top_trends.idxmax()
            pred_df.loc[pred_df['index'] == idx, 'pred_trend'] = pred_trend
    
    output_file = f'./Backtesting/pred/{top_n}_{future_point}_future_{sim_col}.csv'
    pred_df.to_csv(output_file, index=False)