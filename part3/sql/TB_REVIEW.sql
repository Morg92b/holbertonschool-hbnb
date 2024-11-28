CREATE TABLE IF NOT EXISTS 'TB_REVIEW' (
        id VARCHAR(36) PRIMARY KEY NOT NULL, 
        text VARCHAR(255) NOT NULL, 
        rating INTEGER NOT NULL, 
        place_id VARCHAR(36) NOT NULL, 
        user_id VARCHAR(36) NOT NULL, 
        created_at DATETIME, 
        updated_at DATETIME, 
        FOREIGN KEY(place_id) REFERENCES 'TB_PLACE' (id), 
        FOREIGN KEY(user_id) REFERENCES 'TB_USER' (id)
);