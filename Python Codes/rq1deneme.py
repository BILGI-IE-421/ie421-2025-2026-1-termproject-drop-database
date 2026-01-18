import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
import warnings


warnings.filterwarnings('ignore')

def fit_ols_logarithmic(years, values, mode='min'):
    start_year = years.min()
    X_transformed = np.log(years - start_year + 1)
    
    coeffs = np.polyfit(X_transformed, values, 1)
    slope = coeffs[0]     
    intercept = coeffs[1] 
    
    
    y_pred = intercept + slope * X_transformed
    
    
    r2 = r2_score(values, y_pred)
    
    future_log = np.log(2040 - start_year + 1)
    pred_2040 = intercept + slope * future_log
    
    return y_pred, r2, slope, intercept, pred_2040
def analyze_with_ols():    

    try:
        sprint = pd.read_csv('100m_cleaned.csv')
        marathon = pd.read_csv('marathon_cleaned.csv')
        highjump = pd.read_csv('highjump_cleaned.csv')
    except FileNotFoundError:
        print("HATA: Dosyalar bulunamadı.")
        return


    data_map = {
        '100m Sprint': {
            'df': sprint[sprint['Year'].notna()].groupby('Year')['Time_seconds'].min().reset_index(),
            'col': 'Time_seconds', 'mode': 'min', 'color': '#E63946', 'unit': 'sn'
        },
        'Marathon': {
            'df': marathon[marathon['Year'].notna()].groupby('Year')['Time_seconds'].min().reset_index(),
            'col': 'Time_seconds', 'mode': 'min', 'color': '#457B9D', 'unit': 'saat'
        },
        'High Jump': {
            'df': highjump[highjump['Year'].notna()].groupby('Year')['Height_meters'].max().reset_index(),
            'col': 'Height_meters', 'mode': 'max', 'color': '#2A9D8F', 'unit': 'm'
        }
    }


    plt.figure(figsize=(12, 7))
    plt.style.use('ggplot')
    
    print("\n" + "="*95)
    print(f"{'SPOR DALI':<15} | {'R² (UYUM)':<10} | {'GÜNCEL':<10} | {'2040 TAHMİNİ':<12} | {'GELİŞİM HIZI':<15}")
    print("="*95)

    for name, props in data_map.items():
        df = props['df']
        col = props['col']
        mode = props['mode']
        
        X = df['Year'].values
        y = df[col].values
        

        y_pred, r2, slope, intercept, pred_2040 = fit_ols_logarithmic(X, y, mode)
        
        current_rate = abs(slope / (X[-1] - X[0] + 1))
        

        unit = props['unit']
        curr_val = y[-1]
        

        if name == 'Marathon':
            print(f"{name:<15} | {r2:<10.3f} | {curr_val/3600:<9.2f}h | {pred_2040/3600:<11.2f}h | {current_rate*60:<5.4f} dk/yıl (Hız)")
        elif name == '100m Sprint':
            print(f"{name:<15} | {r2:<10.3f} | {curr_val:<9.2f}s | {pred_2040:<11.2f}s | {current_rate:<5.4f} sn/yıl (Hız)")
        else:
            print(f"{name:<15} | {r2:<10.3f} | {curr_val:<9.2f}m | {pred_2040:<11.2f}m | {current_rate*100:<5.4f} cm/yıl (Hız)")

        
        y_indexed = (y / y[0]) * 100 if mode == 'max' else (y[0] / y) * 100
        y_pred_indexed = (y_pred / y[0]) * 100 if mode == 'max' else (y[0] / y_pred) * 100
        
        plt.scatter(X, y_indexed, color=props['color'], alpha=0.3, s=20)
        plt.plot(X, y_pred_indexed, color=props['color'], linewidth=2.5, 
                 label=f"{name} (R²: {r2:.2f})")


    plt.title('OLS Log-Linear Regression:Performance Improvements', fontsize=14, pad=15)
    plt.xlabel('Yıl', fontsize=12)
    plt.ylabel('Performans Index (Starting = 100)', fontsize=12)
    plt.legend(fontsize=11)
    plt.grid(True, linestyle='--', alpha=0.5)
    

    plt.text(0.02, 0.05,
             transform=plt.gca().transAxes, fontsize=9,
             bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray'))

    output_file = 'ols_performance_analysis.png'
    plt.savefig(output_file, dpi=300)
    print("="*95)
    print(f"\nGrafik kaydedildi: {output_file}")
    plt.show()

if __name__ == "__main__":
    analyze_with_ols()