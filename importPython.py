DB_NAME = 'words_dict.db'
LINES = 5

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
			elif spec == FileTypes.EnglishWord:
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
		return {'value' : row[2], 'spec' : row[3]}

def resolveSentence(sentence):

	words = sentence.split()

	positive = 0
	negative = 0

	for word in words:
		lowWord = word.lower()
		valueAndSpec = resolveWord(lowWord, 0)
		if not valueAndSpec:
			res = get_twitter_result(word)
			positive += res[1]
			negative -= res[2]
			print word + " " + str(positive) + " " + str(negative)
		else:
			print word


	# lastNegative = False
	# finalEstimation = 0

	# for word in words:
	# 	valueAndSpec = resolveWord(word, 0)
	# 	if valueAndSpec:
	# 		if valueAndSpec['spec'] == FileTypes.Negating:
	# 			lastNegative = True
	# 		elif valueAndSpec['spec'] == FileTypes.Emotions:
	# 			if lastNegative:
	# 				finalEstimation += valueAndSpec['value'] * -1
	# 				lastNegative = False
	# 			else:
	# 				finalEstimation += valueAndSpec['value']
	# 		elif valueAndSpec['spec'] == FileTypes.Emoteicons:
	# 			finalEstimation += valueAndSpec['value']
	# print finalEstimation

def twitter_client_results(word):
	import subprocess
	output = subprocess.check_output(["java", "-jar", "SentiTwitter.jar", word])
	found = False
	i = 1
	foundLine = 0
	while not found:
		# print "DEBUG"
		if output[-i] == '\n':
			foundLine+=1
			# print "DEBUG if 1"
		if foundLine == LINES:
			# print "DEBUG if 2"
			break
		i+=1

	res = output[len(output)-i:]
	print res
	values = [int(i) for i in res.split()]
	return values

def get_twitter_result(word):
	results = twitter_client_results(word)
	positive = results[1]
	negative = results[2]
	# if abs(positive) + abs(negative) > 0:
	# 	return round(1.0 * positive / ( abs(positive) + abs(negative)) * 10 - 5)
	# else:
	# 	return 0
	return results

# create_db()
FileTypes = enum('Emotions', 'Emoteicons', 'NonEmotions', 'Negating', 'Idiom', 'EnglishWord')
# insert_text_file_in_db(FileTypes.Emotions, "EmotionLookupTable.txt", '^(\w*)\*?\s*?(\d|\-\d)')
# insert_text_file_in_db(FileTypes.Emoteicons, "EmotionLookupTableEXPRESIONS.txt", '^(\S*)\s*?(\d|\-\d)')
# insert_text_file_in_db(FileTypes.NonEmotions, "EnglishWordList.txt", '^(\w*)')
# insert_text_file_in_db(FileTypes.Negating, "NegatingWordList.txt", '^(\w*)')
# insert_text_file_in_db(FileTypes.Idiom, "IdiomLookupTable.txt", '^(\w*\s*)*(\d|\-d)')
# insert_text_file_in_db(FileTypes.EnglishWord, "EnglishWordList.txt", '^(\w*)')
#resolveSentence("This is the last fuckin day at work alol :) ")
#resolveSentence("Hey whats up")
resolveSentence("This will be the most fucking crappy jurney ever!")