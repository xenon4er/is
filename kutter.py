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

	
def antikutter(image,pixels,sigma):
	text = ""
	for i in range(len(pixels)):
		oldb = image[pixels[i][0],pixels[i][1]][0]
#		print pixels[0]
		
		if sigma == 1:
			newb = (image[pixels[i][0]-1,pixels[i][1]][0])		
		elif sigma == 2:
			newb = (image[pixels[i][0]-1,pixels[i][1]][0] + image[pixels[i][0]+1,pixels[i][1]][0] ) / 2
		elif sigma == 3:
			newb = (image[pixels[i][0]-1,pixels[i][1]][0] + image[pixels[i][0]+1,pixels[i][1]][0] + image[pixels[i][0],pixels[i][1]-1][0] ) / 3
		elif sigma == 4:
			newb = (image[pixels[i][0]-1,pixels[i][1]][0] + image[pixels[i][0]+1,pixels[i][1]][0] + image[pixels[i][0],pixels[i][1]-1][0] + image[pixels[i][0],pixels[i][1]+1][0]) / 4
		elif sigma == 5:
			newb = (image[pixels[i][0]-1,pixels[i][1]][0] + image[pixels[i][0]+1,pixels[i][1]][0] + image[pixels[i][0],pixels[i][1]-1][0] + image[pixels[i][0],pixels[i][1]+1][0]+ image[pixels[i][0]-1,pixels[i][1]+1][0]-1) / 5
		elif sigma == 6:
			newb = (image[pixels[i][0]-1,pixels[i][1]][0] + image[pixels[i][0]+1,pixels[i][1]][0] + image[pixels[i][0],pixels[i][1]-1][0] + image[pixels[i][0],pixels[i][1]+1][0]+ image[pixels[i][0]+1,pixels[i][1]+1][0]+1 + image[pixels[i][0]-1,pixels[i][1]+1][0]-1) / 6
		if newb > oldb:
			text += "0"
		else:
			text += "1"	 
	return text


def kutter(image,text,alpha):

	image = cv.LoadImage(image)
#	cv.ShowImage('original',image)
#	cv.WaitKey()
	pixels = []
	y = 10	
	x = 0	
	for i in range(len(text)):
		x += 10	
		if x > image.width: 
			y += 10
			x = 10

		while (image[y,x][0] > 220) or (image[y,x][0] < 20 ):		
#			print (y,x)		
			x+=10
			if x > image.width: 
				y += 10
				x = 10
			
		image[y,x] = make_pixel(text[i],alpha,image[y,x])
		pixels.append((y,x)) 

#	cv.ShowImage('original', image)
#	cv.SaveImage('2.bmp',image)
#	cv.WaitKey()
	data = (image,pixels)
	return data


def make_gist_sigma(data,sigmas):
	plt.errorbar(sigmas, data, fmt='.-')
	plt.show()
	

def make_experiment_sigma(text,img,alpha,sigma):
	err = 0.0
	data = kutter(img,text,alpha)
	t = antikutter(data[0],data[1],sigma)
	for i in range(len(text)):
		if text[i] != t[i]:
			err += 1.0
	return err/len(text)


def make_gist_alpha(data,alphas):
	plt.errorbar(alphas, data, fmt='.-')
	plt.show()


def make_experiment(text,img,alpha):
	err = 0.0
	data = kutter(img,text,alpha)
	t = antikutter(data[0],data[1],4)
	for i in range(len(text)):
		if text[i] != t[i]:
			err += 1.0
	return err/len(text)

def make_gist_mse_alpha(mses,alphas):
	plt.errorbar(alphas, mses, fmt='.-')
	plt.show()
	

def make_experiment_mse_alpha(text,img,alpha):
	image = cv.LoadImage(img)
	image2 = cv.LoadImage(img)
	data = kutter(img,text,alpha)
	pixels = data[1]
	mse = 0.0	
	for pixel in pixels:
		mse += (image2[pixel[0],pixel[1]][0] - data[0][pixel[0],pixel[1]][2])*(image2[pixel[0],pixel[1]][0] - data[0][pixel[0],pixel[1]][0])
		print (image2[pixel[0],pixel[1]][0], data[0][pixel[0],pixel[1]][0])
	return mse/(image.height*image.width)

#def make_gist_mse_sigma(mses, sigmas):
#	plt.errorbar(sigmas, mses, fmt='.-')
#	plt.show()

#def make_experiment_mse_sigma():
#	image = cv.LoadImage(image)

#	pass


if __name__ == "__main__":
	m = str_hex_bin("golovabolitumenyaseychas")
#	data = kutter('1.bmp',m,0.3)
#	t = antikutter(data[0],data[1])
#	print(t,len(t))
#	print(m,len(m))
#	print (t == m)
	data = []


#error for alpha

	n = 10	
	alphas = []
	for i in range(n):
		data.append(make_experiment(m,'1.bmp',0.1+0.01*i))
		alphas.append(0.1+0.01*i)
	make_gist_alpha(data,alphas)
	

#error for sigma

#	sigmas = []
#	for i in range(1,7):
#		data.append(make_experiment_sigma(m,'1.bmp',0.1,i))
#		sigmas.append(i)
#	make_gist_sigma(data,sigmas)


#mse for alpha
#	n = 10	
#	alphas = []
#	for i in range(n):
#		data.append(make_experiment_mse_alpha(m,'1.bmp',0.1+0.01*i))
#		alphas.append(0.1+0.01*i)
#	make_gist_mse_alpha(data,alphas)

