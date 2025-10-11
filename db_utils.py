create_leetBank = '''
CREATE TABLE IF NOT EXISTS leetBank( 
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        leetcode_id INTEGER UNIQUE, 
        problem_statement TEXT, 
        title_slug TEXT,
        difficulty TEXT, 
        hints TEXT, 
        topics TEXT,
        url TEXT);
'''

insert_leetbank = '''
INSERT OR IGNORE INTO leetBank
        (leetcode_id, problem_statement, title_slug,
        difficulty, hints, topics, url)
        VALUES (?, ?, ?, ?, ?, ?, ?)
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