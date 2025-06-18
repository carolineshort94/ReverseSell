DROP TABLE IF EXISTS message;
DROP TABLE IF EXISTS product_image;
DROP TABLE IF EXISTS category;
DROP TABLE IF EXISTS offer;
DROP TABLE IF EXISTS request;
DROP TABLE IF EXISTS user;


CREATE TABLE user (
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
    user_id INT REFERENCES user(id),
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
    user_id INT REFERENCES user(id),
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
    order_index INT
);

CREATE TABLE message (
    id SERIAL PRIMARY KEY,
    sender_id INT REFERENCES user(id),
    receiver_id INT REFERENCES user(id),
    offer_id INT REFERENCES offer(id),
    content TEXT,
    timestamp DATE,
    is_read BOOLEAN
);
