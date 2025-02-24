#!/bin/bash
python run.py \
    --task_name image_bband \
    --save_root ./results/Base_Bollinger_Band_IOU_csv/ \
    --bollinger_img_path ./data/img_data/bollinger_bands/ \
    --feature_pkl ./data/img_data/IMG_vit_features.pkl \
    --start_index 30761 \
    --end_index 47409