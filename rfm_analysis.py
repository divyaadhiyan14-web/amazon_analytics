"""
Question 3: RFM (Recency, Frequency, Monetary) Customer Segmentation Analysis
Build customer segmentation using RFM methodology with scatter plots and insights.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

def rfm_segmentation_analysis(df):
    """
    Perform RFM segmentation analysis on customer base.
    
    Parameters:
    df (pd.DataFrame): Cleaned transaction dataframe
    
    Returns:
    dict: Contains RFM analysis and visualizations
    """
    df['order_date'] = pd.to_datetime(df['order_date'])
    
    # Reference date (latest date in dataset + 1 day)
    reference_date = df['order_date'].max() + pd.Timedelta(days=1)
    
    # Calculate RFM metrics
    rfm = df.groupby('customer_id').agg({
        'order_date': lambda x: (reference_date - x.max()).days,  # Recency
        'transaction_id': 'count',  # Frequency
        'final_amount_inr': 'sum'  # Monetary
    }).rename(columns={
        'order_date': 'recency',
        'transaction_id': 'frequency',
        'final_amount_inr': 'monetary'
    }).reset_index()
    
    # Create RFM scores (1-4 quartile-based scoring)
    rfm['r_score'] = pd.qcut(rfm['recency'], q=4, labels=[4, 3, 2, 1], duplicates='drop')
    rfm['f_score'] = pd.qcut(rfm['frequency'].rank(method='first'), q=4, labels=[1, 2, 3, 4], duplicates='drop')
    rfm['m_score'] = pd.qcut(rfm['monetary'], q=4, labels=[1, 2, 3, 4], duplicates='drop')
    
    # Convert to numeric
    rfm['r_score'] = pd.to_numeric(rfm['r_score'])
    rfm['f_score'] = pd.to_numeric(rfm['f_score'])
    rfm['m_score'] = pd.to_numeric(rfm['m_score'])
    
    # Calculate RFM score
    rfm['rfm_score'] = rfm['r_score'] + rfm['f_score'] + rfm['m_score']
    
    # Segmentation
    def segment_customer(score):
        if score >= 10:
            return 'Champions'
        elif score >= 8:
            return 'Loyal Customers'
        elif score >= 6:
            return 'Potential Loyalists'
        elif score >= 4:
            return 'At Risk'
        else:
            return 'Lost'
    
    rfm['segment'] = rfm['rfm_score'].apply(segment_customer)
    
    # Create visualizations
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # 1. RFM Score Distribution
    ax1 = axes[0, 0]
    segment_counts = rfm['segment'].value_counts()
    colors = ['#FFD700', '#C0C0C0', '#CD7F32', '#FF6B6B', '#808080']
    segment_order = ['Champions', 'Loyal Customers', 'Potential Loyalists', 'At Risk', 'Lost']
    segment_counts = segment_counts.reindex(segment_order)
    ax1.barh(segment_counts.index, segment_counts.values, color=colors[:len(segment_counts)])
    ax1.set_xlabel('Number of Customers', fontsize=12, fontweight='bold')
    ax1.set_title('Q3: Customer Segments Distribution', fontsize=14, fontweight='bold')
    ax1.grid(axis='x', alpha=0.3)
    for i, v in enumerate(segment_counts.values):
        ax1.text(v, i, f' {v:,.0f}', va='center', fontweight='bold')
    
    # 2. Recency vs Frequency (colored by Monetary)
    ax2 = axes[0, 1]
    scatter = ax2.scatter(rfm['recency'], rfm['frequency'], 
                         c=rfm['monetary'], s=50, alpha=0.6, cmap='viridis')
    ax2.set_xlabel('Recency (Days Since Last Purchase)', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Frequency (Number of Purchases)', fontsize=12, fontweight='bold')
    ax2.set_title('Recency vs Frequency (Color: Monetary Value)', fontsize=14, fontweight='bold')
    cbar = plt.colorbar(scatter, ax=ax2)
    cbar.set_label('Monetary Value (INR)', fontweight='bold')
    ax2.grid(alpha=0.3)
    
    # 3. Segment-wise Monetary Value
    ax3 = axes[1, 0]
    segment_monetary = rfm.groupby('segment')['monetary'].agg(['mean', 'sum']).reset_index()
    segment_monetary = segment_monetary.set_index('segment').reindex(segment_order)
    x_pos = np.arange(len(segment_monetary))
    bars = ax3.bar(x_pos, segment_monetary['mean']/1000, color=colors[:len(segment_monetary)], alpha=0.8)
    ax3.set_ylabel('Average Monetary Value (Thousands INR)', fontsize=12, fontweight='bold')
    ax3.set_title('Average Customer Value by Segment', fontsize=14, fontweight='bold')
    ax3.set_xticks(x_pos)
    ax3.set_xticklabels(segment_monetary.index, rotation=45, ha='right')
    ax3.grid(axis='y', alpha=0.3)
    
    # 4. Segment-wise Frequency
    ax4 = axes[1, 1]
    segment_freq = rfm.groupby('segment')['frequency'].agg(['mean', 'count']).reset_index()
    segment_freq = segment_freq.set_index('segment').reindex(segment_order)
    bars = ax4.bar(x_pos, segment_freq['mean'], color=colors[:len(segment_freq)], alpha=0.8)
    ax4.set_ylabel('Average Purchase Frequency', fontsize=12, fontweight='bold')
    ax4.set_title('Average Purchase Frequency by Segment', fontsize=14, fontweight='bold')
    ax4.set_xticks(x_pos)
    ax4.set_xticklabels(segment_freq.index, rotation=45, ha='right')
    ax4.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    
    return {
        'figure': fig,
        'rfm': rfm,
        'segment_summary': rfm.groupby('segment').agg({
            'recency': 'mean',
            'frequency': 'mean',
            'monetary': ['mean', 'sum', 'count']
        }).round(2),
        'statistics': {
            'total_customers': len(rfm),
            'champion_count': len(rfm[rfm['segment'] == 'Champions']),
            'avg_clv': rfm['monetary'].mean()
        }
    }


def get_rfm_insights(rfm):
    """Extract RFM-based customer insights."""
    insights = []
    
    # Segment distribution
    segments = rfm['segment'].value_counts()
    insights.append(f"Total Customers: {len(rfm):,.0f}")
    insights.append(f"Champions: {segments.get('Champions', 0):,.0f} customers ({segments.get('Champions', 0)/len(rfm)*100:.1f}%)")
    
    # Average CLV
    avg_clv = rfm['monetary'].mean()
    insights.append(f"Average Customer Lifetime Value: ₹{avg_clv:,.0f}")
    
    # Top segment value
    champion_value = rfm[rfm['segment'] == 'Champions']['monetary'].sum()
    total_value = rfm['monetary'].sum()
    insights.append(f"Champions contribute: {champion_value/total_value*100:.1f}% of total revenue")
    
    return insights
