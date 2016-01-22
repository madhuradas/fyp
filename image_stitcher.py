import Image

pic1 = Image.open("sampleimages/im1.thumbnail")
pic2 = Image.open("sampleimages/im2.thumbnail")
pic3 = Image.open("sampleimages/im3.thumbnail")
pic4 = Image.open("sampleimages/im4.thumbnail")


pixels = list(pic1.getdata())
w1, h1 = pic1.size
w2, h2 = pic2.size
w3, h3 = pic3.size
w4, h4 = pic4.size


w = max(w1+w2,w3+w4)
h = max(h1+h3,h2+h3)
op_image = Image.new('RGB', (w, h))

if h1 != h2:
	resize_h = max(h1,h2)
	if resize_h == h1:
		pic1.thumbnail((w,h), Image.ANTIALIAS)
		pic1.save("sampleimages/im1", "JPEG")
		pic1 = Image.open("sampleimages/im1.jpg")
	else:
		pic2.thumbnail((w,h), Image.ANTIALIAS)
		pic2.save("sampleimages/im2", "JPEG")
		pic2 = Image.open("sampleimages/im2.jpg")
elif h3 != h4:
	resize_h = max(h3,h4)
	if resize_h == h3:
		pic3.thumbnail((w,h), Image.ANTIALIAS)
		pic3.save("sampleimages/im3", "JPEG")
		pic3 = Image.open("sampleimages/im3.jpg")
	else:
		pic4.thumbnail((w,h), Image.ANTIALIAS)
		pic4.save("sampleimages/im4", "JPEG")
		pic4 = Image.open("sampleimages/im4.jpg")
# op_image.paste(pic1, (0,0))
# op_image.paste(pic2, (max(w1,w3),0))
# op_image.paste(pic3, (0,max(h1,h2,h3,h4)))
# op_image.paste(pic4, (max(w1,w3),max(h1,h2,h3,h4)))
op_image.paste(pic1, (0,0))
op_image.paste(pic2, (w1,0))
op_image.paste(pic3, (0,h3))
op_image.paste(pic4, (w1,h3))
op_image.save("op_image_3.jpg")
