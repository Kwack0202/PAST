#!/bin/bash
python run.py \
    --task_name predict_trend \
    --merged_path ./Backtesting/results_merged/ \
    --label_dir ./data/label/ \
    --stock_csv ./data/origin_data/stock_data.csv \
    --top_n_list 1 3 5 10 20 30 50 100 200 \
    # --similarity_types cosine cosine_IOU_avg DIEM DIEM_IOU_avg dtw_similarity euclidean euclidean_IOU_avg IOU wasserstein wasserstein_IOU_avg 