# Guvi Project Suite

**Complete Analytics & Learning Platform**

A comprehensive collection of production-ready data analytics applications and SQL learning platforms built with Streamlit.

---

## 📋 Projects Overview

### 1. 🛒 Amazon India Sales Analytics (`amazon_project/`)
**A Decade of Sales Analytics Dashboard**

Complete end-to-end data pipeline analyzing 10 years of Amazon India sales data with interactive dashboards and 30+ analytics questions.

**Key Features:**
- 📊 **6 Interactive Dashboards** - Executive Summary, Revenue, Customers, Products, Operations, Executive
- 📈 **20+ EDA Visualizations** - In-depth analysis with charts and insights
- 🗄️ **SQL Database** - Complete schema with fact and dimension tables
- 🧹 **Data Pipeline** - Cleaning → EDA → Database → Dashboards
- 💾 **Optimized Storage** - 266.8 MB CSV → 39.9 MB Parquet (85% compression)

**Tech Stack:**
- Streamlit (Frontend)
- Pandas, NumPy (Data Processing)
- Plotly (Visualizations)
- SQLite (Database)
- Python 3.8+

---

### 2. 🏏 Cricket Analytics Pro (`cric_buzz/`)
**Real-Time Cricket Insights Dashboard**

Interactive cricket analytics platform with live match data, player management, and SQL practice questions.

**Key Features:**
- 📊 **Live Scorecard** - Real-time match updates via Cricbuzz API
- 👥 **Player Management** - Full CRUD operations on 38 international cricketers
- 📚 **SQL Learning** - 25 interactive practice questions (Beginner to Advanced)
- 🏆 **Statistics** - Top performers, rankings, and analytics
- 🔌 **API Integration** - Real-time data from Cricbuzz Cricket API

**Tech Stack:**
- Streamlit (Frontend)
- MySQL 8.0 (Database)
- RapidAPI Integration (Cricbuzz)
- Pandas, NumPy (Data Processing)
- Python 3.8+

---

## 📁 Project Structure

```
Guvi_project/
├── README.md                          # This file
├── .gitignore                         # Git exclusions
│
├── amazon_project/                    # Main Analytics Project
│   ├── app_main.py                    # Main Streamlit app (1735 lines)
│   ├── dashboard.py                   # Data loading utilities
│   ├── requirements.txt               # Python dependencies
│   ├── dashboards/                    # 5 Dashboard modules
│   │   ├── revenue.py                 # Q6-Q10: Revenue Analytics
│   │   ├── customers.py               # Q11-Q15: Customer Analytics
│   │   ├── products.py                # Q16-Q20: Product Analytics
│   │   ├── operations.py              # Q21-Q25: Operations Analytics
│   │   └── executive.py               # Q26-Q30: Executive Summary
│   ├── eda/                           # EDA Analysis Functions
│   │   ├── advanced_analysis_1.py     # Revenue, Category, Geography analyses
│   │   ├── rfm_analysis.py            # RFM Segmentation
│   │   ├── festival_analysis.py       # Festival Impact Analysis
│   │   ├── payment_trends.py          # Payment Method Analysis
│   │   ├── seasonal_patterns.py       # Seasonality Detection
│   │   └── ... (other analyses)
│   ├── database/                      # Database Setup & Management
│   │   ├── schema.sql                 # Database schema (Fact & Dimension tables)
│   │   ├── db_config.py               # Database configuration
│   │   ├── db_analytics.py            # Analytical queries
│   │   ├── data_loader.py             # Bulk data loading
│   │   ├── create_tables.py           # Table creation scripts
│   │   └── queries.py                 # SQL query library
│   ├── data/                          # Data Folder
│   │   └── raw/                       # Raw data files
│   │       ├── amazon_india_*.csv     # Yearly transaction data (2015-2025)
│   │       ├── amazon_india_products_catalog.csv
│   │       ├── cleaned_transactions.csv (266.8 MB)
│   │       └── cleaned_transactions.parquet (39.9 MB)
│   ├── utils/                         # Utility Functions
│   ├── SQL_QUERIES_30_DASHBOARDS.sql  # Master SQL queries
│   └── README.md                      # Project documentation
│
└── cric_buzz/                         # Cricket Analytics Project
    ├── pages/                         # Streamlit pages
    │   ├── Cricket_SQL_Practice.py    # 25 SQL questions
    │   ├── CRUD_operations.py         # Player management
    │   ├── Live_Matches.py            # Real-time scorecards
    │   └── top_stats.py               # Player statistics
    ├── utils/                         # Utility modules
    │   ├── api_client.py              # Cricbuzz API client
    │   ├── db_connection.py           # MySQL connection
    │   ├── data_manager.py            # Data management
    │   └── style.py                   # UI styling
    ├── requirements.txt               # Dependencies
    └── README.md                      # Cricket project docs
```

---

## 🚀 Quick Start

### Prerequisites
```
Python 3.8 or higher
pip or conda package manager
```

### Installation

1. **Clone/Navigate to project:**
```bash
cd C:\Users\bhara\Guvi_project
```

2. **Install dependencies (Amazon Project):**
```bash
cd amazon_project
pip install -r requirements.txt
```

3. **Install dependencies (Cricket Project - Optional):**
```bash
cd ..\cric_buzz
pip install -r requirements.txt
```

---

## 🎯 Running the Applications

### Amazon India Sales Analytics

```bash
cd amazon_project
streamlit run app_main.py
```

**Access:** `http://localhost:8501`

**Available Pages:**
- 🏠 Home - Overview and navigation
- 📊 Visualization EDA - 20+ interactive charts
- 🧹 Data Cleaning Pipeline - Data quality checks
- 🗄️ SQL Database & Tables - Schema visualization
- 📈 Dashboard 25-30 Analytics - Executive dashboards

---

### Cricket Analytics Pro

```bash
cd ..\cric_buzz
streamlit run app.py
```

**Access:** `http://localhost:8502`

**Available Features:**
- 📊 Home - Dashboard overview
- 📊 Live Scorecard - Real-time matches
- 👥 Player Management - CRUD operations
- 🏆 Top Statistics - Leaderboards
- 🔍 SQL Analytics - Practice questions

---

## 📊 Amazon Project - 30 Analytics Questions

### Revenue Analytics (Q6-Q10)
- Q6: Revenue Trends Over Years
- Q7: Category-wise Revenue Distribution
- Q8: Geographic Revenue Performance
- Q9: Festival Impact on Sales
- Q10: Price vs Demand Analysis

### Customer Analytics (Q11-Q15)
- Q11: RFM Segmentation
- Q12: Customer Lifetime Value (CLV)
- Q13: Retention & Repeat Purchase Rate
- Q14: Customer Journey Analysis
- Q15: Churn Prediction Factors

### Product Analytics (Q16-Q20)
- Q16: Top Products by Revenue
- Q17: Category Performance
- Q18: Brand Comparison
- Q19: Price Elasticity
- Q20: Product Lifecycle Stage

### Operations Analytics (Q21-Q25)
- Q21: Delivery Performance
- Q22: Return Rate Analysis
- Q23: Payment Method Trends
- Q24: Order Processing Time
- Q25: Logistics Cost Optimization

### Executive Summary (Q26-Q30)
- Q26: Market Concentration Index
- Q27: Growth Rate Analysis
- Q28: Profitability by Segment
- Q29: Market Share Trends
- Q30: Strategic Recommendations

---

## 🛠️ Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Frontend** | Streamlit | Latest |
| **Data Processing** | Pandas, NumPy | Latest |
| **Visualization** | Plotly, Matplotlib | Latest |
| **Database** | SQLite/MySQL | 8.0+ |
| **Language** | Python | 3.8+ |
| **API** | Cricbuzz Cricket API | RapidAPI |

---

## 📂 Key Files for Git

### ✅ Include in Git Repository:
```
amazon_project/
├── app_main.py
├── dashboard.py
├── requirements.txt
├── dashboards/
├── eda/
├── database/
├── utils/
└── SQL_QUERIES_30_DASHBOARDS.sql

cric_buzz/
├── pages/
├── utils/
└── requirements.txt
```

### ❌ Exclude from Git:
```
# Data files (too large)
data/raw/*.csv
data/raw/*.parquet
data/processed/*.csv

# Python cache
__pycache__/
*.pyc
*.egg-info/

# Logs
*.log
.venv/
.env
```

### Recommended `.gitignore`:
```
# Data
amazon_project/data/raw/*.csv
amazon_project/data/raw/*.parquet
amazon_project/data/processed/*.csv

# Python
__pycache__/
*.pyc
*.pyo
*.egg-info/
.Python
.venv/
venv/

# Logs & temp
*.log
.streamlit/

# OS
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
*.swp
```

---

## 📈 Performance Metrics

### Amazon Project
- **Data Size:** 266.8 MB CSV → 39.9 MB Parquet (85% compression)
- **Load Time:** <5 seconds
- **Dashboard Queries:** <2 seconds
- **Total Records:** 10 years of transaction data
- **Code Size:** ~5000 lines across all modules

### Cricket Project
- **Database:** 38 international cricketers
- **SQL Queries:** 25 practice questions
- **API Response:** Real-time match updates
- **Player Roles:** Batsman, Bowler, All-rounder

---

## 🔧 Configuration

### Amazon Project Database
Located in `amazon_project/database/db_config.py`:
```python
{
    'host': 'localhost',
    'user': 'root',
    'password': 'root123',
    'database': 'amazon_india_analytics'
}
```

### Cricket Project Database
Located in `cric_buzz/utils/db_connection.py`:
```python
{
    'host': 'localhost',
    'user': 'root',
    'password': 'root123',
    'database': 'cricbuzz_db'
}
```

---

## 📚 Documentation

- **Amazon Project:** See `amazon_project/README.md`
- **Cricket Project:** See `cric_buzz/README.md`
- **SQL Queries:** See `amazon_project/SQL_QUERIES_30_DASHBOARDS.sql`
- **Database Schema:** See `amazon_project/database/schema.sql`

---

## ✨ Features Implemented

### Amazon Analytics
✅ End-to-end data pipeline (raw → cleaned → analyzed)
✅ 30 specific business questions answered
✅ Interactive Plotly visualizations
✅ Multi-page Streamlit application
✅ Database integration (SQLite)
✅ RFM, CLV, retention analysis
✅ Geographic heat maps
✅ Festival impact analysis
✅ Price elasticity modeling
✅ Error handling & fallback logic

### Cricket Analytics
✅ Real-time API integration
✅ CRUD player management
✅ SQL practice questions with solutions
✅ Player statistics & rankings
✅ Database CRUD operations
✅ Streamlit multi-page interface
✅ Pre-populated sample data
✅ Responsive UI design

---

## 🎓 Learning Outcomes

By working with this project suite, you'll learn:

**Data Engineering:**
- ETL pipeline design
- Data cleaning & validation
- Schema optimization
- Parquet format & compression

**Data Analysis:**
- EDA techniques
- Statistical modeling
- RFM & customer segmentation
- Time series analysis

**Web Development:**
- Streamlit application development
- Multi-page app architecture
- Interactive UI/UX design
- API integration

**Database:**
- SQL query optimization
- Fact & dimension table design
- Database normalization
- Query performance tuning

**Python Best Practices:**
- Code organization
- Error handling
- Documentation
- Version control

---

## 📞 Support & Troubleshooting

### Common Issues

1. **Data files not found:**
   - Ensure `data/raw/` folder contains CSV files
   - Check file paths in `dashboard.py`

2. **Database connection error:**
   - Verify MySQL/SQLite is running
   - Check credentials in `db_config.py`

3. **Missing dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Streamlit cache issues:**
   ```bash
   streamlit cache clear
   ```

---

## 📊 Project Statistics

| Metric | Value |
|--------|-------|
| **Total Python Files** | 40+ |
| **Lines of Code** | 8000+ |
| **Documentation Files** | 15+ |
| **SQL Queries** | 50+ |
| **Dashboard Pages** | 11 |
| **Analytics Questions** | 30+ |
| **Database Tables** | 8+ |
| **Visualizations** | 50+ |

---

## 🎯 Next Steps

1. **Clone/Fork the repository**
2. **Install dependencies** for desired project
3. **Run the application** (see Quick Start)
4. **Explore the dashboards** and data
5. **Modify and customize** for your use case

---

## 📄 License

This project suite is created for educational and learning purposes.

---

## ✅ Project Status

🟢 **Both Projects Complete and Production-Ready**

- ✅ All dashboards functional
- ✅ Database schema implemented
- ✅ Data pipelines tested
- ✅ Documentation complete
- ✅ Error handling in place
- ✅ Performance optimized

---

## 📅 Last Updated

January 2026

---

**Built with ❤️ for Data Analytics Learning**

For questions or improvements, review the individual project READMEs or check the source code documentation.
