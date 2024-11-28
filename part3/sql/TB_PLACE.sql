CREATE TABLE IF NOT EXISTS 'TB_PLACE' (
        id VARCHAR(36) PRIMARY KEY NOT NULL,
        title VARCHAR(100) NOT NULL,
        description VARCHAR(255),
        price FLOAT NOT NULL,
        latitude FLOAT NOT NULL,
        longitude FLOAT,
        owner_id VARCHAR(36) NOT NULL,
        created_at DATETIME,
        updated_at DATETIME,
        FOREIGN KEY(owner_id) REFERENCES 'TB_USER' (id)
);