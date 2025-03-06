#!/bin/bash
python run.py \
    --task_name image_similarity_diem \
    --save_root ./results/DIEM_similarity/ \
    --feature_pkl ./data/img_data/IMG_vit_features.pkl \
    --start_index 30761 \
    --end_index 47409