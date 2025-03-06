from common_imports import *

def merge_csv_files(save_root, data_path, start_idx, end_idx):
    """./results/ 경로 내 하위 폴더의 동일한 이름 CSV 파일을 병합하여 index 기반으로 저장"""
    os.makedirs(save_root, exist_ok=True)
    
    # ./results/ 내 모든 하위 폴더 목록 수집
    input_dirs = [d for d in os.listdir(data_path) if os.path.isdir(os.path.join(data_path, d))]
    all_files = {}
    
    # 각 하위 폴더에서 CSV 파일 목록 수집
    for dir_name in input_dirs:
        dir_path = os.path.join(data_path, dir_name)
        files = [f for f in os.listdir(dir_path) if f.endswith('.csv')]
        all_files[dir_name] = sorted(files)
    
    # 동일한 파일 이름 확인
    common_files = set(all_files[input_dirs[0]])
    for dir_name in input_dirs[1:]:
        common_files.intersection_update(all_files[dir_name])
    common_files = sorted(list(common_files))
    
    # 청크 범위 내 파일만 처리
    chunk_files = common_files[start_idx:end_idx]
    
    for filename in tqdm(chunk_files, desc=f'Merging CSV files (from {start_idx} to {end_idx})'):
        try:
            merged_data = None
            
            # 각 폴더에서 동일한 파일 병합
            for dir_name in input_dirs:
                file_path = os.path.join(data_path, dir_name, filename)
                df = pd.read_csv(file_path)
                
                # index 추출
                if 'Image' in df.columns:
                    df['index'] = df['Image'].apply(lambda x: int(x.split('-')[0]))
                    df = df.drop(columns=['Image'])
                elif 'csv_name' in df.columns:
                    df['index'] = df['csv_name'].apply(lambda x: int(x.split('-')[0]))
                    df = df.drop(columns=['csv_name'])
                
                # 병합
                if merged_data is None:
                    merged_data = df
                else:
                    merged_data = pd.merge(merged_data, df, on='index', how='inner')
            
            # 유사도 값 정규화 (0~1)
            similarity_cols = [col for col in merged_data.columns if col != 'index']
            for col in similarity_cols:
                if col == 'DIEM':
                    # DIEM: 음수일수록 유사 -> 양수로 변환 후 정규화
                    max_val = merged_data[col].max()
                    min_val = merged_data[col].min()
                    if max_val == min_val:  # 동일 값일 경우
                        merged_data[col] = 1.0
                    else:
                        # 음수 -> 양수 변환 (최대값에서 뺌)
                        merged_data[col] = max_val - merged_data[col]
                        # 0~1 정규화
                        merged_data[col] = (merged_data[col] - merged_data[col].min()) / (merged_data[col].max() - merged_data[col].min())
                else:
                    # 다른 유사도 컬럼: 이미 양수이므로 직접 정규화
                    max_val = merged_data[col].max()
                    min_val = merged_data[col].min()
                    if max_val == min_val:
                        merged_data[col] = 1.0
                    else:
                        merged_data[col] = (merged_data[col] - min_val) / (max_val - min_val)
            
            # 이미지 피처 유사도 + IOU 평균 계산
            image_similarity_cols = [col for col in merged_data.columns if col not in ['index', 'dtw_similarity']]
            if 'IOU' in merged_data.columns:
                for col in image_similarity_cols:
                    if col != 'IOU':  # IOU 자기 자신 제외
                        avg_col_name = f"{col}_IOU_avg"
                        merged_data[avg_col_name] = (merged_data[col] + merged_data['IOU']) / 2
            
            # index를 첫 번째 컬럼으로, 오름차순 정렬
            merged_data = merged_data.sort_values(by='index')
            columns = ['index'] + [col for col in merged_data.columns if col != 'index']
            merged_data = merged_data[columns]
            
            # 저장
            output_path = os.path.join(save_root, filename)
            merged_data.to_csv(output_path, index=False)
        
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            continue