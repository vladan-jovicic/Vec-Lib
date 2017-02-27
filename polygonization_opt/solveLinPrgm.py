##This file contain the code to solve the linear program or quadratic program. It consider that in input it has a set of pixel that correspond to the representation of a convexe set.

##Importation of the solver
from cvxopt import matrix, solvers


#basic stuff
def scalProd(v1,v2):
	#scalar products in R^2
	return v1[0]*v2[0] + v1[1]*v2[1]

def vector(e,f):
	#vector between 2 points e and f: return vector ef->
	return (f[0]-e[0],f[1]-e[1])

#to compute the coefficient relative to e,f1,f2
def coef(e,f1,f2,delta):
	f1e = vector(f1,e)
	f2e = vector(f2,e)
	aux = scalProd(f1e,f2e)-delta
	return abs(aux)-aux

#compute the min real postive and representable
def minReal():
	x,y=0,1,2
	while x!=0:
		y=x
		x=x/2
	return y

#main
def computeLigne(e,liste,delta):
	res = []
	for f1 in liste:
		for f2 in liste:
			res.append(coef(e,f1,f2,delta))
	return res

def computeAPdelta(convexList,delta):
	return [computeLigne(e,convexList,delta) for e in convexList]
	

def solvePdelta(convexList,delta):
	#function to use when you know what distance you want, at most, between each pixel and an edge (the closest one). It compute the better number of point you can use (the min).	 
	#first create the matrix
	A=matrix(computeAPdelta(convexList,delta))
	epsilon=minReal()
	

def solvePnum(convexList,num):
	
	#first create the matrix
