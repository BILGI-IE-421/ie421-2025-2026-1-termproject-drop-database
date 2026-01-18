import pandas as pd
import numpy as np
import re
import os
import warnings
import sys

# Proje yapısına göre data klasörünü bul
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')

def get_data_path(filename):
    """Data dosyasının yolunu döndür"""
    if os.path.exists(filename):
        return filename
    data_path = os.path.join(DATA_DIR, filename)
    if os.path.exists(data_path):
        return data_path
    raise FileNotFoundError(f"Data file not found: {filename}")

warnings.filterwarnings("ignore", category=UserWarning) 

def load_data():
    """
    Verileri çalışma dizininden doğrudan okur.
    Dosyaların bu script ile AYNI klasörde olması gerekir.
    """
    print("Veriler yükleniyor...")
    try:
        data = {
            'meter_100': pd.read_csv(get_data_path('100meter.csv')),
            'marathon': pd.read_csv(get_data_path('maraton11.csv')),
            'highjump': pd.read_excel(get_data_path('highjump.xlsx')),
            'athlete_events': pd.read_csv(get_data_path('processed_athlete_events.csv')),
            'hofstede': pd.read_excel(get_data_path('temizlenmis_hofstede_data.xlsx'))
        }
        print("Tüm veriler başarıyla okundu.\n")
        return data
    except FileNotFoundError as e:
        print(f"\nHATA: Dosya bulunamadı! -> {e.filename}")
        print("Lütfen veri dosyasının bu kod dosyasıyla AYNI klasörde olduğundan emin ol.")
        exit()

def convert_time_to_seconds(time_str):
    if pd.isna(time_str):
        return np.nan
    time_str = str(time_str).strip()
    try:
        return float(time_str)
    except:
        if 'second' in time_str.lower():
            try:
                return float(re.findall(r'\d+\.\d+', time_str)[0])
            except IndexError:
                return np.nan
    return np.nan

def convert_marathon_time(time_str):
    if pd.isna(time_str):
        return np.nan
    time_str = str(time_str).strip()
    try:
        parts = time_str.split(':')
        if len(parts) == 3:
            return float(parts[0]) * 3600 + float(parts[1]) * 60 + float(parts[2])
        elif len(parts) == 2:
            return float(parts[0]) * 60 + float(parts[1])
    except:
        pass
    return np.nan

def main():

    datasets = load_data()
    
    meter_100 = datasets['meter_100']
    marathon = datasets['marathon']
    highjump = datasets['highjump']
    athlete_events = datasets['athlete_events']
    hofstede = datasets['hofstede']

    meter_100['Time_seconds'] = meter_100['Time'].apply(convert_time_to_seconds)
    meter_100['Year'] = pd.to_datetime(meter_100['Date'], dayfirst=True, errors='coerce').dt.year

    marathon['Time_seconds'] = marathon['Time'].apply(convert_marathon_time)
    marathon['Year'] = pd.to_datetime(marathon['Date'], dayfirst=True, errors='coerce').dt.year

    if 'Mark' in highjump.columns:
        highjump['Height_meters'] = pd.to_numeric(highjump['Mark'], errors='coerce')
    elif 'Height' in highjump.columns:
        highjump['Height_meters'] = pd.to_numeric(highjump['Height'], errors='coerce')
    
    if 'Date' in highjump.columns:
        highjump['Year'] = pd.to_datetime(highjump['Date'], dayfirst=True, errors='coerce').dt.year

    medal_counts = athlete_events.groupby('NOC').agg({
        'Medal': lambda x: (x.notna()).sum(),
    }).reset_index()
    medal_counts.columns = ['NOC', 'Total_Medals']

    for medal_type in ['Gold', 'Silver', 'Bronze']:
        counts = athlete_events[athlete_events['Medal'] == medal_type].groupby('NOC').size().reset_index(name=f'{medal_type}_Medals')
        medal_counts = medal_counts.merge(counts, on='NOC', how='left')
    
    medal_counts = medal_counts.fillna(0)

    noc_to_country = {
        'USA': 'U.S.A.', 'GBR': 'Great Britain', 'GER': 'Germany', 'FRA': 'France',
        'ITA': 'Italy', 'CAN': 'Canada', 'AUS': 'Australia', 'JPN': 'Japan',
        'CHN': 'China', 'RUS': 'Russia', 'NED': 'Netherlands', 'SWE': 'Sweden',
        'NOR': 'Norway', 'FIN': 'Finland', 'BRA': 'Brazil', 'ARG': 'Argentina',
        'MEX': 'Mexico', 'ESP': 'Spain', 'POL': 'Poland', 'BEL': 'Belgium',
        'SUI': 'Switzerland', 'AUT': 'Austria', 'DEN': 'Denmark', 'GRE': 'Greece',
        'KOR': 'Korea South', 'NZL': 'New Zealand', 'IND': 'India', 'TUR': 'Turkey',
        'CZE': 'Czech Rep', 'HUN': 'Hungary', 'ROU': 'Romania', 'UKR': 'Ukraine',
        'POR': 'Portugal', 'IRL': 'Ireland', 'RSA': 'South Africa white', 'EGY': 'Egypt',
        'CHI': 'Chile', 'COL': 'Colombia', 'VEN': 'Venezuela', 'PER': 'Peru',
        'CUB': 'Cuba', 'JAM': 'Jamaica', 'KEN': 'Kenya', 'NGA': 'Nigeria',
        'MAR': 'Morocco', 'ALG': 'Algeria', 'THA': 'Thailand', 'MYS': 'Malaysia',
        'SGP': 'Singapore', 'PHI': 'Philippines', 'PAK': 'Pakistan',
        'BGD': 'Bangladesh', 'VIE': 'Vietnam', 'INA': 'Indonesia', 'ISR': 'Israel',
        'IRI': 'Iran', 'IRQ': 'Iraq', 'URS': 'Russia',
        'FRG': 'Germany', 'GDR': 'Germany', 'TCH': 'Czech Rep', 'YUG': 'Serbia',
        'BUL': 'Bulgaria', 'EST': 'Estonia', 'LTU': 'Lithuania', 'LVA': 'Latvia',
        'SLO': 'Slovenia', 'CRO': 'Croatia', 'SRB': 'Serbia', 'SVK': 'Slovak Rep',
        'TPE': 'Taiwan', 'HKG': 'Hong Kong', 'URU': 'Uruguay'
    }
    
    medal_counts['Country'] = medal_counts['NOC'].map(noc_to_country)

    merged_data = medal_counts.merge(
        hofstede, 
        left_on='Country', 
        right_on='country',
        how='inner'
    )

    print("Veriler işlendi, kaydediliyor...")
    
    meter_100.to_csv('100m_cleaned.csv', index=False)
    marathon.to_csv('marathon_cleaned.csv', index=False)
    highjump.to_csv('highjump_cleaned.csv', index=False)
    merged_data.to_csv('medals_hofstede_merged.csv', index=False)

    print("\n" + "="*80)
    print("DATA PROCESSING COMPLETE ✓")
    print("="*80)
    print(f"100m Records: {len(meter_100)}")
    print(f"Marathon Records: {len(marathon)}")
    print(f"High Jump Records: {len(highjump)}")
    print(f"Merged Countries: {len(merged_data)}")
    print(f"Dosyalar kaydedildi: {os.getcwd()}")
    print("="*80)

if __name__ == "__main__":
    main()