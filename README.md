# hoj3d
Code for preparing histograms on kinetic data.

Need to download the data (specifically the skeleton_pos.txt files). 

Import rectToSph and stats in a Python shell (I used anaconda with Python v3) and run by passing the path of the s01s03/s01s03 folder to
getStats. From the getStats' return value, pass the 'data' and 'stats' field to getHisto. Returned data structure is of the form [{a or b postures}][{action}][{frame}][{joint}] to get the histograms. Histograms have two fields: 'angle', which returns a 1x2 1D array specifying the (alpha, theta) coordinates of that joint at the time, and 'prob', which returns a 3x24 2D array of bin probabilities.
