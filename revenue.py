"""
Revenue Analytics Dashboard Module
Comprehensive Q6-Q10 revenue analysis and visualization
"""
import streamlit as st
import pandas as pd
from eda.revenue_trends_analysis import revenue_trend_analysis
from eda.advanced_analysis_1 import (
    category_performance_analysis,
    geographic_analysis,
    festival_impact_analysis,
    price_demand_analysis
)


def show_revenue_dashboard(df):
    """Display comprehensive revenue analytics dashboard"""
    
    st.header("💰 Revenue Analytics Dashboard")
    st.markdown("*Comprehensive revenue analysis covering trends, categories, geography, festivals, and pricing*")
    
    # Create tabs for each question
    rev_tab1, rev_tab2, rev_tab3, rev_tab4, rev_tab5 = st.tabs([
        "Q6: Trends",
        "Q7: Categories",
        "Q8: Geography",
        "Q9: Festivals",
        "Q10: Pricing"
    ])
    
    # Q6: Revenue Trend Analysis
    with rev_tab1:
        st.markdown("## Q6: Revenue Trend Analysis")
        st.markdown("*Monthly, quarterly, and yearly revenue patterns*")
        
        with st.spinner("Analyzing revenue trends..."):
            result = revenue_trend_analysis(df)
        
        st.pyplot(result['figure'], use_container_width=True)
        
        # Extract metrics from statistics
        stats = result['statistics']
        yearly_data = result['yearly_revenue']
        
        # Revenue metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            yearly_rev = stats['total_revenue'] / 1_000_000
            st.metric(
                "📈 Total Revenue",
                f"₹{yearly_rev:.1f}M",
                "2015-2025"
            )
        
        with col2:
            growth_rate = stats['avg_yearly_growth']
            st.metric(
                "📊 Avg YoY Growth",
                f"{growth_rate:.1f}%",
                "Rate"
            )
        
        with col3:
            max_growth_rate = stats['max_growth_rate']
            st.metric(
                "🚀 Peak Growth",
                f"{max_growth_rate:.1f}%",
                f"Year {int(stats['max_growth_year'])}"
            )
        
        with col4:
            transaction_count = yearly_data['transaction_count'].sum() / 1_000_000
            st.metric(
                "📦 Total Orders",
                f"{transaction_count:.1f}M",
                "Transactions"
            )
        
        # Detailed statistics
        st.markdown("### 📊 Yearly Revenue Statistics")
        display_data = yearly_data.copy()
        display_data.columns = ['Year', 'Revenue (₹)', 'Avg Transaction (₹)', 'Orders', 'Growth (%)']
        
        st.dataframe(
            display_data.style.format({
                'Revenue (₹)': '₹{:,.0f}',
                'Avg Transaction (₹)': '₹{:,.0f}',
                'Orders': '{:,.0f}',
                'Growth (%)': '{:.2f}%'
            }),
            use_container_width=True
        )
        
        st.markdown("### 💡 Key Insights")
        st.markdown(f"""
        - **Total Revenue (2015-2025)**: ₹{yearly_rev:.1f}M
        - **Average YoY Growth**: {growth_rate:.1f}%
        - **Peak Growth Year**: {int(stats['max_growth_year'])} with {max_growth_rate:.1f}% growth
        - **Total Transactions**: {transaction_count:.1f}M orders
        - **Trend**: Strong overall growth trajectory with seasonal variations
        """)
    
    # Q7: Category Performance
    with rev_tab2:
        st.markdown("## Q7: Category Performance Analysis")
        st.markdown("*Revenue by category, category contribution, and performance metrics*")
        
        with st.spinner("Analyzing category performance..."):
            result = category_performance_analysis(df)
        
        st.pyplot(result['figure'], use_container_width=True)
        
        cat_data = result['category_perf']
        
        # Category metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            top_cat = cat_data.index[0]
            top_rev = cat_data['revenue'].iloc[0]
            st.metric(
                "🏆 Top Category",
                top_cat,
                f"₹{top_rev/1_000_000:.1f}M"
            )
        
        with col2:
            total_cat = len(cat_data)
            st.metric(
                "📦 Total Categories",
                total_cat,
                "Products"
            )
        
        with col3:
            avg_rating = cat_data['rating'].mean()
            st.metric(
                "⭐ Avg Category Rating",
                f"{avg_rating:.2f}/5",
                "Overall"
            )
        
        # Category Details
        st.markdown("### 📊 Category Performance Details")
        cat_display = cat_data.copy()
        # Ensure correct column ordering and include market share
        cols = [c for c in ['revenue', 'avg_value', 'items_sold', 'transactions', 'rating', 'market_share'] if c in cat_display.columns]
        cat_display = cat_display[cols]
        cat_display.columns = ['Revenue (₹)', 'Avg Order Value (₹)', 'Items Sold',
                               'Transactions', 'Avg Rating', 'Market Share (%)']

        st.dataframe(
            cat_display.style.format({
                'Revenue (₹)': '₹{:,.0f}',
                'Avg Order Value (₹)': '₹{:,.0f}',
                'Items Sold': '{:,.0f}',
                'Transactions': '{:,.0f}',
                'Avg Rating': '{:.2f}',
                'Market Share (%)': '{:.2f}%'
            }),
            use_container_width=True
        )
        
        st.markdown("### 💡 Category Insights")
        st.markdown(f"""
        - **Top Performer**: {top_cat} leads with ₹{top_rev/1_000_000:.1f}M revenue
        - **Category Diversity**: {total_cat} distinct product categories
        - **Quality Indicator**: Average rating of {avg_rating:.2f}/5 across categories
        - **Strategic Focus**: Top 3 categories account for majority of revenue
        """)
    
    # Q8: Geographic Revenue Analysis
    with rev_tab3:
        st.markdown("## Q8: Geographic Revenue Analysis")
        st.markdown("*State-wise revenue distribution, regional performance, and geographic tiers*")
        
        with st.spinner("Analyzing geographic patterns..."):
            result = geographic_analysis(df)
        
        st.pyplot(result['figure'], use_container_width=True)
        
        # EDA returns 'geo_perf' (top-15) and 'all_geo_perf'
        geo_data = result.get('geo_perf', result.get('all_geo_perf'))
        
        # Geographic metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            top_state = geo_data.index[0]
            top_state_rev = geo_data['revenue'].iloc[0]
            st.metric(
                "📍 Top State",
                top_state,
                f"₹{top_state_rev/1_000_000:.1f}M"
            )
        
        with col2:
            total_states = len(geo_data)
            st.metric(
                "🗺️ States Covered",
                total_states,
                "Regions"
            )
        
        with col3:
            # Ensure 'tier' column exists; if geo_data is top-15 it may be missing.
            all_geo = result.get('all_geo_perf')
            if 'tier' not in geo_data.columns and all_geo is not None and 'tier' in all_geo.columns:
                geo_data = geo_data.copy()
                geo_data['tier'] = all_geo.reindex(geo_data.index)['tier']

            # Accept multiple tier name formats (e.g. 'Tier-1' or 'Tier 1')
            if 'tier' in geo_data.columns:
                tier1_rev = geo_data[geo_data['tier'].isin(['Tier-1', 'Tier 1', 'Tier1'])]['revenue'].sum()
            else:
                # Fallback to aggregated tier_analysis if available
                tier_analysis = result.get('tier_analysis')
                if tier_analysis is not None and 'revenue' in tier_analysis.columns:
                    possible_keys = [k for k in ['Tier-1', 'Tier 1', 'Tier1'] if k in tier_analysis.index]
                    if possible_keys:
                        tier1_rev = tier_analysis.loc[possible_keys, 'revenue'].sum()
                    else:
                        tier1_rev = 0
                else:
                    tier1_rev = 0
            st.metric(
                "🌟 Tier 1 Revenue",
                f"₹{tier1_rev/1_000_000:.1f}M",
                "Top states"
            )
        
        with col4:
            geo_concentration = (top_state_rev / geo_data['revenue'].sum()) * 100
            st.metric(
                "📊 Top State Share",
                f"{geo_concentration:.1f}%",
                "of total"
            )
        
        # Geographic tiers
        st.markdown("### 🏅 State Revenue Tiers")
        if 'tier' in geo_data.columns:
            tier_summary = geo_data.groupby('tier')['revenue'].agg(['sum', 'count'])
            tier_summary.columns = ['Total Revenue (₹)', 'Number of States']
        else:
            # Fallback: use tier_analysis if available
            tier_analysis = result.get('tier_analysis')
            if tier_analysis is not None:
                tier_summary = tier_analysis[['revenue']].rename(columns={'revenue': 'Total Revenue (₹)'}).copy()
                tier_summary['Number of States'] = tier_analysis.get('transactions', 0)
            else:
                tier_summary = None
        
        st.dataframe(
            tier_summary.style.format({
                'Total Revenue (₹)': '₹{:,.0f}',
                'Number of States': '{:,.0f}'
            }),
            use_container_width=True
        )
        
        # Detailed state data
        st.markdown("### 📊 State-wise Performance Details")
        geo_display = geo_data.copy()
        # Select and rename columns that exist in the EDA output
        display_cols = [c for c in ['revenue', 'avg_value', 'transactions', 'unique_customers', 'tier', 'revenue_density'] if c in geo_display.columns]
        geo_display = geo_display[display_cols]
        rename_map = {
            'revenue': 'Revenue (₹)',
            'avg_value': 'Avg Order Value (₹)',
            'transactions': 'Transactions',
            'unique_customers': 'Unique Customers',
            'tier': 'Tier',
            'revenue_density': 'Density Index'
        }
        geo_display = geo_display.rename(columns=rename_map)
        
        st.dataframe(
            geo_display.style.format({
                'Revenue (₹)': '₹{:,.0f}',
                'Avg Order Value (₹)': '₹{:,.0f}',
                'Items Sold': '{:,.0f}',
                'Transactions': '{:,.0f}',
                'Density Index': '{:.2f}'
            }),
            use_container_width=True
        )
        
        st.markdown("### 💡 Geographic Insights")
        st.markdown(f"""
        - **Geographic Concentration**: {total_states} states with {geo_concentration:.1f}% from {top_state}
        - **Tier 1 Performance**: Top tier states generating ₹{tier1_rev/1_000_000:.1f}M
        - **Expansion Opportunity**: Tier 2 and Tier 3 states showing growth potential
        - **Market Penetration**: Geographic expansion critical for revenue growth
        """)
    
    # Q9: Festival Impact Analysis
    with rev_tab4:
        st.markdown("## Q9: Festival Sales Impact Analysis")
        st.markdown("*Festival-specific revenue, customer behavior during festivals, and seasonal patterns*")
        
        with st.spinner("Analyzing festival impact..."):
            result = festival_impact_analysis(df)
        
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
        - **Peak Revenue**: {top_fest} generates **₹{top_rev/1_000_000:.1f}M** revenue
        - **Festival Impact**: Festivals account for **{fest_pct:.1f}%** of annual revenue
        - **Customer Engagement**: Average festival AOV is **₹{avg_aov:,.0f}**
        - **Strategic Importance**: Festival sales critical for quarterly targets
        """)
    
    # Q10: Price Optimization
    with rev_tab5:
        st.markdown("## Q10: Price Optimization (Elasticity & Discount Impact)")
        st.markdown("*Price elasticity analysis, discount effectiveness, and optimal pricing strategies*")
        
        with st.spinner("Analyzing price optimization..."):
            result = price_demand_analysis(df)
        
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
        # price_data index contains the price bin label; columns: ['quantity','avg_value','rating','discount']
        price_display = price_data.reset_index().rename(columns={
            'index': 'Price Range',
            'quantity': 'Quantity Sold',
            'avg_value': 'Avg Price (₹)',
            'rating': 'Avg Rating',
            'discount': 'Avg Discount %'
        })

        # Compute revenue per bin if not present
        if 'Revenue (₹)' not in price_display.columns:
            price_display['Revenue (₹)'] = price_display['Quantity Sold'] * price_display['Avg Price (₹)']

        st.dataframe(
            price_display.style.format({
                'Avg Price (₹)': '₹{:,.0f}',
                'Quantity Sold': '{:,.0f}',
                'Revenue (₹)': '₹{:,.0f}',
                'Avg Rating': '{:.2f}',
                'Avg Discount %': '{:.1f}%'
            }),
            use_container_width=True
        )
        
        st.markdown("### 💡 Pricing Strategy Insights")
        st.markdown(f"""
        - **Optimal Price**: {optimal_price} yields maximum revenue of ₹{optimal_rev:.1f}M
        - **Discount Strategy**: Average {avg_discount:.1f}% discount impacts revenue elasticity
        - **Premium Segment**: High-price products maintain {high_price_rating:.2f}/5 rating
        - **Price Elasticity**: Demand decreases with price increases, optimize margin vs volume
        """)
