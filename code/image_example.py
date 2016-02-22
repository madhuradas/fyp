from alchemyapi_python.alchemyapi import AlchemyAPI 		#add alchemyapi_python to /usr/lib/python27/site-packages/
import json

image_url = 'http://demo1.alchemyapi.com/images/vision/football.jpg'

# Create the AlchemyAPI Object
alchemyapi = AlchemyAPI()

response = alchemyapi.imageTagging('url', image_url)

if response['status'] == 'OK':
    print('## Response Object ##')
    print(json.dumps(response, indent=4))

    print('')
    print('## Keywords ##')
    for keyword in response['imageKeywords']:
        print(keyword['text'], ' : ', keyword['score'])
    print('')
else:
    print('Error in image tagging call: ', response['statusInfo'])