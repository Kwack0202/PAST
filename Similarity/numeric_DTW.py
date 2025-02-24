from common_imports import *

def numeric_DTW(save_root, data_path, sorted_files, start_idx):
    """숫자 데이터 DTW 유사도 계산 함수 (멀티프로세싱용, start_idx부터 끝까지 처리)"""
    os.makedirs(save_root, exist_ok=True)
    
    # 모든 파일의 데이터를 캐싱
    data_cache = {}
    for current_file in tqdm(sorted_files, desc="Caching numeric files"):
        parts = current_file.split('-')
        file_date_str = parts[1] + '-' + parts[2] + '-' + parts[3].replace('.csv', '')
        file_date = datetime.strptime(file_date_str, "%Y-%m-%d")
        
        df = pd.read_csv(os.path.join(data_path, current_file))
        close_data = df['close'].values
        
        data_cache[current_file] = {
            "date": file_date,
            "close": close_data
        }
    
    # start_idx부터 마지막 파일까지 처리
    for i in tqdm(range(start_idx, len(sorted_files)), desc=f'Calculating DTW similarity (from {start_idx} to end)'):
        try:
            current_file = sorted_files[i]
            current_close = data_cache[current_file]["close"]
            dtw_results = []
            
            # 과거 파일들과 비교 (0부터 i-1까지)
            for j in range(i):
                past_file = sorted_files[j]
                past_close = data_cache[past_file]["close"]
                
                # DTW 계산 (절대 차이를 거리 함수로 사용)
                distance, _ = fastdtw(current_close, past_close, dist=lambda x, y: abs(x - y))
                dtw_results.append({'csv_name': past_file, 'dtw_similarity': distance})
            
            # 결과 DataFrame 생성 및 정렬 후 저장
            if dtw_results:
                dtw_df = pd.DataFrame(dtw_results)
                dtw_df = dtw_df.sort_values(by='dtw_similarity', ascending=False)
                csv_path = os.path.join(save_root, current_file)
                dtw_df.to_csv(csv_path, index=False)
        
        except Exception as e:
            print(f"Error processing {current_file}: {e}")
            continue