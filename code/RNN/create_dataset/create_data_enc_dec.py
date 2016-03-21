import pickle
from gensim.models import Word2Vec

ques = pickle.load(open("../../../data/image_wise_quesn.pickle",'rb'))
classes = []
initial_questions = []
for k in ques.keys():
	for v in ques[k]:
		classes.append(v[0])
		initial_questions.append(v[1])

questions=[]
for q in initial_questions:
	words = q.split(" ")
	last_word = words[-1]
	del words[-1]
	words.append(last_word.split("?")[0])
	words.append("?")
	questions.append(" ".join(words))

model_q = Word2Vec([q.split(" ") for q in questions], size=30, window=1, min_count=1, workers=4)
pickle.dump(model_q, open("../../../data/questions.pickle",'wb'))

model_cls = Word2Vec([[i] for i in classes] , size=30, window=1, min_count=1, workers=4)
pickle.dump(model_cls, open("../../../data/classes.pickle",'wb'))


open("classes.txt","w").write(";".join(classes))
open("questions.txt","w").write(";".join(questions))

inputs = []
targets = []
d = eval(open('ques.txt').read())
ques_vocab = set()
first_words = set()
for q in questions:
	for i in q.split(' '):
		ques_vocab.add(i)
	first_words.add(q.split(' ')[0])

ix_to_first_word = {i: ch for i, ch in enumerate(first_words)}
first_word_to_ix = {ch: i for i, ch in enumerate(first_words)}
vocab_to_ix = {ch: i for i, ch in enumerate(ques_vocab)}
ix_to_vocab = {i: ch for i, ch in enumerate(ques_vocab)}

for img in d.keys():
    for tup in d[img]:
        inputs.append(model_cls[tup[0]])
        targets.append(tup[1])

pickle.dump(inputs, open('../../../data/enc_dec_inputs.pickle', 'wb'))
pickle.dump(targets, open('../../../data/enc_dec_targets.pickle', 'wb'))
pickle.dump(ix_to_vocab, open('../../../data/ix_to_vocab.pickle', 'wb'))
pickle.dump(ix_to_first_word, open('../../../data/ix_to_first_word.pickle', 'wb'))
pickle.dump(vocab_to_ix, open('../../../data/vocab_to_ix.pickle', 'wb'))
pickle.dump(first_word_to_ix, open('../../../data/first_word_to_ix.pickle', 'wb'))