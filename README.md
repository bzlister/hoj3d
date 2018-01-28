# hoj3d
Code for preparing histograms on kinetic data.

Need to download the data (specifically the skeleton_pos.txt files). 

Import rectToSph and stats in a Python shell (I used anaconda with Python v3) and run by passing the path of the s01s03/s01s03 folder to
getStats. From the getStats' return value, pass the 'data' and 'stats' field to getHisto. Returned data structure is of the form ['<a or b> postures'][<action>][<frame>][<joint>]['<angle or probs>'][<1x2 1D array or 3x24 2D array>]
