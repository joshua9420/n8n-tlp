-- DELETE FROM source_documents WHERE source_type = 'notion';

-- DELETE FROM notion_page;

-- DELETE FROM notion_page
-- WHERE title 

SELECT *
FROM notion_page
LIMIT 5;

-- DELETE FROM notion_page
-- WHERE title = 'Parker Woods Flats Master Notes';

SELECT *
FROM zillow_zip_codes;

-- insert 45223
INSERT INTO zillow_zip_codes (zip_code, city, state, county, country)
VALUES ('45223', 'Cincinnati', 'OH', 'Hamilton', 'USA');

INSERT INTO zillow_zip_codes (zip_code, city, state, county, country)
VALUES ('45224', 'Cincinnati', 'OH', 'Hamilton', 'USA');

SELECT *
FROM zillow_listings;


SELECT count(*)
FROM zillow_metrics_aggregated;
