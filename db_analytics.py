"""
Database Connection Manager
Handles connection pooling and execution of analytical queries
"""

import mysql.connector
from mysql.connector import Error, pooling
import pandas as pd
import logging
from typing import Optional, List, Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseManager:
    """
    Manages database connections and provides query execution interface
    """
    
    def __init__(self, config: Dict[str, str], pool_size: int = 5):
        """
        Initialize database connection pool
        
        Args:
            config: Database configuration dict (host, user, password, database)
            pool_size: Number of connections in pool
        """
        self.config = config
        self.pool_size = pool_size
        self.connection_pool = None
        self._initialize_pool()
    
    def _initialize_pool(self):
        """Create connection pool"""
        try:
            self.connection_pool = pooling.MySQLConnectionPool(
                pool_name='amazon_analytics_pool',
                pool_size=self.pool_size,
                pool_reset_session=True,
                **self.config
            )
            logger.info("Connection pool initialized successfully")
        except Error as e:
            logger.error(f"Error creating connection pool: {e}")
            raise
    
    def get_connection(self):
        """Get connection from pool"""
        try:
            return self.connection_pool.get_connection()
        except Error as e:
            logger.error(f"Error getting connection: {e}")
            return None
    
    def execute_query(self, query: str, params: Optional[tuple] = None) -> Optional[pd.DataFrame]:
        """
        Execute SELECT query and return results as DataFrame
        
        Args:
            query: SQL query string
            params: Query parameters tuple
            
        Returns:
            DataFrame with results or None if error
        """
        connection = self.get_connection()
        if not connection:
            return None
        
        try:
            df = pd.read_sql(query, connection, params=params)
            return df
        except Error as e:
            logger.error(f"Error executing query: {e}")
            return None
        finally:
            if connection.is_connected():
                connection.close()
    
    def execute_update(self, query: str, params: Optional[tuple] = None) -> int:
        """
        Execute INSERT/UPDATE/DELETE and return affected rows
        
        Args:
            query: SQL query string
            params: Query parameters tuple
            
        Returns:
            Number of affected rows
        """
        connection = self.get_connection()
        if not connection:
            return 0
        
        try:
            cursor = connection.cursor()
            cursor.execute(query, params or ())
            connection.commit()
            affected_rows = cursor.rowcount
            cursor.close()
            return affected_rows
        except Error as e:
            connection.rollback()
            logger.error(f"Error executing update: {e}")
            return 0
        finally:
            if connection.is_connected():
                connection.close()
    
    def execute_stored_procedure(self, proc_name: str, args: Optional[List] = None) -> bool:
        """
        Execute stored procedure
        
        Args:
            proc_name: Procedure name
            args: Procedure arguments
            
        Returns:
            Success boolean
        """
        connection = self.get_connection()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            cursor.callproc(proc_name, args or [])
            connection.commit()
            cursor.close()
            logger.info(f"Stored procedure '{proc_name}' executed successfully")
            return True
        except Error as e:
            connection.rollback()
            logger.error(f"Error executing procedure '{proc_name}': {e}")
            return False
        finally:
            if connection.is_connected():
                connection.close()


class AnalyticsQueries:
    """
    Repository of pre-built analytical queries for dashboards
    """
    
    def __init__(self, db_manager: DatabaseManager):
        """
        Initialize with database manager
        
        Args:
            db_manager: DatabaseManager instance
        """
        self.db = db_manager
    
    # ========================================================
    # REVENUE ANALYSIS QUERIES
    # ========================================================
    
    def get_revenue_trends(self, start_year: int = 2015, end_year: int = 2025) -> pd.DataFrame:
        """Get annual revenue trends with growth metrics"""
        query = """
        SELECT 
            dd.year,
            SUM(ft.final_amount) as annual_revenue,
            COUNT(DISTINCT ft.transaction_id) as transactions,
            COUNT(DISTINCT ft.customer_id) as unique_customers,
            ROUND(AVG(ft.final_amount), 2) as avg_order_value
        FROM fact_transactions ft
        JOIN dim_date dd ON ft.date_id = dd.date_id
        WHERE dd.year BETWEEN %s AND %s
        GROUP BY dd.year
        ORDER BY dd.year
        """
        return self.db.execute_query(query, (start_year, end_year))
    
    def get_monthly_revenue(self, year: int) -> pd.DataFrame:
        """Get monthly revenue for specific year"""
        query = """
        SELECT 
            dd.month,
            dd.month_name,
            SUM(ft.final_amount) as monthly_revenue,
            COUNT(DISTINCT ft.transaction_id) as transactions,
            COUNT(DISTINCT ft.customer_id) as unique_customers,
            ROUND(AVG(ft.final_amount), 2) as avg_order_value
        FROM fact_transactions ft
        JOIN dim_date dd ON ft.date_id = dd.date_id
        WHERE dd.year = %s
        GROUP BY dd.month, dd.month_name
        ORDER BY dd.month
        """
        return self.db.execute_query(query, (year,))
    
    def get_daily_kpis(self, days: int = 30) -> pd.DataFrame:
        """Get last N days KPIs"""
        query = """
        SELECT 
            dd.calendar_date,
            SUM(ft.final_amount) as daily_revenue,
            COUNT(DISTINCT ft.transaction_id) as transactions,
            COUNT(DISTINCT ft.customer_id) as unique_customers,
            ROUND(AVG(ft.final_amount), 2) as avg_order_value,
            ROUND(AVG(ft.delivery_days), 1) as avg_delivery_days,
            ROUND(100 * SUM(CASE WHEN ft.is_returned = 1 THEN 1 ELSE 0 END) 
                  / COUNT(*), 2) as return_rate_percent,
            ROUND(AVG(ft.rating), 2) as avg_satisfaction
        FROM fact_transactions ft
        JOIN dim_date dd ON ft.date_id = dd.date_id
        WHERE dd.calendar_date >= DATE_SUB(CURDATE(), INTERVAL %s DAY)
        GROUP BY dd.calendar_date, dd.date_id
        ORDER BY dd.calendar_date DESC
        """
        return self.db.execute_query(query, (days,))
    
    # ========================================================
    # CATEGORY ANALYSIS QUERIES
    # ========================================================
    
    def get_category_performance(self) -> pd.DataFrame:
        """Get performance metrics by product category"""
        query = """
        SELECT 
            dp.category,
            COUNT(DISTINCT ft.transaction_id) as transactions,
            COUNT(DISTINCT ft.customer_id) as unique_customers,
            SUM(ft.final_amount) as total_revenue,
            ROUND(100 * SUM(ft.final_amount) / 
                  (SELECT SUM(final_amount) FROM fact_transactions), 2) as revenue_pct,
            ROUND(AVG(ft.final_amount), 2) as avg_order_value,
            ROUND(AVG(ft.rating), 2) as avg_product_rating,
            ROUND(AVG(ft.rating), 2) as avg_customer_rating,
            ROUND(100 * SUM(CASE WHEN ft.is_returned = 1 THEN 1 ELSE 0 END) 
                  / COUNT(*), 2) as return_rate_percent
        FROM fact_transactions ft
        JOIN dim_product dp ON ft.product_id = dp.product_id
        GROUP BY dp.category
        ORDER BY total_revenue DESC
        """
        return self.db.execute_query(query)
    
    def get_top_brands(self, limit: int = 20) -> pd.DataFrame:
        """Get top brands by revenue"""
        query = """
        SELECT 
            dp.brand,
            SUM(ft.final_amount) as total_revenue,
            COUNT(DISTINCT ft.transaction_id) as transactions,
            COUNT(DISTINCT ft.customer_id) as unique_customers,
            ROUND(AVG(ft.final_amount), 2) as avg_order_value,
            ROUND(AVG(ft.rating), 2) as avg_rating,
            ROUND(100 * SUM(ft.final_amount) / 
                  (SELECT SUM(final_amount) FROM fact_transactions), 2) as revenue_pct
        FROM fact_transactions ft
        JOIN dim_product dp ON ft.product_id = dp.product_id
        GROUP BY dp.brand
        ORDER BY total_revenue DESC
        LIMIT %s
        """
        return self.db.execute_query(query, (limit,))
    
    # ========================================================
    # CUSTOMER ANALYSIS QUERIES
    # ========================================================
    
    def get_customer_segments(self) -> pd.DataFrame:
        """Get customer segmentation summary"""
        query = """
        SELECT 
            dc.rfm_segment as segment,
            COUNT(DISTINCT dc.customer_id) as customer_count,
            ROUND(100 * COUNT(DISTINCT dc.customer_id) / 
                  (SELECT COUNT(*) FROM dim_customer), 2) as pct_of_customers,
            ROUND(SUM(ft.final_amount), 2) as segment_revenue,
            ROUND(100 * SUM(ft.final_amount) / 
                  (SELECT SUM(final_amount) FROM fact_transactions), 2) as pct_of_revenue,
            ROUND(AVG(ft.final_amount), 2) as avg_order_value,
            COUNT(DISTINCT ft.transaction_id) as total_transactions
        FROM dim_customer dc
        LEFT JOIN fact_transactions ft ON dc.customer_id = ft.customer_id
        WHERE dc.rfm_segment IS NOT NULL
        GROUP BY dc.rfm_segment
        ORDER BY segment_revenue DESC
        """
        return self.db.execute_query(query)
    
    def get_top_customers(self, limit: int = 10) -> pd.DataFrame:
        """Get top customers by lifetime value"""
        query = """
        SELECT 
            dc.customer_id,
            dc.customer_name,
            dc.customer_state,
            dc.rfm_segment,
            COUNT(DISTINCT ft.transaction_id) as purchases,
            ROUND(SUM(ft.final_amount), 2) as lifetime_value,
            ROUND(AVG(ft.final_amount), 2) as avg_order_value,
            ROUND(AVG(ft.rating), 2) as satisfaction_score,
            dc.is_prime_member
        FROM dim_customer dc
        LEFT JOIN fact_transactions ft ON dc.customer_id = ft.customer_id
        GROUP BY dc.customer_id
        ORDER BY SUM(ft.final_amount) DESC
        LIMIT %s
        """
        return self.db.execute_query(query, (limit,))
    
    def get_customer_by_tier(self) -> pd.DataFrame:
        """Get customer metrics by tier"""
        query = """
        SELECT 
            dc.rfm_segment as customer_tier,
            COUNT(DISTINCT dc.customer_id) as customer_count,
            ROUND(SUM(ft.final_amount), 2) as total_revenue,
            ROUND(AVG(ft.final_amount), 2) as avg_order_value,
            ROUND(AVG(ft.rating), 2) as avg_satisfaction
        FROM dim_customer dc
        LEFT JOIN fact_transactions ft ON dc.customer_id = ft.customer_id
        WHERE dc.rfm_segment IS NOT NULL
        GROUP BY dc.rfm_segment
        ORDER BY total_revenue DESC
        """
        return self.db.execute_query(query)
    
    # ========================================================
    # GEOGRAPHIC ANALYSIS QUERIES
    # ========================================================
    
    def get_geographic_performance(self) -> pd.DataFrame:
        """Get performance by state/region"""
        query = """
        SELECT 
            dc.customer_state,
            dc.customer_tier,
            COUNT(DISTINCT dc.customer_id) as unique_customers,
            COUNT(DISTINCT ft.transaction_id) as transactions,
            ROUND(SUM(ft.final_amount), 2) as total_revenue,
            ROUND(100 * SUM(ft.final_amount) / 
                  (SELECT SUM(final_amount) FROM fact_transactions), 2) as revenue_pct,
            ROUND(AVG(ft.final_amount), 2) as avg_order_value,
            ROUND(AVG(ft.delivery_days), 1) as avg_delivery_days,
            ROUND(AVG(ft.rating), 2) as avg_satisfaction
        FROM dim_customer dc
        LEFT JOIN fact_transactions ft ON dc.customer_id = ft.customer_id
        GROUP BY dc.customer_state, dc.customer_tier
        ORDER BY total_revenue DESC
        """
        return self.db.execute_query(query)
    
    # ========================================================
    # PAYMENT & DELIVERY ANALYSIS
    # ========================================================
    
    def get_payment_method_trends(self, start_year: int = 2015) -> pd.DataFrame:
        """Get payment method adoption over time"""
        query = """
        SELECT 
            dd.year,
            dpm.payment_method_name as payment_method,
            COUNT(DISTINCT ft.transaction_id) as transactions,
            SUM(ft.final_amount) as total_value,
            ROUND(100 * COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY dd.year), 2) as pct_of_year
        FROM fact_transactions ft
        JOIN dim_date dd ON ft.date_id = dd.date_id
        LEFT JOIN dim_payment_method dpm ON ft.payment_method_id = dpm.payment_method_id
        WHERE dd.year >= %s AND ft.payment_method_id IS NOT NULL
        GROUP BY dd.year, dpm.payment_method_name
        ORDER BY dd.year DESC, transactions DESC
        """
        return self.db.execute_query(query, (start_year,))
    
    def get_delivery_metrics(self) -> pd.DataFrame:
        """Get delivery performance metrics"""
        query = """
        SELECT 
            ddt.delivery_type_name as delivery_type,
            COUNT(DISTINCT ft.transaction_id) as total_orders,
            ROUND(AVG(ft.delivery_days), 2) as avg_delivery_days,
            MIN(ft.delivery_days) as min_days,
            MAX(ft.delivery_days) as max_days,
            ROUND(100 * SUM(CASE WHEN ft.delivery_days <= 3 THEN 1 ELSE 0 END) / 
                  COUNT(*), 2) as pct_on_time_3days,
            ROUND(100 * SUM(CASE WHEN ft.delivery_days <= 7 THEN 1 ELSE 0 END) / 
                  COUNT(*), 2) as pct_on_time_7days,
            ROUND(AVG(ft.rating), 2) as avg_satisfaction
        FROM fact_transactions ft
        LEFT JOIN dim_delivery_type ddt ON ft.delivery_type_id = ddt.delivery_type_id
        WHERE ft.delivery_type_id IS NOT NULL
        GROUP BY ddt.delivery_type_name
        """
        return self.db.execute_query(query)
    
    # ========================================================
    # PRODUCT & PRICING ANALYSIS
    # ========================================================
    
    def get_discount_effectiveness(self) -> pd.DataFrame:
        """Analyze discount impact on sales volume and revenue"""
        query = """
        SELECT 
            ROUND(ft.discount_percent / 10) * 10 as discount_range,
            COUNT(DISTINCT ft.transaction_id) as transactions,
            ROUND(SUM(ft.final_amount), 2) as total_revenue,
            ROUND(AVG(ft.final_amount), 2) as avg_order_value,
            ROUND(AVG(ft.rating), 2) as avg_rating,
            ROUND(100 * SUM(CASE WHEN ft.is_returned = 1 THEN 1 ELSE 0 END) / 
                  COUNT(*), 2) as return_rate_pct
        FROM fact_transactions ft
        WHERE ft.discount_percent >= 0
        GROUP BY ROUND(ft.discount_percent / 10) * 10
        ORDER BY discount_range
        """
        return self.db.execute_query(query)
    
    def get_rating_impact(self) -> pd.DataFrame:
        """Analyze impact of product rating on sales"""
        query = """
        SELECT 
            ROUND(dp.rating) as product_rating,
            COUNT(DISTINCT ft.transaction_id) as transactions,
            SUM(ft.final_amount) as total_revenue,
            COUNT(DISTINCT ft.customer_id) as unique_customers,
            ROUND(AVG(ft.final_amount), 2) as avg_order_value,
            COUNT(DISTINCT dp.product_id) as product_count,
            ROUND(100 * SUM(CASE WHEN ft.is_returned = 1 THEN 1 ELSE 0 END) / 
                  COUNT(*), 2) as return_rate_pct
        FROM fact_transactions ft
        JOIN dim_product dp ON ft.product_id = dp.product_id
        WHERE dp.rating IS NOT NULL
        GROUP BY ROUND(dp.rating)
        ORDER BY product_rating DESC
        """
        return self.db.execute_query(query)
    
    # ========================================================
    # TIME-BASED ANALYSIS
    # ========================================================
    
    def get_seasonal_patterns(self) -> pd.DataFrame:
        """Get sales patterns by month across all years"""
        query = """
        SELECT 
            dd.month,
            dd.month_name,
            ROUND(AVG(ft.final_amount), 2) as avg_transaction_value,
            COUNT(DISTINCT ft.transaction_id) as avg_transactions,
            SUM(ft.final_amount) as total_revenue,
            dd.is_festival_season,
            dd.festival_name
        FROM fact_transactions ft
        JOIN dim_date dd ON ft.date_id = dd.date_id
        GROUP BY dd.month, dd.month_name, dd.is_festival_season, dd.festival_name
        ORDER BY dd.month
        """
        return self.db.execute_query(query)
    
    def get_day_of_week_patterns(self) -> pd.DataFrame:
        """Get sales patterns by day of week"""
        query = """
        SELECT 
            dd.day_of_week,
            dd.day_name,
            COUNT(DISTINCT ft.transaction_id) as transactions,
            ROUND(SUM(ft.final_amount), 2) as total_revenue,
            ROUND(AVG(ft.final_amount), 2) as avg_order_value,
            COUNT(DISTINCT ft.customer_id) as unique_customers
        FROM fact_transactions ft
        JOIN dim_date dd ON ft.date_id = dd.date_id
        GROUP BY dd.day_of_week, dd.day_name
        ORDER BY dd.day_of_week
        """
        return self.db.execute_query(query)
    
    # ========================================================
    # PRIME MEMBERSHIP ANALYSIS
    # ========================================================
    
    def get_prime_impact(self) -> pd.DataFrame:
        """Compare Prime vs Non-Prime customers"""
        query = """
        SELECT 
            ft.is_prime_member,
            CASE WHEN ft.is_prime_member THEN 'Prime' ELSE 'Non-Prime' END as membership_type,
            COUNT(DISTINCT ft.transaction_id) as transactions,
            SUM(ft.final_amount) as total_revenue,
            COUNT(DISTINCT ft.customer_id) as unique_customers,
            ROUND(AVG(ft.final_amount), 2) as avg_order_value,
            ROUND(AVG(ft.delivery_days), 2) as avg_delivery_days,
            ROUND(AVG(ft.rating), 2) as avg_satisfaction,
            ROUND(100 * SUM(CASE WHEN ft.is_returned = 1 THEN 1 ELSE 0 END) / 
                  COUNT(*), 2) as return_rate_pct
        FROM fact_transactions ft
        GROUP BY ft.is_prime_member
        """
        return self.db.execute_query(query)
    
    # ========================================================
    # EXECUTIVE DASHBOARDS
    # ========================================================
    
    def get_executive_summary(self) -> pd.DataFrame:
        """Get high-level business metrics"""
        query = """
        SELECT 
            'Total Revenue' as metric_name,
            ROUND(SUM(final_amount), 0) as metric_value,
            'INR' as unit
        FROM fact_transactions
        UNION ALL
        SELECT 
            'Total Transactions',
            COUNT(DISTINCT transaction_id),
            'Count'
        FROM fact_transactions
        UNION ALL
        SELECT 
            'Unique Customers',
            COUNT(DISTINCT customer_id),
            'Count'
        FROM fact_transactions
        UNION ALL
        SELECT 
            'Average Order Value',
            ROUND(AVG(final_amount), 2),
            'INR'
        FROM fact_transactions
        UNION ALL
        SELECT 
            'Return Rate %',
            ROUND(100 * SUM(CASE WHEN is_returned = 1 THEN 1 ELSE 0 END) / 
                  COUNT(*), 2),
            'Percent'
        FROM fact_transactions
        """
        return self.db.execute_query(query)


# ============================================================
# USAGE EXAMPLE
# ============================================================

if __name__ == "__main__":
    # Database configuration
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'root123',
        'database': 'amazon_india_analytics'
    }
    
    # Initialize database manager
    db_manager = DatabaseManager(db_config)
    
    # Initialize analytics queries
    analytics = AnalyticsQueries(db_manager)
    
    # Example: Get revenue trends
    df_revenue = analytics.get_revenue_trends()
    print("Revenue Trends:")
    print(df_revenue)
    
    # Example: Get category performance
    df_categories = analytics.get_category_performance()
    print("\nCategory Performance:")
    print(df_categories)
    
    # Example: Get top customers
    df_top_customers = analytics.get_top_customers(limit=10)
    print("\nTop 10 Customers:")
    print(df_top_customers)
