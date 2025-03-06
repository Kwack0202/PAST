from common_imports import *

def calculate_similarity(metric, vec1, vec2):
    vec1 = np.ravel(vec1)
    vec2 = np.ravel(vec2)
    
    if metric == 'cosine':
        return cosine_similarity([vec1], [vec2])[0][0]
    elif metric == 'euclidean':
        return 1 / (1 + euclidean(vec1, vec2))
    elif metric == 'manhattan':
        return 1 / (1 + cityblock(vec1, vec2))
    elif metric == 'chebyshev':
        return 1 / (1 + chebyshev(vec1, vec2))
    elif metric == 'minkowski':
        return 1 / (1 + minkowski(vec1, vec2, 3))
    elif metric == 'canberra':
        return 1 / (1 + canberra(vec1, vec2))
    elif metric == 'braycurtis':
        return 1 / (1 + braycurtis(vec1, vec2))
    elif metric == 'wasserstein':
        return 1 / (1 + wasserstein_distance(vec1, vec2))
    else:
        raise ValueError(f"Unknown similarity metric: {metric}")

def image_similarity(save_root, features_dict, sorted_keys, start_idx, end_idx):
    os.makedirs(save_root, exist_ok=True)
    similarity_metrics = ['cosine', 'euclidean', 'wasserstein',  
                          # 'manhattan', 'chebyshev', 'minkowski', 'canberra', 'braycurtis'
                          ]
    
    for i in tqdm(range(start_idx, end_idx), desc=f'Calculating image similarity (from {start_idx} to {end_idx})'):
        try:
            current_image_key = sorted_keys[i]
            current_image_features = features_dict[current_image_key]
            similarity_data = []
            
            for j in range(i):
                compare_image_key = sorted_keys[j]
                compare_image_features = features_dict[compare_image_key]
                row = {'Image': compare_image_key}
                for metric in similarity_metrics:
                    row[metric] = calculate_similarity(metric, current_image_features, compare_image_features)
                similarity_data.append(row)
            
            if similarity_data:
                similar_images_df = pd.DataFrame(similarity_data)
                csv_filename = f"{current_image_key.split('.')[0]}.csv"
                csv_path = os.path.join(save_root, csv_filename)
                similar_images_df.to_csv(csv_path, index=False)
        
        except Exception as e:
            print(f"Error processing {current_image_key}: {e}")
            continue