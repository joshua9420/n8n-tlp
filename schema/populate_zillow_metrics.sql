-- ==============================================================================
-- Populate zillow_metrics_aggregated table
-- ==============================================================================
-- This script aggregates zillow_listings data into the metrics table
-- for different time periods and dimensions.
-- ==============================================================================

-- ==============================================================================
-- 1. DAILY AGGREGATION - By ZIP, Home Type, Bedrooms, Bathrooms, Status
-- ==============================================================================
-- Run this query daily to populate yesterday's metrics
INSERT INTO zillow_metrics_aggregated (
    aggregation_type,
    period_start_date,
    period_end_date,
    zip_code,
    home_type,
    bedrooms,
    bathrooms,
    home_status,
    total_listings,
    new_listings,
    active_listings,
    pending_listings,
    sold_listings,
    average_price,
    median_price,
    min_price,
    max_price,
    average_price_per_sqft,
    median_price_per_sqft,
    average_days_on_market,
    median_days_on_market,
    min_days_on_market,
    max_days_on_market,
    average_area_sqft,
    median_area_sqft,
    min_area_sqft,
    max_area_sqft
)
SELECT
    'daily' AS aggregation_type,
    CURRENT_DATE - INTERVAL '1 day' AS period_start_date,
    CURRENT_DATE - INTERVAL '1 day' AS period_end_date,
    zip_code,
    home_type,
    bedrooms,
    bathrooms,
    home_status,
    
    -- Listing counts
    COUNT(*) AS total_listings,
    COUNT(*) FILTER (WHERE DATE(created_at) = CURRENT_DATE - INTERVAL '1 day') AS new_listings,
    COUNT(*) FILTER (WHERE home_status = 'FOR_SALE') AS active_listings,
    COUNT(*) FILTER (WHERE home_status = 'PENDING') AS pending_listings,
    COUNT(*) FILTER (WHERE home_status = 'SOLD') AS sold_listings,
    
    -- Price metrics
    AVG(price)::NUMERIC(12,2) AS average_price,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY price)::NUMERIC(12,2) AS median_price,
    MIN(price)::NUMERIC(12,2) AS min_price,
    MAX(price)::NUMERIC(12,2) AS max_price,
    
    -- Price per sqft
    AVG(CASE WHEN living_area > 0 THEN price::NUMERIC / living_area ELSE NULL END)::NUMERIC(10,2) AS average_price_per_sqft,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY CASE WHEN living_area > 0 THEN price::NUMERIC / living_area ELSE NULL END)::NUMERIC(10,2) AS median_price_per_sqft,
    
    -- Days on market (convert time_on_zillow from seconds to days)
    AVG(CASE WHEN time_on_zillow > 0 THEN time_on_zillow::NUMERIC / 86400000 ELSE NULL END)::NUMERIC(8,2) AS average_days_on_market,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY CASE WHEN time_on_zillow > 0 THEN time_on_zillow::NUMERIC / 86400000 ELSE NULL END)::NUMERIC(8,2) AS median_days_on_market,
    MIN(CASE WHEN time_on_zillow > 0 THEN time_on_zillow / 86400000 ELSE NULL END) AS min_days_on_market,
    MAX(CASE WHEN time_on_zillow > 0 THEN time_on_zillow / 86400000 ELSE NULL END) AS max_days_on_market,
    
    -- Area metrics
    AVG(living_area)::NUMERIC(10,2) AS average_area_sqft,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY living_area)::NUMERIC(10,2) AS median_area_sqft,
    MIN(living_area) AS min_area_sqft,
    MAX(living_area) AS max_area_sqft
FROM zillow_listings
WHERE DATE(created_at) <= CURRENT_DATE - INTERVAL '1 day'
GROUP BY zip_code, home_type, bedrooms, bathrooms, home_status
ON CONFLICT (aggregation_type, period_start_date, period_end_date, zip_code, home_type, bedrooms, bathrooms, home_status) 
DO UPDATE SET
    total_listings = EXCLUDED.total_listings,
    new_listings = EXCLUDED.new_listings,
    active_listings = EXCLUDED.active_listings,
    pending_listings = EXCLUDED.pending_listings,
    sold_listings = EXCLUDED.sold_listings,
    average_price = EXCLUDED.average_price,
    median_price = EXCLUDED.median_price,
    min_price = EXCLUDED.min_price,
    max_price = EXCLUDED.max_price,
    average_price_per_sqft = EXCLUDED.average_price_per_sqft,
    median_price_per_sqft = EXCLUDED.median_price_per_sqft,
    average_days_on_market = EXCLUDED.average_days_on_market,
    median_days_on_market = EXCLUDED.median_days_on_market,
    min_days_on_market = EXCLUDED.min_days_on_market,
    max_days_on_market = EXCLUDED.max_days_on_market,
    average_area_sqft = EXCLUDED.average_area_sqft,
    median_area_sqft = EXCLUDED.median_area_sqft,
    min_area_sqft = EXCLUDED.min_area_sqft,
    max_area_sqft = EXCLUDED.max_area_sqft,
    updated_at = CURRENT_TIMESTAMP;


-- ==============================================================================
-- 2. WEEKLY AGGREGATION (ROLLING) - By ZIP, Home Type, Bedrooms, Bathrooms, Status
-- ==============================================================================
-- Run this query daily to update the current week's rolling metrics
INSERT INTO zillow_metrics_aggregated (
    aggregation_type,
    period_start_date,
    period_end_date,
    zip_code,
    home_type,
    bedrooms,
    bathrooms,
    home_status,
    total_listings,
    new_listings,
    active_listings,
    pending_listings,
    sold_listings,
    average_price,
    median_price,
    min_price,
    max_price,
    average_price_per_sqft,
    median_price_per_sqft,
    average_days_on_market,
    median_days_on_market,
    min_days_on_market,
    max_days_on_market,
    average_area_sqft,
    median_area_sqft,
    min_area_sqft,
    max_area_sqft
)
SELECT
    'weekly' AS aggregation_type,
    DATE_TRUNC('week', CURRENT_DATE)::DATE AS period_start_date,
    (DATE_TRUNC('week', CURRENT_DATE) + INTERVAL '6 days')::DATE AS period_end_date,
    zip_code,
    home_type,
    bedrooms,
    bathrooms,
    home_status,
    
    -- Listing counts (snapshot as of today within the current week)
    COUNT(*) AS total_listings,
    COUNT(*) FILTER (WHERE DATE(created_at) >= DATE_TRUNC('week', CURRENT_DATE) 
                      AND DATE(created_at) <= CURRENT_DATE) AS new_listings,
    COUNT(*) FILTER (WHERE home_status = 'FOR_SALE') AS active_listings,
    COUNT(*) FILTER (WHERE home_status = 'PENDING') AS pending_listings,
    COUNT(*) FILTER (WHERE home_status = 'SOLD') AS sold_listings,
    
    -- Price metrics
    AVG(price)::NUMERIC(12,2) AS average_price,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY price)::NUMERIC(12,2) AS median_price,
    MIN(price)::NUMERIC(12,2) AS min_price,
    MAX(price)::NUMERIC(12,2) AS max_price,
    
    -- Price per sqft
    AVG(CASE WHEN living_area > 0 THEN price::NUMERIC / living_area ELSE NULL END)::NUMERIC(10,2) AS average_price_per_sqft,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY CASE WHEN living_area > 0 THEN price::NUMERIC / living_area ELSE NULL END)::NUMERIC(10,2) AS median_price_per_sqft,
    
    -- Days on market (convert time_on_zillow from seconds to days)
    AVG(CASE WHEN time_on_zillow > 0 THEN time_on_zillow::NUMERIC / 86400000 ELSE NULL END)::NUMERIC(8,2) AS average_days_on_market,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY CASE WHEN time_on_zillow > 0 THEN time_on_zillow::NUMERIC / 86400000 ELSE NULL END)::NUMERIC(8,2) AS median_days_on_market,
    MIN(CASE WHEN time_on_zillow > 0 THEN time_on_zillow / 86400000 ELSE NULL END) AS min_days_on_market,
    MAX(CASE WHEN time_on_zillow > 0 THEN time_on_zillow / 86400000 ELSE NULL END) AS max_days_on_market,
    
    -- Area metrics
    AVG(living_area)::NUMERIC(10,2) AS average_area_sqft,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY living_area)::NUMERIC(10,2) AS median_area_sqft,
    MIN(living_area) AS min_area_sqft,
    MAX(living_area) AS max_area_sqft
FROM zillow_listings
WHERE DATE(created_at) <= CURRENT_DATE
GROUP BY zip_code, home_type, bedrooms, bathrooms, home_status
ON CONFLICT (aggregation_type, period_start_date, period_end_date, zip_code, home_type, bedrooms, bathrooms, home_status) 
DO UPDATE SET
    total_listings = EXCLUDED.total_listings,
    new_listings = EXCLUDED.new_listings,
    active_listings = EXCLUDED.active_listings,
    pending_listings = EXCLUDED.pending_listings,
    sold_listings = EXCLUDED.sold_listings,
    average_price = EXCLUDED.average_price,
    median_price = EXCLUDED.median_price,
    min_price = EXCLUDED.min_price,
    max_price = EXCLUDED.max_price,
    average_price_per_sqft = EXCLUDED.average_price_per_sqft,
    median_price_per_sqft = EXCLUDED.median_price_per_sqft,
    average_days_on_market = EXCLUDED.average_days_on_market,
    median_days_on_market = EXCLUDED.median_days_on_market,
    min_days_on_market = EXCLUDED.min_days_on_market,
    max_days_on_market = EXCLUDED.max_days_on_market,
    average_area_sqft = EXCLUDED.average_area_sqft,
    median_area_sqft = EXCLUDED.median_area_sqft,
    min_area_sqft = EXCLUDED.min_area_sqft,
    max_area_sqft = EXCLUDED.max_area_sqft,
    updated_at = CURRENT_TIMESTAMP;


-- ==============================================================================
-- 3. MONTHLY AGGREGATION (ROLLING) - By ZIP, Home Type, Bedrooms, Bathrooms, Status
-- ==============================================================================
-- Run this query daily to update the current month's rolling metrics
INSERT INTO zillow_metrics_aggregated (
    aggregation_type,
    period_start_date,
    period_end_date,
    zip_code,
    home_type,
    bedrooms,
    bathrooms,
    home_status,
    total_listings,
    new_listings,
    active_listings,
    pending_listings,
    sold_listings,
    average_price,
    median_price,
    min_price,
    max_price,
    average_price_per_sqft,
    median_price_per_sqft,
    average_days_on_market,
    median_days_on_market,
    min_days_on_market,
    max_days_on_market,
    average_area_sqft,
    median_area_sqft,
    min_area_sqft,
    max_area_sqft
)
SELECT
    'monthly' AS aggregation_type,
    DATE_TRUNC('month', CURRENT_DATE)::DATE AS period_start_date,
    (DATE_TRUNC('month', CURRENT_DATE) + INTERVAL '1 month' - INTERVAL '1 day')::DATE AS period_end_date,
    zip_code,
    home_type,
    bedrooms,
    bathrooms,
    home_status,
    
    -- Listing counts (snapshot as of today within the current month)
    COUNT(*) AS total_listings,
    COUNT(*) FILTER (WHERE DATE(created_at) >= DATE_TRUNC('month', CURRENT_DATE) 
                      AND DATE(created_at) <= CURRENT_DATE) AS new_listings,
    COUNT(*) FILTER (WHERE home_status = 'FOR_SALE') AS active_listings,
    COUNT(*) FILTER (WHERE home_status = 'PENDING') AS pending_listings,
    COUNT(*) FILTER (WHERE home_status = 'SOLD') AS sold_listings,
    
    -- Price metrics
    AVG(price)::NUMERIC(12,2) AS average_price,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY price)::NUMERIC(12,2) AS median_price,
    MIN(price)::NUMERIC(12,2) AS min_price,
    MAX(price)::NUMERIC(12,2) AS max_price,
    
    -- Price per sqft
    AVG(CASE WHEN living_area > 0 THEN price::NUMERIC / living_area ELSE NULL END)::NUMERIC(10,2) AS average_price_per_sqft,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY CASE WHEN living_area > 0 THEN price::NUMERIC / living_area ELSE NULL END)::NUMERIC(10,2) AS median_price_per_sqft,
    
    -- Days on market (convert time_on_zillow from seconds to days)
    AVG(CASE WHEN time_on_zillow > 0 THEN time_on_zillow::NUMERIC / 86400000 ELSE NULL END)::NUMERIC(8,2) AS average_days_on_market,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY CASE WHEN time_on_zillow > 0 THEN time_on_zillow::NUMERIC / 86400000 ELSE NULL END)::NUMERIC(8,2) AS median_days_on_market,
    MIN(CASE WHEN time_on_zillow > 0 THEN time_on_zillow / 86400000 ELSE NULL END) AS min_days_on_market,
    MAX(CASE WHEN time_on_zillow > 0 THEN time_on_zillow / 86400000 ELSE NULL END) AS max_days_on_market,
    
    -- Area metrics
    AVG(living_area)::NUMERIC(10,2) AS average_area_sqft,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY living_area)::NUMERIC(10,2) AS median_area_sqft,
    MIN(living_area) AS min_area_sqft,
    MAX(living_area) AS max_area_sqft
FROM zillow_listings
WHERE DATE(created_at) <= CURRENT_DATE
GROUP BY zip_code, home_type, bedrooms, bathrooms, home_status
ON CONFLICT (aggregation_type, period_start_date, period_end_date, zip_code, home_type, bedrooms, bathrooms, home_status) 
DO UPDATE SET
    total_listings = EXCLUDED.total_listings,
    new_listings = EXCLUDED.new_listings,
    active_listings = EXCLUDED.active_listings,
    pending_listings = EXCLUDED.pending_listings,
    sold_listings = EXCLUDED.sold_listings,
    average_price = EXCLUDED.average_price,
    median_price = EXCLUDED.median_price,
    min_price = EXCLUDED.min_price,
    max_price = EXCLUDED.max_price,
    average_price_per_sqft = EXCLUDED.average_price_per_sqft,
    median_price_per_sqft = EXCLUDED.median_price_per_sqft,
    average_days_on_market = EXCLUDED.average_days_on_market,
    median_days_on_market = EXCLUDED.median_days_on_market,
    min_days_on_market = EXCLUDED.min_days_on_market,
    max_days_on_market = EXCLUDED.max_days_on_market,
    average_area_sqft = EXCLUDED.average_area_sqft,
    median_area_sqft = EXCLUDED.median_area_sqft,
    min_area_sqft = EXCLUDED.min_area_sqft,
    max_area_sqft = EXCLUDED.max_area_sqft,
    updated_at = CURRENT_TIMESTAMP;


-- ==============================================================================
-- 4. QUARTERLY AGGREGATION (ROLLING) - By ZIP, Home Type, Bedrooms, Bathrooms, Status
-- ==============================================================================
-- Run this query daily to update the current quarter's rolling metrics
INSERT INTO zillow_metrics_aggregated (
    aggregation_type,
    period_start_date,
    period_end_date,
    zip_code,
    home_type,
    bedrooms,
    bathrooms,
    home_status,
    total_listings,
    new_listings,
    active_listings,
    pending_listings,
    sold_listings,
    average_price,
    median_price,
    min_price,
    max_price,
    average_price_per_sqft,
    median_price_per_sqft,
    average_days_on_market,
    median_days_on_market,
    min_days_on_market,
    max_days_on_market,
    average_area_sqft,
    median_area_sqft,
    min_area_sqft,
    max_area_sqft
)
SELECT
    'quarterly' AS aggregation_type,
    DATE_TRUNC('quarter', CURRENT_DATE)::DATE AS period_start_date,
    (DATE_TRUNC('quarter', CURRENT_DATE) + INTERVAL '3 months' - INTERVAL '1 day')::DATE AS period_end_date,
    zip_code,
    home_type,
    bedrooms,
    bathrooms,
    home_status,
    
    -- Listing counts (snapshot as of today within the current quarter)
    COUNT(*) AS total_listings,
    COUNT(*) FILTER (WHERE DATE(created_at) >= DATE_TRUNC('quarter', CURRENT_DATE) 
                      AND DATE(created_at) <= CURRENT_DATE) AS new_listings,
    COUNT(*) FILTER (WHERE home_status = 'FOR_SALE') AS active_listings,
    COUNT(*) FILTER (WHERE home_status = 'PENDING') AS pending_listings,
    COUNT(*) FILTER (WHERE home_status = 'SOLD') AS sold_listings,
    
    -- Price metrics
    AVG(price)::NUMERIC(12,2) AS average_price,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY price)::NUMERIC(12,2) AS median_price,
    MIN(price)::NUMERIC(12,2) AS min_price,
    MAX(price)::NUMERIC(12,2) AS max_price,
    
    -- Price per sqft
    AVG(CASE WHEN living_area > 0 THEN price::NUMERIC / living_area ELSE NULL END)::NUMERIC(10,2) AS average_price_per_sqft,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY CASE WHEN living_area > 0 THEN price::NUMERIC / living_area ELSE NULL END)::NUMERIC(10,2) AS median_price_per_sqft,
    
    -- Days on market (convert time_on_zillow from seconds to days)
    AVG(CASE WHEN time_on_zillow > 0 THEN time_on_zillow::NUMERIC / 86400000 ELSE NULL END)::NUMERIC(8,2) AS average_days_on_market,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY CASE WHEN time_on_zillow > 0 THEN time_on_zillow::NUMERIC / 86400000 ELSE NULL END)::NUMERIC(8,2) AS median_days_on_market,
    MIN(CASE WHEN time_on_zillow > 0 THEN time_on_zillow / 86400000 ELSE NULL END) AS min_days_on_market,
    MAX(CASE WHEN time_on_zillow > 0 THEN time_on_zillow / 86400000 ELSE NULL END) AS max_days_on_market,
    
    -- Area metrics
    AVG(living_area)::NUMERIC(10,2) AS average_area_sqft,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY living_area)::NUMERIC(10,2) AS median_area_sqft,
    MIN(living_area) AS min_area_sqft,
    MAX(living_area) AS max_area_sqft
FROM zillow_listings
WHERE DATE(created_at) <= CURRENT_DATE
GROUP BY zip_code, home_type, bedrooms, bathrooms, home_status
ON CONFLICT (aggregation_type, period_start_date, period_end_date, zip_code, home_type, bedrooms, bathrooms, home_status) 
DO UPDATE SET
    total_listings = EXCLUDED.total_listings,
    new_listings = EXCLUDED.new_listings,
    active_listings = EXCLUDED.active_listings,
    pending_listings = EXCLUDED.pending_listings,
    sold_listings = EXCLUDED.sold_listings,
    average_price = EXCLUDED.average_price,
    median_price = EXCLUDED.median_price,
    min_price = EXCLUDED.min_price,
    max_price = EXCLUDED.max_price,
    average_price_per_sqft = EXCLUDED.average_price_per_sqft,
    median_price_per_sqft = EXCLUDED.median_price_per_sqft,
    average_days_on_market = EXCLUDED.average_days_on_market,
    median_days_on_market = EXCLUDED.median_days_on_market,
    min_days_on_market = EXCLUDED.min_days_on_market,
    max_days_on_market = EXCLUDED.max_days_on_market,
    average_area_sqft = EXCLUDED.average_area_sqft,
    median_area_sqft = EXCLUDED.median_area_sqft,
    min_area_sqft = EXCLUDED.min_area_sqft,
    max_area_sqft = EXCLUDED.max_area_sqft,
    updated_at = CURRENT_TIMESTAMP;


-- ==============================================================================
-- 5. ZIP-LEVEL AGGREGATION (ROLLING) - All types, bedrooms, bathrooms combined
-- ==============================================================================
-- Run this daily for high-level ZIP code metrics (current month rolling)
INSERT INTO zillow_metrics_aggregated (
    aggregation_type,
    period_start_date,
    period_end_date,
    zip_code,
    home_type,
    bedrooms,
    bathrooms,
    home_status,
    total_listings,
    new_listings,
    active_listings,
    pending_listings,
    sold_listings,
    average_price,
    median_price,
    min_price,
    max_price,
    average_price_per_sqft,
    median_price_per_sqft,
    average_days_on_market,
    median_days_on_market,
    min_days_on_market,
    max_days_on_market,
    average_area_sqft,
    median_area_sqft,
    min_area_sqft,
    max_area_sqft
)
SELECT
    'zip_level' AS aggregation_type,
    DATE_TRUNC('month', CURRENT_DATE)::DATE AS period_start_date,
    (DATE_TRUNC('month', CURRENT_DATE) + INTERVAL '1 month' - INTERVAL '1 day')::DATE AS period_end_date,
    zip_code,
    NULL AS home_type,  -- All types
    NULL AS bedrooms,   -- All bedrooms
    NULL AS bathrooms,  -- All bathrooms
    NULL AS home_status, -- All statuses
    
    -- Listing counts (snapshot as of today within the current month)
    COUNT(*) AS total_listings,
    COUNT(*) FILTER (WHERE DATE(created_at) >= DATE_TRUNC('month', CURRENT_DATE) 
                      AND DATE(created_at) <= CURRENT_DATE) AS new_listings,
    COUNT(*) FILTER (WHERE home_status = 'FOR_SALE') AS active_listings,
    COUNT(*) FILTER (WHERE home_status = 'PENDING') AS pending_listings,
    COUNT(*) FILTER (WHERE home_status = 'SOLD') AS sold_listings,
    
    -- Price metrics
    AVG(price)::NUMERIC(12,2) AS average_price,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY price)::NUMERIC(12,2) AS median_price,
    MIN(price)::NUMERIC(12,2) AS min_price,
    MAX(price)::NUMERIC(12,2) AS max_price,
    
    -- Price per sqft
    AVG(CASE WHEN living_area > 0 THEN price::NUMERIC / living_area ELSE NULL END)::NUMERIC(10,2) AS average_price_per_sqft,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY CASE WHEN living_area > 0 THEN price::NUMERIC / living_area ELSE NULL END)::NUMERIC(10,2) AS median_price_per_sqft,
    
    -- Days on market (convert time_on_zillow from seconds to days)
    AVG(CASE WHEN time_on_zillow > 0 THEN time_on_zillow::NUMERIC / 86400000 ELSE NULL END)::NUMERIC(8,2) AS average_days_on_market,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY CASE WHEN time_on_zillow > 0 THEN time_on_zillow::NUMERIC / 86400000 ELSE NULL END)::NUMERIC(8,2) AS median_days_on_market,
    MIN(CASE WHEN time_on_zillow > 0 THEN time_on_zillow / 86400000 ELSE NULL END) AS min_days_on_market,
    MAX(CASE WHEN time_on_zillow > 0 THEN time_on_zillow / 86400000 ELSE NULL END) AS max_days_on_market,
    
    -- Area metrics
    AVG(living_area)::NUMERIC(10,2) AS average_area_sqft,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY living_area)::NUMERIC(10,2) AS median_area_sqft,
    MIN(living_area) AS min_area_sqft,
    MAX(living_area) AS max_area_sqft
FROM zillow_listings
WHERE DATE(created_at) <= CURRENT_DATE
GROUP BY zip_code
ON CONFLICT (aggregation_type, period_start_date, period_end_date, zip_code, home_type, bedrooms, bathrooms, home_status) 
DO UPDATE SET
    total_listings = EXCLUDED.total_listings,
    new_listings = EXCLUDED.new_listings,
    active_listings = EXCLUDED.active_listings,
    pending_listings = EXCLUDED.pending_listings,
    sold_listings = EXCLUDED.sold_listings,
    average_price = EXCLUDED.average_price,
    median_price = EXCLUDED.median_price,
    min_price = EXCLUDED.min_price,
    max_price = EXCLUDED.max_price,
    average_price_per_sqft = EXCLUDED.average_price_per_sqft,
    median_price_per_sqft = EXCLUDED.median_price_per_sqft,
    average_days_on_market = EXCLUDED.average_days_on_market,
    median_days_on_market = EXCLUDED.median_days_on_market,
    min_days_on_market = EXCLUDED.min_days_on_market,
    max_days_on_market = EXCLUDED.max_days_on_market,
    average_area_sqft = EXCLUDED.average_area_sqft,
    median_area_sqft = EXCLUDED.median_area_sqft,
    min_area_sqft = EXCLUDED.min_area_sqft,
    max_area_sqft = EXCLUDED.max_area_sqft,
    updated_at = CURRENT_TIMESTAMP;
