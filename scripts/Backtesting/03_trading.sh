#!/bin/bash
python run.py \
    --task_name trading \
    --pred_dir ./Backtesting/pred/ \
    --stock_data_path ./data/origin_data/stock_data.csv \
    --opposite_count 2 \
    --similarity_types cosine cosine_IOU_avg DIEM DIEM_IOU_avg dtw_similarity euclidean euclidean_IOU_avg IOU wasserstein wasserstein_IOU_avg 