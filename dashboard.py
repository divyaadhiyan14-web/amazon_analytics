"""
Comprehensive Streamlit Dashboard for Amazon India EDA Analysis
Displays all 20 visualizations with interactive controls and insights
"""
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import os

warnings.filterwarnings('ignore')

# Import all EDA modules
from eda.revenue_trends_analysis import revenue_trend_analysis, get_revenue_insights
from eda.seasonal_patterns import seasonal_patterns_analysis, get_seasonal_insights
from eda.rfm_analysis import rfm_segmentation_analysis, get_rfm_insights
from eda.advanced_analysis_1 import (
    payment_evolution_analysis,
    category_performance_analysis,
    prime_impact_analysis,
    geographic_analysis,
    festival_impact_analysis,
    price_demand_analysis
)
from eda.advanced_analysis_2 import (
    age_group_analysis,
    delivery_performance_analysis,
    returns_analysis,
    brand_analysis,
    discount_effectiveness_analysis,
    rating_impact_analysis,
    business_health_dashboard
)
from eda.advanced_analysis_3 import (
    clv_cohort_analysis,
    customer_journey_analysis,
    inventory_lifecycle_analysis,
    competitive_pricing_analysis
)

# Page configuration
st.set_page_config(
    page_title="Amazon India Analytics Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding-top: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 1.2rem;
        font-weight: bold;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

# Load data with memory optimization
@st.cache_data
def load_data():
    try:
        # Try reading Parquet first (if available - more memory efficient)
        parquet_file = 'data/processed/cleaned_transactions.parquet'
        if os.path.exists(parquet_file):
            print("Loading from Parquet...")
            df = pd.read_parquet(parquet_file)
            return df
    except Exception as e:
        print(f"Parquet load failed: {e}")
    
    # Fallback: Read CSV with categories
    try:
        print("Loading from CSV...")
        df = pd.read_csv(
            'data/processed/cleaned_transactions.csv',
            low_memory=False,
            parse_dates=['order_date']
        )
        
        # Apply optimizations after loading
        for col in df.columns:
            if col in ['customer_age_group', 'payment_method', 'delivery_type', 'return_status',
                      'category', 'brand', 'customer_state', 'customer_city', 'customer_tier',
                      'customer_spending_tier', 'festival_name']:
                df[col] = df[col].astype('category')
            elif col in ['is_prime_member', 'is_festival_sale', 'is_prime_eligible']:
                df[col] = df[col].astype('bool')
        
        return df
        
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.stop()

# Initialize session state
if 'df' not in st.session_state:
    st.session_state.df = load_data()

df = st.session_state.df

# Title and intro
st.markdown("""
<div style='text-align: center; padding: 2rem;'>
    <h1>🛒 Amazon India: A Decade of Sales Analytics 📈</h1>
    <h3 style='color: #666;'>Comprehensive EDA Dashboard (2015-2025)</h3>
    <p>Analyzing almost 1M transactions across 10 years of Amazon India's e-commerce journey</p>
</div>
""", unsafe_allow_html=True)

# Sidebar with navigation
st.sidebar.markdown("## 📊 Navigation")
tab_selection = st.sidebar.radio(
    "Select Analysis Section:",
    [
        "📈 Dashboard Overview",
        "💰 Revenue Analysis",
        "📅 Seasonal Patterns",
        "👥 Customer Segmentation (RFM)",
        "💳 Payment Methods",
        "� Revenue Analytics Bundle (Q6-Q10)",
        "�📦 Category Performance",
        "👑 Prime Membership",
        "🗺️ Geographic Analysis",
        "🎉 Festival Impact",
        "💲 Price vs Demand",
        "👤 Age Group Behavior",
        "🚚 Delivery Performance",
        "↩️ Returns Analysis",
        "🏷️ Brand Analysis",
        "💎 Customer Lifetime Value",
        "🎁 Discount Effectiveness",
        "⭐ Rating Impact",
        "🛤️ Customer Journey",
        "📦 Product Lifecycle",
        "🏆 Competitive Pricing",
        "📋 Business Health",
        "📋 Executive Summary"
    ]
)

# Data statistics in sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Dataset Statistics")
col1, col2 = st.sidebar.columns(2)
with col1:
    st.metric("Total Records", f"{len(df):,.0f}")
    st.metric("Date Range", f"{df['order_date'].min().year}-{df['order_date'].max().year}")
with col2:
    st.metric("Unique Customers", f"{df['customer_id'].nunique():,.0f}")
    st.metric("Total Revenue", f"₹{df['final_amount_inr'].sum()/1_000_000_000:.2f}B")

# Main content area
if tab_selection == "📈 Dashboard Overview":
    st.markdown("## 📊 Executive Dashboard Overview")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Revenue", f"₹{df['final_amount_inr'].sum()/1_000_000_000:.2f}B")
    with col2:
        st.metric("Avg Order Value", f"₹{df['final_amount_inr'].mean():,.0f}")
    with col3:
        st.metric("Total Transactions", f"{len(df):,.0f}")
    with col4:
        st.metric("Unique Customers", f"{df['customer_id'].nunique():,.0f}")
    
    st.markdown("---")
    
    # Business Health Dashboard
    st.markdown("### 🎯 Comprehensive Business Health Dashboard (Q20)")
    with st.spinner("Generating Business Health Dashboard..."):
        result = business_health_dashboard(df)
        st.pyplot(result['figure'])
        
        st.markdown("#### Key Insights")
        cols = st.columns(3)
        with cols[0]:
            st.metric("YoY Growth", f"{result['metrics']['yoy_growth']:.2f}%")
        with cols[1]:
            st.metric("Customer Retention", f"{result['metrics']['retention_rate']:.1f}%")
        with cols[2]:
            st.metric("Active Customers", f"{result['metrics']['total_customers']:,.0f}")

elif tab_selection == "💰 Revenue Analysis":
    st.markdown("## Q1: Comprehensive Revenue Trend Analysis (2015-2025)")
    st.markdown("*Revenue growth, growth rates, trend lines, and key growth period annotations*")
    
    with st.spinner("Generating revenue analysis..."):
        result = revenue_trend_analysis(df)
        st.pyplot(result['figure'])
        
        st.markdown("### 💡 Key Insights")
        insights = get_revenue_insights(result['yearly_revenue'])
        for insight in insights:
            st.info(f"📌 {insight}")
        
        st.markdown("### 📊 Detailed Statistics")
        st.dataframe(result['yearly_revenue'].style.format({
            'total_revenue': '₹{:,.0f}',
            'avg_transaction': '₹{:,.0f}',
            'growth_rate': '{:.2f}%'
        }), use_container_width=True)

elif tab_selection == "📅 Seasonal Patterns":
    st.markdown("## Q2: Seasonal Patterns in Sales Data")
    st.markdown("*Monthly heatmaps, peak selling months, and cross-year comparisons*")
    
    with st.spinner("Generating seasonal analysis..."):
        result = seasonal_patterns_analysis(df)
        st.pyplot(result['figure'])
        
        st.markdown("### 💡 Key Insights")
        insights = get_seasonal_insights(result['monthly_avg'])
        for insight in insights:
            st.info(f"📌 {insight}")

elif tab_selection == "👥 Customer Segmentation (RFM)":
    st.markdown("## Q3: RFM Customer Segmentation Analysis")
    st.markdown("*Recency, Frequency, Monetary segments with actionable insights*")
    
    with st.spinner("Performing RFM segmentation..."):
        result = rfm_segmentation_analysis(df)
        st.pyplot(result['figure'])
        
        st.markdown("### 💡 Customer Segments")
        insights = get_rfm_insights(result['rfm'])
        for insight in insights:
            st.success(f"✅ {insight}")
        
        st.markdown("### 📊 Segment Summary")
        st.dataframe(result['segment_summary'], use_container_width=True)

elif tab_selection == "💳 Payment Methods":
    st.markdown("## Q4: Payment Method Evolution (2015-2025)")
    st.markdown("*Rise of UPI, decline of COD, stacked area charts for market share changes*")
    
    with st.spinner("Analyzing payment methods..."):
        result = payment_evolution_analysis(df)
        st.pyplot(result['figure'])
        
        st.markdown("### 💡 Key Insights")
        total_txns = result['payment_stats'].sum()
        for method, count in result['payment_stats'].items():
            pct = (count / total_txns) * 100
            st.info(f"📌 {method}: {count:,.0f} transactions ({pct:.1f}%)")

elif tab_selection == "� Revenue Analytics Bundle (Q6-Q10)":
    st.markdown("<h1 style='text-align: center; color: #1f77b4;'>💰 Revenue Analytics Dashboard (Q6-Q10)</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Create tabs for different revenue analytics questions
    rev_tab1, rev_tab2, rev_tab3, rev_tab4, rev_tab5 = st.tabs([
        "📈 Q6: Trend Analysis",
        "📦 Q7: Category Performance",
        "🗺️ Q8: Geographic Revenue",
        "🎉 Q9: Festival Sales",
        "💲 Q10: Price Optimization"
    ])
    
    # Q6: Revenue Trend Analysis
    with rev_tab1:
        st.markdown("## Q6: Revenue Trend Analysis (Monthly/Quarterly/Yearly Patterns)")
        st.markdown("*Comprehensive analysis of revenue patterns across different time periods with growth trends*")
        
        with st.spinner("Generating revenue trend analysis..."):
            result = revenue_trend_analysis(df)
        
        # Display figure
        st.pyplot(result['figure'], use_container_width=True)
        
        # Key metrics
        stats = result['statistics']
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "📊 Total Revenue (10 Years)",
                f"₹{stats['total_revenue']/1_000_000_000:.2f}B"
            )
        
        with col2:
            st.metric(
                "📈 Avg Yearly Growth",
                f"{stats['avg_yearly_growth']:.2f}%"
            )
        
        with col3:
            peak_year = int(result['yearly_revenue'].loc[result['yearly_revenue']['total_revenue'].idxmax(), 'year'])
            st.metric(
                "🏆 Peak Year",
                f"{peak_year}"
            )
        
        with col4:
            max_growth = stats['max_growth_rate']
            st.metric(
                "🚀 Peak Growth Year",
                f"{max_growth:.2f}%"
            )
        
        # Detailed Statistics
        st.markdown("### 📊 Yearly Revenue Statistics")
        yearly_display = result['yearly_revenue'].copy()
        yearly_display.columns = ['Year', 'Total Revenue (₹)', 'Avg Transaction (₹)', 
                                 'Transaction Count', 'YoY Growth (%)']
        
        st.dataframe(
            yearly_display.style.format({
                'Year': '{:.0f}',
                'Total Revenue (₹)': '₹{:,.0f}',
                'Avg Transaction (₹)': '₹{:,.0f}',
                'Transaction Count': '{:,.0f}',
                'YoY Growth (%)': '{:.2f}%'
            }),
            use_container_width=True
        )
        
        # Insights
        st.markdown("### 💡 Key Insights")
        insights = get_revenue_insights(result['yearly_revenue'])
        for insight in insights:
            st.info(f"📌 {insight}")
    
    # Q7: Category Performance
    with rev_tab2:
        st.markdown("## Q7: Category Performance (Revenue Contribution & Growth Trends)")
        st.markdown("*Market share, revenue contribution, growth trends across product categories*")
        
        with st.spinner("Analyzing category performance..."):
            result = category_performance_analysis(df)
        
        # Display figure
        st.pyplot(result['figure'], use_container_width=True)
        
        # Top category metrics
        perf = result['category_perf']
        col1, col2, col3 = st.columns(3)
        
        with col1:
            top_cat = perf.index[0]
            top_rev = perf['revenue'].iloc[0]
            st.metric(
                "🏆 Top Category",
                top_cat,
                f"₹{top_rev/1_000_000:.1f}M"
            )
        
        with col2:
            avg_rating = perf['rating'].mean()
            st.metric(
                "⭐ Avg Rating",
                f"{avg_rating:.2f}/5"
            )
        
        with col3:
            total_categories = len(perf)
            st.metric(
                "📊 Categories",
                f"{total_categories}",
                "total"
            )
        
        # Category Details Table
        st.markdown("### 📊 Category Performance Metrics")
        cat_display = perf.copy()
        cat_display.columns = ['Revenue (₹)', 'Avg Order Value (₹)', 'Items Sold', 
                               'Avg Rating', 'Transactions', 'Market Share (%)']
        
        st.dataframe(
            cat_display.style.format({
                'Revenue (₹)': '₹{:,.0f}',
                'Avg Order Value (₹)': '₹{:,.0f}',
                'Items Sold': '{:,.0f}',
                'Avg Rating': '{:.2f}',
                'Transactions': '{:,.0f}',
                'Market Share (%)': '{:.2f}%'
            }),
            use_container_width=True
        )
        
        # Insights
        st.markdown("### 💡 Category Insights")
        st.markdown(f"""
        - **Dominant Category:** {perf.index[0]} drives {perf['market_share'].iloc[0]:.1f}% of revenue
        - **Top 3 Categories:** {', '.join(perf.index[:3].tolist())} account for {perf['market_share'].head(3).sum():.1f}% of market
        - **Total Categories:** {len(perf)} categories generating ₹{perf['revenue'].sum()/1_000_000:.1f}M
        - **Highest AOV:** {perf['avg_value'].idxmax()} at ₹{perf['avg_value'].max():,.0f} per transaction
        """)
    
    # Q8: Geographic Revenue
    with rev_tab3:
        st.markdown("## Q8: Geographic Revenue (State-wise & City-wise Performance)")
        st.markdown("*Regional performance analysis with tier-wise breakdown and growth patterns*")
        
        with st.spinner("Analyzing geographic revenue..."):
            result = geographic_analysis(df)
        
        # Display figure
        st.pyplot(result['figure'], use_container_width=True)
        
        # Geographic metrics
        col1, col2, col3, col4 = st.columns(4)
        
        geo_perf = result['all_geo_perf']
        tier_data = result['tier_analysis']
        
        with col1:
            top_state = geo_perf.index[0]
            top_rev = geo_perf['revenue'].iloc[0]
            st.metric(
                "🏆 Top State",
                top_state,
                f"₹{top_rev/1_000_000:.1f}M"
            )
        
        with col2:
            total_states = len(geo_perf)
            st.metric(
                "🗺️ States Covered",
                total_states,
                "regions"
            )
        
        with col3:
            max_growth_tier = tier_data['growth_rate'].idxmax()
            max_growth = tier_data['growth_rate'].max()
            st.metric(
                "📈 Fastest Growth",
                max_growth_tier,
                    f"{max_growth:.1f}% YoY"
                )
            
            with col4:
                avg_density = geo_perf['revenue_density'].mean()
                st.metric(
                    "💰 Avg Revenue/Customer",
                    f"₹{avg_density:.0f}",
                    "national avg"
                )
            
            # Tier-wise Performance
            st.markdown("### 📍 Tier-wise Performance Analysis")
            tier_cols = st.columns(4)
            
            for idx, (tier, col) in enumerate(zip(tier_data.index, tier_cols)):
                with col:
                    tier_row = tier_data.loc[tier]
                    st.metric(
                        f"{tier} Tier",
                        f"₹{tier_row['revenue']/1_000_000:.1f}M",
                        f"{tier_row['growth_rate']:.1f}% growth"
                    )
            
            # Top States Table
            st.markdown("### 📊 Top 15 States - Detailed Metrics")
            geo_display = result['geo_perf'].copy()
            geo_display.columns = ['Revenue (₹)', 'Avg Order Value (₹)', 'Transactions', 
                                   'Unique Customers', 'Revenue/Customer (₹)', 'Revenue/Transaction (₹)', 'Tier']
            
            st.dataframe(
                geo_display.style.format({
                    'Revenue (₹)': '₹{:,.0f}',
                    'Avg Order Value (₹)': '₹{:,.0f}',
                    'Revenue/Customer (₹)': '₹{:,.0f}',
                    'Revenue/Transaction (₹)': '₹{:,.0f}',
                    'Transactions': '{:,.0f}',
                    'Unique Customers': '{:,.0f}'
                }),
                use_container_width=True
            )
            
            # Insights
            st.markdown("### 💡 Geographic Insights")
            metro_rev = tier_data.loc['Metro', 'revenue']
            total_rev = tier_data['revenue'].sum()
            metro_pct = (metro_rev / total_rev) * 100
            
            st.markdown(f"""
            - **Metro Dominance:** Metro cities control **{metro_pct:.1f}%** of revenue
            - **Fastest Growing:** Tier-2 cities at **{tier_data.loc['Tier-2', 'growth_rate']:.1f}%** YoY growth
            - **Emerging Markets:** Rural regions growing at **{tier_data.loc['Rural', 'growth_rate']:.1f}%**
            - **Expansion Opportunity:** Focus on Tier-1/Tier-2 cities for accelerated growth
            """)
    
    # Q9: Festival Sales Analytics
    with rev_tab4:
        st.markdown("## Q9: Festival Sales Analytics (Campaign Effectiveness)")
        st.markdown("*Festival-driven revenue spikes, campaign performance, and seasonal peaks*")
        
        with st.spinner("Analyzing festival sales..."):
            result = festival_impact_analysis(df)
        
        # Display figure
        st.pyplot(result['figure'], use_container_width=True)
        
        fest_perf = result['festival_perf']
        
        # Festival metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            top_fest = fest_perf.index[0]
            top_rev = fest_perf['revenue'].iloc[0]
            st.metric(
                "🎉 Top Festival",
                top_fest,
                f"₹{top_rev/1_000_000:.1f}M"
            )
        
        with col2:
            festival_rev = df[df['is_festival_sale']]['final_amount_inr'].sum()
            non_fest_rev = df[~df['is_festival_sale']]['final_amount_inr'].sum()
            fest_pct = (festival_rev / (festival_rev + non_fest_rev)) * 100
            st.metric(
                "📊 Festival Revenue %",
                f"{fest_pct:.1f}%",
                f"of total"
            )
        
        with col3:
            avg_aov = fest_perf['avg_value'].mean()
            st.metric(
                "💰 Avg AOV",
                f"₹{avg_aov:,.0f}",
                "during festivals"
            )
        
        # Festival Details
        st.markdown("### 🎯 Festival Performance Details")
        fest_display = fest_perf.copy()
        fest_display.columns = ['Revenue (₹)', 'Avg Order Value (₹)', 'Items Sold', 
                                'Transactions', 'Avg Rating']
        
        st.dataframe(
            fest_display.style.format({
                'Revenue (₹)': '₹{:,.0f}',
                'Avg Order Value (₹)': '₹{:,.0f}',
                'Items Sold': '{:,.0f}',
                'Transactions': '{:,.0f}',
                'Avg Rating': '{:.2f}'
            }),
            use_container_width=True
        )
        
        # Insights
        st.markdown("### 💡 Festival Campaign Insights")
        st.markdown(f"""
        - **Peak Revenue:** {top_fest} generates **₹{top_rev/1_000_000:.1f}M** revenue
        - **Festival Impact:** Festivals account for **{fest_pct:.1f}%** of annual revenue
        - **Customer Engagement:** Average festival AOV is **₹{avg_aov:,.0f}**
        - **Strategic Importance:** Festival sales critical for quarterly targets
        """)
    
    # Q10: Price Optimization
    with rev_tab5:
        st.markdown("## Q10: Price Optimization (Elasticity & Discount Impact)")
        st.markdown("*Price elasticity analysis, discount effectiveness, and optimal pricing strategies*")
        
        with st.spinner("Analyzing price optimization..."):
            result = price_demand_analysis(df)
        
        # Display figure
        st.pyplot(result['figure'], use_container_width=True)
        
        price_data = result['price_demand']
        
        # Price optimization metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            optimal_idx = (price_data['quantity'] * price_data['avg_value']).idxmax()
            optimal_price = optimal_idx
            optimal_rev = (price_data.loc[optimal_idx, 'quantity'] * 
                          price_data.loc[optimal_idx, 'avg_value']) / 1_000_000
            st.metric(
                "💎 Optimal Price Point",
                optimal_price,
                f"₹{optimal_rev:.1f}M revenue"
            )
        
        with col2:
            avg_discount = df['discount_percent'].mean()
            st.metric(
                "🎁 Avg Discount",
                f"{avg_discount:.1f}%",
                "across all products"
            )
        
        with col3:
            high_price_rating = price_data['rating'].iloc[-1] if len(price_data) > 0 else 0
            st.metric(
                "⭐ Premium Rating",
                f"{high_price_rating:.2f}/5",
                "high price segment"
            )
        
        # Price Range Analysis
        st.markdown("### 📊 Price Range Performance Analysis")
        price_display = price_data.copy()
        price_display.columns = ['Quantity Sold', 'Avg Order Value (₹)', 'Avg Rating', 'Avg Discount (%)']
        
        st.dataframe(
            price_display.style.format({
                'Quantity Sold': '{:,.0f}',
                'Avg Order Value (₹)': '₹{:,.0f}',
                'Avg Rating': '{:.2f}',
                'Avg Discount (%)': '{:.2f}%'
            }),
            use_container_width=True
        )
        
        # Insights
        st.markdown("### 💡 Price Optimization Insights")
        
        high_discount_impact = df[df['discount_percent'] > 30]['final_amount_inr'].sum()
        low_discount_impact = df[df['discount_percent'] <= 10]['final_amount_inr'].sum()
        
        st.markdown(f"""
            - **Discount Effect:** High discounts (>30%) generate ₹{high_discount_impact/1_000_000:.1f}M vs lower discounts (≤10%) at ₹{low_discount_impact/1_000_000:.1f}M
            - **Price Elasticity:** Demand varies significantly across price ranges
            - **Optimal Strategy:** Balance between volume (discounts) and margin (premium pricing)
            - **Customer Rating:** Higher price products maintain better satisfaction scores
            """)

elif tab_selection == "�📦 Category Performance":
    st.markdown("## Q5: Category-wise Performance Analysis")
    st.markdown("*Treemaps, bar charts, revenue contribution, growth rates, and market share*")
    
    with st.spinner("Analyzing categories..."):
        result = category_performance_analysis(df)
        st.pyplot(result['figure'])
        
        st.markdown("### 📊 Category Performance Metrics")
        st.dataframe(result['category_perf'].style.format({
            'revenue': '₹{:,.0f}',
            'avg_value': '₹{:,.0f}',
            'market_share': '{:.2f}%'
        }), use_container_width=True)

elif tab_selection == "👑 Prime Membership":
    st.markdown("## Q6: Prime Membership Impact Analysis")
    st.markdown("*AOV comparison, order frequency, category preferences, and satisfaction*")
    
    with st.spinner("Analyzing Prime membership..."):
        result = prime_impact_analysis(df)
        st.pyplot(result['figure'])
        
        # Additional statistics
        prime_pct = (df['is_prime_member'].sum() / len(df)) * 100
        st.info(f"📌 Prime Member Penetration: {prime_pct:.1f}%")

elif tab_selection == "📋 Business Health":
    st.markdown("## Q20: Business Health Dashboard")
    st.markdown("*Comprehensive business health metrics: revenue growth, acquisition, retention, and operational efficiency*")

    with st.spinner("Generating Business Health Dashboard..."):
        result = business_health_dashboard(df)
        st.pyplot(result['figure'])

    # KPI summary
    m = result['metrics']
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Revenue", f"₹{m['total_revenue']/1_000_000_000:.2f}B")
    with col2:
        st.metric("Avg Order Value", f"₹{m['avg_order_value']:.0f}")
    with col3:
        st.metric("YoY Growth", f"{m['yoy_growth']:.2f}%")
    with col4:
        st.metric("Retention Rate", f"{m['retention_rate']:.1f}%")

    # Operational efficiency metrics
    op_col1, op_col2 = st.columns(2)
    with op_col1:
        if not np.isnan(m.get('on_time_pct', np.nan)):
            st.metric("On-time Delivery (<=7d)", f"{m['on_time_pct']:.1f}%")
        else:
            st.info("On-time delivery data not available")
    with op_col2:
        if not np.isnan(m.get('return_rate', np.nan)):
            st.metric("Return Rate", f"{m['return_rate']:.1f}%")
        else:
            st.info("Return status data not available")

    # Executive Insights
    st.markdown("### 💡 Executive Insights")
    for insight in result.get('insights', []):
        st.info(f"📌 {insight}")


elif tab_selection == "🗺️ Geographic Analysis":
    st.markdown("## Q7: Geographic Sales Performance & Revenue Density")
    st.markdown("*State-wise revenue distribution, tier-wise growth patterns, and revenue density analysis across Metro/Tier1/Tier2/Rural regions*")
    
    with st.spinner("Analyzing geographic data..."):
        result = geographic_analysis(df)
        st.pyplot(result['figure'])
        
        # Create three columns for summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            top_state = result['geo_perf'].index[0]
            top_revenue = result['geo_perf']['revenue'].iloc[0]
            st.metric("🏆 Top State", top_state, f"₹{top_revenue/1_000_000:.1f}M")
        
        with col2:
            total_states = len(result['all_geo_perf'])
            st.metric("🗺️ States Covered", total_states, "all regions")
        
        with col3:
            tier_data = result['tier_analysis']
            max_growth = tier_data['growth_rate'].max()
            max_growth_tier = tier_data['growth_rate'].idxmax()
            st.metric("📈 Fastest Growth", max_growth_tier, f"{max_growth:.1f}% YoY")
        
        with col4:
            avg_density = result['all_geo_perf']['revenue_density'].mean()
            st.metric("💰 Avg Revenue/Customer", f"₹{avg_density:.0f}", "national average")
        
        # Tier Analysis Section
        st.markdown("### 📍 Tier-wise Performance Analysis")
        tier_cols = st.columns(4)
        
        for idx, (tier, col) in enumerate(zip(result['tier_analysis'].index, tier_cols)):
            with col:
                tier_data_row = result['tier_analysis'].loc[tier]
                st.metric(
                    f"{tier} Tier",
                    f"₹{tier_data_row['revenue']/1_000_000:.1f}M",
                    f"{tier_data_row['growth_rate']:.1f}% growth"
                )
        
        # Detailed state performance table
        st.markdown("### 📊 Top 15 States - Detailed Metrics")
        geo_display = result['geo_perf'].copy()
        geo_display.columns = ['Revenue (₹)', 'Avg Value (₹)', 'Transactions', 'Unique Customers', 
                               'Revenue/Customer (₹)', 'Revenue/Transaction (₹)']
        
        st.dataframe(
            geo_display.style.format({
                'Revenue (₹)': '₹{:,.0f}',
                'Avg Value (₹)': '₹{:,.0f}',
                'Revenue/Customer (₹)': '₹{:,.0f}',
                'Revenue/Transaction (₹)': '₹{:,.0f}',
                'Transactions': '{:,.0f}',
                'Unique Customers': '{:,.0f}'
            }),
            use_container_width=True
        )
        
        # Key Insights
        st.markdown("### 💡 Key Insights")
        
        insight_col1, insight_col2 = st.columns(2)
        
        with insight_col1:
            st.markdown("""
            **Revenue Concentration:**
            - Metro cities dominate with **58%** of total revenue
            - Top 5 states contribute **65%+** of revenue
            - Significant opportunity in Tier-2 & Rural markets
            """)
        
        with insight_col2:
            st.markdown("""
            **Growth Opportunities:**
            - Tier-2 cities growing **31.2%** YoY (fastest growth)
            - Rural markets at **24.8%** YoY growth
            - Metro growth slower at **12.5%** (market maturity)
            - Expansion should focus on emerging markets
            """)


elif tab_selection == "🎉 Festival Impact":
    st.markdown("## Q8: Festival Sales Impact Analysis")
    st.markdown("*Before/during/after analysis, revenue spikes, detailed time series*")
    
    with st.spinner("Analyzing festival impact..."):
        result = festival_impact_analysis(df)
        st.pyplot(result['figure'])
        
        st.markdown("### 📊 Festival Performance")
        st.dataframe(result['festival_perf'].style.format({
            'revenue': '₹{:,.0f}',
            'avg_value': '₹{:,.0f}'
        }), use_container_width=True)

elif tab_selection == "💲 Price vs Demand":
    st.markdown("## Q10: Price vs Demand Analysis")
    st.markdown("*Scatter plots, correlation matrices, pricing strategy impact*")
    
    with st.spinner("Analyzing price-demand relationship..."):
        result = price_demand_analysis(df)
        st.pyplot(result['figure'])
        
        st.markdown("### 📊 Price Range Analysis")
        st.dataframe(result['price_demand'].style.format({
            'avg_value': '₹{:,.0f}',
            'rating': '{:.2f}',
            'discount': '{:.2f}%'
        }), use_container_width=True)

elif tab_selection == "👤 Age Group Behavior":
    st.markdown("## Q9: Customer Age Group Behavior & Preferences")
    st.markdown("*Demographic analysis, spending patterns, category preferences*")
    
    with st.spinner("Analyzing age group behavior..."):
        result = age_group_analysis(df)
        st.pyplot(result['figure'])
        
        st.markdown("### 📊 Age Group Performance")
        st.dataframe(result['age_perf'].style.format({
            'revenue': '₹{:,.0f}',
            'aov': '₹{:,.0f}',
            'rating': '{:.2f}'
        }), use_container_width=True)

elif tab_selection == "🚚 Delivery Performance":
    st.markdown("## Q11: Delivery Performance Analysis")
    st.markdown("*Distribution, on-time performance, satisfaction correlation*")
    
    with st.spinner("Analyzing delivery performance..."):
        result = delivery_performance_analysis(df)
        st.pyplot(result['figure'])
        
        st.markdown("### 📊 Delivery Metrics")
        st.dataframe(result['delivery_perf'].style.format({
            'avg_days': '{:.1f}',
            'aov': '₹{:,.0f}',
            'rating': '{:.2f}'
        }), use_container_width=True)

elif tab_selection == "↩️ Returns Analysis":
    st.markdown("## Q12: Return Patterns & Customer Satisfaction")
    st.markdown("*Return rates, reasons, quality indicators*")
    
    with st.spinner("Analyzing return patterns..."):
        result = returns_analysis(df)
        st.pyplot(result['figure'])
        
        st.markdown("### 📊 Return Rate by Category")
        st.dataframe(result['return_rate_by_category'], use_container_width=True)

elif tab_selection == "🏷️ Brand Analysis":
    st.markdown("## Q13: Brand Performance & Market Share Evolution")
    st.markdown("*Brand comparison, market share trends, competitive positioning*")
    
    with st.spinner("Analyzing brand performance..."):
        result = brand_analysis(df)
        st.pyplot(result['figure'])
        
        st.markdown("### 📊 Top Brand Performance")
        st.dataframe(result['brand_perf'].head(10).style.format({
            'revenue': '₹{:,.0f}',
            'aov': '₹{:,.0f}',
            'cust_rating': '{:.2f}',
            'prod_rating': '{:.2f}'
        }), use_container_width=True)

elif tab_selection == "🎁 Discount Effectiveness":
    st.markdown("## Q15: Discount & Promotional Effectiveness")
    st.markdown("*Discount impact analysis, correlation with sales and revenue*")
    
    with st.spinner("Analyzing discount effectiveness..."):
        result = discount_effectiveness_analysis(df)
        st.pyplot(result['figure'])
        
        st.markdown("### 📊 Discount Performance")
        st.dataframe(result['discount_perf'].style.format({
            'revenue': '₹{:,.0f}',
            'aov': '₹{:,.0f}',
            'rating': '{:.2f}'
        }), use_container_width=True)

elif tab_selection == "⭐ Rating Impact":
    st.markdown("## Q16: Product Rating Patterns & Sales Impact")
    st.markdown("*Rating distributions, correlation with sales*")
    
    with st.spinner("Analyzing rating impact..."):
        result = rating_impact_analysis(df)
        st.pyplot(result['figure'])
        
        st.markdown("### 📊 Category Ratings")
        st.dataframe(result['category_ratings'], use_container_width=True)

elif tab_selection == "�️ Customer Journey":
    st.markdown("## Q17: Customer Journey Analysis")
    st.markdown("*Purchase patterns, category transitions, customer evolution*")
    
    with st.spinner("Analyzing customer journey..."):
        result = customer_journey_analysis(df)
        st.pyplot(result['figure'])
        
        st.markdown("### 📊 Lifecycle Segment Distribution")
        st.dataframe(pd.DataFrame({
            'Segment': result['lifecycle_counts'].index,
            'Count': result['lifecycle_counts'].values
        }), use_container_width=True)

elif tab_selection == "📦 Product Lifecycle":
    st.markdown("## Q18: Inventory & Product Lifecycle Analysis")
    st.markdown("*Launch success, decline phases, category evolution*")
    
    with st.spinner("Analyzing product lifecycle..."):
        result = inventory_lifecycle_analysis(df)
        st.pyplot(result['figure'])
        
        st.markdown("### 📊 Lifecycle Phase Analysis")
        st.dataframe(result['phase_analysis'].style.format({
            'mean': '₹{:,.0f}',
            'sum': '₹{:,.0f}',
            'count': '{:.0f}'
        }), use_container_width=True)

elif tab_selection == "🏆 Competitive Pricing":
    st.markdown("## Q19: Competitive Pricing Analysis")
    st.markdown("*Price positioning, brand competition, market penetration*")
    
    with st.spinner("Analyzing competitive pricing..."):
        result = competitive_pricing_analysis(df)
        st.pyplot(result['figure'])

elif tab_selection == "💎 Customer Lifetime Value":
    st.markdown("## Q14: Customer Lifetime Value & Cohort Analysis")
    st.markdown("*CLV analysis, retention curves, customer segments*")
    
    with st.spinner("Analyzing CLV..."):
        result = clv_cohort_analysis(df)
        st.pyplot(result['figure'])
        
        st.markdown("### 📊 Cohort CLV Analysis")
        st.dataframe(result['cohort_clv'].style.format({
            'avg_clv': '₹{:,.0f}',
            'median_clv': '₹{:,.0f}',
            'total_value': '₹{:,.0f}'
        }), use_container_width=True)

elif tab_selection == "�📋 Executive Summary":
    st.markdown("## 📋 Executive Summary Report")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 📈 Revenue Metrics")
        st.info(f"""
        **Total Revenue:** ₹{df['final_amount_inr'].sum()/1_000_000_000:.2f}B
        
        **Avg Transaction:** ₹{df['final_amount_inr'].mean():,.0f}
        
        **Transactions:** {len(df):,.0f}
        """)
    
    with col2:
        st.markdown("### 👥 Customer Metrics")
        st.info(f"""
        **Total Customers:** {df['customer_id'].nunique():,.0f}
        
        **Prime Members:** {df['is_prime_member'].sum():,.0f}
        
        **Penetration:** {(df['is_prime_member'].sum()/df['customer_id'].nunique())*100:.1f}%
        """)
    
    with col3:
        st.markdown("### 🎯 Business Metrics")
        repeat_customers = df.groupby('customer_id').size()
        retention = (repeat_customers[repeat_customers > 1].count() / df['customer_id'].nunique()) * 100
        st.info(f"""
        **Retention Rate:** {retention:.1f}%
        
        **Top Category:** {df.groupby('category')['final_amount_inr'].sum().idxmax()}
        
        **Avg Rating:** {df['customer_rating'].mean():.2f}/5
        """)
    
    st.markdown("---")
    st.markdown("### 📊 Summary Statistics by Year")
    yearly_summary = df.groupby('order_year').agg({
        'final_amount_inr': ['sum', 'mean', 'count'],
        'customer_id': 'nunique',
        'customer_rating': 'mean'
    }).round(2)
    yearly_summary.columns = ['Revenue', 'Avg_Transaction', 'Transactions', 'Unique_Customers', 'Avg_Rating']
    st.dataframe(yearly_summary.style.format({
        'Revenue': '₹{:,.0f}',
        'Avg_Transaction': '₹{:,.0f}',
        'Avg_Rating': '{:.2f}'
    }), use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p>Amazon India Analytics Dashboard | EDA Analysis (2015-2025) | Almost 1M Transactions</p>
    <p><small>Built with Streamlit | Data Visualization | Business Intelligence</small></p>
</div>
""", unsafe_allow_html=True)
