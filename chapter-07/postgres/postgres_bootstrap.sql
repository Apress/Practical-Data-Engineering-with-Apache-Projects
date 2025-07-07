
-- Create tables
CREATE TABLE IF NOT EXISTS users
(
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(255),
    is_vip BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS items
(
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    category VARCHAR(100),
    price DECIMAL(7,2),
    inventory INT,
    inventory_updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS purchases
(
    id SERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id),
    item_id BIGINT REFERENCES items(id),
    campaign_id VARCHAR(50),
    quantity INT DEFAULT 1,
    purchase_price DECIMAL(12,2),
    created_at TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
