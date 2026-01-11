"""
Question 2: Seasonal Patterns Analysis
Analyze seasonal patterns in sales data with monthly heatmaps,
peak selling months identification, and cross-year comparisons.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def seasonal_patterns_analysis(df):
    """
    Analyze seasonal patterns in sales with heatmaps and monthly trends.
    
    Parameters:
    df (pd.DataFrame): Cleaned transaction dataframe
    
    Returns:
    dict: Contains visualizations and seasonal statistics
    """
    df['order_date'] = pd.to_datetime(df['order_date'])
    df['month'] = df['order_date'].dt.month
    df['year'] = df['order_date'].dt.year
    df['month_name'] = df['order_date'].dt.strftime('%B')
    
    # Create pivot table for heatmap
    monthly_pivot = df.pivot_table(
        values='final_amount_inr',
        index='month',
        columns='year',
        aggfunc='sum'
    )
    
    # Monthly averages across all years
    monthly_avg = df.groupby('month')['final_amount_inr'].agg(['sum', 'count', 'mean']).reset_index()
    monthly_avg['month_name'] = pd.to_datetime(monthly_avg['month'], format='%m').dt.strftime('%B')
    
    fig, axes = plt.subplots(2, 2, figsize=(18, 12))
    
    # 1. Monthly heatmap
    ax1 = axes[0, 0]
    sns.heatmap(monthly_pivot/1_000_000, annot=True, fmt='.1f', cmap='YlOrRd', 
                ax=ax1, cbar_kws={'label': 'Revenue (Million INR)'})
    ax1.set_xlabel('Year', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Month', fontsize=12, fontweight='bold')
    ax1.set_title('Q2: Monthly Sales Heatmap (2015-2025)', fontsize=14, fontweight='bold')
    
    # 2. Average monthly revenue across all years
    ax2 = axes[0, 1]
    colors = plt.cm.RdYlGn(np.linspace(0.3, 0.9, len(monthly_avg)))
    ax2.bar(range(1, 13), monthly_avg['sum']/1_000_000, color=colors, alpha=0.8)
    ax2.set_xlabel('Month', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Average Revenue (Million INR)', fontsize=12, fontweight='bold')
    ax2.set_title('Average Monthly Revenue (All Years)', fontsize=14, fontweight='bold')
    ax2.set_xticks(range(1, 13))
    ax2.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                         'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    ax2.grid(axis='y', alpha=0.3)
    
    # 3. Transaction count by month
    ax3 = axes[1, 0]
    ax3.plot(range(1, 13), monthly_avg['count']/1000, marker='o', linewidth=2, 
             markersize=8, color='darkblue')
    ax3.fill_between(range(1, 13), monthly_avg['count']/1000, alpha=0.3, color='blue')
    ax3.set_xlabel('Month', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Transaction Count (Thousands)', fontsize=12, fontweight='bold')
    ax3.set_title('Transaction Volume by Month', fontsize=14, fontweight='bold')
    ax3.set_xticks(range(1, 13))
    ax3.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                         'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    ax3.grid(alpha=0.3)
    
    # 4. Peak months identification
    ax4 = axes[1, 1]
    peak_threshold = monthly_avg['sum'].quantile(0.75)
    colors_peak = ['green' if x >= peak_threshold else 'steelblue' for x in monthly_avg['sum']]
    bars = ax4.bar(range(1, 13), monthly_avg['sum']/1_000_000, color=colors_peak, alpha=0.8)
    ax4.axhline(y=peak_threshold/1_000_000, color='red', linestyle='--', 
                linewidth=2, label='Peak Threshold (75th Percentile)')
    ax4.set_xlabel('Month', fontsize=12, fontweight='bold')
    ax4.set_ylabel('Revenue (Million INR)', fontsize=12, fontweight='bold')
    ax4.set_title('Peak Selling Months Identification', fontsize=14, fontweight='bold')
    ax4.set_xticks(range(1, 13))
    ax4.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                         'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    ax4.legend()
    ax4.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    
    # Identify peak months
    peak_months = monthly_avg[monthly_avg['sum'] >= peak_threshold]
    
    return {
        'figure': fig,
        'monthly_pivot': monthly_pivot,
        'monthly_avg': monthly_avg,
        'peak_months': peak_months,
        'statistics': {
            'peak_month': monthly_avg.loc[monthly_avg['sum'].idxmax(), 'month_name'],
            'lowest_month': monthly_avg.loc[monthly_avg['sum'].idxmin(), 'month_name'],
            'seasonality_variation': (monthly_avg['sum'].max() - monthly_avg['sum'].min()) / monthly_avg['sum'].mean() * 100
        }
    }


def get_seasonal_insights(monthly_avg):
    """Extract key seasonal insights."""
    insights = []
    
    # Peak months
    peak_month = monthly_avg.loc[monthly_avg['sum'].idxmax()]
    insights.append(f"Peak Month: {peak_month['month_name']} with ₹{peak_month['sum']/1_000_000:.2f}M revenue")
    
    # Lowest month
    low_month = monthly_avg.loc[monthly_avg['sum'].idxmin()]
    insights.append(f"Lowest Month: {low_month['month_name']} with ₹{low_month['sum']/1_000_000:.2f}M revenue")
    
    # Seasonality variation
    variation = (monthly_avg['sum'].max() - monthly_avg['sum'].min()) / monthly_avg['sum'].mean() * 100
    insights.append(f"Seasonality Variation: {variation:.2f}%")
    
    # Festival season pattern
    festival_months = [10, 11, 12]  # Oct-Dec typically have festivals
    festival_revenue = monthly_avg[monthly_avg['month'].isin(festival_months)]['sum'].sum()
    total_revenue = monthly_avg['sum'].sum()
    festival_pct = (festival_revenue / total_revenue) * 100
    insights.append(f"Oct-Dec Festival Season: {festival_pct:.2f}% of annual revenue")
    
    return insights
