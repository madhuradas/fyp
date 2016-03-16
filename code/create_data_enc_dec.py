from gensim.models import Word2Vec
import pickle

model_cls = pickle.load(open('class.p'))

inputs = []
targets = []
d = eval(open('ques.txt').read())
ques = open('q.txt').read().split(";")
ques_vocab = set()
first_words = set()
for q in ques:
	for i in q.split(' '):
		ques_vocab.add(i)
	first_words.add(q.split(' ')[0])

ix_to_first_word = { i:ch for i,ch in enumerate(first_words) }
first_word_to_ix = { ch:i for i,ch in enumerate(first_words) }
vocab_to_ix = { ch:i for i,ch in enumerate(ques_vocab) }
ix_to_vocab = { i:ch for i,ch in enumerate(ques_vocab) }


for img in d.keys():
	for tup in d[img]:
		inputs.append(model_cls[tup[0]])
		targets.append(tup[1])

pickle.dump(inputs,open('enc_dec_inputs.p','wb'))
pickle.dump(targets,open('enc_dec_targets.p','wb'))
pickle.dump(ix_to_vocab,open('ix_to_vocab.p','wb'))
pickle.dump(ix_to_first_word ,open('ix_to_first_word.p','wb'))
pickle.dump(vocab_to_ix,open('vocab_to_ix.p','wb'))
pickle.dump(first_word_to_ix,open('first_word_to_ix.p','wb'))