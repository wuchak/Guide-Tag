#Important
#Triangulation 

import numpy as np
#import matplotlib.pyplot as plt

def obj_coor(data):
	data = np.array(data)
	x_n, y_n = data[-1][0], data[-1][1]
	rxy_n = (data[-1][-1]**2) - (x_n**2) - (y_n**2)

	col,row = data.shape

	r_mat = np.zeros((col-1, 1)) # shape (col-1, 1) [[r],[r2]...[rn]] 
	a_mat = np.zeros((col-1,row-1)) #shape (col1,row-1) [[xn-x1, yn-y1],[xn-x2,yn-y2]....[xn-xn-1, yn-yn-1]]
#	print(a_mat.shape)
#	print(a_mat)

	for c in range(col-1):
		rxy_r = int(data[c][-1]**2)
		for r in range(row-1):
			rxy_r -= data[c][r]**2
			a_mat[c][r] = data[-1][r] - data[c][r]
		r_mat[c][0] = rxy_r - rxy_n
#	print(r_mat)
	r_mat = np.matrix(r_mat)
	a_mat = 2 * np.matrix(a_mat)
#	print(a_mat.I)
	xy = a_mat.I.dot(r_mat)
#	print(xy)
	return xy

'''
anchor = np.array([[0,0,4100**(1/2)],[300,0,70100**(1/2)],[150,250,52100**(1/2)]])
x,y = find_usr_coor(anchor)
col,row = anchor.shape
for c in range(col):
	plt.scatter(anchor[c][0],anchor[c][1])
plt.scatter(int(x),int(y))
plt.show()
'''
