from common_imports import *
import matplotlib.dates as mdates  # 날짜 포맷팅을 위해 추가

plt.rcParams.update({
    'axes.titlesize': 30,    # 제목 폰트 크기
    'axes.labelsize': 30,    # Y축 레이블 폰트 크기 (metric 강조)
    'xtick.labelsize': 25,   # X축 눈금 레이블 폰트 크기
    'ytick.labelsize': 25,   # Y축 눈금 레이블 폰트 크기
    'legend.fontsize': 20    # 범례 폰트 크기
})

# 색상 정의
benchmark_colors = {
    'Buy_and_hold_long_results': 'darkred',
    'Buy_and_hold_short_results': 'darkgreen'
}

# 유사도 쌍 색상 (중간 톤)
similarity_pairs = {
    'cosine': ('darkblue', '-'),  # 실선
    'cosine_IOU_avg': ('blue', '--'),  # 점선
    'DIEM': ('darkred', '-'),
    'DIEM_IOU_avg': ('red', '--'),
    'euclidean': ('darkgreen', '-'),
    'euclidean_IOU_avg': ('green', '--'),
    'wasserstein': ('darkorange', '-'),
    'wasserstein_IOU_avg': ('orange', '--')
}

# 범례 이름 변환 함수
def format_legend_name(name):
    if name == 'dtw_similarity':
        return 'DTW'
    elif name == 'IOU':
        return 'IoU'
    elif '_IOU_avg' in name:
        base = name.replace('_IOU_avg', '+IoU')
        return base[0].upper() + base[1:]
    else:
        return name[0].upper() + name[1:]

# Drawdown 시각화 함수 - 월별로 나눠서 시각화
def plot_drawdown_by_similarity(top_n, window_size, simulation_dir, plot_dir):
    pairs = [
        ('cosine', 'cosine_IOU_avg'),
        ('DIEM', 'DIEM_IOU_avg'),
        ('euclidean', 'euclidean_IOU_avg'),
        ('wasserstein', 'wasserstein_IOU_avg')
    ]
    
    # 데이터 사전 로드
    data_dict = {}
    for sim_type in similarity_pairs.keys():
        file = f'{top_n}_{window_size}_future_{sim_type}_results.csv'
        file_path = f'{simulation_dir}/{file}'
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            df['time'] = pd.to_datetime(df['time'])
            data_dict[sim_type] = df

    # 월별 시각화
    for base_sim, iou_sim in pairs:
        for month in range(1, 13):
            plt.figure(figsize=(30, 15))
            
            for sim_type in (base_sim, iou_sim):
                if sim_type in data_dict:
                    df = data_dict[sim_type]
                    month_data = df[df['time'].dt.month <= month].reset_index(drop=True)
                    if not month_data.empty:
                        color, linestyle = similarity_pairs[sim_type]
                        plt.plot(month_data['time'], month_data['Drawdown_rate'], 
                                 label=format_legend_name(sim_type), 
                                 color=color, linestyle=linestyle, linewidth=1.5)
                        plt.fill_between(month_data['time'], 0, month_data['Drawdown_rate'], 
                                         color=color, alpha=0.3)
            
            plt.title(f'Drawdown - {format_legend_name(base_sim)} vs {format_legend_name(iou_sim)} (Top {top_n}, Window {window_size})')
            plt.xlabel('Date')
            plt.ylabel('Drawdown (%)')
            plt.legend()
            plt.grid(True)
            
            # X축 날짜 포맷 설정 (YYYY-MM)
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
            plt.gca().xaxis.set_major_locator(mdates.MonthLocator())  # 월별 눈금
            plt.xticks()
            
            plt.tight_layout()
            output_dir = f'{plot_dir}/drawdown/by_similarity/top_{top_n}_window_{window_size}/{base_sim}_vs_{iou_sim}/'
            os.makedirs(output_dir, exist_ok=True)
            plt.savefig(f'{output_dir}/month_{month}.png', bbox_inches='tight')
            plt.close()