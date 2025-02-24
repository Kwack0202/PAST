#!/bin/bash
python run.py \
    --task_name image_similarity \
    --save_root ./results/Base_Feature_csv/ \
    --feature_pkl ./data/img_data/IMG_vit_features.pkl \
    --start_index 30761 \

