"""
Rental Market Dashboard - Zillow Data Analytics
"""
import streamlit as st
import sys
import os
import pandas as pd
import altair as alt
from datetime import datetime, timedelta

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db import database

# Page configuration
st.set_page_config(
    page_title="Rental Market Dashboard",
    page_icon="📊",
    layout="wide"
)

# Helper function to safely convert to float
def safe_float(value, default=0.0):
    """Safely convert value to float, return default if conversion fails"""
    try:
        return float(value) if value is not None else default
    except (ValueError, TypeError):
        return default

# Helper function to safely convert to int
def safe_int(value, default=0):
    """Safely convert value to int, return default if conversion fails"""
    try:
        return int(value) if value is not None else default
    except (ValueError, TypeError):
        return default

# Sidebar
# Sidebar
with st.sidebar:
    st.markdown("**📊 Rental Market Dashboard**")
    st.caption("Zillow data analytics for Cincinnati")
    
    st.divider()
    
    # Refresh button
    if st.button("🔄 Refresh Data", use_container_width=True, type="primary"):
        st.cache_data.clear()
        st.rerun()
    
    st.divider()
    
    # Test database connection
    try:
        if database.test_connection():
            st.success("🟢 Database Connected")
        else:
            st.error("🔴 Database Disconnected")
    except Exception as e:
        st.error(f"🔴 DB Error: {str(e)[:50]}")
    
    st.divider()
    
    # Navigation
    if st.button("🏠 Back to Hub", use_container_width=True):
        st.switch_page("app.py")

# Main content
st.title("📊 Rental Market Dashboard")
st.caption("Real-time insights from Zillow rental data")

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Market Overview",
    "🗺️ ZIP Code Analysis", 
    "🏠 Property Listings",
    "📊 Metrics Trends"
])

# ============================================================
# TAB 1: MARKET OVERVIEW
# ============================================================
with tab1:
    st.header("Market Overview")
    
    try:
        # Fetch summary statistics
        summary_query = """
            SELECT 
                COUNT(*) as total_listings,
                COUNT(DISTINCT zip_code) as active_zips,
                AVG(CASE WHEN time_on_zillow > 0 THEN time_on_zillow::NUMERIC / 86400000 ELSE NULL END) as avg_dom,
                PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY CASE WHEN time_on_zillow > 0 THEN time_on_zillow::NUMERIC / 86400000 ELSE NULL END) as median_dom,
                AVG(price) as avg_rent,
                PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY price) as median_rent,
                MIN(price) as min_rent,
                MAX(price) as max_rent,
                COUNT(*) FILTER (WHERE home_status = 'FOR_RENT') as for_rent_count,
                COUNT(*) FILTER (WHERE home_status = 'FOR_SALE') as for_sale_count
            FROM zillow_listings
        """
        summary_data = database.fetch_one(summary_query)
        
        if summary_data:
            # KPI Cards
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "Total Listings", 
                    f"{safe_int(summary_data.get('total_listings', 0)):,}"
                )
                st.caption(f"📍 {safe_int(summary_data.get('active_zips', 0))} ZIP codes")
            
            with col2:
                avg_dom = safe_float(summary_data.get('avg_dom', 0))
                st.metric(
                    "Avg Days on Market", 
                    f"{avg_dom:.1f} days"
                )
                median_dom = safe_float(summary_data.get('median_dom', 0))
                st.caption(f"Median: {median_dom:.1f} days")
            
            with col3:
                median_rent = safe_float(summary_data.get('median_rent', 0))
                st.metric(
                    "Median Rent", 
                    f"${median_rent:,.0f}"
                )
                avg_rent = safe_float(summary_data.get('avg_rent', 0))
                st.caption(f"Average: ${avg_rent:,.0f}")
            
            with col4:
                for_rent = safe_int(summary_data.get('for_rent_count', 0))
                for_sale = safe_int(summary_data.get('for_sale_count', 0))
                st.metric(
                    "For Rent", 
                    f"{for_rent:,}"
                )
                st.caption(f"For Sale: {for_sale:,}")
            
            st.divider()
            
            # Distribution charts
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Listings by Property Type")
                type_query = """
                    SELECT home_type, COUNT(*) as count
                    FROM zillow_listings
                    WHERE home_type IS NOT NULL
                    GROUP BY home_type
                    ORDER BY count DESC
                """
                type_data = database.fetch_data(type_query)
                
                if type_data:
                    df_type = pd.DataFrame(type_data)
                    chart = alt.Chart(df_type).mark_bar().encode(
                        x=alt.X('count:Q', title='Count'),
                        y=alt.Y('home_type:N', sort='-x', title='Property Type'),
                        color=alt.Color('home_type:N', legend=None),
                        tooltip=['home_type', 'count']
                    ).properties(height=300)
                    st.altair_chart(chart, use_container_width=True)
                else:
                    st.info("No property type data available")
            
            with col2:
                st.subheader("Listings by Bedrooms")
                bed_query = """
                    SELECT bedrooms, COUNT(*) as count
                    FROM zillow_listings
                    WHERE bedrooms IS NOT NULL
                    GROUP BY bedrooms
                    ORDER BY bedrooms
                """
                bed_data = database.fetch_data(bed_query)
                
                if bed_data:
                    df_bed = pd.DataFrame(bed_data)
                    chart = alt.Chart(df_bed).mark_bar().encode(
                        x=alt.X('bedrooms:O', title='Bedrooms'),
                        y=alt.Y('count:Q', title='Count'),
                        color=alt.Color('bedrooms:O', legend=None),
                        tooltip=['bedrooms', 'count']
                    ).properties(height=300)
                    st.altair_chart(chart, use_container_width=True)
                else:
                    st.info("No bedroom data available")
            
            # Status distribution
            st.subheader("Listings by Status")
            status_query = """
                SELECT home_status, COUNT(*) as count
                FROM zillow_listings
                WHERE home_status IS NOT NULL
                GROUP BY home_status
                ORDER BY count DESC
            """
            status_data = database.fetch_data(status_query)
            
            if status_data:
                df_status = pd.DataFrame(status_data)
                chart = alt.Chart(df_status).mark_arc(innerRadius=50).encode(
                    theta=alt.Theta('count:Q'),
                    color=alt.Color('home_status:N', title='Status'),
                    tooltip=['home_status', 'count']
                ).properties(height=400)
                st.altair_chart(chart, use_container_width=True)
            else:
                st.info("No status data available")
        else:
            st.warning("No data available in the database")
            
    except Exception as e:
        st.error(f"Error loading market overview: {str(e)}")
        st.info("Please ensure the database is populated with data")
    
    # ============================================================
    # TAB 2: ZIP CODE ANALYSIS
    # ============================================================
    with tab2:
        st.header("ZIP Code Analysis")
        
        try:
            # Get available ZIP codes
            zip_query = "SELECT DISTINCT zip_code FROM zillow_listings ORDER BY zip_code"
            zip_data = database.fetch_data(zip_query)
            
            if zip_data:
                available_zips = [row['zip_code'] for row in zip_data]
                
                # ZIP code selector
                col1, col2 = st.columns([1, 3])
                with col1:
                    selected_zips = st.multiselect(
                        "Select ZIP Codes to Compare",
                        options=available_zips,
                        default=available_zips[:2] if len(available_zips) >= 2 else available_zips
                    )
                
                if selected_zips:
                    # ZIP comparison metrics
                    st.subheader("ZIP Code Comparison")
                    
                    zip_metrics_query = """
                        SELECT 
                            zip_code,
                            COUNT(*) as total_listings,
                            AVG(CASE WHEN time_on_zillow > 0 THEN time_on_zillow::NUMERIC / 86400000 ELSE NULL END) as avg_dom,
                            PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY CASE WHEN time_on_zillow > 0 THEN time_on_zillow::NUMERIC / 86400000 ELSE NULL END) as median_dom,
                            PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY price) as median_rent,
                            AVG(price) as avg_rent,
                            AVG(CASE WHEN living_area > 0 THEN price::NUMERIC / living_area ELSE NULL END) as avg_price_per_sqft
                        FROM zillow_listings
                        WHERE zip_code = ANY(%s)
                        GROUP BY zip_code
                        ORDER BY zip_code
                    """
                    zip_metrics = database.fetch_data(zip_metrics_query, (selected_zips,))
                    
                    if zip_metrics:
                        df_zip = pd.DataFrame(zip_metrics)
                        
                        # Format for display
                        df_display = df_zip.copy()
                        df_display['total_listings'] = df_display['total_listings'].astype(int)
                        df_display['avg_dom'] = df_display['avg_dom'].apply(lambda x: f"{safe_float(x):.1f}")
                        df_display['median_dom'] = df_display['median_dom'].apply(lambda x: f"{safe_float(x):.1f}")
                        df_display['median_rent'] = df_display['median_rent'].apply(lambda x: f"${safe_float(x):,.0f}")
                        df_display['avg_rent'] = df_display['avg_rent'].apply(lambda x: f"${safe_float(x):,.0f}")
                        df_display['avg_price_per_sqft'] = df_display['avg_price_per_sqft'].apply(lambda x: f"${safe_float(x):.2f}")
                        
                        df_display.columns = ['ZIP Code', 'Total Listings', 'Avg DOM', 'Median DOM', 'Median Rent', 'Avg Rent', 'Avg $/sqft']
                        st.dataframe(df_display, use_container_width=True, hide_index=True)
                        
                        # Charts
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.subheader("Average Days on Market")
                            chart = alt.Chart(df_zip).mark_bar().encode(
                                x=alt.X('zip_code:N', title='ZIP Code'),
                                y=alt.Y('avg_dom:Q', title='Avg DOM'),
                                color=alt.Color('zip_code:N', legend=None),
                                tooltip=['zip_code', alt.Tooltip('avg_dom:Q', format='.1f')]
                            ).properties(height=300)
                            st.altair_chart(chart, use_container_width=True)
                        
                        with col2:
                            st.subheader("Median Rent Comparison")
                            chart = alt.Chart(df_zip).mark_bar().encode(
                                x=alt.X('zip_code:N', title='ZIP Code'),
                                y=alt.Y('median_rent:Q', title='Median Rent ($)'),
                                color=alt.Color('zip_code:N', legend=None),
                                tooltip=['zip_code', alt.Tooltip('median_rent:Q', format='$,.0f')]
                            ).properties(height=300)
                            st.altair_chart(chart, use_container_width=True)
                    
                    # Rolling metrics from aggregated table
                    st.divider()
                    st.subheader("Rolling Metrics Trends")
                    
                    agg_query = """
                        SELECT 
                            aggregation_type,
                            period_start_date,
                            zip_code,
                            avg(average_days_on_market) as avg_dom,
                            avg(median_price) as median_rent,
                            sum(total_listings) as total_listings
                        FROM zillow_metrics_aggregated
                        WHERE zip_code = ANY(%s)
                            AND aggregation_type IN ('daily', 'weekly', 'monthly')
                        GROUP BY aggregation_type, period_start_date, zip_code
                        ORDER BY period_start_date DESC, aggregation_type
                        LIMIT 50
                    """
                    
                    agg_data = database.fetch_data(agg_query, (selected_zips,))
                    
                    if agg_data:
                        df_agg = pd.DataFrame(agg_data)
                        
                        # Format for display
                        df_agg_display = df_agg.copy()
                        df_agg_display['avg_dom'] = df_agg_display['avg_dom'].apply(lambda x: f"{safe_float(x):.1f}")
                        df_agg_display['median_rent'] = df_agg_display['median_rent'].apply(lambda x: f"${safe_float(x):,.0f}")
                        df_agg_display['total_listings'] = df_agg_display['total_listings'].astype(int)
                        
                        df_agg_display.columns = ['Period Type', 'Start Date', 'ZIP Code', 'Avg DOM', 'Median Rent', 'Total Listings']
                        st.dataframe(df_agg_display, use_container_width=True, hide_index=True)
                    else:
                        st.info("No aggregated metrics available yet. Run the populate_zillow_metrics.sql queries to generate rolling metrics.")
                else:
                    st.info("Please select at least one ZIP code to analyze")
            else:
                st.warning("No ZIP codes found in the database")
                
        except Exception as e:
            st.error(f"Error loading ZIP code analysis: {str(e)}")
        
        # ============================================================
        # TAB 3: PROPERTY LISTINGS
        # ============================================================
    with tab3:
        st.header("Property Listings")
        
        try:
            # Filters
            col1, col2, col3, col4 = st.columns(4)
            
            # Get filter options
            zip_query = "SELECT DISTINCT zip_code FROM zillow_listings WHERE zip_code IS NOT NULL ORDER BY zip_code"
            available_zips = [row['zip_code'] for row in database.fetch_data(zip_query)]
            
            type_query = "SELECT DISTINCT home_type FROM zillow_listings WHERE home_type IS NOT NULL ORDER BY home_type"
            available_types = [row['home_type'] for row in database.fetch_data(type_query)]
            
            with col1:
                filter_zip = st.multiselect("ZIP Code", options=available_zips, default=available_zips)
            
            with col2:
                filter_beds = st.multiselect("Bedrooms", options=[0, 1, 2, 3, 4, 5], default=[0, 1, 2, 3, 4, 5])
            
            with col3:
                filter_type = st.multiselect("Property Type", options=available_types, default=available_types)
            
            with col4:
                filter_status = st.multiselect("Status", options=['FOR_RENT', 'FOR_SALE', 'PENDING', 'SOLD'], default=['FOR_RENT', 'FOR_SALE'])
            
            # Price range
            col1, col2 = st.columns(2)
            with col1:
                min_price = st.number_input("Min Price ($)", min_value=0, value=0, step=100)
            with col2:
                max_price = st.number_input("Max Price ($)", min_value=0, value=10000, step=100)
            
            # Fetch listings with filters
            listings_query = """
                SELECT 
                    zpid,
                    street_address,
                    city,
                    zip_code,
                    bedrooms,
                    bathrooms,
                    living_area,
                    home_type,
                    home_status,
                    price,
                    CASE WHEN time_on_zillow > 0 THEN ROUND((time_on_zillow::NUMERIC / 86400000)::NUMERIC, 0) ELSE NULL END as days_on_zillow,
                    latitude,
                    longitude,
                    CASE WHEN living_area > 0 THEN ROUND((price::NUMERIC / living_area)::NUMERIC, 2) ELSE NULL END as price_per_sqft
                FROM zillow_listings
                WHERE zip_code = ANY(%s)
                    AND bedrooms = ANY(%s)
                    AND home_type = ANY(%s)
                    AND home_status = ANY(%s)
                    AND price >= %s
                    AND price <= %s
                ORDER BY CASE WHEN time_on_zillow > 0 THEN time_on_zillow ELSE NULL END ASC NULLS LAST
                LIMIT 100
            """
            
            listings = database.fetch_data(
                listings_query, 
                (filter_zip, filter_beds, filter_type, filter_status, min_price, max_price)
            )
            
            if listings:
                st.success(f"Found {len(listings)} listings")
                
                # Display table
                df_listings = pd.DataFrame(listings)
                
                # Format for display
                df_display = df_listings[[
                    'street_address', 'zip_code', 'bedrooms', 'bathrooms', 
                    'living_area', 'home_type', 'home_status', 'price', 
                    'days_on_zillow', 'price_per_sqft'
                ]].copy()
                
                df_display['price'] = df_display['price'].apply(lambda x: f"${safe_float(x):,.0f}")
                df_display['price_per_sqft'] = df_display['price_per_sqft'].apply(
                    lambda x: f"${safe_float(x):.2f}" if x else "N/A"
                )
                
                df_display.columns = [
                    'Address', 'ZIP', 'Beds', 'Baths', 'Sqft', 
                    'Type', 'Status', 'Price', 'DOM', '$/Sqft'
                ]
                
                st.dataframe(df_display, use_container_width=True, hide_index=True)
                
                # Map visualization
                st.subheader("Property Locations")
                
                # Filter out listings without coordinates
                df_map = df_listings[
                    (df_listings['latitude'].notna()) & 
                    (df_listings['longitude'].notna())
                ].copy()
                
                if not df_map.empty:
                    # Rename columns for st.map
                    df_map = df_map.rename(columns={'latitude': 'lat', 'longitude': 'lon'})
                    st.map(df_map[['lat', 'lon']], zoom=11)
                else:
                    st.info("No properties with coordinates available for map display")
            else:
                st.info("No listings found matching your filters")
                
        except Exception as e:
            st.error(f"Error loading property listings: {str(e)}")
        
        # ============================================================
        # TAB 4: METRICS TRENDS
        # ============================================================
    with tab4:
        st.header("Metrics Trends")
        
        try:
            # Check if aggregated data exists
            check_query = "SELECT COUNT(*) as count FROM zillow_metrics_aggregated"
            check_result = database.fetch_one(check_query)
            
            if check_result and check_result['count'] > 0:
                # Aggregation type selector
                agg_type = st.selectbox(
                    "Select Period Type",
                    options=['daily', 'weekly', 'monthly', 'quarterly', 'zip_level'],
                    index=2
                )
                
                # Fetch trend data
                trend_query = """
                    SELECT 
                        period_start_date,
                        zip_code,
                        aggregation_type,
                        AVG(average_days_on_market) as avg_dom,
                        AVG(median_price) as median_rent,
                        AVG(average_price) as avg_rent,
                        SUM(total_listings) as total_listings,
                        SUM(new_listings) as new_listings
                    FROM zillow_metrics_aggregated
                    WHERE aggregation_type = %s
                    GROUP BY period_start_date, zip_code, aggregation_type
                    ORDER BY period_start_date DESC
                    LIMIT 100
                """
                
                trend_data = database.fetch_data(trend_query, (agg_type,))
                
                if trend_data:
                    df_trend = pd.DataFrame(trend_data)
                    df_trend['period_start_date'] = pd.to_datetime(df_trend['period_start_date'])
                    
                    # Time series charts
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("Days on Market Trend")
                        chart = alt.Chart(df_trend).mark_line(point=True).encode(
                            x=alt.X('period_start_date:T', title='Date'),
                            y=alt.Y('avg_dom:Q', title='Avg DOM'),
                            color=alt.Color('zip_code:N', title='ZIP Code'),
                            tooltip=[
                                alt.Tooltip('period_start_date:T', title='Date'),
                                alt.Tooltip('zip_code:N', title='ZIP'),
                                alt.Tooltip('avg_dom:Q', title='Avg DOM', format='.1f')
                            ]
                        ).properties(height=350)
                        st.altair_chart(chart, use_container_width=True)
                    
                    with col2:
                        st.subheader("Median Rent Trend")
                        chart = alt.Chart(df_trend).mark_line(point=True).encode(
                            x=alt.X('period_start_date:T', title='Date'),
                            y=alt.Y('median_rent:Q', title='Median Rent ($)'),
                            color=alt.Color('zip_code:N', title='ZIP Code'),
                            tooltip=[
                                alt.Tooltip('period_start_date:T', title='Date'),
                                alt.Tooltip('zip_code:N', title='ZIP'),
                                alt.Tooltip('median_rent:Q', title='Median Rent', format='$,.0f')
                            ]
                        ).properties(height=350)
                        st.altair_chart(chart, use_container_width=True)
                    
                    # Listings trend
                    st.subheader("Total Listings Trend")
                    chart = alt.Chart(df_trend).mark_area(opacity=0.7).encode(
                        x=alt.X('period_start_date:T', title='Date'),
                        y=alt.Y('total_listings:Q', title='Total Listings'),
                        color=alt.Color('zip_code:N', title='ZIP Code'),
                        tooltip=[
                            alt.Tooltip('period_start_date:T', title='Date'),
                            alt.Tooltip('zip_code:N', title='ZIP'),
                            alt.Tooltip('total_listings:Q', title='Total Listings'),
                            alt.Tooltip('new_listings:Q', title='New Listings')
                        ]
                    ).properties(height=350)
                    st.altair_chart(chart, use_container_width=True)
                    
                    # Data table
                    st.subheader("Detailed Metrics")
                    df_display = df_trend.copy()
                    df_display['period_start_date'] = df_display['period_start_date'].dt.strftime('%Y-%m-%d')
                    df_display['avg_dom'] = df_display['avg_dom'].apply(lambda x: f"{safe_float(x):.1f}")
                    df_display['median_rent'] = df_display['median_rent'].apply(lambda x: f"${safe_float(x):,.0f}")
                    df_display['avg_rent'] = df_display['avg_rent'].apply(lambda x: f"${safe_float(x):,.0f}")
                    df_display['total_listings'] = df_display['total_listings'].astype(int)
                    df_display['new_listings'] = df_display['new_listings'].astype(int)
                    
                    df_display.columns = [
                        'Period Start', 'ZIP Code', 'Type', 'Avg DOM', 
                        'Median Rent', 'Avg Rent', 'Total Listings', 'New Listings'
                    ]
                    st.dataframe(df_display, use_container_width=True, hide_index=True)
                else:
                    st.info(f"No {agg_type} metrics available yet")
            else:
                st.warning("No aggregated metrics available")
                st.info("""
                    **To generate metrics:**
                    1. Ensure listings data is in the `zillow_listings` table
                    2. Run the SQL queries from `schema/populate_zillow_metrics.sql`
                    3. Refresh this dashboard
                """)
                
        except Exception as e:
            st.error(f"Error loading metrics trends: {str(e)}")
