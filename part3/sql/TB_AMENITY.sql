CREATE TABLE IF NOT EXISTS "TB_AMENITY" (
        id VARCHAR(36) PRIMARY KEY NOT NULL, 
        name VARCHAR(50) NOT NULL, 
        created_at DATETIME, 
        updated_at DATETIME
);