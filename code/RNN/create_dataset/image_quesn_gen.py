data = eval(open("../../google_api/image_wise_flickr_second.txt").read())
ctr = 0
ctr1 = 0
quesn_data = dict()
for img in data.keys():
	objs = data[img]
	quesn_list = []
	if(len(objs)>=1):
		quesn_list.append((" ".join(str(str(objs[0][2]).split(".")[0]).split("_")), "What type of "+" ".join(str(str(objs[0][2]).split(".")[0]).split("_")) +" is present in the image ?"))
	# if(len(objs)>=1 and ctr%2 == 1):
	# 	quesn_list.append((" ".join(str(str(objs[0][2]).split(".")[0]).split("_")),"Choose the type of "+" ".join(str(str(objs[0][2]).split(".")[0]).split("_")) +" present in the image?"))
	# if(len(objs)>=2 and ctr%2 == 1):
	# 	quesn_list.append((" ".join(str(str(objs[1][2]).split(".")[0]).split("_")),"Which "+" ".join(str(str(objs[1][2]).split(".")[0]).split("_"))+" is shown in the image?" ))
	if(len(objs)>=2):
		quesn_list.append((" ".join(str(str(objs[1][2]).split(".")[0]).split("_")),"Select the "+" ".join(str(str(objs[1][2]).split(".")[0]).split("_"))+" represented by the image ?" ))
	quesn_data[img] = quesn_list
	ctr+=1

open('ques.txt','w').write(str(quesn_data))

import pickle
pickle.dump(quesn_data, open("../../../data/image_wise_quesn.pickle",'wb'))
