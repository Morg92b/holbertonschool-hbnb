CREATE TABLE IF NOT EXISTS 'TB_PLACE_AMENITY' (
        id VARCHAR(36) PRIMARY KEY NOT NULL, 
        place_id VARCHAR(36) NOT NULL, 
        amenity_id VARCHAR(36) NOT NULL, 
        created_at DATETIME, 
        updated_at DATETIME, 
        FOREIGN KEY(place_id) REFERENCES 'TB_PLACE' (id), 
        FOREIGN KEY(amenity_id) REFERENCES 'TB_AMENITY' (id)
);