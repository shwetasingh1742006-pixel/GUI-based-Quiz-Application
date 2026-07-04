CREATE DATABASE quiz_system;
USE quiz_system;

-- Users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Categories Table
CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description TEXT
);

-- Questions Table
CREATE TABLE questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category_id INT NOT NULL,
    question_text TEXT NOT NULL,
    option_a VARCHAR(255) NOT NULL,
    option_b VARCHAR(255) NOT NULL,
    option_c VARCHAR(255) NOT NULL,
    option_d VARCHAR(255) NOT NULL,
    correct_answer CHAR(1) NOT NULL,
    difficulty ENUM('easy', 'medium', 'hard') DEFAULT 'medium',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
);

-- Quiz Results Table
CREATE TABLE quiz_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    score INT NOT NULL,
    total_questions INT NOT NULL,
    category_id INT,
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
);

-- Insert Categories
INSERT INTO categories (name, description) VALUES 
('Python', 'Python programming questions'),
('DBMS', 'Basic questions'),
('Datastructure', 'DS questions'),
('HTML', 'Simple questions'),
('Mathematics', 'Basic math questions');

---------------------------------------------------
-- PYTHON QUESTIONS
---------------------------------------------------
INSERT INTO questions 
(category_id, question_text, option_a, option_b, option_c, option_d, correct_answer, difficulty)
VALUES
(1, 'Which keyword breaks a loop?', 'continue', 'break', 'exit', 'stop', 'b', 'easy'),
(1, 'List data type property?', 'mutable', 'immutable', 'static', 'dynamic', 'a', 'easy'),
(1, 'Convert string to uppercase?', 'upper()', 'uppercase()', 'toUpper()', 'UPPER()', 'a', 'easy'),
(1, 'Can dictionary have duplicate keys?', 'Yes', 'No', 'Sometimes', 'Only integers', 'b', 'easy'),
(1, 'Method to sort list in-place?', 'sort()', 'sorted()', 'arrange()', 'order()', 'a', 'easy'),
(1, 'Exception handling keywords?', 'try-expect','catch-fainally','error-handle','if-else','a','easy'),
(1, 'Lambda functions are called?', 'Anonymous','Named','Static','Global','a','easy'),
(1, 'Datatype of True?', 'bool','int','str','float','a','easy'),
(1, 'Method to read file content?', 'read()','write()','open()','close()','a','easy'),
(1, 'Keyword to modify global variable?','global','nonlocal','static','public','a','easy');

---------------------------------------------------
-- DBMS QUESTIONS
---------------------------------------------------
INSERT INTO questions 
(category_id, question_text, option_a, option_b, option_c, option_d, correct_answer, difficulty)
VALUES
(2, 'Purpose of PRIMARY KEY?', 'Unique identification', 'Allow duplicates', 'NULL values', 'Multiple values', 'a', 'easy'),
(2, 'JOIN that returns all records?', 'FULL OUTER JOIN', 'INNER JOIN', 'LEFT JOIN', 'RIGHT JOIN', 'a', 'easy'),
(2, 'Main goal of Normalization?', 'Reduce redundancy', 'Increase data', 'Increase speed', 'Increase storage', 'a', 'easy'),
(2, 'A in ACID?', 'Atomicity', 'Accuracy', 'Activity', 'Availability', 'a', 'easy'),
(2, 'Constraint for no duplicates?', 'UNIQUE', 'NULL', 'DEFAULT', 'CHECK', 'a', 'easy'),
(2,'Main advantages of INDEX?','Faster queries','Less storage','Data duplication','Backup','a','easy'),
(2,'FOREIGN KEY references?','Parent table','Child table','Both','None','a','easy'),
(2,'GROUP BY used with?','Aggregate functions','Sorting','Filtering','Joining','a','easy'),
(2,'Removes partial dependency?','1NF','2NF','3NF','BCNF','b','easy'),
(2,'Make transaction permanent?','COMMIT','ROLLBACK','SAVEPOINT','BEGIN','a','easy');

---------------------------------------------------
-- DSA QUESTIONS
---------------------------------------------------
INSERT INTO questions 
(category_id, question_text, option_a, option_b, option_c, option_d, correct_answer, difficulty)
VALUES
(3, 'Array access time?', 'O(1)', 'O(n)', 'O(log n)', 'O(n²)', 'a', 'easy'),
(3, 'Binary search requires?', 'Sorted array', 'Unsorted array', 'Linked list', 'Tree', 'a', 'easy'),
(3, 'LIFO stands for?', 'Last In First Out', 'First In Last Out', 'FIFO', 'None', 'a', 'easy'),
(3, 'Heap property?', 'Complete binary tree', 'Balanced tree', 'Sorted tree', 'BST', 'a', 'easy'),
(3, 'Dijkstra algorithm finds?', 'Shortest path', 'Longest path', 'Cycle', 'Sorting', 'a', 'easy'),
(3,'Liked List intersection best case','O(1)', 'O(n)', 'O(log n)', 'O(n²)', 'a', 'easy'),
(3,'Max nodes in Binary Tree at level h','2^h-1','2^h','h^2','2h','a','easy'),
(3,'Hash Table average search?','O(1)', 'O(n)', 'O(log n)', 'O(nlogn)', 'a', 'easy'),
(3,'Quick Sort worst case?','O(nlogn)', 'O(n)', 'O(log n)', 'O(n²)', 'd', 'easy'),
(3,'Graph cycle detection?','DFS/BFS','Linear search','Binary search','Bubble sort','a','easy');

---------------------------------------------------
-- HTML QUESTIONS
---------------------------------------------------
INSERT INTO questions 
(category_id, question_text, option_a, option_b, option_c, option_d, correct_answer, difficulty)
VALUES
(4, 'Full form of HTML?', 'Hyper Text Markup Language', 'High Text Markup Language', 'Hyper Transfer Markup', 'Home Tool Markup', 'a', 'easy'),
(4, 'DOCTYPE position?', 'First line', 'Head', 'Body', 'End', 'a', 'easy'),
(4, 'Heading tags range?', '<h1> to <h6>', '<head1> to <head6>', '<h> to <h6>', '<heading>', 'a', 'easy'),
(4, 'Image tag?', '<img>', '<image>', '<pic>', '<photo>', 'a', 'easy'),
(4, 'Hyperlink tags?', '<a>', '<link>', '<url>', '<href>', 'a', 'easy'),
(4, 'Unordered list tag?','<ul>','<ol>','<li>','<list>','a','easy'),
(4, 'Table container tag?','<table>','<tab>','<data>','<grid>','a','easy'),
(4, 'Form container tag?','<form>','<input>','<button>','<submit>','a','easy'),
(4, 'Semantic HTML element example?','<header>','<div>','<span>','<All of above>','a','easy'),
(4, 'HTML5 video tag?','<video>','<media>','<movie>','<clip>','a','easy');

---------------------------------------------------
-- MATHEMATICS QUESTIONS
---------------------------------------------------
INSERT INTO questions 
(category_id, question_text, option_a, option_b, option_c, option_d, correct_answer, difficulty)
VALUES
(5, '2x + 3 = 7 ?', '2', '3', '4', '1', 'a', 'easy'),
(5, 'sin(90°)?', '1', '0', '0.5', '-1', 'a', 'easy'),
(5, '5! value?', '120', '100', '60', '24', 'a', 'easy'),
(5, '√576 ?', '24', '22', '28', '26', 'a', 'easy'),
(5, 'π value?', '3.14', '2.71', '1.73', '9.8', 'a', 'easy'),
(5,'Matrix multiplication rule?','mxn x nxp','mxn x mxn','pxm x nxp','None','a','easy'),
(5,'Derivative of x²?','2x','x','2','x³','a','easy'),
(5,'Probability range?','0 to 1','-1 to 1','0 to 100','-∞ to +∞','a','easy'),
(5,'Sum of 1+2+3+....+n?','n(n+1)/2','n²','2n','n/2','a','easy'),
(5,'Integration of x²?','2x','x³/3','3','x','b','easy');