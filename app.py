import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="Superstore Dashboard", layout="wide")

# -----------------------------
# Title
# -----------------------------
st.title("📊 Superstore Data Dashboard")
st.markdown("### Analyze Sales, Profit, and Business Performance")

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv('Superstore Dataset/Sample - Superstore.csv', encoding='latin1')
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Year'] = df['Order Date'].dt.year
    df['Month'] = df['Order Date'].dt.to_period('M')
    return df

df = load_data()

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("🔍 Filters")

region = st.sidebar.multiselect("Region", df['Region'].unique(), df['Region'].unique())
category = st.sidebar.multiselect("Category", df['Category'].unique(), df['Category'].unique())
year = st.sidebar.multiselect("Year", df['Year'].unique(), df['Year'].unique())

filtered_df = df[
    (df['Region'].isin(region)) &
    (df['Category'].isin(category)) &
    (df['Year'].isin(year))
]

if filtered_df.empty:
    st.warning("⚠️ No data available")
    st.stop()

# -----------------------------
# KPI CARDS
# -----------------------------
st.markdown("## 📌 Key Performance Indicators")

total_sales = filtered_df['Sales'].sum()
total_profit = filtered_df['Profit'].sum()
profit_margin = total_profit / total_sales if total_sales != 0 else 0
best_region = filtered_df.groupby('Region')['Sales'].sum().idxmax()

col1, col2, col3, col4 = st.columns(4)

col1.markdown(f"""
<div style="background: linear-gradient(135deg, #4facfe, #00f2fe);
            padding:20px; border-radius:12px; text-align:center; color:white;">
    <h4>💰 Revenue</h4>
    <h2>${total_sales:,.0f}</h2>
</div>
""", unsafe_allow_html=True)

col2.markdown(f"""
<div style="background: linear-gradient(135deg, #43e97b, #38f9d7);
            padding:20px; border-radius:12px; text-align:center; color:white;">
    <h4>📈 Profit</h4>
    <h2>${total_profit:,.0f}</h2>
</div>
""", unsafe_allow_html=True)

col3.markdown(f"""
<div style="background: linear-gradient(135deg, #fa709a, #fee140);
            padding:20px; border-radius:12px; text-align:center; color:white;">
    <h4>📊 Margin</h4>
    <h2>{profit_margin:.2%}</h2>
</div>
""", unsafe_allow_html=True)

col4.markdown(f"""
<div style="background: linear-gradient(135deg, #667eea, #764ba2);
            padding:20px; border-radius:12px; text-align:center; color:white;">
    <h4>🏆 Best Region</h4>
    <h2>{best_region}</h2>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# -----------------------------
# Chart Style
# -----------------------------
sns.set_theme(style="whitegrid")

# -----------------------------
# Row 1: Sales & Profit
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("🌍 Sales by Region")

    region_sales = filtered_df.groupby('Region')['Sales'].sum().sort_values(ascending=False)
    colors = sns.color_palette("viridis", len(region_sales))

    fig1, ax1 = plt.subplots(figsize=(8, 4))
    bars = ax1.bar(region_sales.index, region_sales.values, color=colors)

    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2, height, f'{height:,.0f}', 
                 ha='center', va='bottom')

    ax1.set_ylabel("Sales")
    plt.tight_layout()
    st.pyplot(fig1)

with col2:
    st.subheader("📦 Profit by Category")

    category_profit = filtered_df.groupby('Category')['Profit'].sum().sort_values(ascending=False)
    colors = sns.color_palette("magma", len(category_profit))

    fig2, ax2 = plt.subplots(figsize=(8, 4))
    bars = ax2.bar(category_profit.index, category_profit.values, color=colors)

    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2, height, f'{height:,.0f}', 
                 ha='center', va='bottom')

    ax2.set_ylabel("Profit")
    plt.tight_layout()
    st.pyplot(fig2)

# -----------------------------
# Row 2: Monthly & Yearly Trend
# -----------------------------
col3, col4 = st.columns(2)

with col3:
    st.subheader("📅 Monthly Revenue Trend")

    monthly_sales = filtered_df.groupby('Month')['Sales'].sum()

    fig3, ax3 = plt.subplots(figsize=(8, 3))
    monthly_sales.plot(color='blue', linewidth=2, ax=ax3)

    ax3.set_ylabel("Sales")
    plt.tight_layout()
    st.pyplot(fig3)

with col4:
    st.subheader("📈 Sales Over Time")

    sales_trend = filtered_df.groupby('Year')['Sales'].sum()

    fig8, ax8 = plt.subplots(figsize=(8, 3))

    ax8.plot(
        sales_trend.index,
        sales_trend.values,
        marker='o',
        linewidth=2
    )

    for x, y in zip(sales_trend.index, sales_trend.values):
        ax8.text(x, y, f"{y:,.0f}", ha='center', va='bottom')

    ax8.set_xlabel("Year")
    ax8.set_ylabel("Sales")

    plt.tight_layout()
    st.pyplot(fig8)

# -----------------------------
# Row 3: Products & Scatter
# -----------------------------
col5, col6 = st.columns(2)

with col5:
    st.subheader("🏆 Top 10 Products")

    top_products = filtered_df.groupby('Product Name')['Sales'] \
                              .sum() \
                              .sort_values(ascending=False) \
                              .head(10)

    # Fix long labels
    top_products.index = top_products.index.str[:30]

    fig4, ax4 = plt.subplots(figsize=(8, 4))

    top_products.plot(kind='barh', color='purple', ax=ax4)

    ax4.tick_params(axis='y', labelsize=8)

    for i, v in enumerate(top_products.values):
        ax4.text(v, i, f"{v:,.0f}", va='center')

    plt.tight_layout()
    st.pyplot(fig4)

with col6:
    st.subheader("📊 Sales vs Profit")

    fig5, ax5 = plt.subplots(figsize=(8, 4))

    sns.scatterplot(
        x='Sales',
        y='Profit',
        data=filtered_df,
        hue='Category',
        ax=ax5
    )

    plt.tight_layout()
    st.pyplot(fig5)

# -----------------------------
# Row 4: Distribution & Heatmap
# -----------------------------
col7, col8 = st.columns(2)

with col7:
    st.subheader("📉 Sales Distribution")

    fig6, ax6 = plt.subplots(figsize=(8, 4))

    sns.histplot(filtered_df['Sales'], bins=40, kde=True, color='skyblue', ax=ax6)

    ax6.set_xscale('log')
    plt.tight_layout()
    st.pyplot(fig6)

with col8:
    st.subheader("🔥 Correlation Heatmap")

    fig7, ax7 = plt.subplots(figsize=(8, 4))

    sns.heatmap(filtered_df.corr(numeric_only=True), annot=True, cmap='coolwarm', ax=ax7)

    plt.tight_layout()
    st.pyplot(fig7)

# -----------------------------
# Download Button
# -----------------------------
st.markdown("---")

st.download_button(
    "⬇️ Download Filtered Data",
    filtered_df.to_csv(index=False),
    file_name="filtered_data.csv"
)