"""
Operations & Logistics Dashboard Module
Delivery performance, order fulfillment, and operational efficiency
"""
import streamlit as st
import pandas as pd
import numpy as np


def show_operations_dashboard(df):
    """Display operations and logistics dashboard"""
    
    st.header("🚚 Operations & Logistics Dashboard")
    st.markdown("*Delivery performance, fulfillment metrics, and operational efficiency*")
    
    # Create tabs for operations view
    ops_tab1, ops_tab2, ops_tab3 = st.tabs([
        "Delivery Performance",
        "Order Fulfillment",
        "Operational Metrics"
    ])
    
    # Delivery Performance
    with ops_tab1:
        st.markdown("## Delivery Performance Analysis")
        
        # Delivery metrics
        col1, col2, col3, col4 = st.columns(4)
        
        total_orders = len(df)
        avg_delivery_days = df['delivery_days'].mean()
        median_delivery = df['delivery_days'].median()
        on_time = (df['delivery_days'] <= 5).sum()
        on_time_pct = (on_time / total_orders) * 100
        
        with col1:
            st.metric(
                "📦 Total Orders",
                f"{total_orders:,}",
                "Processed"
            )
        
        with col2:
            st.metric(
                "⏱️ Avg Delivery",
                f"{avg_delivery_days:.1f}",
                "days"
            )
        
        with col3:
            st.metric(
                "📊 Median Delivery",
                f"{median_delivery:.0f}",
                "days"
            )
        
        with col4:
            st.metric(
                "✅ On-Time %",
                f"{on_time_pct:.1f}%",
                f"{on_time:,} orders"
            )
        
        # Delivery performance by tier
        st.markdown("### 🎯 Delivery Performance Targets")
        
        targets = {
            'Excellent (≤3 days)': (df['delivery_days'] <= 3).sum(),
            'Good (4-5 days)': ((df['delivery_days'] > 3) & (df['delivery_days'] <= 5)).sum(),
            'Acceptable (6-7 days)': ((df['delivery_days'] > 5) & (df['delivery_days'] <= 7)).sum(),
            'Delayed (>7 days)': (df['delivery_days'] > 7).sum()
        }
        
        target_df = pd.DataFrame({
            'Delivery Tier': list(targets.keys()),
            'Orders': list(targets.values())
        })
        target_df['Percentage'] = (target_df['Orders'] / target_df['Orders'].sum() * 100).round(1)
        
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.dataframe(target_df, use_container_width=True)
        
        with col_right:
            st.bar_chart(target_df.set_index('Delivery Tier')['Orders'])
        
        # Delivery insights
        st.markdown("### 💡 Delivery Performance Insights")
        
        worst_delivery = df['delivery_days'].max()
        best_delivery = df['delivery_days'].min()
        
        st.markdown(f"""
        - **Average Delivery**: {avg_delivery_days:.1f} days
        - **On-Time Performance**: {on_time_pct:.1f}% delivered within 5 days
        - **Delivery Range**: {best_delivery:.0f} to {worst_delivery:.0f} days
        - **Performance Target**: Aim for 90%+ on-time delivery rate
        - **Improvement Area**: Reduce delayed deliveries (>7 days) to improve CSAT
        """)
    
    # Order Fulfillment
    with ops_tab2:
        st.markdown("## Order Fulfillment Metrics")
        
        # Fulfillment analysis
        col1, col2, col3, col4 = st.columns(4)
        
        unique_orders = len(df)
        unique_customers = df['customer_id'].nunique()
        avg_items_per_order = df.groupby(df.index).size().mean()  # Approximation
        fulfillment_rate = 100  # Assuming all processed orders are fulfilled
        
        with col1:
            st.metric(
                "📋 Unique Orders",
                f"{unique_orders:,}",
                "Fulfilled"
            )
        
        with col2:
            st.metric(
                "👥 Unique Customers",
                f"{unique_customers:,}",
                "Served"
            )
        
        with col3:
            st.metric(
                "📦 Avg Items/Order",
                f"{avg_items_per_order:.2f}",
                "Per transaction"
            )
        
        with col4:
            st.metric(
                "✅ Fulfillment Rate",
                f"{fulfillment_rate:.1f}%",
                "Complete"
            )
        
        # Category-wise fulfillment
        st.markdown("### 📊 Fulfillment by Category")
        
        category_stats = df.groupby('category').agg({
            'order_date': 'count',
            'final_amount_inr': 'sum',
            'delivery_days': 'mean'
        }).rename(columns={
            'order_date': 'Orders',
            'final_amount_inr': 'Revenue',
            'delivery_days': 'Avg Delivery Days'
        }).sort_values('Orders', ascending=False)
        
        st.dataframe(
            category_stats.style.format({
                'Orders': '{:,.0f}',
                'Revenue': '₹{:,.0f}',
                'Avg Delivery Days': '{:.1f}'
            }),
            use_container_width=True
        )
        
        # State-wise fulfillment
        st.markdown("### 🗺️ Fulfillment by State (Top 10)")
        
        state_stats = df.groupby('customer_state').agg({
            'order_date': 'count',
            'delivery_days': 'mean',
            'customer_rating': 'mean'
        }).rename(columns={
            'order_date': 'Orders',
            'delivery_days': 'Avg Delivery Days',
            'customer_rating': 'Avg Rating'
        }).sort_values('Orders', ascending=False).head(10)
        
        st.dataframe(
            state_stats.style.format({
                'Orders': '{:,.0f}',
                'Avg Delivery Days': '{:.1f}',
                'Avg Rating': '{:.2f}'
            }),
            use_container_width=True
        )
        
        st.markdown("### 💡 Fulfillment Insights")
        st.markdown(f"""
        - **Total Fulfillment Volume**: {unique_orders:,} orders processed
        - **Customer Base**: {unique_customers:,} unique customers served
        - **Fulfillment Completion**: {fulfillment_rate:.1f}% success rate
        - **Focus Areas**: Monitor high-volume categories and states for efficiency
        """)
    
    # Operational Metrics
    with ops_tab3:
        st.markdown("## Operational Efficiency Metrics")
        
        # Operational KPIs
        col1, col2, col3, col4 = st.columns(4)
        
        customer_satisfaction = df['customer_rating'].mean()
        repeat_rate = (df.groupby('customer_id').size() >= 2).sum() / df['customer_id'].nunique() * 100
        order_value_variance = df['final_amount_inr'].std() / df['final_amount_inr'].mean()
        processing_efficiency = (df[df['delivery_days'] <= 5].shape[0] / len(df)) * 100
        
        with col1:
            st.metric(
                "⭐ Customer Satisfaction",
                f"{customer_satisfaction:.2f}/5",
                "Average rating"
            )
        
        with col2:
            st.metric(
                "🔄 Repeat Rate",
                f"{repeat_rate:.1f}%",
                "Loyalty metric"
            )
        
        with col3:
            st.metric(
                "📊 Order Value CV",
                f"{order_value_variance:.2f}",
                "Variability"
            )
        
        with col4:
            st.metric(
                "⚡ Processing Efficiency",
                f"{processing_efficiency:.1f}%",
                "On-time rate"
            )
        
        # Quality Metrics
        st.markdown("### 🎯 Quality & Efficiency Metrics")
        
        quality_metrics = pd.DataFrame({
            'Metric': [
                'Excellent Rating (4.5-5.0)',
                'Good Rating (4.0-4.49)',
                'Average Rating (3.5-3.99)',
                'Poor Rating (<3.5)'
            ],
            'Count': [
                (df['customer_rating'] >= 4.5).sum(),
                ((df['customer_rating'] >= 4.0) & (df['customer_rating'] < 4.5)).sum(),
                ((df['customer_rating'] >= 3.5) & (df['customer_rating'] < 4.0)).sum(),
                (df['customer_rating'] < 3.5).sum()
            ]
        })
        
        quality_metrics['Percentage'] = (quality_metrics['Count'] / quality_metrics['Count'].sum() * 100).round(1)
        
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.dataframe(quality_metrics, use_container_width=True)
        
        with col_right:
            st.bar_chart(quality_metrics.set_index('Metric')['Count'])
        
        # Operational Dashboard
        st.markdown("### 📈 Operational Health Dashboard")
        
        health_status = []
        
        # Delivery performance
        if processing_efficiency >= 85:
            health_status.append("✅ **Delivery**: Excellent - On-time rate above 85%")
        elif processing_efficiency >= 70:
            health_status.append("⚠️ **Delivery**: Good - On-time rate 70-85%, room for improvement")
        else:
            health_status.append("❌ **Delivery**: Needs improvement - On-time rate below 70%")
        
        # Customer satisfaction
        if customer_satisfaction >= 4.3:
            health_status.append("✅ **Satisfaction**: Excellent - Rating above 4.3/5")
        elif customer_satisfaction >= 4.0:
            health_status.append("⚠️ **Satisfaction**: Good - Rating 4.0-4.3, maintain quality")
        else:
            health_status.append("❌ **Satisfaction**: Needs attention - Rating below 4.0")
        
        # Repeat rate
        if repeat_rate >= 35:
            health_status.append("✅ **Retention**: Strong - Repeat rate above 35%")
        elif repeat_rate >= 25:
            health_status.append("⚠️ **Retention**: Moderate - Repeat rate 25-35%, improve loyalty")
        else:
            health_status.append("❌ **Retention**: Weak - Repeat rate below 25%, focus on retention")
        
        for status in health_status:
            st.markdown(status)
        
        # Operational Recommendations
        st.markdown("### 💡 Operational Recommendations")
        
        recommendations = []
        
        if processing_efficiency < 85:
            recommendations.append("1. **Logistics Optimization**: Implement route optimization to reduce delivery times")
        else:
            recommendations.append("1. **Maintain Delivery Standards**: Continue current logistics performance")
        
        if customer_satisfaction < 4.0:
            recommendations.append("2. **Quality Assurance**: Review product quality and handling procedures")
        else:
            recommendations.append("2. **Sustain Quality**: Maintain current quality standards")
        
        if repeat_rate < 30:
            recommendations.append("3. **Customer Retention**: Develop loyalty and retention programs")
        else:
            recommendations.append("3. **Expand Loyalty**: Leverage strong retention for upselling")
        
        recommendations.append("4. **Performance Monitoring**: Track KPIs weekly to ensure continuous improvement")
        
        for rec in recommendations:
            st.markdown(rec)
