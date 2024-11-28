-- DROP TABLE IF EXISTS 'TB_USER';

CREATE TABLE IF NOT EXISTS 'TB_USER' (
        id VARCHAR(36) PRIMARY KEY NOT NULL,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50) NOT NULL,
        email VARCHAR(120) UNIQUE NOT NULL,
        password VARCHAR(128) NOT NULL,
        is_owner BOOLEAN,
        is_admin BOOLEAN,
        created_at DATETIME,
        updated_at DATETIME
);
