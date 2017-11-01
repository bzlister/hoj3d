# hoj3d
Code for preparing histograms on kinetic data.

Need to download the data (specifically the skeleton_pos.txt files). 

Import rectToSph and stats in a Python shell (I used anaconda with Python v3) and run by passing the path of the s01s03/s01s03 folder to
getStats. From the getStats' return value, pass the 'data' and 'means' field to getHisto alongside the desired number of
alpha (horizontal angle as used in paper) bins and theta (vertical angle as used in paper) bins. If you want the bins to be "square" such that
alpha(n+1)-alpha(n) = theta(m+1)-theta(m), numAlphaBins should be twice that of numThetaBins.
