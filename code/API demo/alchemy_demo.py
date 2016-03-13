from alchemyapi_python.alchemyapi import AlchemyAPI 		#add alchemyapi_python to /usr/lib/python27/site-packages/
import json
import os

alchemyapi = AlchemyAPI()

d = {}

path = raw_input('Enter the directory path to annotate images from : ')

missed = 0
count = 0
for root,dirs,files in os.walk(path):
    for f in files:
    	count += 1
        if f.endswith('.png') or f.endswith('.jpg'):
            response = alchemyapi.imageTagging('image', path + '/' + f)
            if response['status'] == 'OK':
                print '## Response Object ##'
                print response["totalTransactions"]
                d[path + '/' + f] = response['imageKeywords']
                if len(response['imageKeywords']) == 0:
                	missed += 1
            else:
                print 'Error in image tagging call: ', response['statusInfo']
    	print count
print "Missed:",str(missed)

open('first1000_encoding.json','w').write(json.dumps(d))