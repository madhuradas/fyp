from rnn import *
import numpy as np
import sys
import pickle
from gensim.models import *
import pdb

def cos_similarity(model,v2):
	sim = []
	
	for k in open("question_words.txt").read().split('\n'):
		v1 = model[k]
		sim.append((k,np.dot(v1,v2)/float((np.linalg.norm(v1)*np.linalg.norm(v2)))))
	# import pdb;pdb.set_trace()
	scores = zip(*sim)
	return scores[0][scores[1].index(max(scores[1]))]

		

# train_inputs = pickle.load(open('inputs_decoder.p'))
# train_targets = pickle.load(open('targets_decoder.p'))

# #pdb.set_trace()




# rnn = RNN(30,30,100)
# rnn.train(train_inputs,train_targets,100)

# print 'Finished training'

# rnn.save('decoder.p')
rnn = load('decoder.p')
d = eval(open("ques.txt").read())
ques = pickle.load(open("ques.p"))
# test_inputs = [[model[cls]] for cls in open("classes.txt").read().split(";")]
# # import pdb;pdb.set_trace()
# # probs = rnn.predict(test_input)[0][0:,0]  # gives list of probabilities
# # import pdb;pdb.set_trace()
test_inputs = []
for i in d.keys():
	for j in d[i]:
		test_inputs.append(j[1].split(' ')[0])

for first_word in test_inputs[0:1]:
	word = first_word
	while(word != '?'):
		print '---'
		print word, " ",
		word_p = rnn.predict([ques[word]])[0][0:,0]
		# cos_similarity(pickle.load(open("ques.p")),word_p)
		word = cos_similarity(pickle.load(open("ques.p")),word_p)
	print '?\n'
# for word in test_inputs:
# 	# import pdb;pdb.set_trace()
# 	probs = rnn.predict(word)[0][0:,0]  # gives list of probabilities
# 	c+=1
# 	print c
# 	# import pdb;pdb.set_trace()
# 	print 'Question Generated : ', cos_similarity(pickle.load(open("ques.p")),probs)
