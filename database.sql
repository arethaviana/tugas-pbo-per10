-- Buat database
CREATE DATABASE IF NOT EXISTS library;

-- Gunakan database
USE library;

-- Buat tabel buku
CREATE TABLE IF NOT EXISTS books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    year INT NOT NULL
);