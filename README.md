# 📊 PhonePe Pulse Analytics Dashboard

## 📌 Project Overview

The **PhonePe Pulse Analytics Dashboard** is a data analytics application built using **Python, MySQL, and Streamlit**. The project extracts PhonePe Pulse JSON data, loads it into a MySQL database, and provides interactive visualizations to analyze transaction trends, state-wise performance, and yearly growth.

---

## 🚀 Project Workflow

```text
PhonePe Pulse JSON Data
           │
           ▼
   data_process.py
 (Extract, Transform, Load)
           │
           ▼
      MySQL Database
           │
           ▼
         app.py
    (Streamlit Dashboard)
           │
           ▼
   Charts, KPIs & Insights
```

---

## 📂 Project Structure

```text
├── data_process.py      # ETL script for loading JSON data into MySQL
├── app.py               # Streamlit dashboard application
├── project.pdf          # Dashboard output and project results
├── data/                # PhonePe Pulse JSON dataset
└── README.md
```

---

## ⚙️ Components

### 1. data_process.py

This script is responsible for:

- Reading PhonePe Pulse JSON files
- Extracting transaction, insurance, and user data
- Transforming raw JSON into structured records
- Loading processed data into MySQL tables

#### Data Categories Processed

- Aggregated Transactions
- Aggregated Users
- User Device Data
- Map Transactions
- Map Users
- Top Transactions
- Top Users

#### Output Tables

- aggregated_transaction_insurance
- aggregated_user
- aggregated_user_device
- map_transaction_insurance
- map_user
- top_transaction_insurance
- top_user

---

### 2. app.py

This is the main Streamlit application used for data visualization.

#### Features

✅ Year-wise filtering

✅ KPI Metrics

- Total Transaction Amount
- Total Transaction Count

✅ Top 10 States Analysis

- Bar Chart

✅ State Contribution Analysis

- Pie Chart

✅ Year-wise Trend Analysis

- Line Chart

✅ Raw Data Viewer

---

### 3. project.pdf

Contains:

- Dashboard Screenshots
- Analysis Results
- Visualizations
- Insights Generated from the Dataset

---

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|----------|
| Python | Data Processing |
| MySQL | Database Storage |
| Streamlit | Dashboard Development |
| Pandas | Data Analysis |
| Matplotlib | Visualization |
| Seaborn | Visualization |
| JSON | Source Data Format |

---

## 🗄️ Database Setup

Create the database:

```sql
CREATE DATABASE phonepe_pulse;
```

Update database credentials in both files:

```python
mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="phonepe_pulse"
)
```

---

## 📦 Installation

### Clone Repository

```bash
git clone <repository-url>
cd phonepe-pulse-dashboard
```

### Install Dependencies

```bash
pip install pandas
pip install streamlit
pip install matplotlib
pip install seaborn
pip install mysql-connector-python
```

Or:

```bash
pip install -r requirements.txt
```

---

## ▶️ Run ETL Process

Load JSON data into MySQL:

```bash
python data_process.py
```

Expected Output:

```text
Processing Aggregated...
Processing Map...
Processing Top...
✅ DATA INSERTED INTO MYSQL SUCCESSFULLY
```

---

## ▶️ Run Streamlit Dashboard

Start the application:

```bash
streamlit run app.py
```

Open in browser:

```text
http://localhost:8501
```

---

## 📈 Dashboard Insights

The dashboard provides:

### KPI Metrics

- Total Transaction Amount
- Total Transactions

### State Analysis

- Top 10 States by Transaction Amount
- State-wise Contribution

### Trend Analysis

- Year-wise Transaction Growth
- Transaction Volume Trends

### Data Exploration

- Interactive Filters
- Raw Data Display

---

## 📑 Project Results

Detailed outputs, dashboard screenshots, and analysis results can be found in:

```text
project.pdf
```

---

