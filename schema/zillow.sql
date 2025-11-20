-- disable foreign key checks to avoid issues during table creation
SET session_replication_role = 'replica';
-- enable foreign key checks after table creation
SET session_replication_role = 'origin';


DROP TABLE IF EXISTS zillow_zip_codes CASCADE;
CREATE TABLE IF NOT EXISTS zillow_zip_codes (
    id SERIAL PRIMARY KEY,
    zip_code VARCHAR(10) UNIQUE NOT NULL,
    city VARCHAR(100),
    state VARCHAR(100),
    county VARCHAR(100),
    country VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);
CREATE INDEX idx_zillow_zip_code ON zillow_zip_codes(zip_code);

CREATE TABLE IF NOT EXISTS zillow_listings (
    id SERIAL PRIMARY KEY,
    zpid BIGINT UNIQUE NOT NULL,  -- Zillow Property ID
    zip_code VARCHAR(10) REFERENCES zillow_zip_codes(zip_code),
    
    -- Address fields
    street_address TEXT,
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    
    -- Location coordinates
    latitude NUMERIC(10, 7),
    longitude NUMERIC(10, 7),
    
    -- Property details
    bedrooms INT,
    bathrooms INT,
    living_area INT,  -- sqft
    home_type VARCHAR(50),  -- e.g., 'SINGLE_FAMILY', 'CONDO', 'TOWNHOUSE'
    
    -- Listing status
    home_status VARCHAR(50),  -- e.g., 'FOR_SALE', 'FOR_RENT'
    home_status_for_hdp VARCHAR(50),
    days_on_zillow INT,
    time_on_zillow BIGINT,  -- in seconds
    
    -- Pricing
    price BIGINT,
    price_for_hdp BIGINT,
    currency VARCHAR(10),
    price_change INT,  -- nullable
    date_price_changed BIGINT,  -- unix timestamp, nullable
    price_reduction VARCHAR(20),  -- nullable, e.g., '-2%'
    
    -- Estimates and valuations
    zestimate BIGINT,  -- nullable
    rent_zestimate INT,  -- nullable
    tax_assessed_value BIGINT,  -- nullable
    
    -- Media
    img_src TEXT,
    video_count INT,  -- nullable
    
    -- Flags
    is_featured BOOLEAN DEFAULT FALSE,
    is_non_owner_occupied BOOLEAN DEFAULT FALSE,
    is_preforeclosure_auction BOOLEAN DEFAULT FALSE,
    is_premier_builder BOOLEAN DEFAULT FALSE,
    is_showcase_listing BOOLEAN DEFAULT FALSE,
    is_unmappable BOOLEAN DEFAULT FALSE,
    is_zillow_owned BOOLEAN DEFAULT FALSE,
    should_highlight BOOLEAN DEFAULT FALSE,
    
    -- Listing sub-type (JSON)
    listing_sub_type JSONB,  -- { "is_FSBA": boolean, "is_openHouse": boolean }
    
    -- Open house info
    open_house TEXT,  -- nullable, e.g., 'Sun 13:00-15:00'
    open_house_info JSONB,  -- nullable, { "open_house_showing": [{ "open_house_start": int, "open_house_end": int }] }
    
    -- Unit (optional)
    unit VARCHAR(50),  -- nullable
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_zillow_listing_zpid ON zillow_listings(zpid);
CREATE INDEX idx_zillow_listing_zip_code ON zillow_listings(zip_code);
CREATE INDEX idx_zillow_listing_price ON zillow_listings(price);
CREATE INDEX idx_zillow_listing_home_status ON zillow_listings(home_status);
CREATE INDEX idx_zillow_listing_home_type ON zillow_listings(home_type);
CREATE INDEX idx_zillow_listing_bedrooms ON zillow_listings(bedrooms);
CREATE INDEX idx_zillow_listing_bathrooms ON zillow_listings(bathrooms);
CREATE INDEX idx_zillow_listing_living_area ON zillow_listings(living_area);
CREATE INDEX idx_zillow_listing_days_on_zillow ON zillow_listings(days_on_zillow);

CREATE TABLE zillow_metrics_aggregated (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    
    -- Aggregation metadata
    aggregation_type VARCHAR(50) NOT NULL,  -- e.g., 'daily', 'weekly', 'monthly', 'quarterly'
    period_start_date DATE NOT NULL,
    period_end_date DATE NOT NULL,
    
    -- Grouping dimensions
    zip_code VARCHAR(10) NOT NULL,
    home_type VARCHAR(50),  -- nullable for 'all types' aggregation
    bedrooms INT,  -- nullable for 'all bedrooms' aggregation
    bathrooms NUMERIC(3,1),  -- nullable for 'all bathrooms' aggregation
    home_status VARCHAR(50),  -- e.g., 'FOR_SALE', 'FOR_RENT', nullable for 'all statuses'
    
    -- Listing counts
    total_listings INT NOT NULL DEFAULT 0,
    new_listings INT NOT NULL DEFAULT 0,  -- listings added during period
    active_listings INT NOT NULL DEFAULT 0,
    pending_listings INT NOT NULL DEFAULT 0,
    sold_listings INT NOT NULL DEFAULT 0,
    
    -- Price metrics
    average_price NUMERIC(12,2),
    median_price NUMERIC(12,2),
    min_price NUMERIC(12,2),
    max_price NUMERIC(12,2),
    
    -- Price per sqft metrics
    average_price_per_sqft NUMERIC(10,2),
    median_price_per_sqft NUMERIC(10,2),
    
    -- Days on market metrics
    average_days_on_market NUMERIC(8,2),
    median_days_on_market NUMERIC(8,2),
    min_days_on_market INT,
    max_days_on_market INT,
    
    -- Area metrics
    average_area_sqft NUMERIC(10,2),
    median_area_sqft NUMERIC(10,2),
    min_area_sqft INT,
    max_area_sqft INT,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Primary key must include partition key
    PRIMARY KEY (period_start_date, id),
    
    -- Prevent duplicate aggregations
    UNIQUE (
        aggregation_type, 
        period_start_date, 
        period_end_date, 
        zip_code, 
        home_type, 
        bedrooms, 
        bathrooms, 
        home_status
    )
) PARTITION BY RANGE (period_start_date);

-- Create indexes for efficient querying
CREATE INDEX idx_metrics_agg_type_zip ON zillow_metrics_aggregated(aggregation_type, zip_code);
CREATE INDEX idx_metrics_period_start ON zillow_metrics_aggregated(period_start_date);
CREATE INDEX idx_metrics_period_end ON zillow_metrics_aggregated(period_end_date);
CREATE INDEX idx_metrics_home_type ON zillow_metrics_aggregated(home_type) WHERE home_type IS NOT NULL;
CREATE INDEX idx_metrics_home_status ON zillow_metrics_aggregated(home_status) WHERE home_status IS NOT NULL;

-- Create initial partitions (2025-2026 with monthly granularity)
CREATE TABLE zillow_metrics_aggregated_2025_01 PARTITION OF zillow_metrics_aggregated
    FOR VALUES FROM ('2025-01-01') TO ('2025-02-01');
CREATE TABLE zillow_metrics_aggregated_2025_02 PARTITION OF zillow_metrics_aggregated
    FOR VALUES FROM ('2025-02-01') TO ('2025-03-01');
CREATE TABLE zillow_metrics_aggregated_2025_03 PARTITION OF zillow_metrics_aggregated
    FOR VALUES FROM ('2025-03-01') TO ('2025-04-01');
CREATE TABLE zillow_metrics_aggregated_2025_04 PARTITION OF zillow_metrics_aggregated
    FOR VALUES FROM ('2025-04-01') TO ('2025-05-01');
CREATE TABLE zillow_metrics_aggregated_2025_05 PARTITION OF zillow_metrics_aggregated
    FOR VALUES FROM ('2025-05-01') TO ('2025-06-01');
CREATE TABLE zillow_metrics_aggregated_2025_06 PARTITION OF zillow_metrics_aggregated
    FOR VALUES FROM ('2025-06-01') TO ('2025-07-01');
CREATE TABLE zillow_metrics_aggregated_2025_07 PARTITION OF zillow_metrics_aggregated
    FOR VALUES FROM ('2025-07-01') TO ('2025-08-01');
CREATE TABLE zillow_metrics_aggregated_2025_08 PARTITION OF zillow_metrics_aggregated
    FOR VALUES FROM ('2025-08-01') TO ('2025-09-01');
CREATE TABLE zillow_metrics_aggregated_2025_09 PARTITION OF zillow_metrics_aggregated
    FOR VALUES FROM ('2025-09-01') TO ('2025-10-01');
CREATE TABLE zillow_metrics_aggregated_2025_10 PARTITION OF zillow_metrics_aggregated
    FOR VALUES FROM ('2025-10-01') TO ('2025-11-01');
CREATE TABLE zillow_metrics_aggregated_2025_11 PARTITION OF zillow_metrics_aggregated
    FOR VALUES FROM ('2025-11-01') TO ('2025-12-01');
CREATE TABLE zillow_metrics_aggregated_2025_12 PARTITION OF zillow_metrics_aggregated
    FOR VALUES FROM ('2025-12-01') TO ('2026-01-01');
CREATE TABLE zillow_metrics_aggregated_2026_01 PARTITION OF zillow_metrics_aggregated
    FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');
CREATE TABLE zillow_metrics_aggregated_2026_02 PARTITION OF zillow_metrics_aggregated
    FOR VALUES FROM ('2026-02-01') TO ('2026-03-01');
CREATE TABLE zillow_metrics_aggregated_2026_03 PARTITION OF zillow_metrics_aggregated
    FOR VALUES FROM ('2026-03-01') TO ('2026-04-01');
CREATE TABLE zillow_metrics_aggregated_2026_04 PARTITION OF zillow_metrics_aggregated
    FOR VALUES FROM ('2026-04-01') TO ('2026-05-01');
CREATE TABLE zillow_metrics_aggregated_2026_05 PARTITION OF zillow_metrics_aggregated
    FOR VALUES FROM ('2026-05-01') TO ('2026-06-01');
CREATE TABLE zillow_metrics_aggregated_2026_06 PARTITION OF zillow_metrics_aggregated
    FOR VALUES FROM ('2026-06-01') TO ('2026-07-01');
CREATE TABLE zillow_metrics_aggregated_2026_07 PARTITION OF zillow_metrics_aggregated
    FOR VALUES FROM ('2026-07-01') TO ('2026-08-01');
CREATE TABLE zillow_metrics_aggregated_2026_08 PARTITION OF zillow_metrics_aggregated
    FOR VALUES FROM ('2026-08-01') TO ('2026-09-01');
CREATE TABLE zillow_metrics_aggregated_2026_09 PARTITION OF zillow_metrics_aggregated
    FOR VALUES FROM ('2026-09-01') TO ('2026-10-01');
CREATE TABLE zillow_metrics_aggregated_2026_10 PARTITION OF zillow_metrics_aggregated
    FOR VALUES FROM ('2026-10-01') TO ('2026-11-01');
CREATE TABLE zillow_metrics_aggregated_2026_11 PARTITION OF zillow_metrics_aggregated
    FOR VALUES FROM ('2026-11-01') TO ('2026-12-01');
CREATE TABLE zillow_metrics_aggregated_2026_12 PARTITION OF zillow_metrics_aggregated
    FOR VALUES FROM ('2026-12-01') TO ('2027-01-01');
