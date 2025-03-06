from common_imports import *

from data.data_preprocessing import *

from Similarity.image_FE import *
from Similarity.image_similarity import *
from Similarity.image_bband import *
from Similarity.numeric_DTW import *
from Similarity.image_similarity_diem import *

from Backtesting.results_merge import *
from Backtesting.pred import *
from Backtesting.trading import *
from Backtesting.Buy_and_Hold import *
from Backtesting.simulation import *
from Backtesting.ploting import *
from Backtesting.ploting2 import *
from Backtesting.ploting3 import *


fix_seed = 42
random.seed(fix_seed)
np.random.seed(fix_seed)

# CPU 코어 수 설정 (전체 코어 - 1)
NUM_CORES = max(1, mp.cpu_count() - 3)

## ==================================================
parser = argparse.ArgumentParser(description="Stock Similarity")

## ==================================================
## basic config
## ==================================================
parser.add_argument("--task_name", type=str, required=True, default="pretrain", help="task name [options : data_download]")

## ==================================================
## step 1. data preprocessing (csv, image)
## ==================================================
parser.add_argument('--output_dir', type=str, default='./data/csv/', help='origin data directory')
parser.add_argument('--numeric_dir', type=str, default='./data/numeric_data/', help='origin data directory')
parser.add_argument('--candel_dir', type=str, default='./data/img_data/candle_img/', help='origin data directory')
parser.add_argument('--bband_dir', type=str, default='./data/img_data/bollinger_bands/', help='origin data directory')

parser.add_argument('--stock_csv', type=str, default='./data/csv/stock_data.csv', help='origin data directory')
parser.add_argument('--seq_len', type=int, default=60, help='origin data directory')
parser.add_argument('--window_len', type=int, default=5, help='origin data directory')
parser.add_argument('--future_points', type=int, nargs='+', default=[1, 2, 3, 6, 12], help='List of stock tickers')
parser.add_argument('--end_date', type=str, default='2025-01-01', help='origin data directory')

## ==================================================
## step 2. Feature Extraction & Similarity 
## ==================================================
parser.add_argument('--root_path', type=str, default='./img_data/candle_img/', help='origin data directory')
parser.add_argument('--save_root', type=str, default='./Similar_stock_data/Base_Feature_csv/', help='origin data directory')

parser.add_argument('--feature_pkl', type=str, default='./csv/1_origin_csv/IMG_vit_features.pkl', help='origin data directory')
parser.add_argument('--bollinger_img_path', type=str, default='img_data/bollinger_bands/ ', help='origin data directory')
parser.add_argument('--data_path', type=str, default='./data/numeric_data/', help='origin data directory')

parser.add_argument('--start_index', type=int, default=0, help='origin data directory')
parser.add_argument('--end_index', type=int, default=None, help='end index for processing (optional, defaults to total length)')

## ==================================================
## step 3. Backtesting 
## ==================================================
parser.add_argument('--merged_path', type=str, default='./Backtesting/results_merged/', help='merged similarity results directory')
parser.add_argument('--label_dir', type=str, default='./data/label/', help='label CSV directory')
parser.add_argument('--top_n_list', type=int, nargs='+', default=[1, 5, 10], help='list of top N values for prediction')

parser.add_argument('--pred_dir', type=str, default='./Backtesting/pred/', help='prediction CSV directory')
parser.add_argument('--opposite_count', type=int, default=2, help='number of opposite signals before margin transaction')

parser.add_argument('--stock_data_path', type=str, default='./data/origin_data/stock_data.csv', help='1-minute stock data directory')
parser.add_argument('--trading_dir', type=str, default='./Backtesting/trading/', help='trading CSV directory')

## ==================================================
## step 4. Visualization 
## ==================================================
parser.add_argument('--simulation_dir', type=str, default='./Backtesting/simulation/', help='simulation results directory')
parser.add_argument('--plot_dir', type=str, default='./Backtesting/plots/', help='plot output directory')

## ======================================================================================================================================================
# 헬퍼 함수 정의
def process_data_preprocessing(chunk):
    return data_preprocessing(*chunk)

def process_numeric_data(chunk):
    return numeric_data(*chunk)

def process_candlestick_image(chunk):
    return candlestick_image(*chunk)

def process_bollinger_band(chunk):
    return bollinger_band(*chunk)

def process_label_data(chunk):
    return label_data(*chunk)

def process_image_FE(chunk):
    return image_FE(*chunk)

def process_image_similarity(chunk):
    return image_similarity(*chunk)

def process_image_bband(chunk):
    return image_bband(*chunk)

def process_image_similarity_diem(chunk):
    return image_similarity_diem(*chunk)

def process_numeric_DTW(chunk):
    return numeric_DTW(*chunk)

def process_merge_csv(chunk):
    return merge_csv_files(*chunk)

def process_predict_trend(chunk):
    return predict_trend_single(*chunk)

def process_trading_simulation(chunk):
    return process_trading_signals(*chunk)

def process_plot_signals(chunk):
    plot_long_short_signals(*chunk)

def process_plot_returns(chunk):
    plot_margin_transaction_return(*chunk)

def process_plot_by_similarity(chunk):
    plot_by_similarity_type(*chunk)

def process_plot_by_top_n(chunk):
    plot_by_top_n(*chunk)

def process_plot_by_window_size(chunk):
    plot_by_window_size(*chunk)

def process_plot_drawdown(chunk):
    plot_drawdown_by_similarity(*chunk)
    
def main():
    args = parser.parse_args()

    ## ======================================================================================================================================================
    ## Data preparing
    
    # Step 1: Data Preprocessing
    if args.task_name == "data_preprocessing":
        data_preprocessing(args.output_dir)

    # Step 2: Numeric Data
    elif args.task_name == "numeric_data":   
        numeric_data(
            args.numeric_dir,
            args.stock_csv,
            args.seq_len,
            args.window_len,
            args.end_date,
        )
    
    # Step 3: Candlestick Image
    elif args.task_name == "candlestick_image":
        stock_data = pd.read_csv(args.stock_csv)
        trading_days = list(stock_data.groupby(stock_data['time'].dt.date))
        total_days = len(trading_days)
        
        if args.start_index >= total_days:
            raise ValueError(f"start_index {args.start_index} is larger than total days {total_days}")
        end_index = args.end_index if args.end_index is not None else total_days
        if end_index > total_days:
            end_index = total_days
        
        chunk_size = (end_index - args.start_index) // NUM_CORES
        chunk_args = []
        
        for i in range(NUM_CORES):
            start_idx = args.start_index + (i * chunk_size)
            end_idx = start_idx + chunk_size if i < NUM_CORES - 1 else end_index
            chunk_args.append((args.candel_dir, args.stock_csv, args.seq_len, args.window_len, args.end_date, start_idx, end_idx))
        
        with mp.Pool(processes=NUM_CORES) as pool:
            pool.map(process_candlestick_image, chunk_args)
    
    # Step 4: Bollinger Band Image
    elif args.task_name == "bollinger_band":
        stock_data = pd.read_csv(args.stock_csv)
        trading_days = list(stock_data.groupby(stock_data['time'].dt.date))
        total_days = len(trading_days)
        
        if args.start_index >= total_days:
            raise ValueError(f"start_index {args.start_index} is larger than total days {total_days}")
        end_index = args.end_index if args.end_index is not None else total_days
        if end_index > total_days:
            end_index = total_days
        
        chunk_size = (end_index - args.start_index) // NUM_CORES
        chunk_args = []
        
        for i in range(NUM_CORES):
            start_idx = args.start_index + (i * chunk_size)
            end_idx = start_idx + chunk_size if i < NUM_CORES - 1 else end_index
            chunk_args.append((args.bband_dir, args.stock_csv, args.seq_len, args.window_len, args.end_date, start_idx, end_idx))
        
        with mp.Pool(processes=NUM_CORES) as pool:
            pool.map(process_bollinger_band, chunk_args)
                        
    # Step 5: Label Data
    elif args.task_name == "label_data":
        label_data(
            args.output_dir,
            args.stock_csv,
            args.seq_len,
            args.window_len,
            args.future_points,
            args.end_date,
        )
                
    ## ======================================================================================================================================================    
    ## Similarity
    # Feature extraction 
    elif args.task_name == "image_FE":  
        with mp.Pool(processes=NUM_CORES) as pool:
            chunk_args = [(args.root_path,) for _ in range(NUM_CORES)]
            pool.map(process_image_FE, chunk_args)
    
    # Feature similarity
    elif args.task_name == "image_similarity":
        with open(args.feature_pkl, 'rb') as f:
            features = pickle.load(f)
        
        sorted_keys = sorted(features.keys(), key=lambda x: int(x.split('-')[0]))
        total_features = len(sorted_keys)
        
        if args.start_index >= total_features:
            raise ValueError(f"start_index {args.start_index} is larger than total features {total_features}")
        end_index = args.end_index if args.end_index is not None else total_features
        if end_index > total_features:
            end_index = total_features
        
        chunk_size = (end_index - args.start_index) // NUM_CORES
        chunk_args = []
        
        for i in range(NUM_CORES):
            start_idx = args.start_index + (i * chunk_size)
            end_idx = start_idx + chunk_size if i < NUM_CORES - 1 else end_index
            chunk_args.append((args.save_root, features, sorted_keys, start_idx, end_idx))
        
        with mp.Pool(processes=NUM_CORES) as pool:
            pool.map(process_image_similarity, chunk_args)

    # bollinger band area miou
    elif args.task_name == "image_bband":
        sorted_keys = sorted(os.listdir(args.bollinger_img_path), key=lambda x: pd.to_datetime('-'.join(x.split('-')[1:4]).replace('.png', ''), format='%Y-%m-%d'))
        total_features = len(sorted_keys)
        
        if args.start_index >= total_features:
            raise ValueError(f"start_index {args.start_index} is larger than total features {total_features}")
        end_index = args.end_index if args.end_index is not None else total_features
        if end_index > total_features:
            end_index = total_features
        
        chunk_size = (end_index - args.start_index) // NUM_CORES
        chunk_args = []
        
        for i in range(NUM_CORES):
            start_idx = args.start_index + (i * chunk_size)
            end_idx = start_idx + chunk_size if i < NUM_CORES - 1 else end_index
            chunk_args.append((args.save_root, args.bollinger_img_path, sorted_keys, start_idx, end_idx))
        
        with mp.Pool(processes=NUM_CORES) as pool:
            pool.map(process_image_bband, chunk_args)

    # Calculating DIEM score
    elif args.task_name == "image_similarity_diem":
        with open(args.feature_pkl, 'rb') as f:
            features = pickle.load(f)
        
        sorted_keys = sorted(features.keys(), key=lambda x: int(x.split('-')[0]))
        total_features = len(sorted_keys)
        
        if args.start_index >= total_features:
            raise ValueError(f"start_index {args.start_index} is larger than total features {total_features}")
        end_index = args.end_index if args.end_index is not None else total_features
        if end_index > total_features:
            end_index = total_features
        
        chunk_size = (end_index - args.start_index) // NUM_CORES
        chunk_args = []
        
        for i in range(NUM_CORES):
            start_idx = args.start_index + (i * chunk_size)
            end_idx = start_idx + chunk_size if i < NUM_CORES - 1 else end_index
            chunk_args.append((args.save_root, features, sorted_keys, start_idx, end_idx))
        
        with mp.Pool(processes=NUM_CORES) as pool:
            pool.map(process_image_similarity_diem, chunk_args)
        
    # calculating DTW score
    elif args.task_name == "numeric_DTW":
        files = [f for f in os.listdir(args.data_path) if f.endswith('.csv')]
        sorted_files = sorted(files, key=lambda x: int(x.split('-')[0]))
        total_files = len(sorted_files)
        
        if args.start_index >= total_files:
            raise ValueError(f"start_index {args.start_index} is larger than total files {total_files}")
        end_index = args.end_index if args.end_index is not None else total_files
        if end_index > total_files:
            end_index = total_files
        
        chunk_size = (end_index - args.start_index) // NUM_CORES
        chunk_args = []
        
        for i in range(NUM_CORES):
            start_idx = args.start_index + (i * chunk_size)
            end_idx = start_idx + chunk_size if i < NUM_CORES - 1 else end_index
            chunk_args.append((args.save_root, args.data_path, sorted_files, start_idx, end_idx))
        
        with mp.Pool(processes=NUM_CORES) as pool:
            pool.map(process_numeric_DTW, chunk_args)
    
    ## ======================================================================================================================================================
    ## Backtesting
    # results merge
    elif args.task_name == "merge_csv":
        data_path = args.data_path  
        sample_dir = os.path.join(data_path, os.listdir(data_path)[0])  
        total_files = len([f for f in os.listdir(sample_dir) if f.endswith('.csv')])
        
        if args.start_index >= total_files:
            raise ValueError(f"start_index {args.start_index} is larger than total files {total_files}")
        end_index = args.end_index if args.end_index is not None else total_files
        if end_index > total_files:
            end_index = total_files
        
        chunk_size = (end_index - args.start_index) // NUM_CORES
        chunk_args = []
        
        for i in range(NUM_CORES):
            start_idx = args.start_index + (i * chunk_size)
            end_idx = start_idx + chunk_size if i < NUM_CORES - 1 else end_index
            chunk_args.append(('./Backtesting/results_merged/', data_path, start_idx, end_idx))
        
        with mp.Pool(processes=NUM_CORES) as pool:
            pool.map(process_merge_csv, chunk_args)
    
    # predict           
    elif args.task_name == "predict_trend":
        files = [f for f in os.listdir(args.merged_path) if f.endswith('.csv')]
        sorted_files = sorted(files, key=lambda x: int(x.split('-')[0]))
        sample_file = pd.read_csv(os.path.join(args.merged_path, sorted_files[0]))
        similarity_cols = [col for col in sample_file.columns if col not in ['index']]

        tasks = [
            (args.merged_path, args.label_dir, args.stock_csv, top_n, args.seq_len, args.window_len, future_point, sim_col)
            for top_n in args.top_n_list
            for future_point in [5, 10, 15, 30, 60]  # pred.py에 명시된 future_points
            for sim_col in similarity_cols
        ]

        with mp.Pool(processes=NUM_CORES) as pool:
            pool.map(process_predict_trend, tasks)       
            
    # trading
    elif args.task_name == "trading":
        pred_files = [f for f in os.listdir(args.pred_dir) if f.endswith('.csv')]
        sorted_files = sorted(pred_files)
        total_files = len(sorted_files)
        if args.start_index >= total_files:
            raise ValueError(f"start_index {args.start_index} is larger than total files {total_files}")
        end_index = args.end_index if args.end_index is not None else total_files
        if end_index > total_files:
            end_index = total_files
        
        chunk_size = (end_index - args.start_index) // NUM_CORES
        chunk_args = []
        for i in range(NUM_CORES):
            start_idx = args.start_index + (i * chunk_size)
            end_idx = start_idx + chunk_size if i < NUM_CORES - 1 else end_index
            chunk_files = [os.path.join(args.pred_dir, sorted_files[idx]) for idx in range(start_idx, end_idx)]
            for file_path in chunk_files:
                # stock_data_path와 opposite_count를 인자로 전달
                chunk_args.append((file_path, args.stock_data_path, args.opposite_count))
        
        with mp.Pool(processes=NUM_CORES) as pool:
            pool.starmap(process_trading_signals, chunk_args)
        print("All trading simulations completed successfully with 1-minute data.")

    # buy&Hold
    elif args.task_name == "buy_and_hold":
        process_buy_and_hold(
            args.stock_data_path)
        
    # simulation
    elif args.task_name == "simulation":
        trading_files = [f.replace('.csv', '') for f in os.listdir(args.trading_dir) if f.endswith('.csv')]
        total_files = len(trading_files)
        
        if args.start_index >= total_files:
            raise ValueError(f"start_index {args.start_index} is larger than total files {total_files}")
        end_index = args.end_index if args.end_index is not None else total_files
        if end_index > total_files:
            end_index = total_files
        
        chunk_size = (end_index - args.start_index) // NUM_CORES
        chunk_args = []
        
        for i in range(NUM_CORES):
            start_idx = args.start_index + (i * chunk_size)
            end_idx = start_idx + chunk_size if i < NUM_CORES - 1 else end_index
            chunk_files = [trading_files[idx] for idx in range(start_idx, end_idx)]
            for file in chunk_files:
                chunk_args.append((file,))

        # Step 1: process_trading_data
        with mp.Pool(processes=NUM_CORES) as pool:
            pool.starmap(process_trading_data, chunk_args)

        # Step 2: summarize_results
        summarize_results(trading_files[args.start_index:end_index])
        print("All backtesting steps completed successfully.")
    
    # visualization - Long/Short Signals 시각화  
    elif args.task_name == "plot_signals":
        files = [f.replace('_results.csv', '') for f in os.listdir(args.simulation_dir) if f.endswith('_results.csv')]
        total_files = len(files)
        
        if total_files == 0:
            raise ValueError(f"No files found in {args.simulation_dir}")
        
        # 모든 파일을 대상으로 chunk 생성
        chunk_args = [(file, args.simulation_dir, args.plot_dir) for file in files]
        
        with mp.Pool(processes=NUM_CORES) as pool:
            pool.map(process_plot_signals, chunk_args)
        print(f"Long/Short signals plotted for {total_files} files.")

    # visualization - Margin Transaction Return 시각화
    elif args.task_name == "plot_returns":
        files = [f.replace('_results.csv', '') for f in os.listdir(args.simulation_dir) if f.endswith('_results.csv')]
        total_files = len(files)
        
        if total_files == 0:
            raise ValueError(f"No files found in {args.simulation_dir}")
        
        # 모든 파일을 대상으로 chunk 생성
        chunk_args = [(file, args.simulation_dir, args.plot_dir) for file in files]
        
        with mp.Pool(processes=NUM_CORES) as pool:
            pool.map(process_plot_returns, chunk_args)
        print(f"Margin transaction returns plotted for {total_files} files.")
    
    elif args.task_name == "plot_cumulative_profit":
        # top N과 window size 값 정의
        top_n_values = [1, 3, 5, 10, 20, 30, 50, 100, 200]
        window_sizes = [5, 10, 15, 30, 60]
        similarity_types = ['dtw_similarity', 'IOU', 'cosine', 'cosine_IOU_avg', 'DIEM', 'DIEM_IOU_avg', 
                            'euclidean', 'euclidean_IOU_avg', 'wasserstein', 'wasserstein_IOU_avg']

        # By Similarity Type
        chunk_args_similarity = [(top_n, window_size, args.simulation_dir, args.plot_dir) 
                                for top_n in top_n_values 
                                for window_size in window_sizes]
        with mp.Pool(processes=NUM_CORES) as pool:
            pool.map(process_plot_by_similarity, chunk_args_similarity)
        print(f"Cumulative profit by similarity type plotted for {len(chunk_args_similarity)} combinations.")

        # By Top N
        chunk_args_top_n = [(window_size, sim_type, args.simulation_dir, args.plot_dir) 
                            for window_size in window_sizes 
                            for sim_type in similarity_types]
        with mp.Pool(processes=NUM_CORES) as pool:
            pool.map(process_plot_by_top_n, chunk_args_top_n)
        print(f"Cumulative profit by top N plotted for {len(chunk_args_top_n)} combinations.")

        # By Window Size
        chunk_args_window_size = [(top_n, sim_type, args.simulation_dir, args.plot_dir) 
                                  for top_n in top_n_values 
                                  for sim_type in similarity_types]
        with mp.Pool(processes=NUM_CORES) as pool:
            pool.map(process_plot_by_window_size, chunk_args_window_size)
        print(f"Cumulative profit by window size plotted for {len(chunk_args_window_size)} combinations.")
    
    elif args.task_name == "plot_drawdown":
        # top N과 window size 값 정의
        top_n_values = [1, 3, 5, 10, 20, 30, 50, 100, 200]
        window_sizes = [5, 10, 15, 30, 60]

        # Drawdown 시각화 (모든 top N과 window size 조합)
        chunk_args_drawdown = [(top_n, window_size, args.simulation_dir, args.plot_dir) 
                               for top_n in top_n_values 
                               for window_size in window_sizes]
        with mp.Pool(processes=NUM_CORES) as pool:
            pool.map(process_plot_drawdown, chunk_args_drawdown)
        print(f"Drawdown plotted for {len(chunk_args_drawdown)} combinations.")
        
        
if __name__ == '__main__':
    main()