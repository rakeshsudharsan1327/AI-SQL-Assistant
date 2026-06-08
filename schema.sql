CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    city TEXT,
    created_at DATE
);

CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name TEXT,
    category TEXT,
    price REAL
);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    order_date DATE
);

INSERT INTO customers VALUES
(1,'Vijay','vijay@test.com','perambur','2026-05-10'),
(2,'Trisha','trisha@test.com','chennai','2026-05-04');

INSERT INTO products VALUES
(1,'Laptop','Electronics',1000),
(2,'Phone','Electronics',500);

INSERT INTO orders VALUES
(1,1,1,2,'2026-06-01'),
(2,2,2,1,'2026-06-06');