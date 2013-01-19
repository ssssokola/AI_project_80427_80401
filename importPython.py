DB_NAME = 'words_dict.db'

def create_db(name=DB_NAME):
	import sqlite3

	conn = sqlite3.connect(name)
	c = conn.cursor()
	f = c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='words'")
	if not f.fetchone():
		c.execute('''CREATE TABLE words
	             (id Integer PRIMARY KEY ASC, word text, value Integer, specification Integer, UNIQUE (word) ON CONFLICT REPLACE )''')
	conn.commit()
	conn.close()
	return name

def insert_text_file_in_db(spec, file_name, db_name):
	import re
	import sqlite3

	conn = sqlite3.connect(db_name)
	c = conn.cursor()
	f = open(file_name, 'r')
	for line in f:
		regex_matcher = re.search('^(\w*\*|\w*)\s*?(\d|\-\d)', line)
		if regex_matcher:
			c.execute("INSERT INTO words (word, value, specification) VALUES ('"+regex_matcher.group(1)+"',"+regex_matcher.group(2)+","+str(spec)+")")
	f.close()
	conn.commit()
	conn.close()

#execution
name = create_db()
insert_text_file_in_db(1, "EmotionLookupTable.txt", name)

insert_text_file_in_db(2, "EmotionLookupTableEXPRESIONS.txt", name)

