#!/bin/bash
python run.py \
    --task_name bollinger_band \
    --bband_dir ./data/img_data/bollinger_bands/ \
    --stock_csv ./data/csv/stock_data.csv \
    --seq_len 60 \
    --window_len 5 \
    --end_date 2025-01-01 \
    --start_index 0

