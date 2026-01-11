"""
Customer Analytics Dashboard Module
Customer segmentation, RFM analysis, and behavioral insights
"""
import streamlit as st
import pandas as pd
from eda.rfm_analysis import rfm_segmentation_analysis


def show_customer_dashboard(df):
    """Display comprehensive customer analytics dashboard"""
    
    st.header("👥 Customer Analytics Dashboard")
    st.markdown("*Customer segmentation, lifetime value, and behavioral analysis*")
    
    # Create tabs for customer analysis
    cust_tab1, cust_tab2, cust_tab3 = st.tabs([
        "RFM Segmentation",
        "Customer Lifetime Value",
        "Retention & Loyalty"
    ])
    
    # RFM Segmentation
    with cust_tab1:
        st.markdown("## RFM Segmentation Analysis")
        st.markdown("*Recency, Frequency, Monetary customer classification*")
        
        with st.spinner("Analyzing customer segments..."):
            rfm_analysis = rfm_segmentation_analysis(df)
        
        st.pyplot(rfm_analysis['figure'], use_container_width=True)
        
        # Get the RFM dataframe
        rfm_result = rfm_analysis['rfm']
        
        # Display RFM summary
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_customers = len(rfm_result)
            st.metric(
                "👥 Total Customers",
                f"{total_customers:,}",
                "Active"
            )
        
        with col2:
            champions = (rfm_result['segment'] == 'Champions').sum()
            champ_pct = (champions / len(rfm_result)) * 100
            st.metric(
                "🏆 Champions",
                f"{champions:,}",
                f"{champ_pct:.1f}%"
            )
        
        with col3:
            loyal = (rfm_result['segment'] == 'Loyal Customers').sum()
            loyal_pct = (loyal / len(rfm_result)) * 100
            st.metric(
                "💎 Loyal Customers",
                f"{loyal:,}",
                f"{loyal_pct:.1f}%"
            )
        
        with col4:
            atrisk = (rfm_result['segment'] == 'At Risk').sum()
            atrisk_pct = (atrisk / len(rfm_result)) * 100
            st.metric(
                "⚠️ At Risk",
                f"{atrisk:,}",
                f"{atrisk_pct:.1f}%"
            )
        
        # Segment distribution
        st.markdown("### 📊 Customer Segment Distribution")
        segment_summary = rfm_result['segment'].value_counts()
        
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.dataframe(
                segment_summary.reset_index().rename(
                    columns={'index': 'Segment', 'segment': 'Count'}
                ),
                use_container_width=True
            )
        
        with col_right:
            st.bar_chart(segment_summary)
        
        # RFM Metrics Details
        st.markdown("### 📈 RFM Metrics Summary")
        rfm_metrics = rfm_result[['recency', 'frequency', 'monetary']].describe()
        
        st.dataframe(
            rfm_metrics.style.format({'monetary': '₹{:,.0f}'}),
            use_container_width=True
        )
        
        st.markdown("### 💡 Segmentation Insights")
        st.markdown(f"""
        - **Champions**: Top {champ_pct:.1f}% of customers ({champions:,}) - highest value
        - **Loyal Base**: {loyal_pct:.1f}% consistently engaged customers ({loyal:,})
        - **At Risk**: {atrisk_pct:.1f}% showing decline ({atrisk:,}) - retention opportunity
        - **Focus Areas**: Nurture champions, stabilize at-risk, grow loyal segment
        """)
    
    # Customer Lifetime Value
    with cust_tab2:
        st.markdown("## Customer Lifetime Value Analysis")
        st.markdown("*CLV estimation and customer value segmentation*")
        
        # Calculate CLV on the fly
        clv_result = df.groupby('customer_id').agg({
            'final_amount_inr': 'sum',
            'transaction_id': 'count'
        }).reset_index()
        clv_result.columns = ['customer_id', 'clv', 'transactions']
        
        # CLV Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            avg_clv = clv_result['clv'].mean()
            st.metric(
                "💰 Avg CLV",
                f"₹{avg_clv:,.0f}",
                "Per customer"
            )
        
        with col2:
            total_clv = clv_result['clv'].sum()
            st.metric(
                "📊 Total CLV",
                f"₹{total_clv/1_000_000:.1f}M",
                "All customers"
            )
        
        with col3:
            high_value = (clv_result['clv'] > clv_result['clv'].quantile(0.75)).sum()
            high_value_pct = (high_value / len(clv_result)) * 100
            st.metric(
                "🌟 High Value",
                f"{high_value:,}",
                f"{high_value_pct:.1f}%"
            )
        
        with col4:
            median_clv = clv_result['clv'].median()
            st.metric(
                "📈 Median CLV",
                f"₹{median_clv:,.0f}",
                "50th percentile"
            )
        
        # CLV Distribution
        st.markdown("### 📊 CLV Distribution Analysis")
        
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.markdown("**CLV Percentiles**")
            percentiles = pd.DataFrame({
                'Percentile': ['10th', '25th', '50th', '75th', '90th'],
                'CLV (₹)': [
                    f"₹{clv_result['clv'].quantile(0.1):,.0f}",
                    f"₹{clv_result['clv'].quantile(0.25):,.0f}",
                    f"₹{clv_result['clv'].quantile(0.50):,.0f}",
                    f"₹{clv_result['clv'].quantile(0.75):,.0f}",
                    f"₹{clv_result['clv'].quantile(0.90):,.0f}"
                ]
            })
            st.dataframe(percentiles, use_container_width=True)
        
        with col_right:
            st.markdown("**Top 10 Customers**")
            top_customers = clv_result.nlargest(10, 'clv')[['customer_id', 'clv']].copy()
            top_customers.columns = ['Customer ID', 'CLV (₹)']
            st.dataframe(
                top_customers.style.format({'CLV (₹)': '₹{:,.0f}'}),
                use_container_width=True
            )
        
        st.markdown("### 💡 CLV Insights")
        st.markdown(f"""
        - **Average CLV**: ₹{avg_clv:,.0f} per customer
        - **High-Value Segment**: {high_value_pct:.1f}% of customers ({high_value:,}) drive significant revenue
        - **Total Customer Value**: ₹{total_clv/1_000_000:.1f}M across all customers
        - **Strategic Focus**: Prioritize high CLV customers for retention and upselling
        """)
    
    # Retention & Loyalty
    with cust_tab3:
        st.markdown("## Retention & Loyalty Metrics")
        st.markdown("*Customer retention rates and loyalty indicators*")
        
        # Calculate retention metrics
        customer_freq = df.groupby('customer_id').size()
        repeat_customers = (customer_freq >= 2).sum()
        repeat_rate = (repeat_customers / len(customer_freq)) * 100
        
        # NPS calculation (using ratings > 4 as promoters, <= 2 as detractors)
        promoters = (df['customer_rating'] >= 4.5).sum() / len(df) * 100
        detractors = (df['customer_rating'] <= 2).sum() / len(df) * 100
        nps_score = promoters - detractors
        
        # Retention Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "🔄 Repeat Customer Rate",
                f"{repeat_rate:.1f}%",
                "Made 2+ purchases"
            )
        
        with col2:
            avg_frequency = customer_freq.mean()
            st.metric(
                "📈 Avg Purchases/Customer",
                f"{avg_frequency:.2f}",
                "Per customer"
            )
        
        with col3:
            satisfaction = df['customer_rating'].mean()
            st.metric(
                "⭐ Avg Satisfaction",
                f"{satisfaction:.2f}/5",
                "Customer rating"
            )
        
        with col4:
            st.metric(
                "📊 NPS Score",
                f"{nps_score:.0f}",
                "Net Promoter Score"
            )
        
        # Loyalty segments
        st.markdown("### 👥 Loyalty Segments")
        
        one_time = (customer_freq == 1).sum()
        repeat = ((customer_freq >= 2) & (customer_freq <= 5)).sum()
        loyal = (customer_freq > 5).sum()
        
        loyalty_data = pd.DataFrame({
            'Segment': ['One-Time Buyers', 'Repeat Customers', 'Loyal Advocates'],
            'Count': [one_time, repeat, loyal]
        })
        
        loyalty_data['Percentage'] = (loyalty_data['Count'] / loyalty_data['Count'].sum() * 100).round(1)
        
        st.dataframe(
            loyalty_data,
            use_container_width=True
        )
        
        # Cohort Analysis
        st.markdown("### 📅 Cohort Retention Analysis")
        st.info("Retention tracking by customer acquisition cohort helps identify:")
        st.markdown("""
        - Monthly cohort performance
        - Retention decay patterns
        - Seasonal acquisition variations
        - Lifetime cohort value trends
        """)
        
        st.markdown("### 💡 Retention & Loyalty Insights")
        st.markdown(f"""
        - **Repeat Rate**: {repeat_rate:.1f}% customers make repeat purchases
        - **Average Engagement**: {avg_frequency:.2f} purchases per customer
        - **Satisfaction Level**: {satisfaction:.2f}/5 indicates strong product quality
        - **NPS Score**: {nps_score:.0f} - customer advocacy potential
        - **Retention Focus**: Build loyalty programs for one-time buyers
        """)
