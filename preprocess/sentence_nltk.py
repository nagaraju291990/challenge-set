import nltk
nltk.download('punkt')
# nltk.download('nltk:tokenizers/punkt/hindi.pickle')
# tokenizer = nltk.data.load('nltk:tokenizers/punkt/hindi.pickle')
import sys

# Read input from file
with open(sys.argv[1], "r", encoding="utf-8") as file:
	for line in file:
		line = line.strip()
		if line:
			# Tokenize sentences in Hindi using NLTK
			sentences_hin = nltk.tokenize.sent_tokenize(line)
			# Print the output
			for sent in sentences_hin:
				print(sent)
