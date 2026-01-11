"""
Products & Inventory Dashboard Module
Product performance, category analysis, and inventory insights
"""
import streamlit as st
import pandas as pd
import numpy as np


def show_products_dashboard(df):
    """Display products and inventory dashboard"""
    
    st.header("📦 Products & Inventory Dashboard")
    st.markdown("*Product performance, category analysis, and inventory insights*")
    
    # Create tabs for products view
    prod_tab1, prod_tab2, prod_tab3 = st.tabs([
        "Product Performance",
        "Category Analysis",
        "Inventory & Stocking"
    ])
    
    # Product Performance
    with prod_tab1:
        st.markdown("## Product Performance Analysis")
        
        # Product metrics
        col1, col2, col3, col4 = st.columns(4)
        
        total_products = df['category'].nunique()
        total_items_sold = len(df)
        avg_rating = df['customer_rating'].mean()
        avg_discount = df['discount_percent'].mean()
        
        with col1:
            st.metric(
                "📦 Product Categories",
                f"{total_products}",
                "Total"
            )
        
        with col2:
            st.metric(
                "🛒 Items Sold",
                f"{total_items_sold:,}",
                "Units"
            )
        
        with col3:
            st.metric(
                "⭐ Avg Rating",
                f"{avg_rating:.2f}/5",
                "Quality"
            )
        
        with col4:
            st.metric(
                "🎁 Avg Discount",
                f"{avg_discount:.1f}%",
                "Promotion"
            )
        
        # Top performing products
        st.markdown("### 🏆 Top Performing Categories (by Revenue)")
        
        top_products = df.groupby('category').agg({
            'final_amount_inr': ['sum', 'count', 'mean'],
            'customer_rating': 'mean',
            'discount_percent': 'mean'
        }).round(2)
        
        top_products.columns = ['Revenue', 'Units Sold', 'Avg Price', 'Rating', 'Avg Discount %']
        top_products = top_products.sort_values('Revenue', ascending=False).head(15)
        
        st.dataframe(
            top_products.style.format({
                'Revenue': '₹{:,.0f}',
                'Units Sold': '{:,.0f}',
                'Avg Price': '₹{:,.0f}',
                'Rating': '{:.2f}',
                'Avg Discount %': '{:.1f}%'
            }),
            use_container_width=True
        )
        
        # Product performance insights
        st.markdown("### 💡 Product Performance Insights")
        
        best_category = top_products.index[0]
        best_revenue = top_products.iloc[0]['Revenue']
        best_rating_category = df.groupby('category')['customer_rating'].mean().idxmax()
        best_rating = df.groupby('category')['customer_rating'].mean().max()
        
        st.markdown(f"""
        - **Best Performer**: {best_category} with ₹{best_revenue/1_000_000:.1f}M revenue
        - **Highest Quality**: {best_rating_category} with {best_rating:.2f}/5 rating
        - **Product Diversity**: {total_products} categories across portfolio
        - **Average Quality**: {avg_rating:.2f}/5 overall customer satisfaction
        - **Pricing Strategy**: Average {avg_discount:.1f}% discount applied across products
        """)
    
    # Category Analysis
    with prod_tab2:
        st.markdown("## Category Deep Dive Analysis")
        
        # Select category for detailed analysis
        categories = sorted(df['category'].unique())
        selected_category = st.selectbox(
            "Select Category for Analysis:",
            categories,
            key="category_select"
        )
        
        # Category-specific metrics
        cat_data = df[df['category'] == selected_category]
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "💰 Category Revenue",
                f"₹{cat_data['final_amount_inr'].sum()/1_000_000:.2f}M",
                "Total"
            )
        
        with col2:
            st.metric(
                "📊 Revenue Share",
                f"{(cat_data['final_amount_inr'].sum() / df['final_amount_inr'].sum() * 100):.1f}%",
                "of total"
            )
        
        with col3:
            st.metric(
                "📦 Units Sold",
                f"{len(cat_data):,}",
                "Items"
            )
        
        with col4:
            st.metric(
                "⭐ Avg Rating",
                f"{cat_data['customer_rating'].mean():.2f}/5",
                "Satisfaction"
            )
        
        # Category trends
        st.markdown(f"### 📈 {selected_category} Analysis")
        
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.markdown("**Price Distribution**")
            price_stats = pd.DataFrame({
                'Metric': ['Min Price', 'Avg Price', 'Median Price', 'Max Price'],
                'Value': [
                    f"₹{cat_data['original_price_inr'].min():,.0f}",
                    f"₹{cat_data['original_price_inr'].mean():,.0f}",
                    f"₹{cat_data['original_price_inr'].median():,.0f}",
                    f"₹{cat_data['original_price_inr'].max():,.0f}"
                ]
            })
            st.dataframe(price_stats, use_container_width=True)
        
        with col_right:
            st.markdown("**Sales Distribution**")
            sales_stats = pd.DataFrame({
                'Metric': ['Total Sales', 'Avg Order Value', 'Max Order', 'Min Order'],
                'Value': [
                    f"₹{cat_data['final_amount_inr'].sum():,.0f}",
                    f"₹{cat_data['final_amount_inr'].mean():,.0f}",
                    f"₹{cat_data['final_amount_inr'].max():,.0f}",
                    f"₹{cat_data['final_amount_inr'].min():,.0f}"
                ]
            })
            st.dataframe(sales_stats, use_container_width=True)
        
        # Rating distribution
        st.markdown("### ⭐ Customer Rating Distribution")
        
        rating_bins = [0, 2, 3, 4, 5.1]
        rating_labels = ['Poor (0-2)', 'Fair (2-3)', 'Good (3-4)', 'Excellent (4-5)']
        rating_dist = pd.cut(cat_data['customer_rating'], bins=rating_bins, labels=rating_labels).value_counts()
        
        st.bar_chart(rating_dist)
        
        # Category insights
        st.markdown("### 💡 Category-Specific Insights")
        
        avg_discount = cat_data['discount_percent'].mean()
        discount_impact = cat_data[cat_data['discount_percent'] > avg_discount]['final_amount_inr'].mean()
        no_discount_impact = cat_data[cat_data['discount_percent'] <= avg_discount]['final_amount_inr'].mean()
        
        st.markdown(f"""
        - **Revenue Contribution**: {(cat_data['final_amount_inr'].sum() / df['final_amount_inr'].sum() * 100):.1f}% of total sales
        - **Average Discount**: {avg_discount:.1f}% applied
        - **Discounted Avg Order**: ₹{discount_impact:,.0f} (higher discount)
        - **Non-Discounted Avg Order**: ₹{no_discount_impact:,.0f} (lower discount)
        - **Customer Satisfaction**: {cat_data['customer_rating'].mean():.2f}/5 rating
        - **Growth Opportunity**: Consider expansion if rating > 4.0 or discount strategy adjustment
        """)
    
    # Inventory & Stocking
    with prod_tab3:
        st.markdown("## Inventory & Stocking Strategy")
        
        # Inventory metrics
        col1, col2, col3, col4 = st.columns(4)
        
        # Calculate inventory-related metrics
        category_velocity = df.groupby('category').size().sort_values(ascending=False)
        slow_moving = len(df[df.groupby('category')['customer_rating'].transform('mean') < 3.5])
        high_demand = len(df[df.groupby('category')['customer_rating'].transform('mean') >= 4.5])
        
        with col1:
            st.metric(
                "🚀 High Demand Categories",
                f"{high_demand:,}",
                "Units"
            )
        
        with col2:
            st.metric(
                "🐢 Slow Moving",
                f"{slow_moving:,}",
                "Units"
            )
        
        with col3:
            st.metric(
                "📊 Fast Moving",
                f"{category_velocity.iloc[0]:,}",
                f"{category_velocity.index[0]}"
            )
        
        with col4:
            st.metric(
                "⚖️ Inventory Balance",
                f"{(high_demand / len(df) * 100):.1f}%",
                "Healthy stock"
            )
        
        # Stock recommendation
        st.markdown("### 📋 Inventory Stock Recommendations")
        
        recommendations = df.groupby('category').agg({
            'customer_rating': 'mean',
            'order_date': 'count',
            'final_amount_inr': 'sum'
        }).rename(columns={
            'customer_rating': 'Avg Rating',
            'order_date': 'Sales Volume',
            'final_amount_inr': 'Revenue'
        }).sort_values('Sales Volume', ascending=False)
        
        recommendations['Stock Level'] = recommendations.apply(
            lambda row: 'HIGH' if row['Avg Rating'] >= 4.3 or row['Sales Volume'] > 100 
                        else 'MEDIUM' if row['Avg Rating'] >= 3.5 
                        else 'LOW', axis=1
        )
        
        st.dataframe(
            recommendations[['Sales Volume', 'Avg Rating', 'Revenue', 'Stock Level']].style.format({
                'Sales Volume': '{:,.0f}',
                'Avg Rating': '{:.2f}',
                'Revenue': '₹{:,.0f}'
            }),
            use_container_width=True
        )
        
        # Stocking strategy
        st.markdown("### 🎯 Stocking Strategy Matrix")
        
        # High priority: High demand + High satisfaction
        st.markdown("**Priority 1 (High Stock) - High Demand + Excellent Rating:**")
        high_priority = recommendations[(recommendations['Avg Rating'] >= 4.3) & (recommendations['Sales Volume'] > 100)]
        if len(high_priority) > 0:
            st.dataframe(
                high_priority[['Sales Volume', 'Avg Rating', 'Revenue']],
                use_container_width=True
            )
        else:
            st.info("No categories in this tier - identify high performers")
        
        # Medium priority
        st.markdown("**Priority 2 (Medium Stock) - Growing Demand or Average Rating:**")
        med_priority = recommendations[(recommendations['Avg Rating'] >= 3.5) & (recommendations['Avg Rating'] < 4.3)]
        if len(med_priority) > 0:
            st.dataframe(
                med_priority[['Sales Volume', 'Avg Rating', 'Revenue']],
                use_container_width=True
            )
        else:
            st.info("No categories in this tier")
        
        # Insights
        st.markdown("### 💡 Inventory Management Insights")
        st.markdown(f"""
        - **Fast-Moving Stock**: {category_velocity.index[0]} is top performer ({category_velocity.iloc[0]} units)
        - **Stock Optimization**: Focus on high-satisfaction, high-volume categories
        - **Slow Movers**: Consider discontinuation or promotion for low-rating items
        - **Seasonal Adjustments**: Increase stock before festival periods
        - **Safety Stock**: Maintain 15-20% buffer for unexpected demand spikes
        - **Reorder Points**: Set reorder levels based on 30-day average velocity
        """)
        
        # Dynamic Stock Calculator
        st.markdown("### 📊 Dynamic Stock Level Calculator")
        
        calculator_col1, calculator_col2 = st.columns(2)
        
        with calculator_col1:
            forecast_days = st.slider("Forecast Period (days):", 7, 90, 30)
        
        with calculator_col2:
            safety_stock_pct = st.slider("Safety Stock %:", 5, 50, 20)
        
        # Calculate recommended stock
        daily_velocity = len(df) / ((df['order_date'].max() - df['order_date'].min()).days or 1)
        recommended_stock = daily_velocity * forecast_days * (1 + safety_stock_pct/100)
        
        st.metric(
            "📦 Recommended Stock Level",
            f"{recommended_stock:,.0f} units",
            f"For {forecast_days} days with {safety_stock_pct}% buffer"
        )
