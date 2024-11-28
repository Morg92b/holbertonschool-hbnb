INSERT INTO TB_USER(
    id,
    first_name,
    last_name,
    email,
    password,
    is_owner,
    is_admin,
    created_at,
    updated_at
)
VALUES(
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$09qN4ait6c/agxpHRvdfMu08KlJV8UN5cksgFJyD81fNLEZuJnAyy',
    false,
    true,
    datetime(),
    datetime()
);

