from common_imports import *

def process_buy_and_hold(stock_data_path='./data/origin_data/stock_data.csv'):
    for target_dir in ['long', 'short']:
        buy_and_hold_df = pd.read_csv(stock_data_path)
        buy_and_hold_df = buy_and_hold_df[buy_and_hold_df['time'] >= '2024-01-01'].reset_index(drop=True)
        buy_and_hold_df = buy_and_hold_df[['time', 'open', 'high', 'low', 'close', 'volume']]
        
        signal_results = []

        # 날짜별 매매 신호 생성을 위해 데이터를 분할하여 리스트로 저장
        buy_and_hold_df['time'] = pd.to_datetime(buy_and_hold_df['time'])
        trading_days = list(buy_and_hold_df.groupby(buy_and_hold_df['time'].dt.date))

        for trading_day in tqdm(range(len(trading_days))):
            date, group = trading_days[trading_day]
            
            # position 컬럼 초기화
            trading_df = group.reset_index(drop=True).copy()  # 명시적으로 복사본 생성
            
            # position 컬럼 생성
            trading_df['position'] = 'holding'

            # 첫 행의 값 설정
            trading_df.at[0, 'position'] = target_dir

            # 마지막 행의 값 설정
            trading_df.at[trading_df.index[-1], 'position'] = 'margin transaction'

            # 각 날짜별 데이터프레임을 리스트에 추가
            signal_results.append(trading_df)

        # 모든 날짜의 데이터를 하나의 데이터프레임으로 병합
        trading_df = pd.concat(signal_results, ignore_index=True)
        
        output_dir = './Backtesting/trading/'
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir + f'Buy_and_hold_{target_dir}.csv')
        trading_df.to_csv(output_file, encoding='utf-8-sig', index=False)