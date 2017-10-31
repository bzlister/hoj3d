import pandas
import math
import os, os.path
import numpy as np

#Ben Lister
#module for converting the skeleton frame data from rectangular to sphereical cordinates
def sphereical(filename):
	ex = pandas.read_csv(filename, header=None)
	i = 0
	spA = []
	spB = []
	while (i < len(ex)):
		spA.append([])
		spB.append([])
		j = 1
		k = 46
		while (j <= 43):
			x1 = getX(ex[j][i])
			y1 = getY(ex[j+1][i])
			z1 = getZ(ex[j+2][i])
			alpha = math.atan2(y1,x1)
			if (alpha < 0):
				alpha = alpha+2*math.pi
			spA[i].append(alpha)
			spA[i].append(math.acos(z1/math.sqrt(math.pow(z1,2)+math.pow(y1,2)+math.pow(x1,2))))
			
			j = j + 3
		
		while (k <= 88):
			x2 = getX(ex[k][i])
			y2 = getY(ex[k+1][i])
			z2 = getZ(ex[k+2][i])
			
			alpha = math.atan2(y2,x2)
			if (alpha < 0):
				alpha = alpha+2*math.pi
			spB[i].append(alpha)
			spB[i].append(math.acos(z2/math.sqrt(math.pow(z2,2)+math.pow(y2,2)+math.pow(x2,2))))
			
			k = k + 3
		i = i+1
		
	data = {'a data': spA, 'b data': spB}
	return data

def getX(nrmX):
	return 1280 - (nrmX * 2560)

def getY(nrmY):
	return 960 - (nrmY * 1920)

def getZ(nrmZ):
	return (nrmZ * 10000)/7.8125