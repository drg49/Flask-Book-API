DROP TABLE IF EXISTS book;

CREATE TABLE book (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255),
    published_date DATE,
    genre VARCHAR(100),
    price DECIMAL(10, 2)
);

INSERT INTO book (title, author, published_date, genre, price) 
VALUES
    ('The Great Gatsby', 'F. Scott Fitzgerald', '1925-04-10', 'Fiction', 10.99),
    ('To Kill a Mockingbird', 'Harper Lee', '1960-07-11', 'Fiction', 7.99),
    ('1984', 'George Orwell', '1949-06-08', 'Dystopian', 8.99),
    ('The Catcher in the Rye', 'J.D. Salinger', '1951-07-16', 'Fiction', 9.99),
    ('Pride and Prejudice', 'Jane Austen', '1813-01-28', 'Romance', 6.99),
    ('Moby-Dick', 'Herman Melville', '1851-11-14', 'Adventure', 12.99);
