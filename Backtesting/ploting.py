from common_imports import *

# 1. 거래 신호 시각화 (Long/Short/Margin) - x축을 index로
def plot_long_short_signals(file, base_dir='./Backtesting/simulation/', output_base='./Backtesting/plots/'):
    df = pd.read_csv(f'{base_dir}/{file}_results.csv')
    df['time'] = pd.to_datetime(df['time'])
    
    output_dir = f'{output_base}/long_short_signal/{file}/'
    os.makedirs(output_dir, exist_ok=True)
    
    # 월별 시각화
    for month in range(1, 13):
        month_data = df[df['time'].dt.month <= month].reset_index(drop=True)
        if month_data.empty:
            continue
        
        plt.figure(figsize=(20, 12))
        long_signal = month_data[month_data['position'] == 'long']
        short_signal = month_data[month_data['position'] == 'short']
        margin_signal = month_data[month_data['position'] == 'margin transaction']
        
        plt.plot(month_data.index, month_data['close'], label='Close', color='black', alpha=0.5)
        plt.scatter(long_signal.index, long_signal['close'] * 0.999, label='Long', marker='^', color='r', s=50)
        plt.scatter(short_signal.index, short_signal['close'] * 1.001, label='Short', marker='v', color='g', s=50)
        plt.scatter(margin_signal.index, margin_signal['close'], label='Margin Transaction', marker='o', color='b', s=50)
        
        plt.title(f'Long/Short Signals - {file} - Month {month}')
        plt.xlabel('Index')
        plt.ylabel('Price')
        plt.legend()
        plt.grid(True)
        
        plt.savefig(f'{output_dir}/month_{month}.png')
        plt.close()

# 2. Margin Transaction Return 시각화 - x축을 index로
def plot_margin_transaction_return(file, base_dir='./Backtesting/simulation/', output_base='./Backtesting/plots/'):
    df = pd.read_csv(f'{base_dir}/{file}_results.csv')
    df['time'] = pd.to_datetime(df['time'])
    
    output_dir = f'{output_base}/margin_transaction_return/{file}/'
    os.makedirs(output_dir, exist_ok=True)

    # 월별 시각화
    for month in range(1, 13):
        month_data = df[df['time'].dt.month <= month].reset_index(drop=True)
        if month_data.empty:
            continue
        
        plt.figure(figsize=(20, 12))
        margin_data = month_data[month_data['position'] == 'margin transaction']
        marker_size = 1000 * abs(margin_data['Margin_Return'])
        colors = ['red' if x >= 0 else 'blue' for x in margin_data['Margin_Return']]
        
        plt.axhline(y=0, color='gray', linestyle='--')
        plt.scatter(margin_data.index, margin_data['Margin_Return'], s=marker_size, alpha=0.5, c=colors, label='Margin Transaction Return')
        
        plt.title(f'Margin Transaction Return - {file} - Month {month}')
        plt.xlabel('Index')
        plt.ylabel('Margin Return (%)')
        plt.legend()
        
        plt.savefig(f'{output_dir}/month_{month}.png')
        plt.close()
        