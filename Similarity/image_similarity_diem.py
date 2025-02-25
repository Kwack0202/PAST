from common_imports import *

def calculate_diem(vec1, vec2, v_min, v_max, expected_dist, variance):
    """DIEM 유사도 계산 함수"""
    vec1 = np.ravel(vec1)
    vec2 = np.ravel(vec2)
    euclidean_dist = np.sqrt(np.sum((vec1 - vec2) ** 2))
    diem = ((v_max - v_min) / variance) * (euclidean_dist - expected_dist)
    return diem

def image_similarity_diem(save_root, features_dict, sorted_keys, start_idx, end_idx):
    """DIEM 유사도 계산 함수 (멀티프로세싱용, 샘플링 크게 증가)"""
    os.makedirs(save_root, exist_ok=True)
    
    # 초기 최대/최소값 계산
    v_max = float('-inf')
    v_min = float('inf')
    for j in range(start_idx):
        features = features_dict[sorted_keys[j]]
        v_max = max(v_max, np.max(features))
        v_min = min(v_min, np.min(features))
    
    for i in tqdm(range(start_idx, end_idx), desc=f'Calculating DIEM similarity (from {start_idx} to {end_idx})'):
        try:
            current_image_key = sorted_keys[i]
            current_image_features = features_dict[current_image_key]
            similarity_data = []
            
            v_max = max(v_max, np.max(current_image_features))
            v_min = min(v_min, np.min(current_image_features))
            
            total_pairs = i * (i - 1) // 2
            sample_ratio = 0.05  # 5%로 증가
            sample_size = int(total_pairs * sample_ratio) if total_pairs > 0 else 0
            if total_pairs <= sample_size:
                sample_size = total_pairs
            
            # 샘플링 크기 조정
            distances_sum = 0
            distances_sq_sum = 0
            if sample_size > 0:
                n_indices = min(i, max(1, int(np.sqrt(sample_size) * 2)))
                sampled_indices = random.sample(range(i), n_indices)
                n_samples = 0
                for idx in sampled_indices:
                    for _ in range(min(20, idx)):  # 최대 20개 비교
                        jdx = random.randrange(idx)
                        dist = np.sqrt(np.sum((features_dict[sorted_keys[idx]] - features_dict[sorted_keys[jdx]]) ** 2))
                        distances_sum += dist
                        distances_sq_sum += dist ** 2
                        n_samples += 1
                
                expected_dist = distances_sum / n_samples if n_samples > 0 else 0
                variance = (distances_sq_sum / n_samples - expected_dist ** 2) if n_samples > 1 else 1
            else:
                expected_dist = 0
                variance = 1
            
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