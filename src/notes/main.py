import os
import datetime
import atexit
import sqlite3
import argparse
from datetime import datetime
import sys

cursor = None
def db():
    global cursor

    if cursor is None:
        
        conn = sqlite3.connect(os.path.expanduser('~/database.db'), detect_types=sqlite3.PARSE_DECLTYPES)
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")

        if not isMain:
            def close():
                conn.commit()
                cursor.close()
                conn.close()

            atexit.register(close)
    
    return cursor

# Register datetime adapter and converter
def adapt_datetime(dt):
    return dt.isoformat()

def convert_datetime(s):
    if type(s) is str:
        return datetime.fromisoformat(s)
    elif type(s) is bytes:
        return datetime.fromisoformat(s.decode())
    else:
        return s

sqlite3.register_adapter(datetime, adapt_datetime)
sqlite3.register_converter("timestamp", convert_datetime)

def insert_note(text):
    try:
        db().execute(
            "INSERT INTO notes (text, created_at) VALUES (?, ?)",
            (text, datetime.now())
        )
        return db().lastrowid
    except sqlite3.Error as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        db().rollback()

def create_category(category):
    try:
        #  Upsert category
        db().execute("""
            INSERT INTO categories (name)
            VALUES (?)
            ON CONFLICT(name) DO NOTHING
        """, (category,))

        # Get category id
        db().execute("SELECT id FROM categories WHERE name = ?", (category,))
        return db().fetchone()[0]

    except sqlite3.Error as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        db().rollback()

def assign_category(note_id, category_id):
    try:
        # Link note to category
        db().execute("""
            INSERT INTO note_categories (note_id, category_id)
            VALUES (?, ?)
        """, (note_id, category_id))

    except sqlite3.Error as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        db().rollback()

def add_note(text, categories):
    try:
        note_id = insert_note(text)

        # Handle categories
        for category in categories:
            category_id = create_category(category)
            assign_category(note_id, category_id)

        print(f"Note added successfully with ID: {note_id}")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        db().rollback()

def get_notes():
    try:
        db().execute("SELECT * FROM notes")
        notes = db().fetchall()
        return notes
    
    except sqlite3.Error as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        db().rollback()

def get_note(id):
    try:
        # Get note with categories
        db().execute("""
            SELECT notes.*, GROUP_CONCAT(categories.name) AS categories
            FROM notes
            LEFT JOIN note_categories ON notes.id = note_categories.note_id
            LEFT JOIN categories ON note_categories.category_id = categories.id
            WHERE notes.id = ?
            GROUP BY notes.id
        """, (id,))
        note = db().fetchone()
        return note

    except sqlite3.Error as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        db().rollback()

def main():
    parser = argparse.ArgumentParser(description='Manage notes')
    parser.add_argument('text', 
                       nargs='*',  # '*' allows 0 or more arguments
                       help='The note text (optional)')
    parser.add_argument('-c', '--category', 
                       action='append', 
                       default=[],
                       help='Category for the note (can be used multiple times)')
    
    parser.add_argument('-n', '--note',
                       help='A note to view')

    args = parser.parse_args()

    if len(args.text) == 0:
        if args.note is not None:
            note = get_note(args.note)
            print('')
            formatted_date = note[2].strftime("%m/%d/%y\n")
            print(f"{note[0]} -- {formatted_date}")
            print(note[1])
            print(f"Categories: {note[3]}\n")
        else:
            for note in get_notes():
                formatted_date = note[2].strftime("%m/%d/%y")
                print(f"{note[0]} {formatted_date} {note[1]}")
    else:
        add_note(' '.join(args.text), args.category)

isMain = False
if __name__ == "__main__":
    isMain = True
    main()
