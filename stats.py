import math
import os, os.path
import numpy as np
import scipy.stats as st
import rectToSph

#Ben Lister
#compute average position (in sphereical coordinates) of every joint over the frames
#returns a dictionary of polar data and associated means
def getStats(directory):
	a_means = [0]*30
	b_means = [0]*30
	a_data = []
	b_data = []
	n = [0]*30

	for i in range(0, len(os.listdir(directory))):
		ssD = directory + "\\" + os.listdir(directory)[i]
		if (os.listdir(directory)[i] != ".DS_Store"):
			for j in range(0, len((os.listdir(ssD)))):
				sD = ssD + "\\" + os.listdir(ssD)[j]
				if (os.listdir(ssD)[j] != ".DS_Store"):
						data = rectToSph.sphereical(sD+"\\skeleton_pos.txt")
						a_data.extend(data['a data'])
						b_data.extend(data['b data'])
						for k in range(0,  30):
							for m in range(0, len(data['a data'])):
								if ((m == 0) & (i == 0)):
									a_means[k] = data['a data'][m][k]
									b_means[k] = data['b data'][m][k]
								else:
									a_means[k] = a_means[k]*(n[k]/(n[k]+1)) + data['a data'][m][k]*(1/(n[k]+1))
									b_means[k] = b_means[k]*(n[k]/(n[k]+1)) + data['b data'][m][k]*(1/(n[k]+1))
								n[k] = n[k]+1
	data = {'a data': a_data, 'b data': b_data}
	means = {'a means': a_means, 'b means': b_means}
	return {'data': data, 'means': means}
	

#First computes standard deviation of the data, 
#then generates a histogram for every joint in every frame based on the probability the joint is in any of the 9 surrounding bins at that instant
#the target bin, where the joint actually is, is the 5th entry in the returned histogram data structure
def getHisto(data, means, numAlphaBins, numThetaBins):
	stDevsA = [0]*30
	stDevsB = [0]*30
	for i in range(0, 30):
		num = 0;
		for j in range(0, len(data['a data'])):
			num = num+1
			stDevsA[i] = stDevsA[i] + math.pow((data['a data'][j][i] - means['a means'][i]), 2)
			stDevsB[i] = stDevsB[i] + math.pow((data['b data'][j][i] - means['b means'][i]), 2)
		stDevsA[i] = math.sqrt((1.0/num)*stDevsA[i])
		stDevsB[i] = math.sqrt((1.0/num)*stDevsB[i])
	

	histoA = {}
	histoB = {}
	alphaBins = []
	thetaBins = []
	for v in range(0, numAlphaBins):
		alphaBins.append(v*(2*math.pi)/numAlphaBins)
	for w in range(0, numThetaBins):
		thetaBins.append(w*(math.pi/numThetaBins))
	
	for p in range(0, len(data['a data'])):
		k = 0
		while (k < 29):		
			if (k == 0):
				histoA[p] = []
				histoB[p] = []
			hA = {'angle':[], 'bins':[], 'prob':[]}
			hB = {'angle':[], 'bins':[], 'prob':[]}
			Na = 0
			Ma = 0
			Nb = 0
			Mb = 0
			alphaBins.append(2*math.pi)
			thetaBins.append(math.pi)
			while (Na < numAlphaBins):
				if ((alphaBins[Na] <= data['a data'][p][k])  & (data['a data'][p][k] <= alphaBins[Na+1])):
					break
				else:
					Na = Na + 1
			while (Ma < numThetaBins):
				if ((thetaBins[Ma] <= data['a data'][p][k+1])  & (data['a data'][p][k+1] <= thetaBins[Ma+1])):
					break
				else:
					Ma = Ma + 1
			while (Nb < numAlphaBins):
				if ((alphaBins[Nb] <= data['b data'][p][k])  & (data['b data'][p][k] <= alphaBins[Nb+1])):
					break
				else:
					Nb = Nb + 1
			while (Mb < numThetaBins):
				if ((thetaBins[Mb] <= data['b data'][p][k+1])  & (data['b data'][p][k+1] <= thetaBins[Mb+1])):
					break
				else:
					Mb = Mb + 1
			alphaBins.remove(alphaBins[len(alphaBins)-1])
			thetaBins.remove(thetaBins[len(thetaBins)-1])
			hA['angle'] = [data['a data'][p][k], data['a data'][p][k+1]]
			hB['angle'] = [data['b data'][p][k], data['b data'][p][k+1]]
			
			#something might be off about the probability calculation. The 5th probability (when n and m are 0 and the bins evaluated at are Na/Ma and Nb/Mb) should be the highest, but that is often not the case
			for n in range (-1, 2):
				for m in range (-1, 2):
					#yikes
					#the index for alphaBins and thetaBins refer to the way they wrap around differently
					#the probability lines are essentially |P((|alpha*-alpha0|-|alpha*-alpha1|)/stDevAlpha) * P((|theta*-theta0|-|theta*-theta1|)/stDevTheta)|
					hA['bins'].append([alphaBins[(Na+n)%numAlphaBins], '< alpha <', alphaBins[(Na+n+1)%numAlphaBins], thetaBins[int(math.fabs(numThetaBins-1-math.fabs(Ma+m-numThetaBins+1)))], '< beta <', thetaBins[int(math.fabs(numThetaBins-1-math.fabs(Ma+m-numThetaBins+2)))]])
					hB['bins'].append([alphaBins[(Nb+n)%numAlphaBins], '< alpha <', alphaBins[(Nb+n+1)%numAlphaBins], thetaBins[int(math.fabs(numThetaBins-1-math.fabs(Mb+m-numThetaBins+1)))], '< beta <', thetaBins[int(math.fabs(numThetaBins-1-math.fabs(Mb+m-numThetaBins+2)))]])
					
					hA['prob'].append(math.fabs((st.norm.cdf(math.fabs(data['a data'][p][k] - alphaBins[(Na+n)%numAlphaBins])/stDevsA[k]) 
										- st.norm.cdf(math.fabs(data['a data'][p][k] - alphaBins[(Na+n+1)%numAlphaBins])/stDevsA[k]))
										*(st.norm.cdf(math.fabs(data['a data'][p][k+1] - thetaBins[int(math.fabs(numThetaBins-1-math.fabs(Ma+m-numThetaBins+1)))])/stDevsA[k+1]) 
										- st.norm.cdf(math.fabs(data['a data'][p][k+1] - thetaBins[int(math.fabs(numThetaBins-1-math.fabs(Ma+m-numThetaBins+2)))])/stDevsA[k+1]))))
					
					hB['prob'].append(math.fabs((st.norm.cdf(math.fabs(data['b data'][p][k] - alphaBins[(Nb+n)%numAlphaBins])/stDevsB[k])
										- st.norm.cdf(math.fabs(data['b data'][p][k] - alphaBins[(Nb+n+1)%numAlphaBins])/stDevsB[k]))
										*(st.norm.cdf(math.fabs(data['b data'][p][k+1] - thetaBins[int(math.fabs(numThetaBins-1-math.fabs(Mb+m-numThetaBins+1)))])/stDevsB[k+1])
										- st.norm.cdf(math.fabs(data['b data'][p][k+1] - thetaBins[int(math.fabs(numThetaBins-1-math.fabs(Mb+m-numThetaBins+1)))])/stDevsB[k+1]))))
										
					

			k = k + 2
			histoA[p].append(hA)
			histoB[p].append(hB)

		
		
		
	postures = {'a postures': histoA, 'b postures': histoB}
	return postures
		
	