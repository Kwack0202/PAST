from common_imports import *
import numpy as np

def calculate_diem(vec1, vec2, v_min, v_max, expected_dist, variance):
    """DIEM 유사도 계산 함수"""
    vec1 = np.ravel(vec1)
    vec2 = np.ravel(vec2)
    
    # 유클리드 거리 계산
    euclidean_dist = np.sqrt(np.sum((vec1 - vec2) ** 2))
    
    # DIEM 계산
    diem = ((v_max - v_min) / variance) * (euclidean_dist - expected_dist)
    return diem

def image_similarity_diem(save_root, features_dict, sorted_keys, start_idx, end_idx):
    """DIEM 유사도 계산 함수 (멀티프로세싱용, start_idx부터 end_idx까지 처리)"""
    os.makedirs(save_root, exist_ok=True)
    
    # 데이터셋의 최대/최소값 및 통계값 계산
    all_features = np.array([features_dict[key] for key in sorted_keys])
    v_max = np.max(all_features)
    v_min = np.min(all_features)
    
    # 유클리드 거리의 기대값과 분산 추정
    distances = []
    for i in range(len(sorted_keys)):
        for j in range(i):
            dist = np.sqrt(np.sum((features_dict[sorted_keys[i]] - features_dict[sorted_keys[j]]) ** 2))
            distances.append(dist)
    expected_dist = np.mean(distances) if distances else 0
    variance = np.var(distances) if distances else 1  # 분산이 0이면 기본값 1
    
    # start_idx부터 end_idx까지 처리
    for i in tqdm(range(start_idx, end_idx), desc=f'Calculating DIEM similarity (from {start_idx} to {end_idx})'):
        try:
            current_image_key = sorted_keys[i]
            current_image_features = features_dict[current_image_key]
            similarity_data = []
            
            # 과거 이미지들과 비교 (0부터 i-1까지)
            for j in range(i):
                compare_image_key = sorted_keys[j]
                compare_image_features = features_dict[compare_image_key]
                diem_value = calculate_diem(
                    current_image_features, compare_image_features, 
                    v_min, v_max, expected_dist, variance
                )
                similarity_data.append({'Image': compare_image_key, 'DIEM': diem_value})
            
            if similarity_data:
                similar_images_df = pd.DataFrame(similarity_data)
                csv_filename = f"{current_image_key.split('.')[0]}.csv"
                csv_path = os.path.join(save_root, csv_filename)
                similar_images_df.to_csv(csv_path, index=False)
        
        except Exception as e:
            print(f"Error processing {current_image_key}: {e}")
            continue