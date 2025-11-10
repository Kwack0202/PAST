from common_imports import *
import matplotlib.dates as mdates  # 날짜 포맷팅을 위해 추가

plt.rcParams.update({
    'axes.titlesize': 30,    # 제목 폰트 크기
    'axes.labelsize': 30,    # Y축 레이블 폰트 크기 (metric 강조)
    'xtick.labelsize': 25,   # X축 눈금 레이블 폰트 크기
    'ytick.labelsize': 25,   # Y축 눈금 레이블 폰트 크기
    'legend.fontsize': 20    # 범례 폰트 크기
})

# 범례 이름 변환 함수
def format_legend_name(name):
    if name == 'Buy_and_hold_long_results':
        return 'Buy and Hold (Long)'
    elif name == 'Buy_and_hold_short_results':
        return 'Buy and Hold (Short)'
    elif name == 'dtw_similarity':
        return 'DTW'
    elif name == 'IOU':
        return 'IoU'
    elif '_IOU_avg' in name:
        base = name.replace('_IOU_avg', '+IoU')
        return base[0].upper() + base[1:]
    else:
        return name[0].upper() + name[1:]

# 키워드 추출 함수
def extract_keyword(file):
    # 파일 이름에서 '_results.csv' 제거
    file = file.replace('_results.csv', '')
    # 'future_' 이후의 부분 추출
    if 'future_' in file:
        return file.split('future_')[-1]
    return file

# 1. 거래 신호 시각화 (Long/Short/Margin) - X축을 날짜로
def plot_long_short_signals(file, base_dir='./Backtesting/simulation/', output_base='./Backtesting/plots/'):
    df = pd.read_csv(f'{base_dir}/{file}_results.csv')
    df['time'] = pd.to_datetime(df['time'])
    
    keyword = extract_keyword(file)  # 키워드 추출
    formatted_keyword = format_legend_name(keyword)  # 키워드 포맷팅
    output_dir = f'{output_base}/long_short_signal/{file}/'
    os.makedirs(output_dir, exist_ok=True)
    
    # 월별 시각화
    for month in range(1, 13):
        month_data = df[df['time'].dt.month <= month].reset_index(drop=True)
        if month_data.empty:
            continue
        
        plt.figure(figsize=(30, 15))
        long_signal = month_data[month_data['position'] == 'long']
        short_signal = month_data[month_data['position'] == 'short']
        margin_signal = month_data[month_data['position'] == 'margin transaction']
        
        # X축을 time으로 변경
        plt.plot(month_data['time'], month_data['close'], label='Closing Price', color='black', alpha=0.5)
        plt.scatter(long_signal['time'], long_signal['close'] * 0.999, label='Long Position', marker='^', color='r', s=50)
        plt.scatter(short_signal['time'], short_signal['close'] * 1.001, label='Short Position', marker='v', color='g', s=50)
        plt.scatter(margin_signal['time'], margin_signal['close'], label='Margin Trade', marker='o', color='b', s=50)
        
        plt.title(f'Long/Short Trading signals - {formatted_keyword}')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.grid(True)
        
        # X축 날짜 포맷 설정 (YYYY-MM)
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator())  # 월별 눈금
        plt.xticks() 
        
        plt.tight_layout()
        plt.savefig(f'{output_dir}/month_{month}.png', bbox_inches='tight')  # 레이블 잘림 방지
        plt.close()

# 2. Margin Transaction Return 시각화 - X축을 날짜로
def plot_margin_transaction_return(file, base_dir='./Backtesting/simulation/', output_base='./Backtesting/plots/'):
    df = pd.read_csv(f'{base_dir}/{file}_results.csv')
    df['time'] = pd.to_datetime(df['time'])
    
    keyword = extract_keyword(file)  # 키워드 추출
    formatted_keyword = format_legend_name(keyword)  # 키워드 포맷팅
    output_dir = f'{output_base}/margin_transaction_return/{file}/'
    os.makedirs(output_dir, exist_ok=True)

    # 월별 시각화
    for month in range(1, 13):
        month_data = df[df['time'].dt.month <= month].reset_index(drop=True)
        if month_data.empty:
            continue
        
        plt.figure(figsize=(30, 15))
        margin_data = month_data[month_data['position'] == 'margin transaction']
        marker_size = 1000 * abs(margin_data['Margin_Return'])
        colors = ['red' if x >= 0 else 'blue' for x in margin_data['Margin_Return']]
        
        plt.axhline(y=0, color='gray', linestyle='--')
        # X축을 time으로 변경
        plt.scatter(margin_data['time'], margin_data['Margin_Return'], s=marker_size, alpha=0.5, c=colors, label='Margin return')
        
        plt.title(f'Margin return - {formatted_keyword}')
        plt.xlabel('Date')
        plt.ylabel('Margin return (%)')
        plt.legend()
        
        # X축 날짜 포맷 설정 (YYYY-MM)
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator())  # 월별 눈금
        plt.xticks()
        
        plt.tight_layout()
        plt.savefig(f'{output_dir}/month_{month}.png', bbox_inches='tight')  # 레이블 잘림 방지
        plt.close()