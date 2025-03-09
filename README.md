# PAST
**PAST : Price Analysis using Similarity Tracking**

## Concept of PAST
![Framework](./assets/concept_fig.png)
- **Current Chart** (C, 🔴): Historical charts similar to the current window
- **Future Chart** (F, 🟢): Future price movements of the chart (C) browsed based on similarities

**PAST is a “model-learning-independent system” that does not use the concept of model learning**

## 🛠 System setting
- **CPU** AMD Ryzen 9 5950X 16-Core Processor
- **GPU** NVIDIA GeForce RTX 4080
- **Memory RAM** 128GB

**The computational efficiency of PAST is proportional to the CPU's power(Logical processor)**

## 📑 Usage
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

## 📊 Backtesting
| **similarity**          | **trading_trial** | **total_trades** | **long_entries** | **short_entries** | **total_win_rate** | **long_win_rate** | **short_win_rate** | **total_payoff_ratio** | **total_profit_factor** | **long_payoff_ratio** | **long_profit_factor** | **short_payoff_ratio** | **short_profit_factor** | **final_cumulative_profit** | **final_cumulative_return** | **max_realized_profit** | **max_realized_return** | **final_portfolio_return** | **max_portfolio_return** | **MaxDrawdown** | **MaxDrawdown_rate** |
|-------------------------|-------------------|------------------|------------------|-------------------|--------------------|-------------------|--------------------|-----------------------|------------------------|---------------------|-----------------------|---------------------|-----------------------|--------------------------|---------------------------|------------------------|---------------------|----------------------------|--------------------------|-----------------|--------------------|
| **DIEM**                | 2.982             | 709.711          | 342.289          | 367.422           | 43.858             | 42.857            | 44.78              | 1.232                 | 1.007                  | 1.186               | 0.913                 | 1.276               | 1.102                 | 1.306                    | 0.404                     | 6.087                  | 1.757               | 323.83                    | 0.404                    | 6.345           | -5.815           |
| **DIEM_IOU_avg**        | 3.019             | 718.533          | 350.089          | 368.444           | 44.439             | 44.373            | 44.493             | 1.254                 | 1.052                  | 1.166               | 0.965                 | 1.339               | 1.137                 | 14.336                   | 4.446                     | 6.146                  | 1.781               | 336.722                   | 4.446                    | 7.673           | -4.71            |
| **IOU**                 | 3.084             | 733.889          | 357.2            | 376.689           | 44.369             | 43.457            | 45.235             | 1.273                 | 1.06                   | 1.218               | 0.948                 | 1.326               | 1.177                 | 17.037                   | 5.281                     | 5.824                  | 1.704               | 339.578                   | 5.281                    | 9.332           | -4.256           |
| cosine                  | 2.983             | 709.844          | 344.067          | 365.778           | 43.941             | 42.948            | 44.863             | 1.233                 | 1.009                  | 1.178               | 0.903                 | 1.284               | 1.119                 | 1.746                    | 0.541                     | 5.964                  | 1.727               | 324.267                   | 0.541                    | 6.275           | -6.206           |
| **cosine_IOU_avg**      | 3.02              | 718.667          | 355              | 363.667           | 44.145             | 43.981            | 44.306             | 1.256                 | 1.037                  | 1.159               | 0.938                 | 1.352               | 1.139                 | 10.224                   | 3.17                      | 6.306                  | 1.831               | 332.691                   | 3.17                     | 7.353           | -4.911           |
| dtw_similarity          | 0.995             | 236.889          | 210.733          | 26.156            | 48.834             | 48.563            | 31.844             | 0.864                 | 0.845                  | 0.859               | 0.82                  | 0.568               | 0.684                 | -29.532                  | -9.165                    | 5.217                  | 1.584               | 292.67                    | -9.165                   | 0               | -11.151          |
| euclidean               | 2.982             | 709.711          | 342.289          | 367.422           | 43.858             | 42.857            | 44.78              | 1.232                 | 1.007                  | 1.186               | 0.913                 | 1.276               | 1.102                 | 1.306                    | 0.404                     | 6.087                  | 1.757               | 323.83                    | 0.404                    | 6.345           | -5.815           |
| **euclidean_IOU_avg**   | 2.997             | 713.267          | 346.622          | 366.644           | 44.249             | 43.624            | 44.825             | 1.28                  | 1.061                  | 1.214               | 0.976                 | 1.343               | 1.145                 | 17.219                   | 5.341                     | 6.188                  | 1.788               | 339.624                   | 5.341                    | 8.107           | -4.677           |
| wasserstein             | 2.917             | 694.289          | 339.578          | 354.711           | 43.633             | 42.229            | 44.975             | 1.247                 | 1.009                  | 1.208               | 0.915                 | 1.283               | 1.108                 | 1.284                    | 0.398                     | 6.022                  | 1.76                | 323.788                   | 0.398                    | 6.785           | -7.07            |
| **wasserstein_IOU_avg** | 3.006             | 715.533          | 350.556          | 364.978           | 43.692             | 43.332            | 44.046             | 1.277                 | 1.035                  | 1.221               | 0.944                 | 1.331               | 1.13                  | 9.508                    | 2.949                     | 6.269                  | 1.829               | 331.992                   | 2.949                    | 7.937           | -4.71            |
| long                    | 1                 | 238              | 238              | 0                 | 45.378             | 45.378            | 0                  | 0.9                   | 0.76                   | 0.9                 | 0.76                  | 0                   | 0                     | -77.4                    | -24.241                 | 11.1                 | 3.284               | 241.9                     | -24.241                | 0               | -26.675          |
| short                   | 1                 | 238              | 0                | 238               | 53.782             | 0                 | 53.782             | 1.111                 | 1.316                  | 0                   | 0                     | 1.111               | 1.316                 | 77.4                    | 24.241                 | 10.65                | 3.062               | 396.7                     | 24.241                | 26.675          | -3.284           |


<div align="center">
    <img src="./assets/final_output.gif" />
    <br>
    <img src="./assets/cum_result_sample.gif" />
</div>
