import cv
import matplotlib.pyplot as plt
import numpy as np
 

def str_hex_bin(s):
	b = s.encode('hex')
	s = bin(int(b, 16))[2:]	
	#l = len(s)%8	
	return s

def bin_hex_str(h):
	s = hex(int(h,2))[2:]
	if s[len(s)-1] == 'L':
		s=s[:-1]
	return s.decode('hex')


def make_pixel(d,alpha,pixel):
	L = 0.3*pixel[2] + 0.6*pixel[1] + 0.1*pixel[0] # R G B
	if int(d) == 0:
		newPixel = (pixel[0]-alpha*L,pixel[1],pixel[2])  #(B,G,R)
	elif int(d) == 1:
		newPixel = (pixel[0]+alpha*L,pixel[1],pixel[2])	
	return newPixel
	

def kutter(image,text,alpha):

	image = cv.LoadImage(image)
	cv.ShowImage('original',image)
	cv.WaitKey()

	for x in range(len(m)):
		print x,m[x]		
		print image[2,x] 
		image[2,x] = make_pixel(m[x],alpha,image[2,x]) 
		print image[2,x]

	cv.ShowImage('original', image)
	cv.SaveImage('2.bmp',image)
	cv.WaitKey()


def make_gist():
	y = np.random.randn(1000)
	plt.hist(y, 250)
	plt.show()
	

if __name__ == "__main__":
	m = str_hex_bin("golovabolitumenyaseychas")
	print(m,len(m))
	print(bin_hex_str(m))
	kutter('1.bmp',m,0.1)


