import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
import warnings
import os
import sys

warnings.filterwarnings('ignore')
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(PROJECT_ROOT, 'processed data')

def get_data_path(filename):
    """Data dosyasının yolunu döndür"""
    if os.path.exists(filename):
        return filename
    data_path = os.path.join(DATA_DIR, filename)
    if os.path.exists(data_path):
        return data_path
    raise FileNotFoundError(f"Data file not found: {filename}")

def generate_charts():
    print("Loading data...")
    try:
        df = pd.read_csv(get_data_path('medals_hofstede_merged.csv'))
    except FileNotFoundError:
        print("Error: 'medals_hofstede_merged.csv' not found.")
        return

    country_col = 'Country_Mapped'
    if 'Country_Mapped' not in df.columns:
        if 'country' in df.columns:
            country_col = 'country'
        elif 'Country' in df.columns:
            country_col = 'Country'
    
    print(f"Using column '{country_col}' for country names.")

    print("Generating Static Chart (Quartile Ladder)...")
    
    df['IDV_Quartile'] = pd.qcut(df['idv'], 4, labels=['Q1 (Collectivist)', 'Q2', 'Q3', 'Q4 (Individualist)'])
    quartile_data = df.groupby('IDV_Quartile')['Total_Medals'].mean().reset_index()

    sns.set_style("whitegrid")
    plt.figure(figsize=(12, 7))

    palette = sns.color_palette("Blues", n_colors=4)
    ax = sns.barplot(x='IDV_Quartile', y='Total_Medals', data=quartile_data, palette=palette)

    plt.title('The Undeniable Trend: Cultural Individualism vs. Medal Success', fontsize=16, fontweight='bold', pad=20)
    plt.ylabel('Average Total Medals (1896-2024)', fontsize=12)
    plt.xlabel('Cultural Orientation (Hofstede Individualism Quartiles)', fontsize=12)

    for i, row in quartile_data.iterrows():
        ax.text(i, row.Total_Medals + 15, f"{int(row.Total_Medals)}", 
                color='black', ha="center", fontweight='bold', fontsize=12)

    q1_val = quartile_data.iloc[0]['Total_Medals']
    q4_val = quartile_data.iloc[3]['Total_Medals']
    growth_factor = q4_val / q1_val

    plt.annotate(f'From Collectivist to Individualist:\n~{growth_factor:.1f}x Performance Jump!', 
                 xy=(3, q4_val), xytext=(0.5, q4_val),
                 arrowprops=dict(facecolor='#d62728', shrink=0.05, width=3, alpha=0.8),
                 fontsize=13, color='#b30000', fontweight='bold', ha='center',
                 bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#b30000", alpha=0.9))

    sns.despine()
    plt.tight_layout()
    plt.savefig('visual_quartile_trend.png', dpi=300)
    print("✓ Static chart saved.")

    print("Generating Interactive Dashboard...")

    # FIX: Daha iyi log scale handling
    df_filtered = df[df['Total_Medals'] > 0].copy()
    
    brush = alt.selection_interval()

    # FIX: Normal scale kullan, log scale yerine - daha görünür olacak
    scatter = alt.Chart(df_filtered).mark_circle(size=120, opacity=0.75).encode(
        x=alt.X('idv:Q', title='Individualism Score (0-100)', scale=alt.Scale(domain=[0, 100])),
        y=alt.Y('Total_Medals:Q', title='Total Olympic Medals', scale=alt.Scale(type='sqrt')),  # sqrt scale daha iyi
        color=alt.condition(
            brush,
            alt.Color('idv:Q', scale=alt.Scale(scheme='blues'), legend=None),
            alt.value('lightgray')
        ),
        tooltip=[
            alt.Tooltip(f'{country_col}:N', title='Nation'),
            alt.Tooltip('Total_Medals:Q', title='Total Medals'),
            alt.Tooltip('idv:Q', title='Individualism Score')
        ]
    ).properties(
        title='1. EXPLORE: Select an area to filter nations',
        width=450,
        height=400
    ).add_selection(
        brush
    )

    # Regression line
    reg_line = scatter.transform_regression(
        'idv', 'Total_Medals', method='poly', order=1
    ).mark_line(color='#d62728', strokeWidth=3, strokeDash=[5, 5])

    left_panel = scatter + reg_line

    # Bar chart
    bars = alt.Chart(df_filtered).mark_bar().encode(
        y=alt.Y(f'{country_col}:N', sort='-x', title=None),
        x=alt.X('Total_Medals:Q', title='Total Medals'),
        color=alt.Color('idv:Q', scale=alt.Scale(scheme='blues'), legend=None),
        tooltip=[f'{country_col}:N', 'Total_Medals:Q', 'idv:Q']
    ).transform_filter(
        brush 
    ).transform_window(
        rank='rank(Total_Medals)',
        sort=[alt.SortField('Total_Medals', order='descending')]
    ).transform_filter(
        alt.datum.rank <= 15 
    ).properties(
        title='2. DETAILS: Top Nations in Selection',
        width=350,
        height=400
    )

    dashboard = alt.hconcat(left_panel, bars).properties(
        title='Interactive Cultural Analysis: Filter by Individualism'
    ).configure_view(
        strokeWidth=0
    ).configure_axis(
        gridOpacity=0.3
    )

    dashboard.save('visual_interactive_dashboard.json')
    dashboard.save('visual_interactive_dashboard.html')
    print("✓ Interactive Dashboard saved as 'visual_interactive_dashboard.html'")

if __name__ == "__main__":
    generate_charts()