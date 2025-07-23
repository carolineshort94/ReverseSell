DROP TABLE IF EXISTS message;
DROP TABLE IF EXISTS product_image;
DROP TABLE IF EXISTS offer;
DROP TABLE IF EXISTS request;
DROP TABLE IF EXISTS category;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS account;


CREATE TABLE account (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    user_type VARCHAR,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    contact_phone VARCHAR,
    registration_date DATE,
    last_login DATE,
    profile_description TEXT,
    profile_img VARCHAR,
    session_token TEXT UNIQUE,
    session_expires_at TIMESTAMP
);

CREATE TABLE category (
    id SERIAL PRIMARY KEY,
    name VARCHAR,
    description VARCHAR
);

CREATE TABLE request (
    id SERIAL PRIMARY KEY,
    account_id INT REFERENCES account(id),
    category_id INT REFERENCES category(id),
    title VARCHAR,
    description TEXT,
    quantity INT,
    price_range FLOAT,
    location VARCHAR,
    location_range VARCHAR,
    expiry_date DATE,
    status VARCHAR,
    post_date DATE
);

CREATE TABLE offer (
    id SERIAL PRIMARY KEY,
    request_id INT REFERENCES request(id),
    account_id INT REFERENCES account(id),
    offer_description TEXT,
    offer_price FLOAT,
    offer_quantity INT,
    seller_location VARCHAR,
    product_link VARCHAR,
    delivery_time VARCHAR,
    warranty VARCHAR,
    offer_date DATE,
    status VARCHAR
);

CREATE TABLE product_image (
    id SERIAL PRIMARY KEY,
    offer_id INT REFERENCES offer(id),
    upload_date DATE,
    image_url TEXT NOT NULL,
    order_index INT
);

CREATE TABLE message (
    id SERIAL PRIMARY KEY,
    sender_id INT REFERENCES account(id),
    receiver_id INT REFERENCES account(id),
    offer_id INT REFERENCES offer(id),
    content TEXT,
    timestamp DATE,
    is_read BOOLEAN
);

-- Users Table
INSERT INTO account (email, password_hash, user_type, first_name, last_name, contact_phone, registration_date, last_login, profile_description, profile_img, session_token, session_expires_at)
VALUES
('alice@example.com', 'hashed_pw_1', 'buyer', 'Alice', 'Johnson', '555-1234', '2024-01-15', '2025-06-15', 'Looking for sustainable goods.', 'alice.jpg', 'token123', '2025-06-30 12:00:00'),
('bob@example.com', 'hashed_pw_2', 'seller', 'Bob', 'Smith', '555-5678', '2023-11-20', '2025-06-18', 'Experienced vendor of tech items.', 'bob.png', 'token456', '2025-06-28 15:00:00'),
('carol@example.com', 'hashed_pw_3', 'buyer', 'Carol', 'Nguyen', '555-9999', '2024-05-05', '2025-06-19', 'Interested in handmade goods.', NULL, NULL, NULL);

-- Category Table
INSERT INTO category (name, description)
VALUES
('Electronics', 'Devices, gadgets, and accessories'),
('Furniture', 'Home and office furniture'),
('Handmade', 'Custom and handmade products');


-- Request Table
INSERT INTO request (account_id, category_id, title, description, quantity, price_range, location, location_range, expiry_date, status, post_date)
VALUES
(1, 1, 'Looking for a used laptop', 'I need a reliable laptop for travel.', 1, 500.00, 'San Francisco', '10 miles', '2025-07-01', 'open', '2025-06-10'),
(3, 3, 'Need handmade candles', 'Looking for custom-scented candles as gifts.', 10, 200.00, 'Los Angeles', '15 miles', '2025-07-10', 'open', '2025-06-12');

-- Offer Table
INSERT INTO offer (request_id, account_id, offer_description, offer_price, offer_quantity, seller_location, product_link, delivery_time, warranty, offer_date, status)
VALUES
(1, 2, 'Dell XPS 13, lightly used, includes charger.', 450.00, 1, 'San Francisco', 'https://example.com/dell-xps13', '3 days', '6 months', '2025-06-11', 'pending'),
(2, 2, 'Set of 10 soy candles in assorted scents.', 180.00, 10, 'Los Angeles', NULL, '5 days', 'no warranty', '2025-06-13', 'accepted');

-- Product_Image Table
INSERT INTO product_image (offer_id, upload_date, image_url, order_index)
VALUES
(1, '2025-06-11', 'https://example.com/images/laptop1.jpg', 1),
(2, '2025-06-13', 'https://example.com/images/candles1.jpg', 1),
(2, '2025-06-13', 'https://example.com/images/candles2.jpg', 2);


-- Message Table
INSERT INTO message (sender_id, receiver_id, offer_id, content, timestamp, is_read)
VALUES
(1, 2, 1, 'Hi Bob, is the laptop still available?', '2025-06-11', TRUE),
(2, 1, 1, 'Yes, it is. Can deliver by Thursday.', '2025-06-12', FALSE),
(3, 2, 2, 'Thanks for the quick response!', '2025-06-14', TRUE);
