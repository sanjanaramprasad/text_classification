import json
import pandas as pd
import re
import string

with open('contractions.json' , 'r') as f:
	contractions = json.load(f)

def replace_contractions(sentence, contractions):
    for key ,val in contractions.items():
        key_p = "\s*'\s*".join(key.split("'"))
        if key == "n't":
            key_p = "\s+"+key_p+"\s+|\s+"+key_p+"$"
        val = val[0]
        pattern = re.compile(key_p)
        patterns_found = re.findall(pattern , sentence)
        spans = [ m.span() for m in re.finditer(pattern, sentence)]
        sentence = pattern.sub(val , sentence)
    return sentence

def preprocess(sentence):

	def process_word(w):
		w = w.strip(string.punctuation)
		w = ''.join([c for c in w if c not in set(string.punctuation)])
		if re.findall('\w-\w|\w_\w' , token):
			w = ' '.join(w.split('-'))
		return w.lower().strip()

	sentence = sentence.encode('utf-8').decode('ascii' , 'ignore').lower()
	puncts = set(string.punctuation)
	sentence = replace_contractions(sentence , contractions)
	tokens = sentence.split()
	sentence = ''
	for token in tokens:
		token = process_word(token)
		if token:
			sentence += token + ' '
	return sentence.strip()
	


class DataProcessor():

	def __init__(self ):
		return

	def process_sst_trec(self, filename):
		sst_df = pd.DataFrame([])
		with open(filename , 'r') as fp:
			sentences = fp.readlines()
		labels = []
		sentence_texts = []
		for sentence in sentences:
			label = sentence.split(' ')[0].strip()
			sentence = ' '.join(sentence.split()[1:]) 
			sentence = preprocess(sentence)
			sentence_texts.append(sentence)
			labels.append(label)
		sst_df['text'] = sentence_texts
		sst_df['label'] = labels
		sst_df.to_csv(filename.split('.txt')[0].strip() + '.csv')

	def process_sa_emotions(self, filename):
		file_df = pd.read_csv(filename)
		df = pd.DataFrame([])

		if 'sentiment' in file_df:
			labels = list(file_df['sentiment'].values)
			label_dict = {label : i for i, label in enumerate(list(set(labels)))}
			labels_ind = [label_dict[label] for label in labels]
			df['label_ind'] = labels_ind
			df['label'] = labels

		sentences = list(file_df['content'].values)
		sentences = [preprocess(each) for each in sentences]
		df['text'] = sentences
		df.to_csv(filename.split('.csv')[0].strip() + '_processed.csv')

DataProcessor().process_sst_trec('/Users/srampras/text_classification/datasets/'
	'qa_trec/TREC-dev1.txt')

