from __future__ import print_function

import math
import time
from sr.robot import *

"""
"""
a_th = 2.0
""" float: Threshold for the control of the linear distance"""
d_th = 0.4
""" float: Threshold for the control of the orientation"""
#silver = True
""" boolean: variable for letting the robot know if it has to look for a silver or for a golden marker"""

R = Robot()
""" instance of the class Robot"""

def drive(speed, seconds):
    """
    Function for setting a linear velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
    
def turn_by_degree(angle):
    """
    Function to turn by a specific angle
    
    """
    dist, rot_y=find_landmark()
    rot_y_new=rot_y-angle
    print(rot_y, rot_y_new)
    while rot_y_new-10<rot_y <=rot_y_new+10:
    	print("not yet")
    	turn(50,1)
    	dist, rot_y=find_landmark()
    print("done")
    
    
       
def find_obstacles():
    """
    Function to find the closest object on path

    Returns:
	dist (float): distance of the closest object (-1 if no token is detected)
	kind
	rot
    """
    dist=100
    for obj in R.see():
        if obj.dist < dist and -30<abs(obj.rot_y)<30:
            dist=round(obj.dist,2)
	    kind=obj.info.marker_type
	    rot=-round(obj.rot_y,2)
    print ("\n \n "+str(kind)+ (" Distance: ")+str(dist)+" Angle: "+ str(rot)+"\n \n")	    
    if dist==100:
	return 100, "No Obstacles", 0
    else: 
   	return dist, kind, rot    
    
    
def find_next_silver_token():
    """
    Function to find the closest silver token

    Returns:
	dist (float): distance of the closest silver token (-1 if no silver token is detected)
	rot_y (float): angle between the robot and the silver token (-1 if no silver token is detected)
    """
    dist=1
    for token in R.see():
        if token.dist < dist and -50<abs(token.rot_y)<50 and token.info.marker_type is MARKER_TOKEN_SILVER:
            dist=token.dist
	    rot_y=-round(token.rot_y,2)
    if dist==1:
	return 100, 0
    else: 
   	return dist, rot_y    

def find_next_golden_token():
    """
    Function to find the closest golden token

    Returns:
	dist (float): distance of the closest golden token (-1 if no golden token is detected)
	rot_y (float): angle between the robot and the golden token (-1 if no golden token is detected)
    """
    dist=10
    for token in R.see():
        if token.dist < dist and -30<abs(token.rot_y)<30 and token.info.marker_type is MARKER_TOKEN_GOLD:
            dist=token.dist
	    rot_y=-round(token.rot_y,2)
    if dist==10:
	return 100, 0
    else: 
   	return dist, rot_y    
   	
def check_direction():
    	dist=1.2 
	sx=range(4,9)
	out=-1
	for token in R.see():
		if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and round(-token.rot_y/10) in sx:
			print("a sx ostacolo quindi vado a dx")
			out=-1
				
    	return out        

def set_speed(speed):
    """
    Function for setting a linear velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(1)





while 1:   
	        
	g_dist, g_angle=find_next_golden_token() 
	
	if g_dist>0.9 or not(-30<=g_angle<=30):  
		#print("Going")     
        	s_dist, s_angle=find_next_silver_token()
        	
        	if s_dist<=0.4:
        		print("FOUND\n")
        		repositioning=0;     
        		while not R.grab():
        			print("grabbing..")
        			s_dist, s_angle=find_next_silver_token()
        			repositioning=repositioning-math.sin(math.radians(s_angle))*10			
				turn(-math.sin(math.radians(s_angle))*10,0.5)
			turn(-repositioning,0.5)				
			turn(30,2)
			R.release()
			turn(-30,2)
		elif s_dist<100:
			print("Reaching him\n")
    			turn(-math.sin(math.radians(s_angle))*20,1) 
    		else:
    			print("Not found \n") 
    		set_speed(40)
        	g_dist, g_angle=find_next_golden_token()
        else:
		print("STOOOOOOOP\n")
		turnsign=check_direction()
		turn(turnsign*30,1)
		
		#time.sleep(3.0)
		#if g_angle<=0:
		        #turn(-(30-abs(g_angle))/2,1)
		        #turn((g_angle/abs(g_angle))*math.cos(math.radians(g_angle))*30,1)
		#elif g_angle>0:
			#turn((30-g_angle)/2,1)
			#turn(math.cos(math.radians(g_angle))*30,1)
	       	#drive(15,1)
		    #drive(30,1)   
	    
	    
	    
	
	    
	    
	    
	    
	    
	     
	"""
	    o_dist, o_type, o_angle = find_obstacles()    
	    while o_type is MARKER_TOKEN_SILVER and o_dist>0.4:
	    	drive(15,1)
	    	o_dist, o_type, o_angle= find_obstacles()	
	    	
	    while g_dist>0.9:
	    	
	    	s_dist, s_angle=find_next_silver_token()
	    	if s_dist<=0.4:
			R.grab()
			turn(30,2)
			R.release()
			turn(30,2)
		else:
	    		turn(angle/3,1)    
	    	drive(15,1)
	    	o_dist, o_type, o_angle= find_obstacles()	
	    	
	    
	    if o_type is MARKER_TOKEN_GOLD and o_dist<=0.9:	
		print("STOOOOOOOP")
		if o_angle>=0:
			turn(10,1)
		if o_angle<0:
			turn(-10,1)
		time.sleep(3.0)
		
	    
	    
	    
		
	    time.sleep(3.0)
	    g_dist, g_rot_y = find_golden_token()
	    s_dist, s_rot_y = find_silver_token()
	    if -30<abs(g_rot_y)<30 and g_dist<30:
	    	print("\n Golden in front is close")
	    	print("  Dist: "+str(g_dist)+"\n")
	    else:
	    	print("Golden in front is NOT close")
	    	print("  Dist: "+str(g_dist)+"\n")
	    
	    drive(60,1)    


	    
		print("Golden: ")
		    print(g_dist, g_rot_y)
		    print("Silver: ")
		    print(s_dist, s_rot_y)
		    drive(50,1)
		    		

		"while not((abs(s_rot_y)<30) and (s_dist<d_th)) or not((abs(g_rot_y)<30) and (g_dist<d_th))"
			drive(50,1)
			g_dist, g_rot_y = find_golden_token()
			s_dist, s_rot_y = find_silver_token()
		if abs(s_rot_y)<30 
			print("Found it silver!")
			grab()
			turn(50,1)
			release()
			turn(50,1)
		if abs(g_rot_y)<30 
			print("Found it golden")
			grab()
			turn(50,1)
			release()
			turn(50,1)
		
	  
		while 1:

		
		
		
		
		
		
		
		
		
		
		#turn_by_degree(90.0)
		time.sleep(3.0)
		dist, rot_y=find_landmark()
		print("The object is " + str(rot_y) + " degree to the right (left) if +(-)")
		for i in range(31000,32000,50):
			#time.sleep(3.0)
			dist, rot_y=find_landmark()
			rot_old=rot_y
			turn(i/10,1)
			dist, rot_y=find_landmark()
			if abs(abs(rot_y)-abs(rot_old))>=89.9 and abs(abs(rot_y)-abs(rot_old))<=90.1:
				print("WE DID IT \nYEEEAH \n    " + str (i) +"\n \n \n")
				print("Angle: "+str(abs(abs(rot_y)-abs(rot_old))))
				time.sleep(3.0)
		
				
		time.sleep(2.0)
		print("Turn 31.5 ,1")
		dist, rot_y=find_landmark()
		rot_old=rot_y
		turn(315/10,1)
		dist, rot_y=find_landmark()
		print("Angle: "+str(abs(abs(rot_y)-abs(rot_old))))
		time.sleep(2.0)
		
		time.sleep(2.0)
		print("Turn 32.5 ,1")
		dist, rot_y=find_landmark()
		rot_old=rot_y
		turn(315/10,1)
		dist, rot_y=find_landmark()
		print("Error: "+str(abs(abs(rot_y)-abs(rot_old))))
		time.sleep(2.0)
		
		time.sleep(2.0)
		print("Turn 34.5 ,1")
		dist, rot_y=find_landmark()
		rot_old=rot_y
		turn(315/10,1)
		dist, rot_y=find_landmark()
		print("Error: "+str(abs(abs(rot_y)-abs(rot_old))))
		time.sleep(2.0)
		
		dist, rot_y=find_landmark()
		print("The object is " + str(rot_y) + " degree to the right (left) if +(-)")
		time.sleep(2.0)
		print("Turn 30,1")
		time.sleep(2.0)
		turn(30,1)
		time.sleep(2.0)
		dist, rot_y=find_landmark()
		print("The object is " + str(rot_y) + " degree to the right (left) if +(-)")
		time.sleep(2.0)
		print("Turn 40,1")
		time.sleep(2.0)
		turn(30,1)
		time.sleep(2.0)
		dist, rot_y=find_landmark()
		print("The object is " + str(rot_y) + " degree to the right (left) if +(-)")
		time.sleep(2.0)
		
		
		time.sleep(2.0)
		
		
		
		dist, rot_y=find_landmark()
		rot_y_new=rot_y-angle
		print(rot_y, rot_y_new)
		while rot_y_new-10<rot_y <=rot_y_new+10:
	     	 	print("not yet")
	    		turn(50,1)
	    		dist, rot_y=find_landmark()
		print("done")
	    
	"""











































