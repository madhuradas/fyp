import Image

pic1 = Image.open("sampleimages/cat.thumbnail")
pic2 = Image.open("sampleimages/ball.thumbnail")
pic3 = Image.open("sampleimages/bus.thumbnail")
pic4 = Image.open("sampleimages/car.thumbnail")


pixels = list(pic1.getdata())
w1, h1 = pic1.size
w2, h2 = pic2.size
w3, h3 = pic3.size
w4, h4 = pic4.size

w = max(w1+w2,w3+w4)
h = max(h1+h3,h2+h3)

op_image = Image.new('RGB', (w, h))

op_image.paste(pic1, (0,0))
op_image.paste(pic2, (max(w1,w3),0))
op_image.paste(pic3, (0,max(h1,h2,h3,h4)))
op_image.paste(pic4, (max(w1,w3),max(h1,h2,h3,h4)))
op_image.save("op_image_1.jpg")