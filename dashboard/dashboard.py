import streamlit as st
import pandas as pd
import plotly.express as px

# Config
st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")

# Custom CSS 
st.markdown("""
<style>
.main {
    background-color: #f8fafc;
}
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('dashboard/main_data_clean.csv')
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
    df['year_month'] = df['order_purchase_timestamp'].dt.to_period('M').astype(str)
    return df

df = load_data()

# Title
st.title("📊 E-Commerce Dashboard")
st.caption("Sales performance & customer behavior analysis")

# Sidebar
state = st.sidebar.multiselect(
    "Select State",
    df['customer_state'].unique(),
    default=df['customer_state'].unique()
)

df = df[df['customer_state'].isin(state)]

# ================= KPI =================
total_orders = len(df)
total_revenue = df['price'].sum()
avg_delivery = df['delivery_time'].mean()

col1, col2, col3 = st.columns(3)

col1.metric("📦 Orders", total_orders)
col2.metric("💰 Revenue", f"${total_revenue:,.0f}")
col3.metric("🚚 Delivery", f"{avg_delivery:.1f} days")

# Insight otomatis
if total_revenue > 100000:
    st.success("Revenue is performing well 💰")
else:
    st.warning("Revenue needs improvement 📉")

st.divider()

# ================= SALES TREND =================
sales_trend = df.groupby('year_month')['order_id'].count().reset_index()

fig = px.line(
    sales_trend,
    x='year_month',
    y='order_id',
    title="📈 Monthly Orders Trend",
    markers=True
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# ================= CATEGORY =================
col1, col2 = st.columns(2)

with col1:
    top_category = df.groupby('product_category_name_english')['price'] \
                     .sum().sort_values(ascending=False).head(10).reset_index()

    fig = px.bar(
        top_category,
        x='price',
        y='product_category_name_english',
        orientation='h',
        title="💰 Top Categories by Revenue"
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:
    payment = df['payment_type'].value_counts().reset_index()
    payment.columns = ['payment_type', 'count']

    fig = px.pie(
        payment,
        names='payment_type',
        values='count',
        title="💳 Payment Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

st.divider()

# ================= LOCATION & DELIVERY =================
col1, col2 = st.columns(2)

with col1:
    location = df['customer_state'].value_counts().head(10).reset_index()
    location.columns = ['state', 'count']

    fig = px.bar(
        location,
        x='state',
        y='count',
        title="🌍 Top Customer States"
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:
    late = df['late_delivery'].value_counts().reset_index()
    late.columns = ['late', 'count']

    fig = px.bar(
        late,
        x='late',
        y='count',
        title="🚚 Delivery Performance"
    )

    st.plotly_chart(fig, use_container_width=True)