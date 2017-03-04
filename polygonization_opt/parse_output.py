

def parse(file_name):
	f = open(file_name,"r")
	lines = f.read().split('\n')
	curves = []
	for line in lines:
		if(line[0] == "#"):
			curves.append([])
			pix_point = None
		elif(pix_point == None):
			pix_point = map(int,line.split(" "))
			
		else:
			cur_point = copy(pix_point)
			cur_point[0] += 0.5
			cur_point[1] += 0.5
			new_pix_point = map(int,line.split(" "))
			new_point = copy(new_pix_point)
			new_point[0] += 0.5
			new_point[1] += 0.5
			
			x,y = new_point[0] - cur_point[0], new_point[1] - cur_point[1]
			sign_x, sign_y = (x>0)-(x < 0), (y>0)-(y<0)
			
			while(new_pix_point != pix_point):
				curves.append(pix_point)
				check_x = check_y = 0
				if(x < 0):
					delta_x = int(cur_point[0]) - (cur_point[0] == int(cur_point[0]))
				if(x > 0):
					delta_x = int(cur_point[0]) + (cur_point[0] == int(cur_point[0]))
				if(y < 0):
					delta_y = int(cur_point[1]) - (cur_point[1] == int(cur_point[1]))
				if(y > 0):
					delta_y = int(cur_point[1]) + (cur_point[1] == int(cur_point[1]))
				if(x != 0):
					check_x = delta_x/x
				if(y != 0):
					check_y = delta_y/y
				
				if(check_x == 0 or check_y <= check_x):
					cur_point[0] += x*delta_y
					cur_point[1] += delta_y
					pix_point[1] += sign_y
					if(check_y == check_x):
						pix_point[0] += sign_x
				else:
					cur_point[0] += delta_x
					cur_point[1] += y*delta_x
					pix_point[0] += sign_x	
			