import pickle
from gensim.models import *


model_cls = Word2Vec([open("classes.txt","r").read().split(";")], size=30, window=1, min_count=1, workers=4)
model_q = Word2Vec([i.split(' ') for i in open("q.txt","r").read().split(";")], size=30, window=1, min_count=1, workers=4)
pickle.dump(model_cls,open("class.p","wb"))
pickle.dump(model_q,open("ques.p","wb"))

d = eval(open("ques.txt").read())
cls = pickle.load(open("class.p"))
ques = pickle.load(open("ques.p"))
inputs = []
targets = []

for i in d.keys():
	for j in d[i]:
		inputs.append([cls[j[0]]])
		targets.append([ques[j[1].split(' ')[0]]])

pickle.dump(inputs,open('inputs_encoder.p','wb'))
pickle.dump(targets,open('targets_encoder.p','wb'))