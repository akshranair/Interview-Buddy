import sqlite3

DB = "questionBank.db"

create_leetBank = '''
CREATE TABLE IF NOT EXISTS leetBank( 
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        leetcode_id INTEGER UNIQUE, 
        problem_statement TEXT, 
        title TEXT,
        title_slug TEXT,
        difficulty TEXT, 
        hints TEXT, 
        topics TEXT,
        url TEXT);
'''

insert_leetbank = '''
INSERT OR IGNORE INTO leetBank
        (leetcode_id, problem_statement, title, title_slug,
        difficulty, hints, topics, url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
'''

read_leetbank = '''
SELECT * FROM leetBank 
WHERE id = ?
'''

delete_all_rows = ''' 
DELETE FROM leetbank
'''

drop_leetbank = '''
DROP TABLE IF EXISTS leetbank
''' 

def delete_leetBank_data():
    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()
        cursor.execute(delete_all_rows)
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='leetBank'")
        conn.commit()

def write_leetBank(leetcode_id, problem_statement, title, title_slug, difficulty, hints, topics, url):
    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()
        cursor.execute(insert_leetbank,(leetcode_id, problem_statement, title, title_slug, difficulty, hints, topics, url))
        conn.commit()

def read_leetBank(id):
    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()
        cursor.execute(read_leetbank, (id,))
        row = cursor.fetchone()
        return row

def Build_LeetBank():
    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()
        cursor.execute(create_leetBank)
        conn.commit()
    
def find_total_problems():
    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()
        cursor.execute("Select count(*) from leetbank")
        total = cursor.fetchone()[0]
        return total