import copy

def parse(file_name): #add pixels to have continuous contours
	nb_points = 0
	f = open(file_name,"r")
	lines = f.read().split('\n')
	curves = []
	for line in lines:
		if(len(line) == 0 or (len(line) >= 2 and line[:2] == "##"):
			break
		if(line[0] == "#"):
			curves.append([])
			pix_point = None
		elif(pix_point == None):
			nb_points += 1
			pix_point = map(int,line.split(","))
			curves[-1].append(tuple(pix_point))
		else:
			nb_points += 1			
			cur_point = copy.copy(pix_point)
			cur_point[0] += 0.5
			cur_point[1] += 0.5
			new_pix_point = map(int,line.split(","))
			new_point = copy.copy(new_pix_point)
			new_point[0] += 0.5
			new_point[1] += 0.5
			
			x,y = new_point[0] - cur_point[0], new_point[1] - cur_point[1]
			sign_x, sign_y = (x>0)-(x < 0), (y>0)-(y<0)
			#print "x",x,y,sign_x,sign_y, new_pix_point
			while(new_pix_point != pix_point):
				#print cur_point,pix_point
				
				delta_x = delta_y = 0
				if(x < 0):
					delta_x = int(cur_point[0]) - (cur_point[0] == int(cur_point[0])) - cur_point[0]
				if(x > 0):
					delta_x = int(cur_point[0]+1) - cur_point[0]
				if(y < 0):
					delta_y = int(cur_point[1]) - (cur_point[1] == int(cur_point[1])) - cur_point[1]
				if(y > 0):
					delta_y = int(cur_point[1]+1) - cur_point[1]

				if(delta_y != 0 and (delta_x == 0 or delta_y*x <= delta_x*y)):
					#print "choose y",delta_y,delta_x,delta_y*x,delta_x*y
					cur_point[0] += x*delta_y/y
					cur_point[1] += delta_y
				else:
					#print "choose x",delta_y,delta_x,delta_y*x,delta_x*y
					cur_point[0] += delta_x
					cur_point[1] += y*delta_x/x
				pix_point[0] = int(cur_point[0])
				if(x < 0 and pix_point[0] == int(pix_point[0])):
					pix_point[0] -= 1
				pix_point[1] = int(cur_point[1])
				if(y < 0 and pix_point[1] == int(pix_point[1])):
					pix_point[1] -= 1
				
				curves[-1].append(tuple(pix_point))
				
			#print "end",new_pix_point,cur_point

	return (nb_points,curves)

def get_dir_list(curve,start_point): #return the direction in the list in order to go clockwise 1:0->len(curve), -1:len(curve)->0
	v0 = curve[(start_point+1)%len(curve)][0] - curve[start_point][0], curve[(start_point+1)%len(curve)][1] - curve[start_point][1]
	v1 = curve[start_point-1][0] - curve[start_point][0], curve[start_point-1][1] - curve[start_point][1]

	if(vector_prod(v0,v1) < 0):
		return 1
	return -1
	
def vector_prod(v1,v2):
		return v1[0]*v2[1] - v1[1]*v2[0]

def gen_convex(curve,convex_curves): #decompose curve as a set of convex curves added to convex_curves
	cur_point = 0
	init = 0
	new_curve = True
	slope = None
	change_direction = False
	i = 1
	while(i < len(curve)):
		if(new_curve): #i = cur_point + 1 and it is a new curve
			curve_direction = (curve[i][0] - curve[cur_point][0], curve[i][1] - curve[cur_point][1])
			new_curve = False
		else:
			if(curve_direction != (curve[i][0] - curve[i-1][0], curve[i][1] - curve[i-1][1])): 
				if(change_direction == False): #First change tolerated if it just a oblic line
					slope = (curve[i][0] - curve[cur_point][0], curve[i][1] - curve[cur_point][1])
					change_direction = True
					cur_point = i
				else: #Too much change in one time, either it is not convex anymore, either we need to change the direction
					v1 = (curve[i][0] - curve[cur_point][0], curve[i][1] - curve[cur_point][1])
					v0 = (-slope[0],-slope[1])
					if(vector_prod(v0,v1) > 0): #convex
						curve_direction = (curve[i][0] - curve[i-1][0], curve[i][1] - curve[i-1][1])
						change_direction = False
						slope = None
					else: #not convex, we have a maximal convex curve
						new_curve = True
						convex_curves.append(curve[init:i])
						#print init,i,len(convex_curves),convex_curves[-1]
						#print "i", curve_direction,(curve[i][0] - curve[i-1][0], curve[i][1] - curve[i-1][1])
						i = i-1#convex curves have one pixel in common
						init = i
						cur_point = init
						change_direction = False
						
			else:
				change_direction = False
				if(slope != None and (abs(curve[i][0] - curve[i-1][0]), abs(curve[i][1] - curve[i-1][1])) > (abs(slope[0]),abs(slope[1]))): #Cannot be a line anymore, need to check if convex or not
					v1 = (curve[i][0] - curve[cur_point][0], curve[i][1] - curve[cur_point][1])
					v0 = (-slope[0],-slope[1])
					if(vector_prod(v0,v1) > 0): #convex
						slope = (curve[i][0] - curve[cur_point-1][0], curve[i][1] - curve[cur_point-1][1])
					else:
						new_curve = True
						#print init
						convex_curves.append(curve[init:i])
						i = i - 1
						init = i
						cur_point = init
		i += 1
	#print i,init,len(curve)
	convex_curves.append(curve[init:i])
					
	
def get_convex_curves(curves):#For each contour, transform it in a set of convex curves
	convex_curves = []
	for curve in curves:
		convex_curves.append([])
		start_point = curve.index(min(curve)) #top-left one
		dir_list = get_dir_list(curve,start_point)
		#print "s_p",start_point,dir_list,curve[start_point]
		#print curve[:-10:-1]
		if(start_point == 0 and dir_list == -1): #Wrong behaviour for curves[:-1:-1]
			gen_convex(curve[::dir_list],convex_curves[-1]) 
		else:
			gen_convex(curve[:start_point+dir_list:dir_list],convex_curves[-1])
		gen_convex(curve[start_point::dir_list],convex_curves[-1])
		#print convex_curves[-1][0],convex_curves[-1][1],convex_curves[-1][2],convex_curves[-1][3][:5]
		plop = [len(i) for i in convex_curves[-1]]
		#print plop,sum(plop) - len(plop)
		
	return convex_curves
		
nb_points,curves = parse("../contour_detection/contour_penguin.txt")
#print [(i[0],len(i),i[-1]) for i in curves]
list_of_list_of_convex_curves = get_convex_curves(curves)