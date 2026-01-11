"""
Question 1: Revenue Trend Analysis (2015-2025)
Create comprehensive revenue trend analysis showing yearly revenue growth
with percentage growth rates, trend lines, and key growth period annotations.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

def revenue_trend_analysis(df):
    """
    Analyze revenue trends from 2015-2025 with growth rates and trend lines.
    
    Parameters:
    df (pd.DataFrame): Cleaned transaction dataframe
    
    Returns:
    dict: Contains visualization data and statistics
    """
    df['order_date'] = pd.to_datetime(df['order_date'])
    
    # Yearly revenue aggregation
    yearly_revenue = df.groupby(df['order_date'].dt.year)['final_amount_inr'].agg([
        ('total_revenue', 'sum'),
        ('avg_transaction', 'mean'),
        ('transaction_count', 'count')
    ]).reset_index()
    
    yearly_revenue.columns = ['year', 'total_revenue', 'avg_transaction', 'transaction_count']
    
    # Calculate growth rates
    yearly_revenue['growth_rate'] = yearly_revenue['total_revenue'].pct_change() * 100
    yearly_revenue['growth_rate'] = yearly_revenue['growth_rate'].fillna(0)
    
    # Create visualizations
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # 1. Revenue trend with trend line
    ax1 = axes[0, 0]
    ax1.bar(yearly_revenue['year'], yearly_revenue['total_revenue']/1_000_000, 
            color='steelblue', alpha=0.7, label='Annual Revenue')
    
    # Add trend line
    z = np.polyfit(yearly_revenue['year'], yearly_revenue['total_revenue']/1_000_000, 2)
    p = np.poly1d(z)
    ax1.plot(yearly_revenue['year'], p(yearly_revenue['year']), 
             'r--', linewidth=2, label='Trend Line')
    
    ax1.set_xlabel('Year', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Revenue (Million INR)', fontsize=12, fontweight='bold')
    ax1.set_title('Q1: Yearly Revenue Trend (2015-2025)', fontsize=14, fontweight='bold')
    ax1.legend()
    ax1.grid(axis='y', alpha=0.3)
    
    # 2. Year-over-year growth rate
    ax2 = axes[0, 1]
    colors = ['green' if x > 0 else 'red' for x in yearly_revenue['growth_rate']]
    ax2.bar(yearly_revenue['year'][1:], yearly_revenue['growth_rate'][1:], 
            color=colors[1:], alpha=0.7)
    ax2.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    ax2.set_xlabel('Year', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Growth Rate (%)', fontsize=12, fontweight='bold')
    ax2.set_title('Year-over-Year Revenue Growth Rate', fontsize=14, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)
    
    # 3. Transaction count trend
    ax3 = axes[1, 0]
    ax3.plot(yearly_revenue['year'], yearly_revenue['transaction_count']/1000, 
             marker='o', linewidth=2, markersize=8, color='darkgreen')
    ax3.fill_between(yearly_revenue['year'], yearly_revenue['transaction_count']/1000, 
                     alpha=0.3, color='green')
    ax3.set_xlabel('Year', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Transaction Count (Thousands)', fontsize=12, fontweight='bold')
    ax3.set_title('Annual Transaction Volume Trend', fontsize=14, fontweight='bold')
    ax3.grid(alpha=0.3)
    
    # 4. Average transaction value trend
    ax4 = axes[1, 1]
    ax4.plot(yearly_revenue['year'], yearly_revenue['avg_transaction'], 
             marker='s', linewidth=2, markersize=8, color='darkred')
    ax4.fill_between(yearly_revenue['year'], yearly_revenue['avg_transaction'], 
                     alpha=0.3, color='red')
    ax4.set_xlabel('Year', fontsize=12, fontweight='bold')
    ax4.set_ylabel('Average Transaction Value (INR)', fontsize=12, fontweight='bold')
    ax4.set_title('Average Transaction Value Trend', fontsize=14, fontweight='bold')
    ax4.grid(alpha=0.3)
    
    plt.tight_layout()
    
    return {
        'figure': fig,
        'yearly_revenue': yearly_revenue,
        'statistics': {
            'total_revenue': yearly_revenue['total_revenue'].sum(),
            'avg_yearly_growth': yearly_revenue['growth_rate'].mean(),
            'max_growth_year': yearly_revenue.loc[yearly_revenue['growth_rate'].idxmax(), 'year'],
            'max_growth_rate': yearly_revenue['growth_rate'].max()
        }
    }


def get_revenue_insights(yearly_revenue):
    """Extract key insights from revenue analysis."""
    insights = []
    
    # Identify peak years
    peak_year = yearly_revenue.loc[yearly_revenue['total_revenue'].idxmax()]
    insights.append(f"Peak Revenue Year: {int(peak_year['year'])} with ₹{peak_year['total_revenue']/1_000_000:.2f}M")
    
    # Highest growth year
    if len(yearly_revenue) > 1:
        growth_year = yearly_revenue.loc[yearly_revenue['growth_rate'].idxmax()]
        insights.append(f"Highest Growth: {int(growth_year['year'])} at {growth_year['growth_rate']:.2f}%")
    
    # CAGR calculation
    if len(yearly_revenue) > 1:
        start_revenue = yearly_revenue.iloc[0]['total_revenue']
        end_revenue = yearly_revenue.iloc[-1]['total_revenue']
        years = len(yearly_revenue) - 1
        cagr = ((end_revenue / start_revenue) ** (1/years) - 1) * 100
        insights.append(f"CAGR (2015-2025): {cagr:.2f}%")
    
    return insights
