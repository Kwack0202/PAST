# PAST
**PAST : Price Analysis using Similarity Tracking**

## Concept of PAST
![Framework](./assets/concept_fig.png)
- **Current Chart** (C, 🔴): Historical charts similar to the current window
- **Future Chart** (F, 🟢): Future price movements of the chart (C) browsed based on similarities

**PAST is a “model-learning-independent system” that does not use the concept of model learning**

## System setting
- **CPU** AMD Ryzen 9 5950X 16-Core Processor
- **GPU** NVIDIA GeForce RTX 4080
- **Memory RAM** 128GB

**The computational efficiency of PAST is proportional to the CPU's power(Logical processor)**

## Usage
### Requirments
- **python version** 3.8 
- **TA Library** TA_Lib-0.4.24-cp38-cp38-win_amd64.whl
- **other package** Packages in common_imports.py
- **Futures Data** 1-minute high-frequency trading data (stock indices, individual stocks, etc.)

### run.py
- To run the PAST system, the parser arguments must be passed using the `run.py` and `sh files`
- The `sh file` is divided into subfolders and multiple steps within the ./scripts/ folder.

#### The folder structure is as follows:
```
./scripts/
├── data/
│     ├──01_data_preprocessing.sh
│     ├──02_numeric.sh
│     │         :
│     └──05_label_data.sh
│
├── Similarity/
│     ├──01_image_FE.sh
│     ├──02_image_similarity.sh
│     │         :
│
└── Backtesting/
      ├──01_results_merge.sh
      ├──02_prediction.sh
      │         :
```
#### Example command (Git Bash)
```
sh ./scripts/data/03_candlestick_image.sh
```
#### code in 03_candlestick_image.sh
```
#!/bin/bash
python run.py \
    --task_name candlestick_image \
    --candel_dir ./data/img_data/candle_img/ \
    --stock_csv ./data/csv/stock_data.csv \
    --seq_len 60 \
    --window_len 5 \
    --end_date 2025-01-01 \
    --start_index 0 \
```

## Backtesting (Cumulative_profit)
<div align="center">
    <img src="./assets/final_output.gif" />
    <br>
    <img src="./assets/cum_result_sample.gif" />
</div>
