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
	minTheta = math.pi
	maxTheta = 0
	minAlpha = 2*math.pi
	maxAlpha = 0
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
							
							#prints min and max alpha and theta
							if (k%2==0):
								if (data['a data'][m][k] < minAlpha):
									minAlpha = data['a data'][m][k]
								if (data['b data'][m][k] < minAlpha):
									minAlpha = data['b data'][m][k]
								if (data['a data'][m][k] > maxAlpha):
									maxAlpha = data['a data'][m][k]
								if (data['b data'][m][k] > maxAlpha):
									maxAlpah = data['a data'][m][k]
							if (k%2==1):
								if (data['a data'][m][k] < minTheta):
									minTheta = data['a data'][m][k]
								if (data['b data'][m][k] < minTheta):
									minTheta = data['b data'][m][k]
								if (data['a data'][m][k] > maxTheta):
									maxTheta = data['a data'][m][k]
								if (data['b data'][m][k] > maxTheta):
									maxTheta = data['b data'][m][k]
							
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
	print(minAlpha, maxAlpha)
	print(minTheta, maxTheta)
	data = {'a data': a_data, 'b data': b_data}
	stats = {'a means': a_means, 'b means': b_means, 'a devs': a_stdevs, 'b devs': b_stdevs}
	return {'data': data, 'stats': stats}
	

#returned data structure is of the form ['<a or b> postures'][<action>][<frame>][<joint>]['<angle or probs>'][<1x2 1D array or 3x24 2D array>]
def getHisto(data, stats):

	histoA = {}
	histoB = {}
	
	#defining bin boundaries
	alphaBins = []
	for x in range (0, 25):
		alphaBins.append(x*math.pi/12 - math.pi)
	thetaBins = alphaBins[12:16]
	
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
				jointA = {'angle':[], 'prob':[]}
				jointB = {'angle':[], 'prob':[]}
				alphaA = data['a data'][z][p][k]
				thetaA = data['a data'][z][p][k+1]
				alphaB = data['b data'][z][p][k]
				thetaB = data['b data'][z][p][k+1]
				jointA['angle'] = [alphaA, thetaA]
				jointB['angle'] = [alphaB, thetaB]
				
				probsA = [[0 for x in range(24)] for y in range(3)]
				probsB = [[0 for x in range(24)] for y in range(3)]
				
				alphaProbA = [0]*24
				alphaProbB = [0]*24
				thetaProbA = [0]*3
				thetaProbB = [0]*3
				for i in range(0, 24):
					alphaProbA[i] = st.norm.cdf((alphaBins[i+1]-alphaA)/stats['a devs'][z][k]) - st.norm.cdf((alphaA-alphaBins[i])/stats['a devs'][z][k])
					alphaProbB[i] = st.norm.cdf((alphaBins[i+1]-alphaB)/stats['b devs'][z][k]) - st.norm.cdf((alphaB-alphaBins[i])/stats['b devs'][z][k])
				for j in range(0, 3):
						thetaProbA[j] = st.norm.cdf((thetaBins[j+1]-thetaA)/stats['a devs'][z][k+1]) - st.norm.cdf((thetaA-thetaBins[j])/stats['a devs'][z][k+1])
						thetaProbB[j] = st.norm.cdf((thetaBins[j+1]-thetaB)/stats['b devs'][z][k+1]) - st.norm.cdf((thetaB-thetaBins[j])/stats['b devs'][z][k+1])

				for thetaIndex in range(0, 3):
					for alphaIndex in range(0, 24):
						probsA[thetaIndex][alphaIndex] = math.fabs(alphaProbA[alphaIndex]*thetaProbA[thetaIndex])
						probsB[thetaIndex][alphaIndex] = math.fabs(alphaProbB[alphaIndex]*thetaProbB[thetaIndex])
 
				jointA['prob'] = probsA
				jointB['prob'] = probsB
				
				frameA[int(k/2)] = jointA
				frameB[int(k/2)] = jointB				
				k = k + 2
				
			actionA[p] = frameA
			actionB[p] = frameB
		histoA[z] = actionA
		histoB[z] = actionB		
		
	postures = {'a postures': histoA, 'b postures': histoB}
	return postures
		
	