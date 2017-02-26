import sys
import math
import matplotlib.pyplot as plt

for file_name in sys.argv[1:]:
	print file_name
	fichier = open(file_name)
	curves = [[[]]]
	test_cases = []
	new_curve = True
	for line in fichier.read().split('\n'):
		if(len(line) == 0):
			break
		if(line[0] == "E"):
			curves.append([[]])
			test_cases.append(int(line.split(" ")[1]))
			new_curve = True
		elif(line[0] == "#"):
			if(not new_curve):
				curves[-1].append([])
			new_curve = False
		else:
			points = line.split(',')
			curves[-1][-1].append((int(points[0]),int(points[1])))

	curves = curves[:-1] #The last curve is in fact between END and EOF.

	dist_n1,dist_n2 = [],[]
	max_n1,max_n2 = [],[]
	sum_n1,sum_n2 = [],[]
	nb_curves = []
	for file_curves in curves:
		nb_curves.append(0)
		dist_n1.append([])
		dist_n2.append([])
		for curve in file_curves:
			nb_curves[-1] = nb_curves[-1] + 1
			dist_n1[-1].append(0)
			dist_n2[-1].append(0)
			cur_point = curve[0]
			for points in curve[1:]:
				dist_n1[-1][-1] = dist_n1[-1][-1] + abs(points[0] - cur_point[0]) + abs(points[1] - cur_point[1])
				dist_n2[-1][-1] = dist_n2[-1][-1] + math.sqrt((points[0] - cur_point[0])**2 + (points[1] - cur_point[1])**2)
				cur_point = points
		max_n1.append(max(dist_n1[-1]))
		max_n2.append(max(dist_n2[-1]))
		sum_n1.append(sum(dist_n1[-1]))
		sum_n2.append(sum(dist_n2[-1]))

	def print_norm_plot(tab_y, tab_x,legend):
		mini = min(tab_y)
		maxi = max(tab_y)
		new_tab_y = [(i - mini) / (maxi - mini + (maxi == mini)) for i in tab_y]

		plt.plot(tab_x,new_tab_y, label = legend)


	print_norm_plot(nb_curves,test_cases,"nb_curves")
	#print_norm_plot(max_n1,test_cases,"max_n1")
	#print_norm_plot(max_n2,test_cases,"max_n2")
	print_norm_plot(sum_n1,test_cases,"sum_n1")
	print_norm_plot(sum_n2,test_cases,"sum_n2")

	plt.legend()
	plt.axis([-1,101,-0.1,1.1])
	plt.show()
	fichier.close()

#fichier = open("contour")