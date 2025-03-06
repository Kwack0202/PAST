from common_imports import *

def process_trading_signals(pred_file_path, stock_data_path='./data/origin_data/stock_data.csv', opposite_count=2):
    pred_csv = pd.read_csv(pred_file_path)
    pred_csv['time'] = pd.to_datetime(pred_csv['time'])

    current_csv = pd.read_csv('./data/label/5_current.csv')
    current_csv = current_csv[['index', 'trend']]
    current_csv = current_csv.rename(columns={'trend': 'current_trend'})

    pred_csv = pd.merge(pred_csv, current_csv, on='index', how='left')

    stock_data = pd.read_csv(stock_data_path)
    stock_data['time'] = pd.to_datetime(stock_data['time'])
    stock_data = stock_data[stock_data['time'] >= '2024-01-01'].reset_index(drop=True)
    stock_data = stock_data[['time', 'open', 'high', 'low', 'close', 'volume']]

    trading_days = list(pred_csv.groupby(pred_csv['time'].dt.date))
    signal_results = []

    for trading_day in tqdm(range(len(trading_days)), desc=f"Processing {os.path.basename(pred_file_path)}"):
        date, group = trading_days[trading_day]
        trading_df = group.reset_index(drop=True)

        initial_position_set = False
        current_position = None  # 현재 포지션 상태 추적
        counter = 0  # 반대 신호 누적 카운터 추가

        for i in range(len(trading_df)):
            current_trend = trading_df.loc[i, 'current_trend']
            pred_trend = trading_df.loc[i, 'pred_trend']

            if not initial_position_set:
                # 포지션이 없는 상태
                if current_trend == pred_trend and pred_trend in ['up', 'down']:
                    trading_df.loc[i, 'position'] = 'long' if pred_trend == 'up' else 'short'
                    initial_position_set = True
                    current_position = trading_df.loc[i, 'position']
                    counter = 0  # 카운터 초기화
                else:
                    trading_df.loc[i, 'position'] = 'No action'
            else:
                # 포지션이 있는 상태
                last_position = trading_df.loc[i - 1, 'position']

                if last_position == 'margin transaction':
                    # 이전에 청산된 경우 새 포지션 진입 여부 판단
                    if current_trend == pred_trend and pred_trend in ['up', 'down']:
                        trading_df.loc[i, 'position'] = 'long' if pred_trend == 'up' else 'short'
                        current_position = trading_df.loc[i, 'position']
                        counter = 0  # 카운터 초기화
                    else:
                        trading_df.loc[i, 'position'] = 'No action'
                        initial_position_set = False
                else:
                    # 현재 포지션 유지 중
                    if (current_position == 'long' and pred_trend == 'down') or (current_position == 'short' and pred_trend == 'up'):
                        # 반대 방향 예측 시 카운터 증가
                        counter += 1
                        if counter >= opposite_count:
                            trading_df.loc[i, 'position'] = 'margin transaction'
                            current_position = None
                            counter = 0  # 청산 후 카운터 초기화
                        else:
                            trading_df.loc[i, 'position'] = 'holding'
                    else:
                        # 동일 방향 또는 sideway 시 유지
                        trading_df.loc[i, 'position'] = 'holding'
                        # counter = 0  # 동일 방향 시 카운터 초기화

        # 날짜 마지막 행은 무조건 청산
        trading_df.loc[len(trading_df) - 1, 'position'] = 'margin transaction'
        signal_results.append(trading_df)

    pred_with_position = pd.concat(signal_results, ignore_index=True)

    merged_df = pd.merge(stock_data, pred_with_position[['time', 'index', 'current_trend', 'real_trend', 'pred_trend', 'position']], 
                         on='time', how='left')
    
    position_col = merged_df['position'].copy()
    found_entry = False

    for i in range(len(position_col)):
        if pd.isna(position_col[i]): 
            if not found_entry:
                position_col[i] = 'No action'
            else:
                position_col[i] = 'holding'
        elif position_col[i] in ['short', 'long']:
            found_entry = True
            
        elif position_col[i] == 'margin transaction':
            found_entry = False
            
        elif position_col[i] == 'No action' and found_entry:
            position_col[i] = 'holding'

    merged_df['position'] = position_col

    output_dir = './Backtesting/trading/'
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, os.path.basename(pred_file_path))
    merged_df.to_csv(output_file, encoding='utf-8-sig', index=False)
    print(f"Trading simulation for {os.path.basename(pred_file_path)} completed successfully with 1-minute data.")