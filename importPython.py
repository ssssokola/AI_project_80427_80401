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

def insert_text_file_in_db(spec, file_name, db_name, regexString):
	import re
	import sqlite3

	conn = sqlite3.connect(db_name)
	conn.text_factory = str
	cursor = conn.cursor()

	textFile = open(file_name, 'r')
	for line in textFile:
		regex_matcher = re.search(regexString, line)
		if regex_matcher:
			word = regex_matcher.group(1)
			value = regex_matcher.group(2)
			
			query = """INSERT INTO words (word, value, specification) VALUES (?, ?, ?)"""
			cursor.execute(query, (str(word), value, spec))
	textFile.close()
	conn.commit()
	conn.close()

def resolveWord(word, options):
	import sqlite3
	conn = sqlite3.connect(DB_NAME)
	c = conn.cursor()
	query = "SELECT * FROM words WHERE word = '" + word + "'"
	for row in c.execute(query):
		return row[2] 

def resolveSentence(sentence):
	words = sentence.split()
	i = 0
	result = []
	for word in words:
		value = resolveWord(word, 0)
		result.append(value)

	for value in result:
		print value

dbName = create_db()
insert_text_file_in_db(1, "EmotionLookupTable.txt", dbName, '^(\w*)\*?\s*?(\d|\-\d)')
insert_text_file_in_db(2, "EmotionLookupTableEXPRESIONS.txt", dbName, '^(\S*)\s*?(\d|\-\d)')

resolveSentence("This is the last fuckin day at work alol :) ")

# Fix regex for emotions


