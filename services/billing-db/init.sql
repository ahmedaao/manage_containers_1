CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    number_of_items INTEGER NOT NULL,
    total_amount NUMERIC(10, 2) NOT NULL
);
