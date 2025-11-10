#!/bin/bash
python run.py \
    --task_name label_data \
    --output_dir ./data/label/ \
    --stock_csv  ./data/origin_data/stock_data.csv\
    --seq_len 60 \
    --window_len 5 \
    --future_points 1 5 10 15 30 60  \
    --end_date 2025-01-01

