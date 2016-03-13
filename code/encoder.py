from rnn import *
import numpy as np
import sys
import pickle
from gensim.models import *

def cos_similarity(model,v2):
	sim = []
	
	for k in open("first_words.txt").read().split('\n'):
		v1 = model[k]
		sim.append((k,np.dot(v1,v2)/float((np.linalg.norm(v1)*np.linalg.norm(v2)))))
	# import pdb;pdb.set_trace()
	scores = zip(*sim)
	return scores[0][scores[1].index(max(scores[1]))]

		
#inputs_targets = zip(*eval(open('inputs_targets.txt').read()))
model = pickle.load(open("class.p"))

#inputs = inputs_targets[0]
train_inputs = pickle.load(open('inputs_encoder.p'))
train_targets = pickle.load(open('targets_encoder.p'))

# print inputs, targets
#class_to_ix = {cls: i for i, cls in enumerate(inputs)}
#ques_to_ix = {ques: i for i,ques in enumerate(targets)}

#train_inps = [[class_to_ix[i]] for i in inputs]
#train_outs = [[ques_to_ix[i]] for i in targets]
#print train_inps, train_outs
# rnn = RNN(30,30,100)

# rnn.train(train_inputs,train_targets,100)

print 'Finished training'

# rnn.save('encoder.p')
rnn = load('encoder.p')
test_inputs = [[model[cls]] for cls in open("classes.txt").read().split(";")]
# import pdb;pdb.set_trace()
# probs = rnn.predict(test_input)[0][0:,0]  # gives list of probabilities
# import pdb;pdb.set_trace()


for word in test_inputs:
	# import pdb;pdb.set_trace()
	probs = rnn.predict(word)[0][0:,0]  # gives list of probabilities
	c+=1
	print c
	# import pdb;pdb.set_trace()
	print 'Question Generated : ', cos_similarity(pickle.load(open("ques.p")),probs)
