"""
Questions 14, 17, 18, 19: Additional EDA Analysis
CLV Analysis, Customer Journey, Inventory/Lifecycle, and Competitive Pricing
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def clv_cohort_analysis(df):
    """Question 14: Customer Lifetime Value & Cohort Analysis"""
    df['order_date'] = pd.to_datetime(df['order_date'])
    df['cohort_year'] = df['order_date'].dt.year
    
    # CLV by customer acquisition year
    customer_clv = df.groupby(['customer_id', 'cohort_year']).agg({
        'final_amount_inr': 'sum',
        'order_date': 'count'
    }).rename(columns={'order_date': 'purchase_count'}).reset_index()
    
    cohort_clv = customer_clv.groupby('cohort_year').agg({
        'final_amount_inr': ['mean', 'median', 'sum'],
        'customer_id': 'count'
    }).round(2)
    
    cohort_clv.columns = ['avg_clv', 'median_clv', 'total_value', 'customer_count']
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # Average CLV by cohort
    ax1 = axes[0, 0]
    colors_cohort = plt.cm.Blues(np.linspace(0.4, 0.9, len(cohort_clv)))
    ax1.bar(range(len(cohort_clv)), cohort_clv['avg_clv']/1000, color=colors_cohort, alpha=0.8)
    ax1.set_xticks(range(len(cohort_clv)))
    ax1.set_xticklabels(cohort_clv.index.astype(int))
    ax1.set_ylabel('Average CLV (Thousands INR)', fontsize=12, fontweight='bold')
    ax1.set_title('Q14.1: Average CLV by Customer Cohort', fontsize=14, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3)
    
    # Retention curves (simplified)
    ax2 = axes[0, 1]
    retention_by_cohort = []
    for cohort in sorted(df['cohort_year'].unique()):
        cohort_customers = df[df['cohort_year'] == cohort]['customer_id'].unique()
        repeat_customers = df[(df['customer_id'].isin(cohort_customers)) & 
                             (df['order_date'].dt.year > cohort)]['customer_id'].nunique()
        retention_rate = (repeat_customers / len(cohort_customers) * 100) if len(cohort_customers) > 0 else 0
        retention_by_cohort.append(retention_rate)
    
    ax2.plot(sorted(df['cohort_year'].unique()), retention_by_cohort, marker='o', 
            linewidth=2, markersize=8, color='darkblue')
    ax2.fill_between(sorted(df['cohort_year'].unique()), retention_by_cohort, alpha=0.3)
    ax2.set_xlabel('Cohort Year', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Retention Rate (%)', fontsize=12, fontweight='bold')
    ax2.set_title('Q14.2: Customer Retention by Cohort', fontsize=14, fontweight='bold')
    ax2.grid(alpha=0.3)
    
    # CLV distribution
    ax3 = axes[1, 0]
    ax3.hist(customer_clv['final_amount_inr'], bins=50, color='steelblue', alpha=0.7, edgecolor='black')
    ax3.axvline(customer_clv['final_amount_inr'].mean(), color='red', linestyle='--', linewidth=2, label='Mean')
    ax3.axvline(customer_clv['final_amount_inr'].median(), color='green', linestyle='--', linewidth=2, label='Median')
    ax3.set_xlabel('CLV (INR)', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Number of Customers', fontsize=12, fontweight='bold')
    ax3.set_title('Q14.3: CLV Distribution Across Customer Base', fontsize=14, fontweight='bold')
    ax3.legend()
    ax3.grid(axis='y', alpha=0.3)
    
    # Top CLV segments
    ax4 = axes[1, 1]
    clv_percentiles = pd.qcut(customer_clv['final_amount_inr'], q=4, labels=['Bottom 25%', '25-50%', '50-75%', 'Top 25%'])
    segment_clv = customer_clv.groupby(clv_percentiles)['final_amount_inr'].agg(['sum', 'count'])
    colors_seg = ['#FFB6C6', '#FFE4E1', '#FFC0CB', '#FF69B4']
    ax4.pie(segment_clv['sum'], labels=segment_clv.index, autopct='%1.1f%%', 
           colors=colors_seg, startangle=90)
    ax4.set_title('Q14.4: Revenue Distribution by CLV Segment', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    
    return {
        'figure': fig,
        'cohort_clv': cohort_clv,
        'customer_clv': customer_clv
    }


def customer_journey_analysis(df):
    """Question 17: Customer Journey Analysis"""
    df['order_date'] = pd.to_datetime(df['order_date'])
    
    # Purchase frequency by customer
    purchase_freq = df.groupby('customer_id').size()
    
    # Category transitions (first purchase category vs last purchase category)
    customer_journey = df.sort_values('order_date').groupby('customer_id').agg({
        'category': ['first', 'last', 'count', lambda x: x.nunique()],
        'final_amount_inr': ['sum', 'mean'],
        'order_date': ['min', 'max']
    }).reset_index()
    
    customer_journey.columns = ['customer_id', 'first_category', 'last_category', 
                               'total_purchases', 'category_diversity', 
                               'total_value', 'avg_value', 'first_date', 'last_date']
    
    # Customer lifecycle segments
    def lifecycle_segment(purchases):
        if purchases == 1:
            return 'One-time Buyer'
        elif purchases <= 3:
            return 'Occasional Buyer'
        elif purchases <= 10:
            return 'Regular Buyer'
        else:
            return 'Loyal Customer'
    
    customer_journey['lifecycle'] = customer_journey['total_purchases'].apply(lifecycle_segment)
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # Purchase frequency distribution
    ax1 = axes[0, 0]
    ax1.hist(purchase_freq, bins=50, color='steelblue', alpha=0.7, edgecolor='black')
    ax1.axvline(purchase_freq.mean(), color='red', linestyle='--', linewidth=2)
    ax1.set_xlabel('Purchase Frequency', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Number of Customers', fontsize=12, fontweight='bold')
    ax1.set_title('Q17.1: Purchase Frequency Distribution', fontsize=14, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3)
    
    # Lifecycle segments
    ax2 = axes[0, 1]
    lifecycle_counts = customer_journey['lifecycle'].value_counts()
    lifecycle_order = ['One-time Buyer', 'Occasional Buyer', 'Regular Buyer', 'Loyal Customer']
    lifecycle_counts = lifecycle_counts.reindex(lifecycle_order)
    colors_lifecycle = ['#FFB6C6', '#FFD700', '#87CEEB', '#00CED1']
    ax2.barh(range(len(lifecycle_counts)), lifecycle_counts.values, color=colors_lifecycle, alpha=0.8)
    ax2.set_yticks(range(len(lifecycle_counts)))
    ax2.set_yticklabels(lifecycle_counts.index)
    ax2.set_xlabel('Number of Customers', fontsize=12, fontweight='bold')
    ax2.set_title('Q17.2: Customer Lifecycle Segments', fontsize=14, fontweight='bold')
    ax2.grid(axis='x', alpha=0.3)
    
    # Value by lifecycle
    ax3 = axes[1, 0]
    lifecycle_value = customer_journey.groupby('lifecycle')['total_value'].agg(['mean', 'sum'])
    lifecycle_value = lifecycle_value.reindex(lifecycle_order)
    ax3.bar(range(len(lifecycle_value)), lifecycle_value['mean']/1000, color=colors_lifecycle, alpha=0.8)
    ax3.set_xticks(range(len(lifecycle_value)))
    ax3.set_xticklabels(lifecycle_value.index, rotation=45, ha='right')
    ax3.set_ylabel('Average CLV (Thousands INR)', fontsize=12, fontweight='bold')
    ax3.set_title('Q17.3: CLV by Customer Lifecycle', fontsize=14, fontweight='bold')
    ax3.grid(axis='y', alpha=0.3)
    
    # Category diversity
    ax4 = axes[1, 1]
    ax4.scatter(customer_journey['category_diversity'], customer_journey['total_value']/1000,
               s=customer_journey['total_purchases']*2, alpha=0.5, 
               c=range(len(customer_journey)), cmap='viridis')
    ax4.set_xlabel('Category Diversity (Number of Categories)', fontsize=12, fontweight='bold')
    ax4.set_ylabel('Total Customer Value (Thousands INR)', fontsize=12, fontweight='bold')
    ax4.set_title('Q17.4: Category Diversity vs CLV', fontsize=14, fontweight='bold')
    ax4.grid(alpha=0.3)
    
    plt.tight_layout()
    
    return {
        'figure': fig,
        'customer_journey': customer_journey,
        'lifecycle_counts': lifecycle_counts
    }


def inventory_lifecycle_analysis(df):
    """Question 18: Product Lifecycle & Inventory Patterns"""
    df['order_date'] = pd.to_datetime(df['order_date'])
    
    # Product launch analysis
    product_lifecycle = df.groupby('product_id').agg({
        'order_date': ['min', 'max', 'count'],
        'final_amount_inr': ['sum', 'mean'],
        'category': 'first',
        'product_rating': 'mean'
    }).reset_index()
    
    product_lifecycle.columns = ['product_id', 'launch_date', 'last_sale_date', 
                                'total_sales', 'revenue', 'avg_price', 'category', 'rating']
    
    product_lifecycle['lifecycle_months'] = (product_lifecycle['last_sale_date'] - 
                                             product_lifecycle['launch_date']).dt.days / 30.44
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # Product lifecycle length distribution
    ax1 = axes[0, 0]
    ax1.hist(product_lifecycle['lifecycle_months'].dropna(), bins=50, 
            color='steelblue', alpha=0.7, edgecolor='black')
    ax1.axvline(product_lifecycle['lifecycle_months'].mean(), color='red', 
               linestyle='--', linewidth=2, label='Average')
    ax1.set_xlabel('Lifecycle Length (Months)', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Number of Products', fontsize=12, fontweight='bold')
    ax1.set_title('Q18.1: Product Lifecycle Duration Distribution', fontsize=14, fontweight='bold')
    ax1.legend()
    ax1.grid(axis='y', alpha=0.3)
    
    # Revenue by lifecycle phase
    ax2 = axes[0, 1]
    def lifecycle_phase(months):
        if months <= 12:
            return 'Launch Phase (0-12m)'
        elif months <= 36:
            return 'Growth Phase (12-36m)'
        elif months <= 60:
            return 'Maturity Phase (36-60m)'
        else:
            return 'Decline Phase (60m+)'
    
    product_lifecycle['phase'] = product_lifecycle['lifecycle_months'].apply(lifecycle_phase)
    phase_revenue = product_lifecycle.groupby('phase')['revenue'].agg(['sum', 'count', 'mean'])
    phase_order = ['Launch Phase (0-12m)', 'Growth Phase (12-36m)', 'Maturity Phase (36-60m)', 'Decline Phase (60m+)']
    phase_revenue = phase_revenue.reindex([p for p in phase_order if p in phase_revenue.index])
    
    colors_phase = ['#90EE90', '#FFD700', '#FFA500', '#FF6347']
    ax2.bar(range(len(phase_revenue)), phase_revenue['mean']/1_000_000, 
           color=colors_phase[:len(phase_revenue)], alpha=0.8)
    ax2.set_xticks(range(len(phase_revenue)))
    ax2.set_xticklabels(phase_revenue.index, rotation=45, ha='right', fontsize=9)
    ax2.set_ylabel('Avg Revenue (Million INR)', fontsize=12, fontweight='bold')
    ax2.set_title('Q18.2: Revenue by Product Lifecycle Phase', fontsize=14, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)
    
    # Category lifecycle trends
    ax3 = axes[1, 0]
    cat_lifecycle = product_lifecycle.groupby('category')['lifecycle_months'].mean().sort_values(ascending=False)
    colors_cat = plt.cm.tab10(np.linspace(0, 1, len(cat_lifecycle)))
    ax3.barh(range(len(cat_lifecycle)), cat_lifecycle.values, color=colors_cat)
    ax3.set_yticks(range(len(cat_lifecycle)))
    ax3.set_yticklabels(cat_lifecycle.index)
    ax3.set_xlabel('Average Lifecycle Length (Months)', fontsize=12, fontweight='bold')
    ax3.set_title('Q18.3: Lifecycle Duration by Category', fontsize=14, fontweight='bold')
    ax3.grid(axis='x', alpha=0.3)
    
    # Product rating vs sales
    ax4 = axes[1, 1]
    ax4.scatter(product_lifecycle['rating'].dropna(), product_lifecycle['total_sales'],
               s=product_lifecycle['revenue']/10000, alpha=0.5,
               c=product_lifecycle['lifecycle_months'], cmap='viridis')
    ax4.set_xlabel('Product Rating', fontsize=12, fontweight='bold')
    ax4.set_ylabel('Total Sales (Units)', fontsize=12, fontweight='bold')
    ax4.set_title('Q18.4: Rating vs Sales Volume (Color: Lifecycle)', fontsize=14, fontweight='bold')
    ax4.grid(alpha=0.3)
    
    plt.tight_layout()
    
    return {
        'figure': fig,
        'product_lifecycle': product_lifecycle,
        'phase_analysis': phase_revenue
    }


def competitive_pricing_analysis(df):
    """Question 19: Competitive Pricing Analysis"""
    # Price positioning by category and brand
    competitive_pos = df.groupby(['category', 'brand']).agg({
        'original_price_inr': ['mean', 'min', 'max'],
        'discount_percent': 'mean',
        'final_amount_inr': ['sum', 'count'],
        'product_rating': 'mean'
    }).reset_index()
    
    competitive_pos.columns = ['category', 'brand', 'avg_price', 'min_price', 'max_price',
                              'avg_discount', 'revenue', 'market_share', 'rating']
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # Top 10 categories - price distribution
    ax1 = axes[0, 0]
    top_categories = df.groupby('category')['final_amount_inr'].sum().nlargest(10).index
    df_top = df[df['category'].isin(top_categories)]
    df_top.boxplot(column='original_price_inr', by='category', ax=ax1)
    ax1.set_xlabel('Category', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Price (INR)', fontsize=12, fontweight='bold')
    ax1.set_title('Q19.1: Price Distribution by Top 10 Categories', fontsize=14, fontweight='bold')
    plt.sca(ax1)
    plt.xticks(rotation=45, ha='right')
    
    # Price vs market share
    ax2 = axes[0, 1]
    brand_position = competitive_pos.groupby('brand').agg({
        'avg_price': 'mean',
        'market_share': 'sum',
        'revenue': 'sum'
    }).reset_index()
    brand_position = brand_position[brand_position['market_share'] > 50].sort_values('market_share', ascending=False).head(15)
    
    ax2.scatter(brand_position['avg_price'], brand_position['market_share'],
               s=brand_position['revenue']/10000, alpha=0.6, c=range(len(brand_position)), cmap='viridis')
    for idx, row in brand_position.head(5).iterrows():
        ax2.annotate(row['brand'], (row['avg_price'], row['market_share']), 
                    fontsize=8, ha='center')
    ax2.set_xlabel('Average Price (INR)', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Market Share (Units)', fontsize=12, fontweight='bold')
    ax2.set_title('Q19.2: Price Positioning vs Market Share', fontsize=14, fontweight='bold')
    ax2.grid(alpha=0.3)
    
    # Price elasticity by category
    ax3 = axes[1, 0]
    price_elasticity = df.groupby('category').agg({
        'original_price_inr': 'mean',
        'quantity': 'sum'
    }).reset_index()
    price_elasticity = price_elasticity[price_elasticity['original_price_inr'] > 0]
    price_elasticity['price_quartile'] = pd.qcut(price_elasticity['original_price_inr'], q=4, duplicates='drop')
    
    colors_elasticity = plt.cm.RdYlGn_r(np.linspace(0, 1, len(price_elasticity)))
    ax3.scatter(price_elasticity['original_price_inr']/1000, price_elasticity['quantity'],
               s=100, alpha=0.6, c=range(len(price_elasticity)), cmap='viridis')
    for idx, row in price_elasticity.head(8).iterrows():
        ax3.annotate(row['category'], (row['original_price_inr']/1000, row['quantity']), 
                    fontsize=8, ha='center')
    ax3.set_xlabel('Avg Price (Thousands INR)', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Quantity Sold', fontsize=12, fontweight='bold')
    ax3.set_title('Q19.3: Price Elasticity by Category', fontsize=14, fontweight='bold')
    ax3.grid(alpha=0.3)
    
    # Discount strategy by brand
    ax4 = axes[1, 1]
    brand_discount = competitive_pos.groupby('brand').agg({
        'avg_discount': 'mean',
        'rating': 'mean'
    }).reset_index().sort_values('avg_discount', ascending=False).head(15)
    
    colors_discount = ['green' if x > 3.5 else 'red' for x in brand_discount['rating']]
    ax4.barh(range(len(brand_discount)), brand_discount['avg_discount'], color=colors_discount, alpha=0.8)
    ax4.set_yticks(range(len(brand_discount)))
    ax4.set_yticklabels(brand_discount['brand'], fontsize=9)
    ax4.set_xlabel('Average Discount (%)', fontsize=12, fontweight='bold')
    ax4.set_title('Q19.4: Discount Strategy by Top Brands (Color: Rating)', fontsize=14, fontweight='bold')
    ax4.grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    
    return {
        'figure': fig,
        'competitive_pos': competitive_pos,
        'brand_position': brand_position
    }
