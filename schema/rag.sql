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


CREATE TABLE IF NOT EXISTS source_documents (
    document_id        VARCHAR(128) PRIMARY KEY DEFAULT gen_random_uuid(),
    source_type        TEXT NOT NULL,                    -- "fireflies", "slack", "notion", etc
    source_id          TEXT,                             -- external ref (meeting_id, notion page id)
    title              TEXT,
    url                TEXT,
    created_at         TIMESTAMPTZ DEFAULT NOW(),
    metadata           JSONB                             -- optional: raw metadata payload
);

-- ==============================
-- 2. Chunks Table
-- ==============================
DROP TABLE IF EXISTS document_chunks CASCADE;
CREATE TABLE IF NOT EXISTS document_chunks (
    chunk_id           VARCHAR(128) PRIMARY KEY,
    document_id        VARCHAR(128) REFERENCES source_documents(document_id) ON DELETE CASCADE,
    qdrant_point_id    VARCHAR(128) NOT NULL,                    -- actual Qdrant UUID
    chunk_index        INT,                              -- sequential index per document
    content            TEXT NOT NULL,
    created_at         TIMESTAMPTZ DEFAULT NOW(),

    -- For quick debugging
    embedding_model    TEXT,
    metadata_id        INT
);

-- Index for fast doc-level retrieval
CREATE INDEX IF NOT EXISTS idx_document_chunks_document_id
    ON document_chunks(document_id);

-- ==============================
-- 3. Tags Table
-- ==============================
CREATE TABLE IF NOT EXISTS tags (
    tag_id             SERIAL PRIMARY KEY,
    tag_name           TEXT UNIQUE NOT NULL,             -- "finance", "maintenance", "owner-update"
    tag_type           TEXT,                             -- optional: "topic", "sentiment", "tenant", etc
    description        TEXT
);

-- ==============================
-- 4. Chunk ↔ Tag Linking Table
-- ==============================
CREATE TABLE IF NOT EXISTS chunk_tags (
    chunk_id           UUID REFERENCES document_chunks(chunk_id) ON DELETE CASCADE,
    tag_id             INT  REFERENCES tags(tag_id)       ON DELETE CASCADE,
    PRIMARY KEY(chunk_id, tag_id)
);

CREATE INDEX IF NOT EXISTS idx_chunk_tags_tag_id
    ON chunk_tags(tag_id);

CREATE INDEX IF NOT EXISTS idx_chunk_tags_chunk_id
    ON chunk_tags(chunk_id);


-- Enumerations for stable categories
CREATE TYPE section_type_enum AS ENUM (
    'team_check_in',
    'operations',
    'financials',
    'rent_roll',
    'maintenance',
    'acquisitions',
    'investor_updates',
    'general'
);

CREATE TYPE sentiment_enum AS ENUM (
    'positive',
    'neutral',
    'negative',
    'concerned',
    'mixed',
    'urgent'
);

CREATE TYPE source_type_enum AS ENUM (
    'transcript',
    'document',
    'email',
    'note'
);

CREATE TABLE IF NOT EXISTS chunk_metadata (
    id BIGSERIAL PRIMARY KEY,
    
    chunk_id VARCHAR(128) UNIQUE NOT NULL,           -- UUID from embedding pipeline
    source_type source_type_enum NOT NULL,           -- enum
    source_id VARCHAR(128),                          -- meeting_id / file_id
    root_document_id VARCHAR(128),                   -- groups chunks
    
    section_type section_type_enum,                  -- enum
    sentiment sentiment_enum,                        -- enum

    -- Arrays
    topics TEXT[],                      -- array of strings
    future_topics TEXT[],               -- array of strings

    -- JSON objects
    entities JSONB DEFAULT '{}'::jsonb,              -- object { properties:[], tenants:[], ... }

    -- JSON arrays
    custom_tags JSONB DEFAULT '[]'::jsonb,           -- array of objects or strings
    action_items JSONB DEFAULT '[]'::jsonb,          -- array of strings or objects

    summary TEXT,

    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- Auto-update updated_at
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_chunk_metadata_updated_at ON chunk_metadata;

CREATE TRIGGER trg_chunk_metadata_updated_at
BEFORE UPDATE ON chunk_metadata
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


CREATE TABLE transcripts_to_notion_log (
    id SERIAL PRIMARY KEY,
    transcript_id VARCHAR(128) UNIQUE NOT NULL,
    notion_page_id VARCHAR(128) UNIQUE NOT NULL,
    notion_page_url TEXT NOT NULL,
    status VARCHAR(64) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE notion_page (
    id                  bigserial PRIMARY KEY,

    -- Notion identifiers
    notion_page_id      text NOT NULL UNIQUE,   -- The UUID from Notion
    parent_page_id      text,                   -- Notion’s parent.page_id or null
    parent_type         text,                   -- 'page', 'database', or 'workspace'
    workspace_id        text,                   -- Notion workspace ID
    workspace_name      text,                   -- Notion workspace name

    -- Basic info
    title               text,
    url                 text,
    icon_emoji          text,
    cover_url           text,

    -- Status
    is_archived         boolean NOT NULL DEFAULT false,

    -- From Notion API (ISO strings)
    created_time        timestamptz,
    last_edited_time    timestamptz,

    -- Ingestion tracking for RAG
    ingest_status       text NOT NULL DEFAULT 'pending', 
        -- ENUM-like values:
        -- 'pending'     = discovered but not ingested
        -- 'ingested'    = ingested successfully
        -- 'needs_update' = page changed since last ingestion
        -- 'ignored'     = page excluded from ingestion

    last_ingested_at    timestamptz,
    content_hash        text,   -- hash of full page text or block text for change detection

    -- Raw Notion metadata
    raw                 jsonb NOT NULL,

    -- Sync tracking
    last_synced_at      timestamptz,
    created_at          timestamptz NOT NULL DEFAULT now(),
    updated_at          timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX idx_notion_page_ingest_status ON notion_page(ingest_status);
CREATE INDEX idx_notion_page_last_edited ON notion_page(last_edited_time);
CREATE INDEX idx_notion_page_parent ON notion_page(parent_page_id);
CREATE INDEX idx_notion_page_workspace ON notion_page(workspace_id);
