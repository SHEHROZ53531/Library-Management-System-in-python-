
create database Library_Database;

use Library_Database;


create table Members(
member_id int auto_increment primary key,
name varchar(255),
email varchar(255) unique,
phone varchar(20),
department varchar(30),
password varchar(225)
);


select * from Books where author like '%ee%';
select * from Members;
select count(member_id) from Members;

INSERT INTO Members (name, email, phone, department, password) VALUES
('Alice Johnson', 'alice.johnson@example.com', '555-1234', 'Literature', 'alice123'),
('Bob Smith', 'bob.smith@example.com', '555-5678', 'Science', 'bobpass456'),
('Carol White', 'carol.white@example.com', '555-8765', 'Engineering', 'carolpw789'),
('David Brown', 'david.brown@example.com', '555-4321', 'History', 'david321'),
('Eva Green', 'eva.green@example.com', '555-2468', 'Mathematics', 'eva246'),
('Frank Moore', 'frank.moore@example.com', '555-1357', 'Computer Science', 'frank135'),
('Grace Lee', 'grace.lee@example.com', '555-9753', 'Arts', 'grace975'),
('Henry Adams', 'henry.adams@example.com', '555-8642', 'Biology', 'henry864'),
('Ivy Wilson', 'ivy.wilson@example.com', '555-7531', 'Physics', 'ivy753'),
('Jack Taylor', 'jack.taylor@example.com', '555-1597', 'Chemistry', 'jack159');

INSERT INTO Members (name, email, phone, department, password) VALUES
('Kaleem','Kaleem424@gmail.com','3787469','Computer Science','123');


select * from Admins;



create table Admins(
username varchar(255) unique,
email varchar(255) unique,
password varchar(255)
);

select * from Admins;

insert INTO Admins (username, email, password)
VALUES ('kaleem', 'admin1@example.com', '123');


insert INTO Admins (username, email, password)
VALUES ('shahroz', 'shahroz@gmail.com', '000');


insert INTO Admins (username, email, password)
VALUES ('anas', 'anas1@gmail.com', '098');


CREATE TABLE  Books (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    author VARCHAR(255),
    genre VARCHAR(100),
    quantity INT,
    publisher_id INT,
    FOREIGN KEY (publisher_id) REFERENCES Publishers(publisher_id)
);


INSERT INTO Books (title, author, genre, quantity)
VALUES
('To Kill a Mockingbird', 'Harper Lee', 'Fiction',5),
('1984', 'George Orwell', 'Dystopian', 7),
('The Great Gatsby', 'F. Scott Fitzgerald', 'Classic', 6),
('Pride and Prejudice', 'Jane Austen', 'Romance', 4),
('The Catcher in the Rye', 'J.D. Salinger', 'Fiction', 5),
('The Hobbit', 'J.R.R. Tolkien', 'Fantasy', 10),
('Fahrenheit 451', 'Ray Bradbury', 'Science Fiction', 6),
('Jane Eyre', 'Charlotte Brontë', 'Gothic', 5),
('Animal Farm', 'George Orwell', 'Political Satire', 8),
('The Lord of the Rings', 'J.R.R. Tolkien', 'Fantasy', 9);


INSERT INTO Books (title, author, genre, quantity)
VALUES
('Moby Dick', 'Herman Melville', 'Adventure', 7),
('War and Peace', 'Leo Tolstoy', 'Historical', 4),
('Crime and Punishment', 'Fyodor Dostoevsky', 'Psychological', 6),
('The Odyssey', 'Homer', 'Epic', 5),
('The Iliad', 'Homer', 'Epic', 5),
('The Brothers Karamazov', 'Fyodor Dostoevsky', 'Philosophical', 6),
('Brave New World', 'Aldous Huxley', 'Dystopian', 7),
('The Alchemist', 'Paulo Coelho', 'Adventure', 8),
('Les Misérables', 'Victor Hugo', 'Historical', 5),
('The Divine Comedy', 'Dante Alighieri', 'Epic', 4),
('Great Expectations', 'Charles Dickens', 'Classic', 7),
('Dracula', 'Bram Stoker', 'Gothic', 6),
('Frankenstein', 'Mary Shelley', 'Science Fiction', 5),
('Wuthering Heights', 'Emily Brontë', 'Gothic', 6),
('Don Quixote', 'Miguel de Cervantes', 'Classic', 8),
('A Tale of Two Cities', 'Charles Dickens', 'Historical', 7),
('The Grapes of Wrath', 'John Steinbeck', 'Fiction', 5),
('The Picture of Dorian Gray', 'Oscar Wilde', 'Philosophical', 6),
('The Count of Monte Cristo', 'Alexandre Dumas', 'Adventure', 9),
('Lolita', 'Vladimir Nabokov', 'Fiction', 4);




CREATE TABLE  Publishers (
    publisher_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) UNIQUE,
    address VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(20)
);

SELECT m.member_id, m.name, COUNT(t.transaction_id) AS total_borrowed
FROM Members m
JOIN Transactions t ON m.member_id = t.member_id
GROUP BY m.member_id, m.name
HAVING COUNT(t.transaction_id) > 1;




INSERT INTO Publishers (name, address, email, phone) VALUES
('Pearson Education', '221B Baker Street, London', 'contact@pearson.com', '+44 20 7946 0958'),
('McGraw Hill', '1221 Avenue of the Americas, New York, NY', 'info@mcgrawhill.com', '+1 212-512-2000'),
('Penguin Random House', '1745 Broadway, New York, NY', 'support@penguinrandomhouse.com', '+1 212-782-9000'),
('HarperCollins', '195 Broadway, New York, NY', 'help@harpercollins.com', '+1 212-207-7000'),
('Simon & Schuster', '1230 Avenue of the Americas, New York, NY', 'contact@simonandschuster.com', '+1 212-698-7000'),
('Hachette Book Group', '1290 Avenue of the Americas, New York, NY', 'info@hachettebookgroup.com', '+1 212-364-1100'),
('Oxford University Press', 'Great Clarendon Street, Oxford, UK', 'enquiries@oup.com', '+44 1865 556767'),
('Cambridge University Press', 'University Printing House, Cambridge, UK', 'customer.service@cambridge.org', '+44 1223 326050'),
('Scholastic Inc.', '557 Broadway, New York, NY', 'customer_service@scholastic.com', '+1 800-724-6527'),
('Cengage Learning', '200 Pier 4 Blvd, Boston, MA', 'support@cengage.com', '+1 800-354-9706');



SELECT * FROM Transactions;



CREATE TABLE  BorrowRequests (
    request_id INT AUTO_INCREMENT PRIMARY KEY,
    member_id INT,
    book_id INT,
    request_date DATE,
    FOREIGN KEY (member_id) REFERENCES Members(member_id),
    FOREIGN KEY (book_id) REFERENCES Books(book_id)
);


select * from BorrowRequests;
ALTER TABLE BorrowRequests
ADD COLUMN status VARCHAR(20) NOT NULL DEFAULT 'Pending';

select * from BorrowRequests;

TRUNCATE TABLE BorrowRequests;

DELETE FROM BorrowRequests;


SELECT b.title, b.author, t.borrow_date
FROM Transactions t
JOIN Books b ON t.book_id = b.book_id
WHERE t.member_id = 1 AND t.return_date IS NULL;




CREATE TABLE  Transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    member_id INT,
    book_id INT,
    borrow_date DATE,
    return_date DATE,
    FOREIGN KEY (member_id) REFERENCES Members(member_id),
    FOREIGN KEY (book_id) REFERENCES Books(book_id)
);


CREATE TABLE  Fines (
    fine_id INT AUTO_INCREMENT PRIMARY KEY,
    member_id INT,
    amount DECIMAL(10,2),
    status VARCHAR(50),
    FOREIGN KEY (member_id) REFERENCES Members(member_id)
);

ALTER TABLE Fines ADD COLUMN transaction_id INT,
ADD FOREIGN KEY (transaction_id) REFERENCES Transactions(transaction_id);




drop database  Library_Database;





















