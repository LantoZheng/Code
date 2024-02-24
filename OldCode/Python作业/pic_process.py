from PIL import Image
im=Image.open("pic.jpg")
a=im.size
tig=im.resize((640,480),Image.NEAREST)
tig.save("resized.jpg")
im2=im
im2.thumbnail((128,128))
im2.save("shrink.jpg")
r,g,b=im.split()
ant=Image.merge("RGB",(b,r,g))
ant.save("anti_colored.jpg")
#郑晓旸 202111030007
