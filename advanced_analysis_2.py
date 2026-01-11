"""
Questions 9, 11-20: Advanced EDA Analysis Modules
Age group behavior, delivery performance, returns, brand analysis, CLV,
discounts, ratings, customer journey, inventory, pricing, and business health.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def age_group_analysis(df):
    """Question 9: Customer age group behavior and preferences"""
    age_perf = df.groupby('customer_age_group').agg({
        'final_amount_inr': ['sum', 'mean', 'count'],
        'customer_id': 'nunique',
        'customer_rating': 'mean',
        'quantity': 'mean'
    }).round(2)
    
    age_perf.columns = ['revenue', 'aov', 'transactions', 'unique_customers', 'rating', 'avg_qty']
    age_order = ['13-18', '19-25', '26-35', '36-45', '46-55', '56+']
    age_perf = age_perf.reindex([x for x in age_order if x in age_perf.index])
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # Revenue by age group
    ax1 = axes[0, 0]
    colors_age = plt.cm.viridis(np.linspace(0, 1, len(age_perf)))
    ax1.bar(range(len(age_perf)), age_perf['revenue']/1_000_000, color=colors_age, alpha=0.8)
    ax1.set_xticks(range(len(age_perf)))
    ax1.set_xticklabels(age_perf.index, rotation=0)
    ax1.set_ylabel('Revenue (Million INR)', fontsize=12, fontweight='bold')
    ax1.set_title('Q9.1: Revenue by Age Group', fontsize=14, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3)
    
    # AOV by age
    ax2 = axes[0, 1]
    ax2.plot(range(len(age_perf)), age_perf['aov'], marker='o', linewidth=2.5, 
            markersize=10, color='darkred')
    ax2.fill_between(range(len(age_perf)), age_perf['aov'], alpha=0.3, color='red')
    ax2.set_xticks(range(len(age_perf)))
    ax2.set_xticklabels(age_perf.index, rotation=0)
    ax2.set_ylabel('Average Order Value (INR)', fontsize=12, fontweight='bold')
    ax2.set_title('Q9.2: AOV by Age Group', fontsize=14, fontweight='bold')
    ax2.grid(alpha=0.3)
    
    # Category preferences
    cat_age = df.groupby(['customer_age_group', 'category']).size().unstack(fill_value=0)
    cat_age_pct = cat_age.div(cat_age.sum(axis=1), axis=0) * 100
    cat_age_pct = cat_age_pct.reindex([x for x in age_order if x in cat_age_pct.index])
    
    ax3 = axes[1, 0]
    cat_age_pct.plot(kind='bar', stacked=False, ax=ax3, width=0.8)
    ax3.set_xlabel('Age Group', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Market Share (%)', fontsize=12, fontweight='bold')
    ax3.set_title('Q9.3: Category Preferences by Age', fontsize=14, fontweight='bold')
    ax3.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)
    ax3.grid(axis='y', alpha=0.3)
    plt.setp(ax3.xaxis.get_majorticklabels(), rotation=0)
    
    # Customer satisfaction
    ax4 = axes[1, 1]
    ax4.bar(range(len(age_perf)), age_perf['rating'], color=colors_age, alpha=0.8)
    ax4.set_xticks(range(len(age_perf)))
    ax4.set_xticklabels(age_perf.index, rotation=0)
    ax4.set_ylabel('Average Rating', fontsize=12, fontweight='bold')
    ax4.set_title('Q9.4: Customer Satisfaction by Age', fontsize=14, fontweight='bold')
    ax4.set_ylim([0, 5])
    ax4.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    return {
        'figure': fig,
        'age_perf': age_perf,
        'category_age': cat_age_pct
    }


def delivery_performance_analysis(df):
    """Question 11: Delivery performance and satisfaction analysis"""
    delivery_perf = df.groupby('delivery_type').agg({
        'delivery_days': ['mean', 'median', 'std'],
        'final_amount_inr': 'mean',
        'customer_rating': 'mean',
        'transaction_id': 'count'
    }).round(2)
    
    delivery_perf.columns = ['avg_days', 'median_days', 'std_days', 'aov', 'rating', 'count']
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # Delivery time distribution
    ax1 = axes[0, 0]
    ax1.boxplot([df[df['delivery_type']==dt]['delivery_days'].dropna() 
                 for dt in df['delivery_type'].unique() if pd.notna(dt)],
               labels=[dt for dt in df['delivery_type'].unique() if pd.notna(dt)])
    ax1.set_ylabel('Delivery Days', fontsize=12, fontweight='bold')
    ax1.set_title('Q11.1: Delivery Time Distribution', fontsize=14, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3)
    
    # On-time delivery vs satisfaction
    ax2 = axes[0, 1]
    on_time_analysis = df.groupby('delivery_type').agg({
        'delivery_days': lambda x: (x <= x.median()).sum() / len(x) * 100,
        'customer_rating': 'mean'
    }).round(2)
    ax2_2 = ax2.twinx()
    bars = ax2.bar(range(len(on_time_analysis)), on_time_analysis['delivery_days'], 
                  color='steelblue', alpha=0.7, label='On-Time %')
    ax2_2.plot(range(len(on_time_analysis)), on_time_analysis['customer_rating'], 
              marker='o', color='red', linewidth=2, markersize=8, label='Avg Rating')
    ax2.set_xticks(range(len(on_time_analysis)))
    ax2.set_xticklabels(on_time_analysis.index, rotation=45, ha='right')
    ax2.set_ylabel('On-Time Delivery %', fontsize=12, fontweight='bold', color='steelblue')
    ax2_2.set_ylabel('Average Rating', fontsize=12, fontweight='bold', color='red')
    ax2.set_title('Q11.2: On-Time Delivery vs Satisfaction', fontsize=14, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)
    
    # Geographic delivery performance
    ax3 = axes[1, 0]
    geo_delivery = df.groupby('customer_state')['delivery_days'].mean().sort_values(ascending=False).head(10)
    colors_del = plt.cm.RdYlGn_r(np.linspace(0.3, 0.9, len(geo_delivery)))
    ax3.barh(range(len(geo_delivery)), geo_delivery.values, color=colors_del)
    ax3.set_yticks(range(len(geo_delivery)))
    ax3.set_yticklabels(geo_delivery.index)
    ax3.set_xlabel('Average Delivery Days', fontsize=12, fontweight='bold')
    ax3.set_title('Q11.3: Top 10 States with Longest Delivery', fontsize=14, fontweight='bold')
    ax3.grid(axis='x', alpha=0.3)
    
    # Delivery vs price correlation
    ax4 = axes[1, 1]
    price_bins = pd.cut(df['original_price_inr'], bins=5)
    delivery_by_price = df.groupby(price_bins)['delivery_days'].mean()
    ax4.plot(range(len(delivery_by_price)), delivery_by_price.values, marker='s', 
            linewidth=2, markersize=8, color='darkgreen')
    ax4.set_xticks(range(len(delivery_by_price)))
    ax4.set_xticklabels([f"₹{int(x.left)}-{int(x.right)}" for x in delivery_by_price.index], rotation=45, ha='right')
    ax4.set_ylabel('Average Delivery Days', fontsize=12, fontweight='bold')
    ax4.set_title('Q11.4: Delivery Time vs Price Range', fontsize=14, fontweight='bold')
    ax4.grid(alpha=0.3)
    
    plt.tight_layout()
    return {
        'figure': fig,
        'delivery_perf': delivery_perf
    }


def returns_analysis(df):
    """Question 12: Return patterns and customer satisfaction"""
    return_perf = df.groupby('return_status').agg({
        'final_amount_inr': ['sum', 'mean', 'count'],
        'customer_rating': 'mean',
        'product_rating': 'mean'
    }).round(2)
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # Return status distribution
    ax1 = axes[0, 0]
    return_counts = df['return_status'].value_counts()
    colors_ret = ['green', 'red', 'orange']
    ax1.pie(return_counts.values, labels=return_counts.index, autopct='%1.1f%%',
           colors=colors_ret[:len(return_counts)], startangle=90)
    ax1.set_title('Q12.1: Return Status Distribution', fontsize=14, fontweight='bold')
    
    # Return rate by category
    ax2 = axes[0, 1]
    cat_returns = df[df['return_status']=='Returned'].groupby('category').size()
    cat_total = df.groupby('category').size()
    cat_return_rate = (cat_returns / cat_total * 100).sort_values(ascending=False)
    
    colors_cat = plt.cm.Reds(np.linspace(0.4, 0.9, len(cat_return_rate)))
    ax2.barh(range(len(cat_return_rate)), cat_return_rate.values, color=colors_cat)
    ax2.set_yticks(range(len(cat_return_rate)))
    ax2.set_yticklabels(cat_return_rate.index)
    ax2.set_xlabel('Return Rate (%)', fontsize=12, fontweight='bold')
    ax2.set_title('Q12.2: Return Rate by Category', fontsize=14, fontweight='bold')
    ax2.grid(axis='x', alpha=0.3)
    
    # Product rating impact on returns
    ax3 = axes[1, 0]
    rating_return = df.groupby(pd.cut(df['product_rating'], bins=5))['return_status'].apply(
        lambda x: (x=='Returned').sum()/len(x)*100)
    ax3.plot(range(len(rating_return)), rating_return.values, marker='o', 
            linewidth=2, markersize=8, color='darkblue')
    ax3.fill_between(range(len(rating_return)), rating_return.values, alpha=0.3)
    ax3.set_xticks(range(len(rating_return)))
    ax3.set_xticklabels([f"{int(x.left)}-{int(x.right)}" for x in rating_return.index], rotation=45, ha='right')
    ax3.set_ylabel('Return Rate (%)', fontsize=12, fontweight='bold')
    ax3.set_title('Q12.3: Return Rate vs Product Rating', fontsize=14, fontweight='bold')
    ax3.grid(alpha=0.3)
    
    # Satisfaction by return status
    ax4 = axes[1, 1]
    satisfaction = df.groupby('return_status')['customer_rating'].mean()
    colors_sat = ['green' if x > 3.5 else 'red' for x in satisfaction.values]
    ax4.bar(range(len(satisfaction)), satisfaction.values, color=colors_sat, alpha=0.8)
    ax4.set_xticks(range(len(satisfaction)))
    ax4.set_xticklabels(satisfaction.index, rotation=45, ha='right')
    ax4.set_ylabel('Average Customer Rating', fontsize=12, fontweight='bold')
    ax4.set_title('Q12.4: Satisfaction by Return Status', fontsize=14, fontweight='bold')
    ax4.set_ylim([0, 5])
    ax4.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    return {
        'figure': fig,
        'return_perf': return_perf,
        'return_rate_by_category': cat_return_rate
    }


def brand_analysis(df):
    """Question 13: Brand performance and market share evolution"""
    brand_perf = df.groupby('brand').agg({
        'final_amount_inr': ['sum', 'mean', 'count'],
        'customer_rating': 'mean',
        'product_rating': 'mean'
    }).round(2)
    
    brand_perf.columns = ['revenue', 'aov', 'transactions', 'cust_rating', 'prod_rating']
    brand_perf = brand_perf.sort_values('revenue', ascending=False).head(15)
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # Top brands by revenue
    ax1 = axes[0, 0]
    colors_brand = plt.cm.tab20(np.linspace(0, 1, len(brand_perf)))
    ax1.barh(range(len(brand_perf)), brand_perf['revenue']/1_000_000, color=colors_brand)
    ax1.set_yticks(range(len(brand_perf)))
    ax1.set_yticklabels(brand_perf.index, fontsize=9)
    ax1.set_xlabel('Revenue (Million INR)', fontsize=12, fontweight='bold')
    ax1.set_title('Q13.1: Top 15 Brands by Revenue', fontsize=14, fontweight='bold')
    ax1.grid(axis='x', alpha=0.3)
    
    # Market share
    ax2 = axes[0, 1]
    all_brands = df.groupby('brand')['final_amount_inr'].sum().sort_values(ascending=False)
    top_brands = all_brands.head(10)
    other = all_brands[10:].sum()
    plot_data = pd.concat([top_brands, pd.Series({'Others': other})])
    ax2.pie(plot_data.values, labels=plot_data.index, autopct='%1.1f%%', startangle=90)
    ax2.set_title('Q13.2: Market Share - Top 10 Brands', fontsize=14, fontweight='bold')
    
    # Rating vs revenue scatter
    ax3 = axes[1, 0]
    ax3.scatter(brand_perf['prod_rating'], brand_perf['revenue']/1_000_000, 
               s=brand_perf['transactions']/10, alpha=0.6, c=range(len(brand_perf)), 
               cmap='viridis')
    for idx, row in brand_perf.head(10).iterrows():
        ax3.annotate(idx, (row['prod_rating'], row['revenue']/1_000_000), 
                    fontsize=8, ha='center')
    ax3.set_xlabel('Product Rating', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Revenue (Million INR)', fontsize=12, fontweight='bold')
    ax3.set_title('Q13.3: Rating vs Revenue (Size: Volume)', fontsize=14, fontweight='bold')
    ax3.grid(alpha=0.3)
    
    # AOV by brand
    ax4 = axes[1, 1]
    ax4.bar(range(len(brand_perf)), brand_perf['aov'], color=colors_brand, alpha=0.8)
    ax4.set_xticks(range(len(brand_perf)))
    ax4.set_xticklabels(brand_perf.index, rotation=45, ha='right', fontsize=9)
    ax4.set_ylabel('Average Order Value (INR)', fontsize=12, fontweight='bold')
    ax4.set_title('Q13.4: AOV by Brand', fontsize=14, fontweight='bold')
    ax4.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    return {
        'figure': fig,
        'brand_perf': brand_perf
    }


def discount_effectiveness_analysis(df):
    """Question 15: Discount and promotional effectiveness"""
    discount_bins = pd.cut(df['discount_percent'], bins=[0, 10, 20, 30, 50, 100])
    
    discount_perf = df.groupby(discount_bins).agg({
        'transaction_id': 'count',
        'final_amount_inr': ['sum', 'mean'],
        'customer_rating': 'mean'
    }).round(2)
    
    discount_perf.columns = ['transactions', 'revenue', 'aov', 'rating']
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # Revenue by discount range
    ax1 = axes[0, 0]
    colors_disc = plt.cm.YlGn(np.linspace(0.3, 0.9, len(discount_perf)))
    ax1.bar(range(len(discount_perf)), discount_perf['revenue']/1_000_000, color=colors_disc, alpha=0.8)
    ax1.set_xticks(range(len(discount_perf)))
    ax1.set_xticklabels([f"{int(x.left)}-{int(x.right)}%" for x in discount_perf.index], rotation=0)
    ax1.set_ylabel('Revenue (Million INR)', fontsize=12, fontweight='bold')
    ax1.set_title('Q15.1: Revenue by Discount Range', fontsize=14, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3)
    
    # Sales volume by discount
    ax2 = axes[0, 1]
    ax2.plot(range(len(discount_perf)), discount_perf['transactions']/1000, marker='o', 
            linewidth=2, markersize=8, color='darkblue')
    ax2.fill_between(range(len(discount_perf)), discount_perf['transactions']/1000, alpha=0.3)
    ax2.set_xticks(range(len(discount_perf)))
    ax2.set_xticklabels([f"{int(x.left)}-{int(x.right)}%" for x in discount_perf.index], rotation=0)
    ax2.set_ylabel('Transaction Volume (Thousands)', fontsize=12, fontweight='bold')
    ax2.set_title('Q15.2: Sales Volume by Discount Range', fontsize=14, fontweight='bold')
    ax2.grid(alpha=0.3)
    
    # AOV impact
    ax3 = axes[1, 0]
    ax3.bar(range(len(discount_perf)), discount_perf['aov'], color=colors_disc, alpha=0.8)
    ax3.set_xticks(range(len(discount_perf)))
    ax3.set_xticklabels([f"{int(x.left)}-{int(x.right)}%" for x in discount_perf.index], rotation=0)
    ax3.set_ylabel('Average Order Value (INR)', fontsize=12, fontweight='bold')
    ax3.set_title('Q15.3: AOV Impact of Discounts', fontsize=14, fontweight='bold')
    ax3.grid(axis='y', alpha=0.3)
    
    # Customer satisfaction
    ax4 = axes[1, 1]
    ax4.plot(range(len(discount_perf)), discount_perf['rating'], marker='s', 
            linewidth=2, markersize=8, color='darkgreen')
    ax4.set_xticks(range(len(discount_perf)))
    ax4.set_xticklabels([f"{int(x.left)}-{int(x.right)}%" for x in discount_perf.index], rotation=0)
    ax4.set_ylabel('Average Rating', fontsize=12, fontweight='bold')
    ax4.set_title('Q15.4: Satisfaction vs Discount Level', fontsize=14, fontweight='bold')
    ax4.set_ylim([0, 5])
    ax4.grid(alpha=0.3)
    
    plt.tight_layout()
    return {
        'figure': fig,
        'discount_perf': discount_perf
    }


def rating_impact_analysis(df):
    """Question 16: Product rating patterns and sales impact"""
    rating_bins = pd.cut(df['product_rating'], bins=[0, 2, 3, 4, 4.5, 5])
    
    rating_perf = df.groupby(rating_bins).agg({
        'transaction_id': 'count',
        'final_amount_inr': ['sum', 'mean'],
        'customer_rating': 'mean'
    }).round(2)
    
    rating_perf.columns = ['sales', 'revenue', 'aov', 'cust_rating']
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # Rating distribution
    ax1 = axes[0, 0]
    ax1.hist(df['product_rating'].dropna(), bins=50, color='steelblue', alpha=0.7, edgecolor='black')
    ax1.set_xlabel('Product Rating', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Frequency', fontsize=12, fontweight='bold')
    ax1.set_title('Q16.1: Product Rating Distribution', fontsize=14, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3)
    
    # Sales by rating
    ax2 = axes[0, 1]
    colors_rating = plt.cm.RdYlGn(np.linspace(0, 1, len(rating_perf)))
    ax2.bar(range(len(rating_perf)), rating_perf['sales']/1000, color=colors_rating, alpha=0.8)
    ax2.set_xticks(range(len(rating_perf)))
    ax2.set_xticklabels([f"{int(x.left)}-{int(x.right)}" for x in rating_perf.index], rotation=0)
    ax2.set_ylabel('Sales Volume (Thousands)', fontsize=12, fontweight='bold')
    ax2.set_title('Q16.2: Sales Volume by Product Rating', fontsize=14, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)
    
    # Revenue correlation
    ax3 = axes[1, 0]
    ax3.plot(range(len(rating_perf)), rating_perf['revenue']/1_000_000, marker='o', 
            linewidth=2, markersize=8, color='darkred')
    ax3.fill_between(range(len(rating_perf)), rating_perf['revenue']/1_000_000, alpha=0.3)
    ax3.set_xticks(range(len(rating_perf)))
    ax3.set_xticklabels([f"{int(x.left)}-{int(x.right)}" for x in rating_perf.index], rotation=0)
    ax3.set_ylabel('Revenue (Million INR)', fontsize=12, fontweight='bold')
    ax3.set_title('Q16.3: Revenue by Product Rating', fontsize=14, fontweight='bold')
    ax3.grid(alpha=0.3)
    
    # Category-wise ratings
    ax4 = axes[1, 1]
    cat_ratings = df.groupby('category')['product_rating'].mean().sort_values(ascending=False)
    colors_cat = plt.cm.viridis(np.linspace(0, 1, len(cat_ratings)))
    ax4.barh(range(len(cat_ratings)), cat_ratings.values, color=colors_cat)
    ax4.set_yticks(range(len(cat_ratings)))
    ax4.set_yticklabels(cat_ratings.index)
    ax4.set_xlabel('Average Rating', fontsize=12, fontweight='bold')
    ax4.set_title('Q16.4: Average Rating by Category', fontsize=14, fontweight='bold')
    ax4.grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    return {
        'figure': fig,
        'rating_perf': rating_perf,
        'category_ratings': cat_ratings
    }


def business_health_dashboard(df):
    """Question 20: Comprehensive business health dashboard"""
    df['order_date'] = pd.to_datetime(df['order_date'])
    
    # Key metrics
    total_revenue = df['final_amount_inr'].sum()
    total_customers = df['customer_id'].nunique()
    avg_order_value = df['final_amount_inr'].mean()
    transaction_count = len(df)
    
    # Calculate growth rates
    recent_year = df[df['order_year'] == df['order_year'].max()]
    prev_year = df[df['order_year'] == df['order_year'].max() - 1]
    yoy_growth = ((recent_year['final_amount_inr'].sum() - prev_year['final_amount_inr'].sum()) 
                  / prev_year['final_amount_inr'].sum() * 100) if len(prev_year) > 0 else 0
    
    # Retention metrics
    repeat_customers = df.groupby('customer_id').size()
    retention_rate = (repeat_customers[repeat_customers > 1].count() / total_customers * 100)

    # Operational efficiency metrics
    # On-time delivery: define as deliveries within 7 days (approximation)
    on_time_pct = None
    avg_delivery_days = None
    if 'delivery_days' in df.columns:
        avg_delivery_days = df['delivery_days'].dropna().mean()
        on_time_pct = (df['delivery_days'].dropna() <= 7).sum() / df['delivery_days'].dropna().shape[0] * 100
    else:
        on_time_pct = np.nan
        avg_delivery_days = np.nan

    # Return rate
    if 'return_status' in df.columns:
        return_rate = (df['return_status'] == 'Returned').sum() / len(df) * 100
    else:
        return_rate = np.nan
    
    # Category performance
    top_category = df.groupby('category')['final_amount_inr'].sum().idxmax()
    top_category_revenue = df.groupby('category')['final_amount_inr'].sum().max()
    
    fig = plt.figure(figsize=(18, 12))
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
    
    # KPI cards (as text boxes)
    ax_kpi = fig.add_subplot(gs[0, :])
    ax_kpi.axis('off')
    
    kpi_text = f"""
    KEY PERFORMANCE INDICATORS (2015-2025)
    
    Total Revenue: ₹{total_revenue/1_000_000_000:.2f}B  |  Total Customers: {total_customers:,.0f}  |  Avg Order Value: ₹{avg_order_value:,.0f}
    Total Transactions: {transaction_count:,.0f}  |  YoY Growth: {yoy_growth:.2f}%  |  Customer Retention: {retention_rate:.1f}%
    Top Category: {top_category} (₹{top_category_revenue/1_000_000:.2f}M)
    """
    ax_kpi.text(0.5, 0.5, kpi_text, ha='center', va='center', fontsize=11, 
               bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7),
               family='monospace', fontweight='bold')
    
    # Revenue trend
    ax1 = fig.add_subplot(gs[1, 0])
    yearly_revenue = df.groupby('order_year')['final_amount_inr'].sum()
    ax1.plot(yearly_revenue.index, yearly_revenue.values/1_000_000, marker='o', linewidth=2, markersize=8)
    ax1.fill_between(yearly_revenue.index, yearly_revenue.values/1_000_000, alpha=0.3)
    ax1.set_xlabel('Year', fontweight='bold')
    ax1.set_ylabel('Revenue (Million INR)', fontweight='bold')
    ax1.set_title('Revenue Growth Trend', fontsize=12, fontweight='bold')
    ax1.grid(alpha=0.3)
    
    # Customer acquisition
    ax2 = fig.add_subplot(gs[1, 1])
    yearly_customers = df.groupby('order_year')['customer_id'].nunique()
    ax2.bar(yearly_customers.index, yearly_customers.values/1000, color='steelblue', alpha=0.8)
    ax2.set_xlabel('Year', fontweight='bold')
    ax2.set_ylabel('New Customers (Thousands)', fontweight='bold')
    ax2.set_title('Customer Acquisition Trend', fontsize=12, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)
    
    # Category distribution
    ax3 = fig.add_subplot(gs[1, 2])
    cat_revenue = df.groupby('category')['final_amount_inr'].sum().sort_values(ascending=False)
    ax3.pie(cat_revenue.values, labels=cat_revenue.index, autopct='%1.1f%%', textprops={'fontsize': 8})
    ax3.set_title('Revenue by Category', fontsize=12, fontweight='bold')
    
    # Segment performance
    ax4 = fig.add_subplot(gs[2, 0])
    segment_revenue = df.groupby('customer_spending_tier')['final_amount_inr'].sum()
    colors_seg = plt.cm.Spectral(np.linspace(0, 1, len(segment_revenue)))
    ax4.bar(range(len(segment_revenue)), segment_revenue.values/1_000_000, color=colors_seg)
    ax4.set_xticks(range(len(segment_revenue)))
    ax4.set_xticklabels(segment_revenue.index, rotation=45, ha='right')
    ax4.set_ylabel('Revenue (Million INR)', fontweight='bold')
    ax4.set_title('Revenue by Customer Tier', fontsize=12, fontweight='bold')
    ax4.grid(axis='y', alpha=0.3)
    
    # Prime vs Non-Prime
    ax5 = fig.add_subplot(gs[2, 1])
    prime_revenue = df.groupby('is_prime_member')['final_amount_inr'].sum()
    ax5.pie(prime_revenue.values, labels=['Non-Prime', 'Prime'], autopct='%1.1f%%',
           colors=['#FFB6C6', '#FF69B4'])
    ax5.set_title('Revenue: Prime vs Non-Prime', fontsize=12, fontweight='bold')
    
    # Top 5 brands
    ax6 = fig.add_subplot(gs[2, 2])
    top_brands = df.groupby('brand')['final_amount_inr'].sum().sort_values(ascending=False).head(5)
    ax6.barh(range(len(top_brands)), top_brands.values/1_000_000, color='coral', alpha=0.8)
    ax6.set_yticks(range(len(top_brands)))
    ax6.set_yticklabels(top_brands.index, fontsize=9)
    ax6.set_xlabel('Revenue (Million INR)', fontweight='bold')
    ax6.set_title('Top 5 Brands', fontsize=12, fontweight='bold')
    ax6.grid(axis='x', alpha=0.3)
    
    plt.suptitle('Q20: BUSINESS HEALTH DASHBOARD (2015-2025)', fontsize=16, fontweight='bold', y=0.995)

    # Brief executive insights (automated)
    insights = []
    insights.append(f"Total Revenue: ₹{total_revenue/1_000_000_000:.2f}B")
    insights.append(f"YoY Growth: {yoy_growth:.2f}%")
    insights.append(f"Customer Retention: {retention_rate:.1f}%")
    if not np.isnan(on_time_pct):
        insights.append(f"On-time Delivery: {on_time_pct:.1f}% (≤7 days)")
    if not np.isnan(return_rate):
        insights.append(f"Return Rate: {return_rate:.1f}%")
    insights.append(f"Top Category: {top_category} (₹{top_category_revenue/1_000_000:.2f}M)")

    return {
        'figure': fig,
        'metrics': {
            'total_revenue': total_revenue,
            'total_customers': total_customers,
            'avg_order_value': avg_order_value,
            'yoy_growth': yoy_growth,
            'retention_rate': retention_rate,
            'on_time_pct': on_time_pct,
            'avg_delivery_days': avg_delivery_days,
            'return_rate': return_rate
        },
        'insights': insights
    }
