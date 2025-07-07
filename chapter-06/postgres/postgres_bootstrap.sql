
-- Create tables

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
