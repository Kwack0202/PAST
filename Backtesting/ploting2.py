from common_imports import *  # pandas, matplotlib.pyplot, os, seaborn(sns) 등이 포함되어 있다고 가정

# 색상 정의
benchmark_colors = {
    'Buy_and_hold_long_results': 'lightcoral',  # 연한 빨강
    'Buy_and_hold_short_results': 'lightgreen'  # 연한 초록
}

similarity_colors = {
    'dtw_similarity': 'violet',     # metric: 연한 보라
    'IOU': 'pink',                  # IOU: 분홍
    'cosine': 'darkblue',           # metric: 진한 파랑
    'cosine_IOU_avg': 'blue',       # IOU: 파랑
    'DIEM': 'darkred',              # metric: 진한 빨강
    'DIEM_IOU_avg': 'red',          # IOU: 빨강
    'euclidean': 'darkgreen',       # metric: 진한 초록
    'euclidean_IOU_avg': 'green',   # IOU: 초록
    'wasserstein': 'darkorange',    # metric: 진한 주황
    'wasserstein_IOU_avg': 'orange' # IOU: 주황
}

top_n_palette = sns.color_palette("tab10", 9)  # 9가지 색상 팔레트
top_n_values = [1, 3, 5, 10, 20, 30, 50, 100, 200]
top_n_color_map = dict(zip(top_n_values, top_n_palette))

window_size_palette = sns.color_palette("Set2", 5)  # 5가지 색상 팔레트
window_sizes = [5, 10, 15, 30, 60]
window_size_color_map = dict(zip(window_sizes, window_size_palette))

# 1. 유사도 종류별 시각화 (월별 누적)
def plot_by_similarity_type(top_n, window_size, simulation_dir, plot_dir):
    # 데이터 사전 로드
    data_dict = {}
    for bench_file in benchmark_colors.keys():
        file_path = f'{simulation_dir}/{bench_file}.csv'
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            df['time'] = pd.to_datetime(df['time'])
            data_dict[bench_file] = df
    
    for sim_type in similarity_colors.keys():
        file = f'{top_n}_{window_size}_future_{sim_type}_results.csv'
        file_path = f'{simulation_dir}/{file}'
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            df['time'] = pd.to_datetime(df['time'])
            data_dict[sim_type] = df
    
    # 1월부터 12월까지 누적 플롯
    for month in range(1, 13):
        plt.figure(figsize=(20, 12))
        
        # 벤치마크 플롯 (누적 데이터)
        for bench_file in benchmark_colors.keys():
            if bench_file in data_dict:
                df = data_dict[bench_file]
                cumulative_df = df[df['time'].dt.month <= month].reset_index(drop=True)
                if not cumulative_df.empty:
                    plt.plot(cumulative_df.index, cumulative_df['Cumulative_Profit'], 
                             label=bench_file, color=benchmark_colors[bench_file], 
                             linewidth=1, alpha=0.7)
        
        # 유사도 종류별 플롯 (누적 데이터)
        for sim_type in similarity_colors.keys():
            if sim_type in data_dict:
                df = data_dict[sim_type]
                cumulative_df = df[df['time'].dt.month <= month].reset_index(drop=True)
                if not cumulative_df.empty:
                    plt.plot(cumulative_df.index, cumulative_df['Cumulative_Profit'], 
                             label=sim_type, color=similarity_colors[sim_type], 
                             linewidth=1.5)
        
        plt.title(f'Cumulative Profit by Similarity Type - Top {top_n}, Window {window_size} (Up to Month {month})')
        plt.xlabel('Index')
        plt.ylabel('Cumulative Profit')
        plt.legend()
        plt.grid(True)
        
        output_dir = f'{plot_dir}/cumulative_profit/by_similarity_type/top_{top_n}_window_{window_size}/'
        os.makedirs(output_dir, exist_ok=True)
        plt.savefig(f'{output_dir}/month_{month}.png')
        plt.close()

# 2. top N별 시각화 (월별 누적)
def plot_by_top_n(window_size, sim_type, simulation_dir, plot_dir):
    # 데이터 사전 로드
    data_dict = {}
    for bench_file in benchmark_colors.keys():
        file_path = f'{simulation_dir}/{bench_file}.csv'
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            df['time'] = pd.to_datetime(df['time'])
            data_dict[bench_file] = df
    
    for top_n in top_n_values:
        file = f'{top_n}_{window_size}_future_{sim_type}_results.csv'
        file_path = f'{simulation_dir}/{file}'
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            df['time'] = pd.to_datetime(df['time'])
            data_dict[top_n] = df
    
    # 1월부터 12월까지 누적 플롯
    for month in range(1, 13):
        plt.figure(figsize=(20, 12))
        
        # 벤치마크 플롯 (누적 데이터)
        for bench_file in benchmark_colors.keys():
            if bench_file in data_dict:
                df = data_dict[bench_file]
                cumulative_df = df[df['time'].dt.month <= month].reset_index(drop=True)
                if not cumulative_df.empty:
                    plt.plot(cumulative_df.index, cumulative_df['Cumulative_Profit'], 
                             label=bench_file, color=benchmark_colors[bench_file], 
                             linewidth=1, alpha=0.7)
        
        # top N별 플롯 (누적 데이터)
        for top_n in top_n_values:
            if top_n in data_dict:
                df = data_dict[top_n]
                cumulative_df = df[df['time'].dt.month <= month].reset_index(drop=True)
                if not cumulative_df.empty:
                    plt.plot(cumulative_df.index, cumulative_df['Cumulative_Profit'], 
                             label=f'top_{top_n}', color=top_n_color_map[top_n], 
                             linewidth=1.5, alpha=0.9)
        
        plt.title(f'Cumulative Profit by Top N - Window {window_size}, {sim_type} (Up to Month {month})')
        plt.xlabel('Index')
        plt.ylabel('Cumulative Profit')
        plt.legend()
        plt.grid(True)
        
        output_dir = f'{plot_dir}/cumulative_profit/by_top_n/window_{window_size}_{sim_type}/'
        os.makedirs(output_dir, exist_ok=True)
        plt.savefig(f'{output_dir}/month_{month}.png')
        plt.close()

# 3. 윈도우 사이즈별 시각화 (월별 누적)
def plot_by_window_size(top_n, sim_type, simulation_dir, plot_dir):
    # 데이터 사전 로드
    data_dict = {}
    for bench_file in benchmark_colors.keys():
        file_path = f'{simulation_dir}/{bench_file}.csv'
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            df['time'] = pd.to_datetime(df['time'])
            data_dict[bench_file] = df
    
    for window_size in window_sizes:
        file = f'{top_n}_{window_size}_future_{sim_type}_results.csv'
        file_path = f'{simulation_dir}/{file}'
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            df['time'] = pd.to_datetime(df['time'])
            data_dict[window_size] = df
    
    # 1월부터 12월까지 누적 플롯
    for month in range(1, 13):
        plt.figure(figsize=(20, 12))
        
        # 벤치마크 플롯 (누적 데이터)
        for bench_file in benchmark_colors.keys():
            if bench_file in data_dict:
                df = data_dict[bench_file]
                cumulative_df = df[df['time'].dt.month <= month].reset_index(drop=True)
                if not cumulative_df.empty:
                    plt.plot(cumulative_df.index, cumulative_df['Cumulative_Profit'], 
                             label=bench_file, color=benchmark_colors[bench_file], 
                             linewidth=1, alpha=0.7)
        
        # 윈도우 사이즈별 플롯 (누적 데이터)
        for window_size in window_sizes:
            if window_size in data_dict:
                df = data_dict[window_size]
                cumulative_df = df[df['time'].dt.month <= month].reset_index(drop=True)
                if not cumulative_df.empty:
                    plt.plot(cumulative_df.index, cumulative_df['Cumulative_Profit'], 
                             label=f'window_{window_size}', color=window_size_color_map[window_size], 
                             linewidth=1.5, alpha=0.9)
        
        plt.title(f'Cumulative Profit by Window Size - Top {top_n}, {sim_type} (Up to Month {month})')
        plt.xlabel('Index')
        plt.ylabel('Cumulative Profit')
        plt.legend()
        plt.grid(True)
        
        output_dir = f'{plot_dir}/cumulative_profit/by_window_size/top_{top_n}_{sim_type}/'
        os.makedirs(output_dir, exist_ok=True)
        plt.savefig(f'{output_dir}/month_{month}.png')
        plt.close()