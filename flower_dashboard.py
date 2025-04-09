import streamlit as st
import pymysql
import pandas as pd
import plotly.express as px

# Database connection
def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="Kay@2030",  
        database="molvin_db"
    )

# Fetch data from MySQL
def fetch_data(query):
    conn = get_connection()
    data = pd.read_sql(query, conn)
    conn.close()
    return data

# Queries
query_orders = "SELECT COUNT(order_id) AS total_orders, SUM(total_amount) AS revenue FROM orders_table;"
query_sales = "SELECT SUM(quantity) AS total_quantity, SUM(total_price) AS total_revenue FROM sales_table;"
query_most_ordered = """
SELECT product_name, SUM(quantity) AS total_quantity 
FROM sales_table 
JOIN products_table ON sales_table.product_id = products_table.product_id 
GROUP BY product_name 
ORDER BY total_quantity DESC LIMIT 1;
"""
query_profit_margin = """
SELECT 
    SUM((price * quantity) - total_price) AS profit_margin 
FROM sales_table 
JOIN products_table ON sales_table.product_id = products_table.product_id;
"""
query_revenue_by_time = """
SELECT DATE(sale_date) AS sale_date, SUM(total_price) AS revenue 
FROM sales_table 
GROUP BY DATE(sale_date)
ORDER BY sale_date;
"""

# Streamlit App
st.set_page_config(page_title="Molvin Petals Export Dashboard", layout="wide")

# Sidebar filters
st.sidebar.header("Filters")
selected_day = st.sidebar.selectbox(
    "Day", ["All", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], index=0
)
selected_month = st.sidebar.selectbox(
    "Month", ["All", "Jan", "Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sep", "Oct", "Nov", "Dec"], index=0
)
selected_year = st.sidebar.selectbox(
    "Year", ["All", 2024, 2025], index=0
)

# Main Dashboard
st.title("Molvin Analytics Dashboard")

# Fetch data
total_orders_data = fetch_data(query_orders)
total_sales_data = fetch_data(query_sales)
most_ordered_data = fetch_data(query_most_ordered)
profit_margin_data = fetch_data(query_profit_margin)
revenue_by_time_data = fetch_data(query_revenue_by_time)

# Apply filters dynamically
if selected_day != "All":
    st.warning("Filtering by day is not yet implemented.")
if selected_month != "All":
    st.warning("Filtering by month is not yet implemented.")
if selected_year != "All":
    st.warning("Filtering by year is not yet implemented.")

# Metrics cards
st.subheader("Key Metrics")
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Orders", int(total_orders_data['total_orders'][0]))
col2.metric("Quantity Sold", int(total_sales_data['total_quantity'][0]))
col3.metric("Revenue", f"${total_sales_data['total_revenue'][0]:,.2f}")
col4.metric("Profit Margin", f"${profit_margin_data['profit_margin'][0]:,.2f}")
col5.metric("Most Ordered Product", most_ordered_data['product_name'][0])

# Line chart for revenue over time
st.subheader("Revenue Over Time")
fig = px.line(revenue_by_time_data, x="sale_date", y="revenue", title="Revenue by Date")
st.plotly_chart(fig, use_container_width=True)

