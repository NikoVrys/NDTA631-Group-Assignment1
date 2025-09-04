# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import numpy as np
from scipy import stats

# Page configuration
st.set_page_config(
    page_title="SA Environmental & Social Analysis",
    page_icon="🇿🇦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {font-size: 2.5rem; color: #1f77b4; font-weight: bold;}
    .sub-header {font-size: 1.5rem; color: #ff7f0e; margin-top: 2rem;}
    .metric-card {background-color: #f0f2f6; padding: 1.5rem; border-radius: 0.5rem; margin: 1rem 0;}
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    conn = sqlite3.connect('data/database/south_africa_analysis.db')
    df = pd.read_sql_query("SELECT * FROM environmental_social_data ORDER BY year", conn)
    conn.close()
    return df

# Load the data
df = load_data()

# Sidebar
st.sidebar.title("🇿🇦 Analysis Controls")
st.sidebar.markdown("Customize the dashboard view:")

# Year range selector
year_range = st.sidebar.slider(
    "Select Year Range:",
    min_value=int(df['year'].min()),
    max_value=int(df['year'].max()),
    value=(int(df['year'].min()), int(df['year'].max()))
)

# Filter data based on selection
filtered_df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]

# Main content
st.markdown('<p class="main-header">South Africa: CO2 Emissions vs Food Affordability Analysis</p>', unsafe_allow_html=True)
st.markdown("""
This interactive dashboard explores the relationship between environmental impact (CO2 emissions) 
and social welfare (food affordability) in South Africa from 2017 to 2023.
""")

# Key Metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Average CO2 Emissions",
        value=f"{filtered_df['total_co2_emissions'].mean():.1f}M tonnes",
        delta=f"{filtered_df['total_co2_emissions'].pct_change().mean()*100:.1f}%"
    )

with col2:
    st.metric(
        label="Avg. Unable to Afford Diet",
        value=f"{filtered_df['pct_unable_to_afford_diet'].mean():.1f}%",
        delta=f"{filtered_df['pct_unable_to_afford_diet'].pct_change().mean()*100:.1f}%"
    )

with col3:
    correlation = filtered_df['total_co2_emissions'].corr(filtered_df['pct_unable_to_afford_diet'])
    st.metric(
        label="Correlation Coefficient",
        value=f"{correlation:.2f}",
        delta="Negative" if correlation < 0 else "Positive"
    )

with col4:
    st.metric(
        label="Data Points",
        value=len(filtered_df),
        delta=f"{year_range[0]} - {year_range[1]}"
    )

# Charts
st.markdown('<p class="sub-header">Trend Analysis</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(filtered_df['year'], filtered_df['total_co2_emissions'], 'o-', linewidth=2.5, markersize=8)
    ax.set_xlabel('Year')
    ax.set_ylabel('CO2 Emissions (Million Tonnes)')
    ax.set_title('CO2 Emissions Trend')
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(filtered_df['year'], filtered_df['pct_unable_to_afford_diet'], 's-', color='#ff7f0e', linewidth=2.5, markersize=8)
    ax.set_xlabel('Year')
    ax.set_ylabel('% Unable to Afford Diet')
    ax.set_title('Diet Affordability Trend')
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)

# Scatter plot with regression
st.markdown('<p class="sub-header">Correlation Analysis</p>', unsafe_allow_html=True)

fig, ax = plt.subplots(figsize=(10, 6))
scatter = ax.scatter(
    filtered_df['total_co2_emissions'], 
    filtered_df['pct_unable_to_afford_diet'],
    s=100, alpha=0.7, edgecolor='black'
)

# Add labels
for i, row in filtered_df.iterrows():
    ax.annotate(row['year'], 
               (row['total_co2_emissions'], row['pct_unable_to_afford_diet']),
               xytext=(5, 5), textcoords='offset points', fontsize=9)

# Add trend line
z = np.polyfit(filtered_df['total_co2_emissions'], filtered_df['pct_unable_to_afford_diet'], 1)
p = np.poly1d(z)
ax.plot(filtered_df['total_co2_emissions'], p(filtered_df['total_co2_emissions']), 
        '--', color='red', alpha=0.7, 
        label=f'Trend (r = {correlation:.2f})')

ax.set_xlabel('CO2 Emissions (Million Tonnes)')
ax.set_ylabel('% Unable to Afford Diet')
ax.set_title('Correlation: CO2 vs Diet Affordability')
ax.legend()
ax.grid(True, alpha=0.3)
st.pyplot(fig)

# Data Table
st.markdown('<p class="sub-header">Raw Data</p>', unsafe_allow_html=True)
st.dataframe(
    filtered_df.style.format({
        'total_co2_emissions': '{:.1f}',
        'pct_unable_to_afford_diet': '{:.1f}%'
    }),
    use_container_width=True
)

# Insights section
st.markdown('<p class="sub-header">Key Insights</p>', unsafe_allow_html=True)

with st.expander("View Analysis Insights"):
    st.write("""
    **Trend Observations:**
    - CO2 emissions show a general downward trend from 2017-2023
    - Diet unaffordability remains persistently high (>60%) throughout the period
    - The relationship between the two variables is weak but negative
    
    **Statistical Findings:**
    - Correlation coefficient: {:.2f}
    - Average CO2 emissions: {:.1f} million tonnes
    - Average population unable to afford diet: {:.1f}%
    
    **Limitations:**
    - Short time series (7 years) limits longitudinal analysis
    - Multiple external factors may influence both variables
    - Correlation does not imply causation
    """.format(
        correlation,
        filtered_df['total_co2_emissions'].mean(),
        filtered_df['pct_unable_to_afford_diet'].mean()
    ))

# Footer
st.markdown("---")
st.markdown("""
**NDTA631 - Data Analysis and Visualization**  
*Group Assignment Submission*  
Data Source: World Bank Open Data  
Built with Streamlit & Python
""")