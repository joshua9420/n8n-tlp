CREATE TABLE IF NOT EXISTS ingestion_log (
    id SERIAL PRIMARY KEY,
    source VARCHAR(50) NOT NULL,          -- e.g., 'notion', 'fireflies'
    source_id VARCHAR(128),               -- Notion page ID, Fireflies transcript ID, etc
    document_title TEXT,
    document_url TEXT,
    processed_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    status VARCHAR(20) DEFAULT 'ingested', -- e.g., 'ingested', 'error', 'skipped'
    error_message TEXT,
    metadata JSONB                             -- Flexible: for storing tags, custom metadata, etc.
);
