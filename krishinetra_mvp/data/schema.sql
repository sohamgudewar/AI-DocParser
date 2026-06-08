CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS fields (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    location GEOMETRY(POINT, 4326),
    boundary GEOMETRY(POLYGON, 4326),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS analysis (
    id SERIAL PRIMARY KEY,
    field_id INTEGER REFERENCES fields(id) ON DELETE CASCADE,
    crop_type VARCHAR(100),
    crop_variety VARCHAR(100),
    ndvi_avg DOUBLE PRECISION,
    ndvi_healthy DOUBLE PRECISION,
    ndvi_moderate DOUBLE PRECISION,
    ndvi_stressed DOUBLE PRECISION,
    recommendation TEXT,
    analyzed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS land_records (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    owner_name VARCHAR(255),
    survey_number VARCHAR(100),
    area_hectares DOUBLE PRECISION,
    crop_type VARCHAR(100),
    gps_coordinates VARCHAR(255),
    district VARCHAR(100),
    taluka VARCHAR(100),
    village VARCHAR(100),
    irrigation_type VARCHAR(100),
    source_pdf TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS crop_zones (
    id SERIAL PRIMARY KEY,
    region VARCHAR(100) NOT NULL,
    crop VARCHAR(100) NOT NULL,
    variety VARCHAR(100),
    growing_season VARCHAR(100),
    lat_min DOUBLE PRECISION,
    lat_max DOUBLE PRECISION,
    lon_min DOUBLE PRECISION,
    lon_max DOUBLE PRECISION,
    emoji VARCHAR(10)
);

CREATE INDEX IF NOT EXISTS idx_fields_location ON fields USING GIST (location);
CREATE INDEX IF NOT EXISTS idx_fields_boundary ON fields USING GIST (boundary);
CREATE INDEX IF NOT EXISTS idx_analysis_field ON analysis (field_id);
CREATE INDEX IF NOT EXISTS idx_analysis_time ON analysis (analyzed_at DESC);
CREATE INDEX IF NOT EXISTS idx_land_records_user ON land_records (user_id);
