data = eval(open("google_api/image_wise.txt").read())

quesn_data = dict()
for img in data.keys():
	objs = data[img]
	quesn_list = []
	if(len(objs)>=1):
		quesn_list.append("What type of "+" ".join(str(str(objs[0][2]).split(".")[0]).split("_")) +" is present in the image?")
	if(len(objs)>=2):
		quesn_list.append("Choose the type of "+" ".join(str(str(objs[1][2]).split(".")[0]).split("_")) +" present in the image?")
	if(len(objs)>=3):
		quesn_list.append("What type of "+" ".join(str(str(objs[2][2]).split(".")[0]).split("_"))+" is not shown in the image?" )
	quesn_data[img] = quesn_list

open('ques.txt','w').write(str(quesn_data))

import pickle
pickle.dump(quesn_data, open("image_wise_quesn.pickle",'wb'))
