from common_imports import *

# 색상 정의
benchmark_colors = {
    'Buy_and_hold_long_results': 'lightcoral',  # 연한 빨강
    'Buy_and_hold_short_results': 'lightgreen'  # 연한 초록
}

# 유사도 종류 색상 (metric은 연하게, IOU는 진하게)
similarity_colors = {
    'dtw_similarity': 'violet',     # metric: 연한 파랑
    'IOU': 'pink',                     # IOU: 진한 파랑

    'cosine': 'darkblue',                  # metric: 연한 분홍
    'cosine_IOU_avg': 'blue',           # IOU: 진한 분홍

    'DIEM': 'darkred',               # metric: 연한 녹색
    'DIEM_IOU_avg': 'red',           # IOU: 진한 녹색

    'euclidean': 'darkgreen',        # metric: 연한 노랑
    'euclidean_IOU_avg': 'green',       # IOU: 진한 노랑

    'wasserstein': 'darkorange',            # metric: 연한 베이지
    'wasserstein_IOU_avg': 'orange'    # IOU: 진한 주황
}


top_n_palette = sns.color_palette("tab10", 9)  # 9가지 색상 팔레트
top_n_values = [1, 3, 5, 10, 20, 30, 50, 100, 200]
top_n_color_map = dict(zip(top_n_values, top_n_palette))

window_size_palette = sns.color_palette("Set2", 5)  # 5가지 색상 팔레트
window_sizes = [5, 10, 15, 30, 60]
window_size_color_map = dict(zip(window_sizes, window_size_palette))

# 유사도 종류별 시각화
def plot_by_similarity_type(top_n, window_size, simulation_dir, plot_dir):
    plt.figure(figsize=(20, 12))
    
    # 벤치마크 플롯 (연하고 얇게)
    for bench_file in benchmark_colors.keys():
        file_path = f'{simulation_dir}/{bench_file}.csv'
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            plt.plot(df.index, df['Cumulative_Profit'], label=bench_file, 
                     color=benchmark_colors[bench_file], linewidth=1, alpha=0.7)
    
    # 유사도 종류별 플롯 (진한/연한 색상 구분)
    for sim_type in similarity_colors.keys():
        file = f'{top_n}_{window_size}_future_{sim_type}_results.csv'
        file_path = f'{simulation_dir}/{file}'
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            plt.plot(df.index, df['Cumulative_Profit'], label=sim_type, 
                     color=similarity_colors[sim_type], linewidth=1.5)
    
    plt.title(f'Cumulative Profit by Similarity Type - Top {top_n}, Window {window_size}')
    plt.xlabel('Index')
    plt.ylabel('Cumulative Profit')
    plt.legend()
    plt.grid(True)
    
    output_dir = f'{plot_dir}/cumulative_profit/by_similarity_type/'
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(f'{output_dir}/top_{top_n}_window_{window_size}.png')
    plt.close()

# top N별 시각화
def plot_by_top_n(window_size, sim_type, simulation_dir, plot_dir):
    plt.figure(figsize=(20, 12))
    
    # 벤치마크 플롯 (연하고 얇게)
    for bench_file in benchmark_colors.keys():
        file_path = f'{simulation_dir}/{bench_file}.csv'
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            plt.plot(df.index, df['Cumulative_Profit'], label=bench_file, 
                     color=benchmark_colors[bench_file], linewidth=1, alpha=0.7)
    
    # top N별 플롯 (팔레트 기반 색상)
    for top_n in top_n_values:
        file = f'{top_n}_{window_size}_future_{sim_type}_results.csv'
        file_path = f'{simulation_dir}/{file}'
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            plt.plot(df.index, df['Cumulative_Profit'], label=f'top_{top_n}', 
                     color=top_n_color_map[top_n], linewidth=1.5, alpha=0.9)
    
    plt.title(f'Cumulative Profit by Top N - Window {window_size}, {sim_type}')
    plt.xlabel('Index')
    plt.ylabel('Cumulative Profit')
    plt.legend()
    plt.grid(True)
    
    output_dir = f'{plot_dir}/cumulative_profit/by_top_n/'
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(f'{output_dir}/window_{window_size}_{sim_type}.png')
    plt.close()

# 윈도우 사이즈별 시각화
def plot_by_window_size(top_n, sim_type, simulation_dir, plot_dir):
    plt.figure(figsize=(20, 12))
    
    # 벤치마크 플롯 (연하고 얇게)
    for bench_file in benchmark_colors.keys():
        file_path = f'{simulation_dir}/{bench_file}.csv'
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            plt.plot(df.index, df['Cumulative_Profit'], label=bench_file, 
                     color=benchmark_colors[bench_file], linewidth=1, alpha=0.7)
    
    # 윈도우 사이즈별 플롯 (팔레트 기반 색상)
    for window_size in window_sizes:
        file = f'{top_n}_{window_size}_future_{sim_type}_results.csv'
        file_path = f'{simulation_dir}/{file}'
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            plt.plot(df.index, df['Cumulative_Profit'], label=f'window_{window_size}', 
                     color=window_size_color_map[window_size], linewidth=1.5, alpha=0.9)
    
    plt.title(f'Cumulative Profit by Window Size - Top {top_n}, {sim_type}')
    plt.xlabel('Index')
    plt.ylabel('Cumulative Profit')
    plt.legend()
    plt.grid(True)
    
    output_dir = f'{plot_dir}/cumulative_profit/by_window_size/'
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(f'{output_dir}/top_{top_n}_{sim_type}.png')
    plt.close()