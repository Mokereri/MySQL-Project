import psycopg2
import subprocess
import os
from urllib.parse import quote_plus
import pandas as pd
import streamlit as st
from threading import Thread 
from datetime import datetime
import time
from threading import Lock


host = 'ep-old-frost-a2278yc9.eu-central-1.aws.neon.tech'
database = 'robodine_db'
user = 'core_and_outline'
password = '3mQ3!YH2bkc8uYM5k$7wzr'

connection_string = f"postgresql://{user}:{quote_plus(password)}@{host}/{database}"

# Initialize a global lock
data_lock = Lock()
df = pd.DataFrame()

def fetch_data():
    """
    Connects to the Postgres database and retrieves the data.
    """
    conn = None  
    try:
        conn = psycopg2.connect(connection_string) 
        cur = conn.cursor()
        query = """
        SELECT
            i.id AS product_id,
            t.amount,
            i.created_at AS date,
            t.user_id,
            t.reference_occasion AS session_id,
            u.email AS contact,
            g.username AS name,
            g.profile_picture AS profile_picture,
            i.location,
            i.name AS product_name,
            i.price AS product_price,
            t.payment_status,
            t.amount AS total_revenue
        FROM
            transaction t
        JOIN
            "user" u ON t.user_id = u.id
        JOIN
            inventory i ON i.id = CAST(t.reference_occasion AS INTEGER)
        LEFT JOIN
            google_login g ON t.user_id = g.id
        WHERE
            t.payment_status = 'paid'
            AND t.reference_occasion ~ '^\d+$';
        """
        print("Executing query...")
        cur.execute(query)
        data = cur.fetchall()
        print(f"Number of rows fetched: {len(data)}")

        # Create a DataFrame
        df = pd.DataFrame(data, columns=[
            "product_id", "amount", "date", "user_id", "session_id",
            "contact", "name", "profile_picture", "location",
            "product_name", "product_price", "payment_status", "total_revenue"
        ])
        df['date'] = pd.to_datetime(df['date'])  # Ensure date column is datetime
        return df

    except Exception as e:
        print(f"Error fetching data: {e}")
        return pd.DataFrame()

    finally:
        # Close the connection only if it was successfully created
        if conn:
            cur.close()
            conn.close()


def sync_data_periodically(interval=86400):
    """
    Periodically fetches data every `interval` seconds.
    Default is 86400 seconds (24 hours).
    """
    global df
    while True:
        print(f"Auto-syncing data at {datetime.now()}...")
        df = fetch_data()
        print("Auto-sync completed.")
        time.sleep(interval)


auto_sync_thread = Thread(target=sync_data_periodically, args=(86400,), daemon=True)
auto_sync_thread.start()

# Streamlit Sidebar Navigation
st.sidebar.title("Hi User")

# Sidebar menu for navigation
section = st.sidebar.radio("Select a Section", ("Analytics", "Products", "Customers"))

# Streamlit Main Section based on Sidebar selection
if section == "Analytics":
    st.title("Robodine Analytics Dashboard")
    st.markdown("### Metrics Overview")
    with data_lock:
        local_df = df.copy()
    
    if local_df.empty:
        st.warning("Data is not available yet. Please wait for the initial sync or click 'Sync Now'.")
    else:
        # Metrics Calculation
        total_orders = local_df.shape[0]
        paid_orders = local_df[local_df['payment_status'] == 'paid'].shape[0]
        unique_users = local_df['user_id'].nunique()
        month_total = local_df['date'].dt.to_period('M').value_counts().max()
        revenue = local_df['amount'].sum()

        # Display Metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Orders", total_orders)
        col2.metric("Paid Orders", paid_orders)
        col3.metric("Users", unique_users)
        col4.metric("Month Total", month_total)
        col5.metric("Revenue", f"${revenue:,.2f}")
        
        # Sales Over Time (Bar Chart)
        st.markdown("### Sales Over Time")
        local_df['month'] = local_df['date'].dt.to_period('M')
        sales_over_time = local_df.groupby('month').size()

        fig, ax = plt.subplots()
        sales_over_time.plot(kind='bar', ax=ax, color='skyblue')
        ax.set_title("Sales Over Time")
        ax.set_xlabel("Month")
        ax.set_ylabel("Quantity")
        st.pyplot(fig)

        # Customer Orders Table
        st.markdown("### Customer Orders")
        customer_orders = local_df[[
            "profile_picture", "name", "location", "date", 
            "payment_status", "product_name", "amount"
        ]]
        st.dataframe(customer_orders)

elif section == "Products":
    st.title("Robodine Products Overview")
    st.markdown("### Products List")
    with data_lock:
        local_df = df.copy()

    if local_df.empty:
        st.warning("Data is not available yet. Please wait for the initial sync or click 'Sync Now'.")
    else:
        # List the products in the dataframe
        products = local_df[['product_name', 'product_price', 'amount']].drop_duplicates()
        st.dataframe(products)

elif section == "Customers":
    st.title("Robodine Customer Details")
    st.markdown("### Customers List")
    with data_lock:
        local_df = df.copy()

    if local_df.empty:
        st.warning("Data is not available yet. Please wait for the initial sync or click 'Sync Now'.")
    else:
        # List the customer details
        customers = local_df[['name', 'email', 'location']].drop_duplicates()
        st.dataframe(customers)
        

st.sidebar.markdown("### Update")
if st.sidebar.button("Sync Now"):
    df = fetch_data()
    st.sidebar.success(f"Dashboard updated successfully at {datetime.now()}.")
