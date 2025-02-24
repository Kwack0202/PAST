#!/bin/bash
python run.py \
    --task_name candlestick_image \
    --candel_dir ./data/img_data/candle_img/ \
    --stock_csv  ./data/origin_data/stock_data.csv \
    --seq_len 60 \
    --window_len 5 \
    --end_date 2025-01-01

