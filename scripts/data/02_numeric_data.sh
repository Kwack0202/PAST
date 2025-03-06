#!/bin/bash
python run.py \
    --task_name numeric_data \
    --numeric_dir ./data/numeric_data/ \
    --stock_csv  ./data/origin_data/stock_data.csv \
    --seq_len 60 \
    --window_len 5 \
    --end_date 2025-01-01

