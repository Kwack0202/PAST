from common_imports import *

# 이미지 생성용 함수
def plot_candles(pricing, title=None, trend_line=False, volume_bars=False, color_function=None, technicals=None):
    def default_color(index, open_price, close_price, low, high):
        return 'b' if open_price[index] > close_price[index] else 'r'
    
    color_function = color_function or default_color
    technicals = technicals or []
    open_price = pricing['open']
    close_price = pricing['close']
    low = pricing['low']
    high = pricing['high']
    oc_min = pd.concat([open_price, close_price], axis=1).min(axis=1)
    oc_max = pd.concat([open_price, close_price], axis=1).max(axis=1)
    
    def plot_trendline(ax, pricing, linewidth=5):
        x = np.arange(len(pricing))
        y = pricing.values
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        ax.plot(x, p(x), 'g--', linewidth=2)
        mean_price = np.mean(y)
        std_price = np.std(y)
        ax.plot(x, [mean_price + std_price] * len(x), 'k--', linewidth=2)
        ax.plot(x, [mean_price - std_price] * len(x), 'k--', linewidth=2)
    
    if volume_bars:
        fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, gridspec_kw={'height_ratios': [3,1]}, figsize=(20,10))
    else:
        fig, ax1 = plt.subplots(1, 1, figsize=(20,10))
    
    # 배경을 투명하게 설정
    fig.patch.set_alpha(0.0)  # Figure 배경 투명
    ax1.patch.set_alpha(0.0)   # Axes 배경 투명
    if volume_bars:
        ax2.patch.set_alpha(0.0)  # Volume Axes 배경 투명
    
    if title:
        ax1.set_title(title)
    fig.tight_layout()
    x = np.arange(len(pricing))
    candle_colors = [color_function(i, open_price, close_price, low, high) for i in x]
    candles = ax1.bar(x, oc_max-oc_min, bottom=oc_min, color=candle_colors, linewidth=0)
    lines = ax1.vlines(x, low, high, color=candle_colors, linewidth=1)
    
    if trend_line:
        plot_trendline(ax1, pricing['close'])
    
    ax1.xaxis.grid(True)
    ax1.yaxis.grid(True)
    ax1.xaxis.set_tick_params(which='major', length=3.0, direction='in', top='off')
    ax1.set_xticklabels([])
    ax1.set_yticklabels([])
    ax1.xaxis.set_visible(False)
    ax1.yaxis.set_visible(False)
    ax1.axis(False)

    # 볼린저 밴드 색상 지정
    for indicator in technicals:
        if indicator.name in ['BBAND_UPPER', 'BBAND_MIDDLE', 'BBAND_LOWER']:
            ax1.plot(x, indicator, color='#0000FF', linewidth=1.5, alpha=1.0)
        else:
            ax1.plot(x, indicator, linewidth=1.5)
    
    if volume_bars:
        volume = pricing['volume']
        volume_scale = None
        scaled_volume = volume
        if volume.max() > 1000000:
            volume_scale = 'M'
            scaled_volume = volume / 1000000
        elif volume.max() > 1000:
            volume_scale = 'K'
            scaled_volume = volume / 1000
        ax2.bar(x, scaled_volume, color=candle_colors)
        volume_title = 'volume'
        if volume_scale:
            volume_title = 'volume (%s)' % volume_scale
        ax2.xaxis.grid(True)
        ax2.set_xticklabels([])
        ax2.set_yticklabels([])
        ax2.axis(False)
    
    return fig