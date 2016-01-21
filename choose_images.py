import random

rand_nums = set()
tags = []
temp = open("tags.txt").read().split(",")
for i in temp:
	tags.append(i.strip())

while(len(rand_nums)<4):
	rand_nums.add(random.randint(0,len(tags)-1))

images = dict()

for i in rand_nums:
	l = open("annotate/"+str(tags[i])+".txt").read().split("\n")
	images[l[random.randint(0,len(l)-1)].strip("\r")] = tags[i]

print images		


