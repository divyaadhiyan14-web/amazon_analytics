"""
Executive Summary Dashboard Module
High-level KPIs, business metrics, and strategic insights
"""
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta


def show_executive_dashboard(df):
    """Display executive summary dashboard with key metrics"""
    
    st.header("📊 Executive Summary Dashboard")
    st.markdown("*High-level KPIs, business performance, and strategic metrics*")
    
    # Create tabs for executive view
    exec_tab1, exec_tab2, exec_tab3 = st.tabs([
        "Business Metrics",
        "Performance Trends",
        "Strategic Insights"
    ])
    
    # Business Metrics
    with exec_tab1:
        st.markdown("## Key Business Metrics")
        
        # Calculate key metrics
        total_revenue = df['final_amount_inr'].sum()
        total_orders = len(df)
        avg_order_value = total_revenue / total_orders
        total_customers = df['customer_id'].nunique()
        
        # Display top metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "💰 Total Revenue",
                f"₹{total_revenue/1_000_000:.1f}M",
                "YTD"
            )
        
        with col2:
            st.metric(
                "📦 Total Orders",
                f"{total_orders:,}",
                "Transactions"
            )
        
        with col3:
            st.metric(
                "💵 Avg Order Value",
                f"₹{avg_order_value:,.0f}",
                "AOV"
            )
        
        with col4:
            st.metric(
                "👥 Total Customers",
                f"{total_customers:,}",
                "Unique"
            )
        
        # Revenue Quality Metrics
        st.markdown("### 📈 Revenue Quality Metrics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            repeat_customers = df.groupby('customer_id').size()
            repeat_rate = (repeat_customers >= 2).sum() / len(repeat_customers) * 100
            st.metric(
                "🔄 Repeat Rate",
                f"{repeat_rate:.1f}%",
                "Retention"
            )
        
        with col2:
            avg_rating = df['customer_rating'].mean()
            st.metric(
                "⭐ Avg Rating",
                f"{avg_rating:.2f}/5",
                "Satisfaction"
            )
        
        with col3:
            festival_revenue = df[df['is_festival_sale']]['final_amount_inr'].sum()
            festival_pct = (festival_revenue / total_revenue) * 100
            st.metric(
                "🎉 Festival Sales %",
                f"{festival_pct:.1f}%",
                "Seasonal"
            )
        
        with col4:
            avg_delivery = df['delivery_days'].mean()
            st.metric(
                "📦 Avg Delivery Days",
                f"{avg_delivery:.1f}",
                "Fulfillment"
            )
        
        # Product Performance
        st.markdown("### 📊 Product Performance")
        
        top_categories = df.groupby('category')['final_amount_inr'].agg(['sum', 'count', 'mean']).sort_values('sum', ascending=False)
        top_categories.columns = ['Revenue (₹)', 'Orders', 'Avg Value (₹)']
        
        st.dataframe(
            top_categories.head(10).style.format({
                'Revenue (₹)': '₹{:,.0f}',
                'Orders': '{:,.0f}',
                'Avg Value (₹)': '₹{:,.0f}'
            }),
            use_container_width=True
        )
    
    # Performance Trends
    with exec_tab2:
        st.markdown("## Performance Trends")
        
        # Date-based analysis
        df['date'] = pd.to_datetime(df['order_date'])
        
        # Monthly trend
        st.markdown("### 📈 Monthly Revenue Trend")
        monthly_data = df.groupby(df['date'].dt.to_period('M'))['final_amount_inr'].agg(['sum', 'count', 'mean'])
        monthly_data.index = monthly_data.index.to_timestamp()
        monthly_data.columns = ['Revenue', 'Orders', 'Avg Value']
        
        st.line_chart(monthly_data['Revenue'])
        
        # Key metrics by month
        col1, col2, col3 = st.columns(3)
        
        with col1:
            best_month = monthly_data['Revenue'].idxmax()
            best_revenue = monthly_data['Revenue'].max()
            st.metric(
                "🏆 Best Month",
                best_month.strftime('%B %Y'),
                f"₹{best_revenue/1_000_000:.1f}M"
            )
        
        with col2:
            current_month = pd.Timestamp.now().to_period('M').to_timestamp()
            current_revenue = monthly_data.loc[current_month, 'Revenue'] if current_month in monthly_data.index else 0
            st.metric(
                "🌙 Current Month",
                current_month.strftime('%B'),
                f"₹{current_revenue/1_000_000:.1f}M"
            )
        
        with col3:
            avg_monthly = monthly_data['Revenue'].mean()
            st.metric(
                "📊 Monthly Avg",
                "Across period",
                f"₹{avg_monthly/1_000_000:.1f}M"
            )
        
        # Category performance over time
        st.markdown("### 🎯 Top Category Trends")
        
        top_cat = df.groupby('category')['final_amount_inr'].sum().idxmax()
        cat_monthly = df[df['category'] == top_cat].groupby(df[df['category'] == top_cat]['date'].dt.to_period('M'))['final_amount_inr'].sum()
        cat_monthly.index = cat_monthly.index.to_timestamp()
        
        st.line_chart(cat_monthly)
        
        st.markdown(f"*Tracking {top_cat} category performance over time*")
    
    # Strategic Insights
    with exec_tab3:
        st.markdown("## Strategic Business Insights")
        
        # Calculate strategic metrics
        total_revenue = df['final_amount_inr'].sum()
        top_category = df.groupby('category')['final_amount_inr'].sum().idxmax()
        top_state = df.groupby('customer_state')['final_amount_inr'].sum().idxmax()
        avg_rating = df['customer_rating'].mean()
        repeat_rate = (df.groupby('customer_id').size() >= 2).sum() / df['customer_id'].nunique() * 100
        
        # Strategic KPIs
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🎯 Market Concentration")
            
            cat_revenue = df.groupby('category')['final_amount_inr'].sum().sort_values(ascending=False)
            top_3_pct = (cat_revenue.head(3).sum() / cat_revenue.sum()) * 100
            
            # Build category list safely
            cat_lines = [f"**Top {min(3, len(cat_revenue))} Categories** account for **{top_3_pct:.1f}%** of revenue:"]
            for i in range(min(3, len(cat_revenue))):
                cat_lines.append(f"{i+1}. {cat_revenue.index[i]} - ₹{cat_revenue.iloc[i]/1_000_000:.1f}M")
            cat_lines.append("\n**Diversification**: Consider growth strategies for underperforming categories")
            
            st.markdown("\n".join(cat_lines))
        
        with col2:
            st.markdown("### 📍 Geographic Focus")
            
            state_revenue = df.groupby('customer_state')['final_amount_inr'].sum().sort_values(ascending=False)
            top_5_pct = (state_revenue.head(5).sum() / state_revenue.sum()) * 100
            
            # Build state list safely
            state_lines = [f"**Top {min(5, len(state_revenue))} States** account for **{top_5_pct:.1f}%** of revenue:"]
            for i in range(min(5, len(state_revenue))):
                state_lines.append(f"- {state_revenue.index[i]}: ₹{state_revenue.iloc[i]/1_000_000:.1f}M")
            state_lines.append("\n**Expansion Opportunity**: Tier 2 and Tier 3 cities show growth potential")
            
            st.markdown("\n".join(state_lines))
        
        # Operational Metrics
        st.markdown("### ⚙️ Operational Health")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            avg_rating = df['customer_rating'].mean()
            rating_trend = "✅ Positive" if avg_rating >= 4.0 else "⚠️ Monitor"
            st.metric(
                "Customer Satisfaction",
                f"{avg_rating:.2f}/5",
                rating_trend
            )
        
        with col2:
            avg_delivery = df['delivery_days'].mean()
            delivery_status = "✅ Good" if avg_delivery <= 5 else "⚠️ Improve"
            st.metric(
                "Delivery Performance",
                f"{avg_delivery:.1f} days",
                delivery_status
            )
        
        with col3:
            repeat_rate = (df.groupby('customer_id').size() >= 2).sum() / df['customer_id'].nunique() * 100
            retention_status = "✅ Strong" if repeat_rate >= 30 else "⚠️ Develop"
            st.metric(
                "Customer Retention",
                f"{repeat_rate:.1f}%",
                retention_status
            )
        
        # Strategic Recommendations
        st.markdown("### 💡 Strategic Recommendations")
        
        recommendations = []
        
        if repeat_rate < 30:
            recommendations.append("🎯 **Retention**: Launch loyalty program to increase repeat purchase rate")
        else:
            recommendations.append("✅ **Retention**: Strong repeat rate - focus on upselling")
        
        if avg_rating < 4.0:
            recommendations.append("⚠️ **Quality**: Address product/service quality issues affecting ratings")
        else:
            recommendations.append("✅ **Quality**: Maintain quality standards driving high satisfaction")
        
        if avg_delivery > 5:
            recommendations.append("📦 **Logistics**: Optimize delivery times for better customer experience")
        else:
            recommendations.append("✅ **Logistics**: Delivery performance meeting customer expectations")
        
        if top_3_pct > 80:
            recommendations.append("📊 **Diversification**: Develop underperforming product categories")
        else:
            recommendations.append("✅ **Portfolio**: Good product mix across categories")
        
        if top_5_pct > 70:
            recommendations.append("🗺️ **Geographic**: Expand presence in Tier 2 and Tier 3 cities")
        else:
            recommendations.append("✅ **Geography**: Well-distributed revenue across regions")
        
        for i, rec in enumerate(recommendations, 1):
            st.markdown(f"{i}. {rec}")
