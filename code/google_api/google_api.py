import argparse
import base64
import httplib2
import os
from apiclient.discovery import build
from oauth2client.client import GoogleCredentials
from nltk.corpus import wordnet as wn

def main():
	'''Run a label request on a single image
	d =
	{
		file1: [ (obj,score,class), (obj,score,class),..  ],
		file2: [ (obj,score,class), (obj,score,class),..  ],
	}
	'''

	API_DISCOVERY_FILE = 'https://vision.googleapis.com/$discovery/rest?version=v1'
	http = httplib2.Http()
	d = {}
	credentials = GoogleCredentials.get_application_default().create_scoped(
	  ['https://www.googleapis.com/auth/cloud-platform'])
	credentials.authorize(http)

	service = build('vision', 'v1', http, discoveryServiceUrl=API_DISCOVERY_FILE)
	count = 0
	missed = 0
	for img in os.listdir("../../../first_1000_mirflickr"):
		count += 1  
		with open("../../../first_1000_mirflickr/"+img, 'rb') as image:
			image_content = base64.b64encode(image.read())
			service_request = service.images().annotate(
			  body={
			    'requests': [{
			      'image': {
			        'content': image_content
			       },
			      'features': [{
			        'type': 'LABEL_DETECTION',
			        'maxResults': 5,
			       }]
			     }]
			  })
			response = service_request.execute()

			if 'labelAnnotations' not in response['responses'][0]:
				print "No annotations for: ",response['responses'],img
				missed += 1 
			else:
				res = []
				for tag in response['responses'][0]['labelAnnotations']:
					l = wn.synsets(tag['description'])
					if len(l) > 0:
						hy = l[0].hypernyms()
						if len(hy) > 0:
							res.append((tag['description'],tag['score'],hy[0].name()))
						else:
							print "No hypernyms for :",img,tag['description']
				d[str(img)] = res
		print count   

	print "Missed count:",str(missed)
	open("image_wise_mirflickr.txt","w").write(str(d))
	class_to_img(eval(open("image_wise_mirflickr.txt").read()))

def class_to_img(d):
	'''
	res = 
	{
		class1: {obj1:[file1,file2,..], obj12:[file1,file2,..]},
		class2: {obj1:[file1,file2,..], obj12:[file1,file2,..]},
	}
	'''
	res = {}
	for k,v in d.items():
		for val in v:
			if val[2] in res.keys():
				if val[0] in res[val[2]].keys():
					res[val[2]][val[0]].append(k)
				else:
					res[val[2]][val[0]] = [k]
			else:
				res[val[2]] =  {val[0]:[k]}
	open("class_wise_mirflickr.txt","w").write(str(res))


if __name__ == '__main__':
	main()