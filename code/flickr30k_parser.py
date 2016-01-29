import os,shutil,pickle
import xml.etree.ElementTree as ET

global images,objects

## Remaining
# Some XML files have multiple names for an object. Need to handle them.
# Some object IDs are missing from the Sentences folder, so they are not mapped in the dataset dictionary..
# What is scene 0 and 1?

def parse_images():
	"""
	images = 
	{
		filename : { [(object_id,xmin,ymin,xmax,ymax),(object_id,xmin,ymin,xmax,ymax),...,(object_id,scene_id)] }
	}

	** Some images also have scenes(outdoor, parade, etc) which have scene ID instead of bboxes.
	"""
	temp = os.listdir("Flickr30kEntities/Annotations")
	annotations =[]
	for f in temp:
		annotations.append(int(f.split(".")[0]))

	annotations = sorted(annotations)

	global images
	images = {}
	for item in annotations:
		content = []
		filename = "Flickr30kEntities/Annotations/" + str(item) + ".xml"
		tree = ET.parse(filename)
		root = tree.getroot()
		
		image_id = root[0].text.split(".")[0]
		for child in root:
			if child.tag == "object":
				object_name = child[0].text
				if len(child[1]) > 1:
					l = []
					xmin = child[1][0].text
					ymin = child[1][1].text
					xmax = child[1][2].text
					ymax = child[1][3].text
					content.append((object_name,xmin,ymin,xmax,ymax))
				else:
					scene = child[1].text
					content.append((object_name,scene))
				
		images[image_id] = content

	print len(images.keys())
	f = open("data/images.pickle", 'wb')
	pickle.dump(images, f, pickle.HIGHEST_PROTOCOL)
	f.close()

def parse_objects():
	"""
	To map object IDs to their descriptions
	"""
	global objects
	objects = {}
	count = 0
	res = open("data/grep_output.txt").read().split("\n")
	# res = os.popen("grep -E -oh '#[\\-#A-Za-z0-9/ ]*' Flickr30kEntities/Sentences/*").read()
	for line in res:
		count += 1
		parts = line.split("/")
 		object_id = parts[0].strip("#")
 		if " " not in object_id:
			try:
				temp = parts[1].split(" ")
			except:
				pass
			
			object_tag = temp[0]
			caption = " ".join(temp[1:])

			# Uncomment the code to get all captions for an image instead of just one.
			# if object_id in objects.keys():
			# 	objects[object_id].append(caption)
			# else:
			# 	objects[object_id] = []
			# 	objects[object_id].append(caption)
			# print count

			# Following line gets only the last caption of the object out of 5.
			objects[object_id] =(object_tag,caption)
		else:
			pass
	print len(objects.keys())
	f = open("data/single_caption.pickle", 'wb')
	pickle.dump(objects, f, pickle.HIGHEST_PROTOCOL)
	f.close()

def combine():
	missing_objects = []
	images = pickle.load(open("data/images.pickle","rb"))
	objects = pickle.load(open("data/single_caption.pickle","rb"))
	for f in images.keys():
		l = images[f]
		new_l = []
		for tup in l:
			if len(tup) > 2:
				temp = list(tup)
				try:
					temp[0] = objects[str(tup[0])]
					images[f] = temp
					new_l.append(temp)
				except:
					missing_objects.append(tup)
			else:
				new_l.append(tup)
		images[f] = new_l

	print len(images.keys())
	f = open("data/dataset.pickle", 'wb')
	pickle.dump(images, f, pickle.HIGHEST_PROTOCOL)
	f.close()

def load():
	dataset = pickle.load(open("data/dataset.pickle","rb"))
	print dataset["6620094641"]
	print len(dataset["6620094641"])

# parse_images()
# parse_objects()
# combine() 
load()