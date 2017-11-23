import math
import os, os.path
import scipy.stats as st
import rectToSph

#Ben Lister
#compute average position (in sphereical coordinates) of every joint in a given frame
#returns a dictionary of polar data and associated means and statistics
def getStats(directory):
	a_means = {}
	b_means = {}
	a_stdevs = {}
	b_stdevs = {}
	a_data = {}
	b_data = {}
	numActions = 0

	for i in range(0, len(os.listdir(directory))):
		ssD = directory + "\\" + os.listdir(directory)[i]
		if (os.listdir(directory)[i] != ".DS_Store"):
			for j in range(0, len((os.listdir(ssD)))):
				sD = ssD + "\\" + os.listdir(ssD)[j]
				if (os.listdir(ssD)[j] != ".DS_Store"):
					data = rectToSph.sphereical(sD+"\\skeleton_pos.txt")
					a_data[numActions] = data['a data']
					b_data[numActions] = data['b data']

					a_action_means = [0]*30	
					b_action_means = [0]*30
					a_action_devs = [0]*30
					b_action_devs = [0]*30
					for k in range(0,  30):
						for m in range(0, len(data['a data'])):
							a_action_means[k] = a_action_means[k] + data['a data'][m][k]
							b_action_means[k] = b_action_means[k] + data['b data'][m][k]
						a_action_means[k] = a_action_means[k]/len(data['a data'])
						b_action_means[k] = b_action_means[k]/len(data['b data'])
						for n in range(0, len(data['a data'])):
							a_action_devs[k] = a_action_devs[k] + math.pow(data['a data'][n][k] - a_action_means[k], 2)
							b_action_devs[k] = b_action_devs[k] + math.pow(data['b data'][n][k] - b_action_means[k], 2)
						a_action_devs[k] = math.sqrt((1/len(data['a data']))*a_action_devs[k])
						b_action_devs[k] = math.sqrt((1/len(data['a data']))*b_action_devs[k])
					a_means[numActions] = a_action_means
					b_means[numActions] = b_action_means
					a_stdevs[numActions] = a_action_devs
					b_stdevs[numActions] = b_action_devs
					numActions = numActions+1
	data = {'a data': a_data, 'b data': b_data}
	stats = {'a means': a_means, 'b means': b_means, 'a devs': a_stdevs, 'b devs': b_stdevs}
	return {'data': data, 'stats': stats}
	

#First computes standard deviation of the data, 
#then generates a histogram for every joint in every frame based on the probability the joint is in any of the 9 surrounding bins at that instant
#the target bin, where the joint actually is, is the 5th entry in the returned histogram data structure
def getHisto(data, stats, numAlphaBins, numThetaBins):

	histoA = {}
	histoB = {}
	#for every action
	for z in range(0, len(data['a data'])):
		actionA = {}
		actionB = {}
		#for every frame
		for p in range(0, len(data['a data'][z])):
			frameA = [0]*15
			frameB = [0]*15
			#for every joint
			k = 0
			while (k < 29):
				hA = {'angle':[], 'bins':[], 'prob':[]}
				hB = {'angle':[], 'bins':[], 'prob':[]}
				alphaA = data['a data'][z][p][k]
				thetaA = data['a data'][z][p][k+1]
				alphaB = data['b data'][z][p][k]
				thetaB = data['b data'][z][p][k+1]
				hA['angle'] = [alphaA, thetaA]
				hB['angle'] = [alphaB, thetaB]
				
				aAlphaBins = [0]*4
				bAlphaBins = [0]*4
				aThetaBins = [0]*4
				bThetaBins = [0]*4
				for x in range (-1, 3):
					aAlphaBins[x+1] = (int(alphaA/((2*math.pi)/numAlphaBins))+x)*((2*math.pi)/numAlphaBins)
					bAlphaBins[x+1] = (int(alphaB/((2*math.pi)/numAlphaBins))+x)*((2*math.pi)/numAlphaBins)
					aThetaBins[x+1] = (int(thetaA/(math.pi/numThetaBins))+x)*(math.pi/numThetaBins)
					bThetaBins[x+1] = (int(thetaB/(math.pi/numThetaBins))+x)*(math.pi/numThetaBins)
					if (alphaA < 0):
						aAlphaBins[x+1] = aAlphaBins[x+1] - (2*math.pi)/numAlphaBins
					if (alphaB < 0):
						bAlphaBins[x+1] = bAlphaBins[x+1] - (2*math.pi)/numAlphaBins
				
				hA['bins'].append(aAlphaBins)
				hA['bins'].append(aThetaBins)
				hB['bins'].append(bAlphaBins)
				hB['bins'].append(bThetaBins)
				#bins are calculated with alpha increasing first, then theta
				
				for y in range(0, 3):
					for w in range(0, 3):
						alphaProbA = st.norm.cdf((aAlphaBins[w+1]-alphaA)/stats['a devs'][z][k] - (alphaA-aAlphaBins[w])/stats['a devs'][z][k])
						thetaProbA = st.norm.cdf((aThetaBins[y+1]-thetaA)/stats['a devs'][z][k+1] - (thetaA-aThetaBins[y])/stats['a devs'][z][k+1])
						alphaProbB = st.norm.cdf((bAlphaBins[w+1]-alphaB)/stats['b devs'][z][k] - (alphaB-bAlphaBins[w])/stats['b devs'][z][k+1])
						thetaProbB = st.norm.cdf((bThetaBins[y+1]-thetaB)/stats['b devs'][z][k+1] - (thetaB-bThetaBins[y])/stats['b devs'][z][k+1])
						
						hA['prob'].append(alphaProbA*thetaProbA)
						hB['prob'].append(alphaProbB*thetaProbB)

				frameA[int(k/2)] = hA
				frameB[int(k/2)] = hB				
				k = k + 2
			actionA[p] = frameA
			actionB[p] = frameB
		histoA[z] = actionA
		histoB[z] = actionB		
		
	postures = {'a postures': histoA, 'b postures': histoB}
	return postures
		
	