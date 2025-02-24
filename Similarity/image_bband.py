from common_imports import *

def image_bband(save_root, bollinger_img_path, sorted_keys, start_idx, end_idx):
    """볼린저 밴드 이미지 IOU 계산 함수 (멀티프로세싱용, start_idx부터 end_idx까지 처리)"""
    os.makedirs(save_root, exist_ok=True)
    
    # 모든 이미지를 한 번만 읽어서 메모리에 저장
    image_cache = {key: read_image(os.path.join(bollinger_img_path, key)) for key in sorted_keys}
    
    # start_idx부터 end_idx까지 처리
    for i in tqdm(range(start_idx, end_idx), desc=f'Calculating Bollinger Band IOU (from {start_idx} to {end_idx})'):
        try:
            current_image_key = sorted_keys[i]
            current_image_mask = image_cache[current_image_key]
            bollinger_bands_ious = []
            
            # 과거 이미지들과 비교 (0부터 i-1까지)
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