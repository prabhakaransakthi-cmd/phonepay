import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import mysql.connector

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="PhonePe Analytics", layout="wide")

st.title("📊 PhonePe Transaction Dashboard")

# -------------------------------
# DB CONNECTION
# -------------------------------
@st.cache_resource
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="phonepe_pulse"
    )

conn = get_connection()

# -------------------------------
# FETCH DATA
# -------------------------------
@st.cache_data
def load_data():
    query = """
    SELECT state, year, SUM(amount) AS total_amount, SUM(count) AS total_count
    FROM map_transaction_insurance
    GROUP BY state, year
    """
    return pd.read_sql(query, conn)

df = load_data()

# -------------------------------
# SIDEBAR FILTERS
# -------------------------------
st.sidebar.header("Filters")

selected_year = st.sidebar.selectbox(
    "Select Year",
    sorted(df["year"].unique())
)

filtered_df = df[df["year"] == selected_year]

# -------------------------------
# TOP STATES
# -------------------------------
top_states = filtered_df.groupby("state").sum().reset_index()
top_states = top_states.sort_values(by="total_amount", ascending=False).head(10)

# -------------------------------
# KPI METRICS
# -------------------------------
col1, col2 = st.columns(2)

col1.metric("Total Amount", f"{filtered_df['total_amount'].sum():,.0f}")
col2.metric("Total Transactions", f"{filtered_df['total_count'].sum():,.0f}")

# -------------------------------
# BAR CHART
# -------------------------------
st.subheader("🏆 Top 10 States by Amount")

fig, ax = plt.subplots()
sns.barplot(data=top_states, x="total_amount", y="state", ax=ax)
st.pyplot(fig)

# -------------------------------
# PIE CHART
# -------------------------------
st.subheader("📊 Contribution by State")

fig2, ax2 = plt.subplots()
ax2.pie(
    top_states["total_amount"],
    labels=top_states["state"],
    autopct="%1.1f%%",
    startangle=140
)
st.pyplot(fig2)

# -------------------------------
# YEARLY TREND
# -------------------------------
st.subheader("📈 Year-wise Trend")

year_df = df.groupby("year").sum().reset_index()

fig3, ax3 = plt.subplots()
sns.lineplot(data=year_df, x="year", y="total_amount", ax=ax3)
st.pyplot(fig3)

# -------------------------------
# RAW DATA (OPTIONAL)
# -------------------------------
if st.checkbox("Show Raw Data"):
    st.dataframe(df)