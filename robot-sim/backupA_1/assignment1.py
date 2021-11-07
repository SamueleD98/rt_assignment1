from __future__ import print_function

import math
import time
from sr.robot import *

a_th = 2.0
""" float: Threshold for the control of the linear distance"""
d_th = 0.4
""" float: Threshold for the control of the orientation"""

R = Robot()

def drive(speed, seconds):
    
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
    
def find_next_silver_token():
   
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
	sx=range(5,9)
	out=-1
	for token in R.see():
		if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and round(-token.rot_y/10) in sx:
			print(round(-token.rot_y/10))
			print("a sx ostacolo quindi vado a dx\n")
			out=1
				
    	return out        

def change_direction():
    	dist=1.2 
	sx=range(3,9)
	out=-1
	for token in R.see():
		if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and round(-token.rot_y/10) in sx:
			print("a sx ostacolo quindi vado a dx")
			out=1
				
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

	if g_dist<1.2:
		set_speed(0)
		print("Too close, turning..\n")
		turnsign=check_direction()
		turn(turnsign*20,0.5)
	else: 
		s_dist, s_angle=find_next_silver_token()
		if s_dist<=0.4:
			print("Close enough\n")
        		repositioning=0     
        		while not R.grab():
        			print("grabbing..")
        			s_dist, s_angle=find_next_silver_token()
        			repositioning=repositioning-math.sin(math.radians(s_angle))*10			
				turn(-math.sin(math.radians(s_angle))*10,0.5)
			print("\nGrabbed\n")
			turn(-repositioning,0.5)				
			turn(30,2)
			R.release()
			turn(-30,2)
		elif s_dist<100:
			print("Reaching it..\n")
    			turn(-math.sin(math.radians(s_angle))*20,0.5) 
    		else:
    			print("Searching.. \n") 
    		set_speed(40)
        	



	"""	        
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
	
























