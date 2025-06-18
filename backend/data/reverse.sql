DROP TABLE IF EXISTS message;
DROP TABLE IF EXISTS product_image;
DROP TABLE IF EXISTS category;
DROP TABLE IF EXISTS offer;
DROP TABLE IF EXISTS request;
DROP TABLE IF EXISTS user;


CREATE TABLE users (
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

CREATE TABLE request (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
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

CREATE TABLE category (
    id SERIAL PRIMARY KEY,
    name VARCHAR,
    description VARCHAR
);

CREATE TABLE offer (
    id SERIAL PRIMARY KEY,
    request_id INT REFERENCES request(id),
    user_id INT REFERENCES users(id),
    offer_description TEXT,
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
    sender_id INT REFERENCES users(id),
    receiver_id INT REFERENCES users(id),
    offer_id INT REFERENCES offer(id),
    content TEXT,
    timestamp DATE,
    is_read BOOLEAN
);

-- Users Table
INSERT INTO users (email, password_hash, user_type, first_name, last_name, contact_phone, registration_date, last_login, profile_description, profile_img, session_token, session_expires_at) VALUES
('alice.smith94@example.com', 'hashed_password_alice1234', 'buyer', 'Alice', 'Smith', '555-123-4567', '2024-01-15', '2025-06-16', 'Avid shopper looking for great deals.', 'alice.jpg', 'token_alice_123', '2025-06-18 10:00:00'),
('bob.johnson88@example.com', 'hashed_password_bob1234', 'seller', 'Bob', 'Johnson', '555-987-6543', '2024-02-20', '2025-06-17', 'Reliable seller of electronics and home goods.', 'bob.jpg', 'token_bob_456', '2025-06-19 11:00:00'),
('charlie.brown91@example.com', 'hashed_password_charlie1234', 'buyer', 'Charlie', 'Brown', '555-555-1111', '2024-03-10', '2025-06-15', 'Always on the lookout for unique items.', 'charlie.jpg', 'token_charlie_789', '2025-06-18 12:00:00'),
('diana.prince98@example.com', 'hashed_password_diana1234', 'seller', 'Diana', 'Prince', '555-222-3333', '2024-04-05', '2025-06-17', 'Specializing in handmade crafts and art.', 'diana.jpg', 'token_diana_012', '2025-06-19 13:00:00');

-- Category Table
INSERT INTO category (name, description) VALUES
('Electronics', 'Gadgets, computers, and other electronic devices.'),
('Home Goods', 'Furniture, decor, and household items.'),
('Apparel', 'Clothing, shoes, and accessories.'),
('Books', 'Fiction, non-fiction, and educational books.'),
('Sports & Outdoors', 'Equipment for sports, camping, and outdoor activities.');

-- Request Table
INSERT INTO request (user_id, title, description, quantity, price_range, location, location_range, expiry_date, status, post_date) VALUES
(1, 'Gaming Laptop', 'Looking for a high-performance gaming laptop with at least 16GB RAM and a dedicated GPU.', 1, 1500.00, 'San Francisco, CA', '20 miles', '2025-07-30', 'open', '2025-06-10'),
(3, 'Vintage Camera', 'Seeking a functional vintage film camera, preferably a Canon AE-1 or Nikon FM2.', 1, 300.00, 'Los Angeles, CA', '50 miles', '2025-07-25', 'open', '2025-06-12'),
(1, 'Smartwatch', 'Need a new smartwatch, ideally Apple Watch Series 8 or newer, good condition.', 1, 400.00, 'San Francisco, CA', '10 miles', '2025-07-20', 'open', '2025-06-15');

-- Offer Table
INSERT INTO offer (request_id, user_id, offer_description, seller_location, product_link, delivery_time, warranty, offer_date, status) VALUES
(1, 2, 'I have a lightly used Alienware gaming laptop, 32GB RAM, RTX 3080. Excellent condition.', 'Oakland, CA', 'http://example.com/alienware_laptop', '3-5 business days', '6 months seller warranty', '2025-06-14', 'pending'),
(2, 4, 'I can offer a fully serviced Nikon FM2 with a 50mm f/1.8 lens.', 'Santa Monica, CA', 'http://example.com/nikon_fm2', '7-10 business days', '30-day return policy', '2025-06-16', 'pending'),
(3, 2, 'Selling an Apple Watch Series 9, midnight black, with original box. Perfect condition.', 'Oakland, CA', 'http://example.com/apple_watch_s9', '2-3 business days', 'Manufacturer warranty', '2025-06-17', 'pending');

-- Product_Image Table
INSERT INTO product_image (offer_id, upload_date, image_url, order_index) VALUES
(1, '2025-06-14', 'http://example.com/images/alienware_laptop_1.jpg', 1),
(1, '2025-06-14', 'http://example.com/images/alienware_laptop_2.jpg', 2),
(2, '2025-06-16', 'http://example.com/images/nikon_fm2_1.jpg', 1),
(3, '2025-06-17', 'http://example.com/images/apple_watch_s9_1.jpg', 1);

-- Message Table
INSERT INTO message (sender_id, receiver_id, offer_id, content, timestamp, is_read) VALUES
(1, 2, 1, 'Hi Bob, interested in your Alienware. Can you send more photos?', '2025-06-15', FALSE),
(2, 1, 1, 'Sure Alice, I will upload more photos shortly.', '2025-06-15', TRUE),
(3, 4, 2, 'Hello Diana, is the Nikon FM2 still available? What is the shutter count?', '2025-06-17', FALSE);
