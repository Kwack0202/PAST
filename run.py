from common_imports import *
from data.data_preprocessing import *
from Similarity.image_FE import *
from Similarity.image_similarity import *
from Similarity.image_bband import *
from Similarity.numeric_DTW import *
from Similarity.image_similarity_diem import *
import multiprocessing as mp

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
## step 2. Feature Extraction 
## ==================================================
parser.add_argument('--root_path', type=str, default='./img_data/candle_img/', help='origin data directory')
parser.add_argument('--save_root', type=str, default='./Similar_stock_data/Base_Feature_csv/', help='origin data directory')

parser.add_argument('--feature_pkl', type=str, default='./csv/1_origin_csv/IMG_vit_features.pkl', help='origin data directory')
parser.add_argument('--bollinger_img_path', type=str, default='img_data/bollinger_bands/ ', help='origin data directory')
parser.add_argument('--data_path', type=str, default='./data/numeric_data/', help='origin data directory')


parser.add_argument('--start_index', type=int, default=0, help='origin data directory')
parser.add_argument('--end_index', type=int, default=None, help='end index for processing (optional, defaults to total length)')

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
            
if __name__ == '__main__':
    main()