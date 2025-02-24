from common_imports import *

def image_bband(save_root, bollinger_img_path, sorted_keys, start_idx, end_idx):
    os.makedirs(save_root, exist_ok=True)
    
    image_cache = {key: read_image(os.path.join(bollinger_img_path, key)) for key in sorted_keys}
    
    for i in tqdm(range(start_idx, end_idx), desc=f'Calculating Bollinger Band IOU (from {start_idx} to {end_idx})'):
        try:
            current_image_key = sorted_keys[i]
            current_image_mask = image_cache[current_image_key]
            bollinger_bands_ious = []
            
            for j in range(i):
                compare_image_key = sorted_keys[j]
                compare_image_mask = image_cache[compare_image_key]
                
                iou = calculate_miou(current_image_mask, compare_image_mask)
                bollinger_bands_ious.append((compare_image_key, iou))
            
            if bollinger_bands_ious:
                bollinger_bands_ious.sort(key=lambda x: x[1], reverse=True)
                iou_df = pd.DataFrame(bollinger_bands_ious, columns=['Image', 'IOU'])
                csv_filename = f"{current_image_key.split('.')[0]}.csv"
                csv_path = os.path.join(save_root, csv_filename)
                iou_df.to_csv(csv_path, index=False)
        
        except Exception as e:
            print(f"Error processing {current_image_key}: {e}")
            continue

def read_image(image_path):
    return cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

def calculate_miou(target_image, comparison_image):
    intersection = np.logical_and(target_image, comparison_image)
    union = np.logical_or(target_image, comparison_image)
    miou = np.sum(intersection) / np.sum(union) if np.sum(union) > 0 else 0
    return miou