import os,shutil,pickle
import xml.etree.ElementTree as ET


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

	images = {}
	for item in annotations:
		content = []
		filename = "Flickr30kEntities/Annotations/" + str(item) + ".xml"
		tree = ET.parse(filename)
		root = tree.getroot()
		
		image_id = root[0].text
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

def parse_objects():
	"""
	To map object IDs to their descriptions
	"""
	objects = {}
	res = os.popen("grep -E -oh '#[\\-#A-Za-z0-9/ ]*' Flickr30kEntities/Sentences/*").read()
	for line in res.split("\n"):
		parts = line.split("/")
 		object_id = parts[0].strip("#")
 		if len(object_id) > 2 and " " not in object_id:
			try:
				temp = parts[1].split(" ")
			except:
				pass
			
			object_tag = temp[0]
			caption = " ".join(temp[1:])
			if object_id in objects.keys():
				objects[object_id].append(caption)
			else:
				objects[object_id] = []
				objects[object_id].append(caption)
			# objects[object_id] =(object_tag,caption)
		else:
			pass

	f = open("objects.pickle", 'wb')
	pickle.dump(save, f, pickle.HIGHEST_PROTOCOL)
	f.close()
	
parse_objects() 