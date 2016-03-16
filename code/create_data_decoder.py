import pickle
from gensim.models import *
import pdb

# model_cls = Word2Vec([open("classes.txt","r").read().split(";")], size=30, window=1, min_count=1, workers=4)
model_q = Word2Vec([i.split(' ') for i in open("q.txt","r").read().split(";")], size=30, window=1, min_count=1, workers=4)
#pdb.set_trace()
# pickle.dump(model_cls,open("class.p","wb"))
pickle.dump(model_q,open("ques.p","wb"))

d = eval(open("ques.txt").read())
# cls = pickle.load(open("class.p"))
ques = pickle.load(open("ques.p"))
inputs = []
targets = []

for i in d.keys():
	for j in d[i]:
		for k in range( len(j[1].split(' ')) - 1 ):
			#pdb.set_trace()
			inputs.append([ques[j[1].split(' ')[k]]])
			targets.append([ques[j[1].split(' ')[k+1]]])
			
		

pickle.dump(inputs,open('inputs_decoder.p','wb'))
pickle.dump(targets,open('targets_decoder.p','wb'))