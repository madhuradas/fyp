import random
import pickle

img_set = set()
d = pickle.load(open("dataset.pickle"))

while(len(img_set)<5):
	img_set.add(d.keys()[random.randrange(len(d.keys()))])

for i in img_set:
	print str(i)+" : "+str(d[i])


count_dict = dict()
obj_dict = dict()
class_set = set()
for i in img_set:
	for j in d[i]:
		class_set.add(j[0][1])
		if(j[0][0] in count_dict.keys()):
			count_dict[j[0][0]] +=1
		else:
			count_dict[j[0][0]] = 1
		if(j[0][0] in obj_dict.keys()):
			l = obj_dict[j[0][0]]
			l.append(j[0][1])
			obj_dict[j[0][0]] =  l
		else:
			l = []
			l.append(j[0][1])
			obj_dict[j[0][0]] = l

del count_dict["other"]
del count_dict["scene"]
class_set = list(class_set)
obj_class = count_dict.keys()[random.randrange(len(count_dict.keys()))]
obj_count = count_dict[obj_class]

print "How many " + str(obj_class) + " are there in the images?"
print "Ans: " + str(obj_count)
print obj_dict[obj_class]

print "Which of the following are present in the images?"
print "Ans: " + str(class_set)
