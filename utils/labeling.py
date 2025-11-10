from common_imports import *

def analyze_trend(data, phase, index, current_close=None):
    if data.empty:
        return None                
    
    pricing = data['close']
    
    if len(data) == 1 and phase == 'future' and current_close is not None:
        future_close = pricing.iloc[0]
        trend = 'up' if future_close > current_close else 'down'
        return {'index': f'{index}',
                'date': data['time'].dt.date.iloc[-1], 
                'time': data['time'].dt.time.iloc[-1],
                'trend': trend, 
                'phase': phase}

    x = np.arange(len(pricing))
    y = pricing.values
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    
    # 평균 / 표준편차 생성
    mean_close = pricing.mean()
    std_close = pricing.std()
    
    # 상방, 하방 라인 생성
    upper_bound = mean_close + std_close * 0.43 
    lower_bound = mean_close - std_close * 0.43
    trend_point = z[0] * x[-1] + z[1]
    
    if trend_point > upper_bound:
        trend = 'up'
    elif lower_bound < trend_point < upper_bound:
        trend = 'sideway_up' if z[0] > 0 else 'sideway_down'
    else:
        trend = 'down'
    
    return {'index': f'{index}',
            'date': data['time'].dt.date.iloc[-1], 
            'time': data['time'].dt.time.iloc[-1],
            'trend': trend, 
            'phase': phase}