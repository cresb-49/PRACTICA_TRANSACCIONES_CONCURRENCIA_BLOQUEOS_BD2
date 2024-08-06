-- Create the database
CREATE DATABASE tcbdb2;

-- Connect to the database
\c tcbdb2

-- Create the table with an auto-incrementing primary key
CREATE TABLE movimiento (
    id SERIAL PRIMARY KEY,
    valor INT NOT NULL
);

-- Insert an initial value into the table
INSERT INTO movimiento (valor) VALUES (0);
