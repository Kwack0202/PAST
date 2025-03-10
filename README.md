# PAST
**PAST : Price Analysis using Similarity Tracking**
![Cum full](./assets/final_output.gif)

## Concept of PAST
![Concept Diagram](./assets/concept_fig.png)
- **Current Chart** (**C**, 🔴): Historical charts similar to the current window
- **Future Chart** (**F**, 🟢): Future price movements of the chart (C) browsed based on similarities

**PAST is a model-learning-independent system that does not use the concept of model learning**

PAST uses images of `candlestick charts` and `Bollinger band areas` to make predictions and trades based on the similarity between the current window and the past window

## 🛠 System
- **CPU** `AMD Ryzen 9 5950X 16-Core Processor`
- **GPU** `NVIDIA GeForce RTX 4080`
- **Memory RAM** `128GB`

**The computational efficiency of PAST is proportional to the CPU's power(Logical processor)**

## 📑 Usage
### Requirments
- **python version** `3.8`
- **TA Library** `TA_Lib-0.4.24-cp38-cp38-win_amd64.whl`
- **Other packages** `Packages in common_imports.py`
- **Futures Data** `KOSPI200 Futures Data` 1-minute high-frequency trading data

### run.py
- To run the PAST system, the parser arguments must be passed using the `run.py` and `sh files`
- The `sh file` is divided into subfolders and multiple steps within the ./scripts/ folder.

#### The scripts folder structure is as follows:
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
#### Example code in sh file
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
![Img sample](./assets/Candlestick_img.png)

## 📊 PAST Execution
### KOSPI200 futures data
![Data distribution](./assets/KOSPI200_Futures_distribution.png) 

- **Experimental period** 2022.02.10-2024.12.31
- **Test(Trading)** 2024.01.01-2024.12.31

Each point in the `Test(Trading)` period time series has access to all of the previous time series

- **Specifics in data**
> 1. As of July 31, 2023, the opening hours of the derivatives market on the Korea Exchange have been accelerated due to changes in the derivatives market system `9 AM -> 8:45 AM`
> 2. Some days the market closes early at `3:20`
> 3. First trading day of the new year will have a 1-hour delayed opening time `2023Y: 9 AM -> 10 AM` `2024Y: 8:45 AM -> 9:45 AM`

### Experimental setup
- **Window size** (default, 🔴)
    - 60

- **Window sliding** (default)
    - 5

- **Labeling window size** (🟢) 
    - 5  10  15  30  60 → **best💡** `15 30`

- **Select Top N instances**
    - 1  3  5  10  20  30  50  100  200 ... → **best💡** `1 3 30`

- **Similarity types**
    - Candlestick image feature similarity → `DIEM` `Cosine` `Euclidean` `Wasserstein`
    - Bollinger band area IOU score → `IOU`
    - Numeric feaure → `DTW`


## 📈 Backtesting 📉
### Summary of trading performance by similarity type
#### trading metric
- **PR : payoff ratio**
- **PF : profit factor**
- **CR : Cumulative return (%)**
- **MRR : Maximum Realized Return (%)**
- **MDD : MaxDrawdown (%)**

| **Category**   |      **similarity**     | **total PR**          | **total PF**           | **long PR**           | **long PF**           | **short PR**          | **short PF**          | **CR (%)**               | **MRR (%)**               | **MDD (%)**          |
|----------------|-------------------------|-----------------------|------------------------|-----------------------|-----------------------|-----------------------|-----------------------|--------------------------|---------------------------|----------------------|
| **similarity** | **IOU**                 | **1.273**             | **1.06**               | **1.218**             | **0.948**             | **1.326**             | **1.177**             | **5.281**                | **1.704**                 | **-4.256**           |
|                | DIEM                    | 1.232                 | 1.007                  | 1.186                 | 0.913                 | 1.276                 | 1.102                 | 0.404                    | 1.757                     | -5.815               |
|                | **DIEM_IOU_avg**        | **1.254**             | **1.052**              | **1.166**             | **0.965**             | **1.339**             | **1.137**             | **4.446**                | **1.781**                 | **-4.71**            |
|                | cosine                  | 1.233                 | 1.009                  | 1.178                 | 0.903                 | 1.284                 | 1.119                 | 0.541                    | 1.727                     | -6.206               |
|                | **cosine_IOU_avg**      | **1.256**             | **1.037**              | **1.159**             | **0.938**             | **1.352**             | **1.139**             | **3.17**                 | **1.831**                 | **-4.911**           |
|                | dtw_similarity          | 0.864                 | 0.845                  | 0.859                 | 0.82                  | 0.568                 | 0.684                 | -9.165                   | 1.584                     | -11.151              |
|                | euclidean               | 1.232                 | 1.007                  | 1.186                 | 0.913                 | 1.276                 | 1.102                 | 0.404                    | 1.757                     | -5.815               |
|                | **euclidean_IOU_avg**   | **1.28**              | **1.061**              | **1.214**             | **0.976**             | **1.343**             | **1.145**             | **5.341**                | **1.788**                 | **-4.677**           |
|                | wasserstein             | 1.247                 | 1.009                  | 1.208                 | 0.915                 | 1.283                 | 1.108                 | 0.398                    | 1.76                      | -7.07                |
|                | **wasserstein_IOU_avg** | **1.277**             | **1.035**              | **1.221**             | **0.944**             | **1.331**             | **1.13**              | **2.949**                | **1.829**                 | **-4.71**            |
| **Benchmark**  | long                    | 0.9                   | 0.76                   | 0.9                   | 0.76                  | 0                     | 0                     | -24.241                  | 3.284                     | -26.675              |
|                | short                   | 1.111                 | 1.316                  | 0                     | 0                     | 1.111                 | 1.316                 | 24.241                   | 3.062                     | -3.284               |

![trading results](./assets/trading_results_plt.png)

### Long/Short Trading Signals
![Trading signals](./assets/position_signal.gif)

### Cumulative profit (top: all results, bottom: BEST)
![Cum sample](./assets/cum_result_sample.gif)

### Margin Return
![Margin](./assets/margin_return.gif)

### Drawdown
![DD DIEM](./assets//DIEM_vs_DIEM_IOU_avg_output.gif)
![DD Cosine](./assets/cosine_vs_cosine_IOU_avg_output.gif)
![DD Euclidean](./assets/euclidean_vs_euclidean_IOU_avg_output.gif)
![DD Wasserstein](./assets//wasserstein_vs_wasserstein_IOU_avg_output.gif)


<div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px;">
  <img src="./assets/position_signal.gif" alt="Trading signals" style="width:100%;">
  <img src="./assets/margin_return.gif" alt="Margin" style="width:100%;">
  <img src="./assets/DIEM_vs_DIEM_IOU_avg_output.gif" alt="DD DIEM" style="width:100%;">
  <img src="./assets/cosine_vs_cosine_IOU_avg_output.gif" alt="DD Cosine" style="width:100%;">
  <img src="./assets/euclidean_vs_euclidean_IOU_avg_output.gif" alt="DD Euclidean" style="width:100%;">
  <img src="./assets/wasserstein_vs_wasserstein_IOU_avg_output.gif" alt="DD Wasserstein" style="width:100%;">
</div>