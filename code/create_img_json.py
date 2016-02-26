from alchemyapi_python.alchemyapi import AlchemyAPI 		#add alchemyapi_python to /usr/lib/python27/site-packages/
import json
import os

alchemyapi = AlchemyAPI()

d = {}

path = raw_input('Enter the directory path to annotate images from : ')

for root,dirs,files in os.walk(path):
    for f in files:
        if f.endswith('.png') or f.endswith('.jpg'):
            response = alchemyapi.imageTagging('image', path + '/' + f)
            if response['status'] == 'OK':
                print '## Response Object ##'
                print json.dumps(response, indent=4)
                d[path + '/' + f] = response['imageKeywords']
            else:
                print 'Error in image tagging call: ', response['statusInfo']

open('img_encoding.json','w').write(json.dumps(d))