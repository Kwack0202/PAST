from common_imports import *

def process_trading_data(pred_file, output_dir='./Backtesting/simulation/'):
    trading_df = pd.read_csv(f'./Backtesting/trading/{pred_file}.csv')
    trading_df['time'] = pd.to_datetime(trading_df['time'])
    trading_days = list(trading_df.groupby(trading_df['time'].dt.date))

    signal_results = []
    current_profit = 0
    current_profit_ratio = 0

    for date, group in trading_days:
        day_df = group.reset_index(drop=True).copy()

        new_data = {
            'time': [],
            'Margin_Profit': [],
            'Margin_Return': [],
            'Cumulative_Profit': [],
            'Daily_Cumulative_Profit': []
        }

        entry_price = None
        entry_position = None
        daily_cumulative_profit = 0

        for index, row in day_df.iterrows():
            if row['position'] in ['short', 'long']:
                next_row = day_df.iloc[index + 1] if index + 1 < len(day_df) else None
                if next_row is not None:
                    entry_price = next_row['open']
                    entry_position = row['position']

                    new_data['time'].append(row['time'])
                    new_data['Margin_Profit'].append(0)
                    new_data['Margin_Return'].append(0)
                    new_data['Cumulative_Profit'].append(current_profit)
                    new_data['Daily_Cumulative_Profit'].append(daily_cumulative_profit)
            elif row['position'] == 'margin transaction' and entry_price is not None:
                next_row = day_df.iloc[index + 1] if index + 1 < len(day_df) else row
                exit_price = next_row['open'] if next_row is not row else row['close']

                profit = (entry_price - exit_price) if entry_position == 'short' else (exit_price - entry_price)
                return_ = profit / entry_price * 100 if entry_position == 'long' else profit / exit_price * 100

                current_profit += profit
                current_profit_ratio += return_
                daily_cumulative_profit += profit

                new_data['time'].append(row['time'])
                new_data['Margin_Profit'].append(profit)
                new_data['Margin_Return'].append(return_)
                new_data['Cumulative_Profit'].append(current_profit)
                new_data['Daily_Cumulative_Profit'].append(daily_cumulative_profit)

                entry_price = None
                entry_position = None
            else:
                new_data['time'].append(row['time'])
                new_data['Margin_Profit'].append(0)
                new_data['Margin_Return'].append(0)
                new_data['Cumulative_Profit'].append(current_profit)
                new_data['Daily_Cumulative_Profit'].append(daily_cumulative_profit)

        new_df = pd.DataFrame(new_data)
        merged_df = pd.merge(day_df, new_df, on='time', how='outer')

        merged_df['Holding_Period'] = merged_df.groupby((merged_df['position'] != 'holding').cumsum()).cumcount()
        
        # Unrealized Profit 계산
        merged_df["Unrealized_Profit"] = 0.0
        entry_price = None
        entry_position = None

        for i, row in merged_df.iterrows():
            position = row["position"]
            close_price = row["close"]

            if position in ["long", "short"]:
                entry_price = merged_df.at[i + 1, "open"] if i + 1 < len(merged_df) else None
                entry_position = position
            elif position == "holding" and entry_price is not None:
                if entry_position == "long":
                    merged_df.at[i, "Unrealized_Profit"] = close_price - entry_price
                elif entry_position == "short":
                    merged_df.at[i, "Unrealized_Profit"] = entry_price - close_price
            elif position == "margin transaction":
                entry_price = None
                entry_position = None

        merged_df['Account_performance'] = merged_df['Cumulative_Profit'] + merged_df['Unrealized_Profit']

        position_mask = (merged_df['position'] == 'short') | (merged_df['position'] == 'long')
        if position_mask.sum() == 0:
            print(f"Warning: No 'short' or 'long' positions found in {pred_file} for date {date}. Skipping this day.")
            initial_investment = merged_df.iloc[0]['open'] 
        else:
            initial_investment = merged_df.iloc[merged_df[position_mask].index[0] + 1]['open']
            
        merged_df['Cumulative_Return'] = (merged_df['Cumulative_Profit'] / initial_investment) * 100
        merged_df['Unrealized_Return'] = (merged_df['Unrealized_Profit'] / initial_investment) * 100
    
        merged_df['Daily_Cumulative_Return'] = (merged_df['Daily_Cumulative_Profit'] / initial_investment) * 100
        merged_df['Account_Performance_Return'] = (merged_df['Account_performance'] / initial_investment) * 100
        merged_df['portfolio_performance'] = merged_df['Cumulative_Profit'] + initial_investment
        merged_df['Portfolio_Performance_Return'] = ((merged_df['portfolio_performance'] - initial_investment) / initial_investment) * 100

        # Drawdown
        max_pp = 0
        max_pp_rate = 0
        
        for index, row in merged_df.iterrows():
            if row['Cumulative_Profit'] > max_pp:
                max_pp = row['Cumulative_Profit']
            merged_df.at[index, 'Drawdown'] = -(max_pp - row['Cumulative_Profit']) if row['Cumulative_Profit'] != 0 else 0

            if row['Cumulative_Return'] > max_pp_rate:
                max_pp_rate = row['Cumulative_Return']
            merged_df.at[index, 'Drawdown_rate'] = -(max_pp_rate - row['Cumulative_Return']) if row['Cumulative_Return'] != 0 else 0

            
        signal_results.append(merged_df)
    
    final_trading_df = pd.concat(signal_results, ignore_index=True)
    
    column_names = [
        "time", "open", "high", "low", "close", "volume", "position",
        "Unrealized_Profit", "Unrealized_Return", "Margin_Profit", "Margin_Return",
        "Holding_Period", "Daily_Cumulative_Profit", "Daily_Cumulative_Return",
        "Cumulative_Profit", "Cumulative_Return",
        "Account_performance", "Account_Performance_Return",
        "portfolio_performance", "Portfolio_Performance_Return",
        "Drawdown", "Drawdown_rate"
    ]
    
    final_trading_df = final_trading_df[column_names]
    
    os.makedirs(output_dir, exist_ok=True)
    final_trading_df.to_csv(f"{output_dir}/{pred_file}_results.csv", encoding='utf-8-sig', index=False)
    print(f"Backtesting Completed for {pred_file}")

def summarize_results(trading_files, input_dir='./Backtesting/simulation/', output_dir='./Backtesting/summary/'):
    summary_data = []
    
    for pred_file in tqdm(trading_files, desc="Summarizing results"):
        backtesting_df = pd.read_csv(f'{input_dir}/{pred_file}_results.csv')
        backtesting_df['time'] = pd.to_datetime(backtesting_df['time'])

        unique_days = backtesting_df['time'].dt.date.nunique()
        margin_transactions_df = backtesting_df[backtesting_df['position'].isin(['long', 'short', 'margin transaction'])].reset_index(drop=True)
        mask = (margin_transactions_df['position'] == 'margin transaction') & (margin_transactions_df['position'].shift() == 'margin transaction')
        margin_transactions_df = margin_transactions_df[~mask].reset_index(drop=True)

        long_entries = len(margin_transactions_df[margin_transactions_df["position"] == "long"])
        short_entries = len(margin_transactions_df[margin_transactions_df["position"] == "short"])
        total_trades = long_entries + short_entries

        trading_trial = total_trades / unique_days if unique_days > 0 else 0
        total_profit_trades = len(margin_transactions_df[(margin_transactions_df["position"] == "margin transaction") & (margin_transactions_df["Margin_Profit"] > 0)])
        total_win_rate = total_profit_trades / total_trades * 100 if total_trades > 0 else 0

        long_profit_trades = margin_transactions_df[(margin_transactions_df["position"] == "margin transaction") & (margin_transactions_df["Margin_Profit"] > 0) & (margin_transactions_df["position"].shift(1) == "long")]
        long_win_rate = len(long_profit_trades) / long_entries * 100 if long_entries > 0 else 0

        short_profit_trades = margin_transactions_df[(margin_transactions_df["position"] == "margin transaction") & (margin_transactions_df["Margin_Profit"] > 0) & (margin_transactions_df["position"].shift(1) == "short")]
        short_win_rate = len(short_profit_trades) / short_entries * 100 if short_entries > 0 else 0

        profit_trades = margin_transactions_df[(margin_transactions_df["position"] == "margin transaction") & (margin_transactions_df["Margin_Profit"] > 0)]
        loss_trades = margin_transactions_df[(margin_transactions_df["position"] == "margin transaction") & (margin_transactions_df["Margin_Profit"] < 0)]

        total_profit_avg = profit_trades["Margin_Profit"].mean() if not profit_trades.empty else 0
        total_loss_avg = loss_trades["Margin_Profit"].mean() if not loss_trades.empty else 0

        long_profit_avg = long_profit_trades["Margin_Profit"].mean() if not long_profit_trades.empty else 0
        long_loss_avg = loss_trades["Margin_Profit"].mean() if not loss_trades.empty else 0

        short_profit_avg = short_profit_trades["Margin_Profit"].mean() if not short_profit_trades.empty else 0
        short_loss_avg = loss_trades["Margin_Profit"].mean() if not loss_trades.empty else 0

        total_payoff_ratio = total_profit_avg / -total_loss_avg if total_loss_avg < 0 else 0
        total_profit_factor = (-margin_transactions_df[margin_transactions_df['Margin_Profit'] > 0]['Margin_Profit'].sum() / 
                               margin_transactions_df[margin_transactions_df['Margin_Profit'] < 0]['Margin_Profit'].sum() 
                               if margin_transactions_df[margin_transactions_df['Margin_Profit'] < 0]['Margin_Profit'].sum() != 0 else 0)

        long_payoff_ratio = long_profit_avg / -long_loss_avg if long_loss_avg < 0 else 0
        long_profit_factor = (-margin_transactions_df[(margin_transactions_df["position"].shift(1) == "long") & (margin_transactions_df["Margin_Profit"] > 0)]['Margin_Profit'].sum() / 
                              margin_transactions_df[(margin_transactions_df["position"].shift(1) == "long") & (margin_transactions_df["Margin_Profit"] < 0)]['Margin_Profit'].sum() 
                              if margin_transactions_df[(margin_transactions_df["position"].shift(1) == "long") & (margin_transactions_df["Margin_Profit"] < 0)]['Margin_Profit'].sum() != 0 else 0)

        short_payoff_ratio = short_profit_avg / -short_loss_avg if short_loss_avg < 0 else 0
        short_profit_factor = (-margin_transactions_df[(margin_transactions_df["position"].shift(1) == "short") & (margin_transactions_df["Margin_Profit"] > 0)]['Margin_Profit'].sum() / 
                               margin_transactions_df[(margin_transactions_df["position"].shift(1) == "short") & (margin_transactions_df["Margin_Profit"] < 0)]['Margin_Profit'].sum() 
                               if margin_transactions_df[(margin_transactions_df["position"].shift(1) == "short") & (margin_transactions_df["Margin_Profit"] < 0)]['Margin_Profit'].sum() != 0 else 0)
        
        final_cumulative_profit = backtesting_df['Cumulative_Profit'].iloc[-1]
        final_cumulative_return = backtesting_df['Cumulative_Return'].iloc[-1]
        max_realized_profit = backtesting_df['Margin_Profit'].max()
        max_realized_return = backtesting_df['Margin_Return'].max()

        final_portfolio_performance = backtesting_df['portfolio_performance'].iloc[-1]
        final_portfolio_return = backtesting_df['Portfolio_Performance_Return'].iloc[-1]
        max_portfolio_performance = backtesting_df['portfolio_performance'].max()
        max_portfolio_return = backtesting_df['Portfolio_Performance_Return'].max()

        MDD = backtesting_df['Drawdown'].min()
        MDD_rate = backtesting_df['Drawdown_rate'].min()


        summary_data.append([
            pred_file, trading_trial, total_trades, long_entries, short_entries,
            total_win_rate, long_win_rate, short_win_rate,
            total_payoff_ratio, total_profit_factor,
            long_payoff_ratio, long_profit_factor,
            short_payoff_ratio, short_profit_factor,
            final_cumulative_profit, final_cumulative_return,
            max_realized_profit, max_realized_return,
            final_portfolio_performance, final_portfolio_return,
            max_portfolio_performance, max_portfolio_return,
            MDD, MDD_rate
        ])

    summary_df = pd.DataFrame(summary_data, columns=[
        "data_frame_name", "trading_trial",
        "total_trades", "long_entries", "short_entries",
        "total_win_rate", "long_win_rate", "short_win_rate",
        "total_payoff_ratio", "total_profit_factor",
        "long_payoff_ratio", "long_profit_factor",
        "short_payoff_ratio", "short_profit_factor",
        "final_cumulative_profit", "final_cumulative_return",
        "max_realized_profit", "max_realized_return",
        "final_portfolio_performance", "final_portfolio_return",
        "max_portfolio_performance", "max_portfolio_return",
        "MaxDrawdown", "MaxDrawdown_rate"
    ])

    os.makedirs(output_dir, exist_ok=True)
    summary_df.to_csv(f"{output_dir}/results_summary.csv", encoding='utf-8-sig', index=False)
    print("Summary completed and saved.")