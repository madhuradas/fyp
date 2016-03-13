from clarifai.client import ClarifaiApi
import os

clarifai_api = ClarifaiApi()

images = os.listdir("first_1000")
# result = clarifai_api.tag_images(files)

missed = 0
d = {}
count = 0
for img in images:
	count += 1
	print count
	result = clarifai_api.tag_images(open('first_1000/'+img, 'rb'))
	res = result['results'][0]['result']['tag']['classes']
	if len(res) == 0:
		missed += 1
	d[img] = res
	print "Missed:",str(missed)