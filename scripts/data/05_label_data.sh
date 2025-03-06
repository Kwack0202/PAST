#!/bin/bash
python run.py \
    --task_name label_data \
    --output_dir ./data/label/ \
    --stock_csv  ./data/origin_data/stock_data.csv\
    --seq_len 60 \
    --window_len 5 \
    --future_points 1 2 3 6 12 \
    --end_date 2025-01-01

