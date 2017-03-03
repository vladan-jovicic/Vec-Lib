import copy

def parse(file_name):#Problem with < 0 direction
	f = open(file_name,"r")
	lines = f.read().split('\n')
	curves = []
	for line in lines:
		if(len(line) == 0):
			break
		if(line[0] == "#"):
			curves.append([])
			pix_point = None
		elif(pix_point == None):
			pix_point = map(int,line.split(" "))
			curves[-1].append(copy.copy(pix_point))
		else:
			cur_point = copy.copy(pix_point)
			cur_point[0] += 0.5
			cur_point[1] += 0.5
			new_pix_point = map(int,line.split(" "))
			new_point = copy.copy(new_pix_point)
			new_point[0] += 0.5
			new_point[1] += 0.5
			
			x,y = new_point[0] - cur_point[0], new_point[1] - cur_point[1]
			sign_x, sign_y = (x>0)-(x < 0), (y>0)-(y<0)
			print "x",x,y,sign_x,sign_y, new_pix_point
			while(new_pix_point != pix_point):
				print cur_point,pix_point
				
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
					print "choose y",delta_y,delta_x,delta_y*x,delta_x*y
					cur_point[0] += x*delta_y/y
					cur_point[1] += delta_y
				else:
					print "choose x",delta_y,delta_x,delta_y*x,delta_x*y
					cur_point[0] += delta_x
					cur_point[1] += y*delta_x/x
				pix_point[0] = int(cur_point[0])
				if(x < 0 and pix_point[0] == int(pix_point[0])):
					pix_point[0] -= 1
				pix_point[1] = int(cur_point[1])
				if(y < 0 and pix_point[1] == int(pix_point[1])):
					pix_point[1] -= 1
				
				curves[-1].append(copy.copy(pix_point))
				
			print "end",new_pix_point,cur_point

	return curves
	
parse("test.txt")