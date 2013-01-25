DB_NAME = 'words_dict.db'

def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

def create_db():
	import sqlite3

	conn = sqlite3.connect(DB_NAME)
	c = conn.cursor()
	f = c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='words'")
	if not f.fetchone():
		c.execute('''CREATE TABLE words
	             (id Integer PRIMARY KEY ASC, word text, value Integer, specification Integer, UNIQUE (word) ON CONFLICT REPLACE )''')
	conn.commit()
	conn.close()


def insert_text_file_in_db(spec, fileName, regexString):
	import re
	import sqlite3

	conn = sqlite3.connect(DB_NAME)
	conn.text_factory = str
	cursor = conn.cursor()

	textFile = open(fileName, 'r')
	for line in textFile:
		regex_matcher = re.search(regexString, line)
		if regex_matcher:
			word = regex_matcher.group(1)

			if spec == FileTypes.Negating:
				value = 0
			elif spec == FileTypes.NonEmotions:
				value = 0
			else:
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
	result = []
	for word in words:
		value = resolveWord(word, 0)
		result.append(value)

	for value in result:
		print value

create_db()

FileTypes = enum('Emotions', 'Emoteicons', 'NonEmotions', 'Negating')
insert_text_file_in_db(FileTypes.Emotions, "EmotionLookupTable.txt", '^(\w*)\*?\s*?(\d|\-\d)')
insert_text_file_in_db(FileTypes.Emoteicons, "EmotionLookupTableEXPRESIONS.txt", '^(\S*)\s*?(\d|\-\d)')
insert_text_file_in_db(FileTypes.NonEmotions, "EnglishWordList.txt", '^(\w*)')
insert_text_file_in_db(FileTypes.Negating, "NegatingWordList.txt", '^(\w*)')

resolveSentence("This is the last fuckin day at work alol :) ")


