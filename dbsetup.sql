CREATE TABLE notes (id INTEGER PRIMARY KEY, text TEXT, created_at TIMESTAMP);
CREATE TABLE categories (id INTEGER PRIMARY KEY, name TEXT UNIQUE NOT NULL);
CREATE TABLE note_categories(id INTEGER PRIMARY KEY, note_id INTEGER, category_id INTEGER, 
    FOREIGN KEY (note_id) 
        REFERENCES notes (id) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE, 
    FOREIGN KEY(category_id)
        REFERENCES categories(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);