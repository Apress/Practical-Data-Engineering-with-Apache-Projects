import streamlit as st
import pandas as pd
import plotly.express as px
from clickhouse_connect import get_client
from datetime import datetime, timedelta

# Set up ClickHouse connection
CLICKHOUSE_HOST = 'clickhouse'  # Replace with your ClickHouse host
CLICKHOUSE_PORT = 8123         # Default HTTP port
CLICKHOUSE_USER = 'default'
CLICKHOUSE_PASSWORD = 'mysecret'

client = get_client(host=CLICKHOUSE_HOST, port=CLICKHOUSE_PORT, username=CLICKHOUSE_USER, password=CLICKHOUSE_PASSWORD)

st.set_page_config(page_title="Flash Sale Performance Dashboard", layout="wide")
st.title("🛒 Flash Sale [FLASH2025] Performance")

# --- 1. Hourly breakdown of sales volume for the last 24 hours ---

st.header("Hourly Sales Volume (Last 24 Hours)")

hourly_sales_query = """
SELECT 
    toStartOfHour(created_at) AS hour,
    SUM(quantity) AS total_sales
FROM oneshop.purchases
WHERE deleted = 0
  AND created_at >= now() - INTERVAL 24 HOUR
GROUP BY hour
ORDER BY hour ASC
"""

hourly_sales_df = client.query_df(hourly_sales_query)

fig = px.bar(hourly_sales_df, x="hour", y="total_sales", title="Hourly Sales Volume (Past 24 Hours)", labels={"hour": "Hour", "total_sales": "Quantity Sold"})
st.plotly_chart(fig, use_container_width=True)

# --- 2. Top 10 most selling product IDs with their revenue ---

st.header("Top 10 Selling Product IDs by Revenue")
top_products_query = """
SELECT 
    item_id,
    SUM(quantity) AS total_quantity,
    SUM(quantity * purchase_price) AS total_revenue
FROM oneshop.purchases
GROUP BY item_id
ORDER BY total_revenue DESC
LIMIT 10
"""

top_products_df = client.query_df(top_products_query)
st.dataframe(top_products_df, use_container_width=True)



