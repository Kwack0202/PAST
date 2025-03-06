from common_imports import *

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

# Drawdown 시각화 함수
def plot_drawdown_by_similarity(top_n, window_size, simulation_dir, plot_dir):
    pairs = [
        ('cosine', 'cosine_IOU_avg'),
        ('DIEM', 'DIEM_IOU_avg'),
        ('euclidean', 'euclidean_IOU_avg'),
        ('wasserstein', 'wasserstein_IOU_avg')
    ]
    
    for base_sim, iou_sim in pairs:
        plt.figure(figsize=(20, 12))
        
        # 유사도 쌍 플롯만 포함
        for sim_type in (base_sim, iou_sim):
            file = f'{top_n}_{window_size}_future_{sim_type}_results.csv'
            file_path = f'{simulation_dir}/{file}'
            if os.path.exists(file_path):
                df = pd.read_csv(file_path)
                color, linestyle = similarity_pairs[sim_type]
                plt.plot(df.index, df['Drawdown_rate'], label=sim_type, 
                         color=color, linestyle=linestyle, linewidth=1.5)
                # 반투명 영역 채우기
                plt.fill_between(df.index, 0, df['Drawdown_rate'], 
                                 color=color, alpha=0.3)
        
        plt.title(f'Drawdown Rate - {base_sim} vs {iou_sim} (Top {top_n}, Window {window_size})')
        plt.xlabel('Index')
        plt.ylabel('Drawdown Rate (%)')
        plt.legend()
        plt.grid(True)
        
        output_dir = f'{plot_dir}/drawdown/by_similarity/top_{top_n}_window_{window_size}/'
        os.makedirs(output_dir, exist_ok=True)
        plt.savefig(f'{output_dir}/{base_sim}_vs_{iou_sim}.png')
        plt.close()