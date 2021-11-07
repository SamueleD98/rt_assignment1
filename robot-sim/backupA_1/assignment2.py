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
   	
def check_direction(dist):
	
	sx=0
	dx=0
	if not dist:
		print("\ndistanza standard")
		dist=1.0
	for token in R.see():			
		if token.dist<=dist and token.info.marker_type is MARKER_TOKEN_GOLD:
			if 40<=round(-token.rot_y)<=110:
				sx=sx+1
			elif -110<=round(-token.rot_y)<=-40:
				dx=dx+1
	print("\na sx stanno "+str(sx)+"\nmentre a dx stanno "+str(dx))
	if sx>dx:
		out=1.0
		print("\nscelgo dx")
	elif sx==dx and dist==1.0:
		print("\naumento la distanza")
		out=check_direction(1.5)
	else:
		out=-1.0
		print("\nscelgo sx")
	return out
	
	
	
	
	
	
	"""
	done=0
	dist=2
	while done==0 or dist==0:
		
		out=-1 #sinistra
		done==1
		for token in R.see():			
				if token.dist<=dist and token.info.marker_type is MARKER_TOKEN_GOLD:
					if 50<=token.rot_y<=90:
						#provo a dx
						if -50<=token.rot_y<=-90:
							#diminusco la distanza e riprovo
							dist=dist-0.2
							done==0
						else:
							out=1
	return out
		
	
    	check=0
    	dist=1 
    	while check==0:	    	
		sx=range(5,9)
		dx=range(-5,-9)
		sx_ev=1
		dx_ev=1
		out=-1
		for token in R.see():
			if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and round(-token.rot_y/10) in sx:
				sx_ev=0
				print("sx bocciata perche")
				print(round(-token.rot_y/10))
			if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and round(-token.rot_y/10) in dx:
				dx_ev=0
				print("dx bocciata perche")
				print(round(-token.rot_y/10))
		if sx_ev and dx_ev:
			dist=dist+0.2
		elif sx_ev:
			out=-1
			check=1
		elif dx_ev:
			out=1
			check=1
		else:
			out=-1
			check=1		
    	return out        
	"""
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
		turnsign=check_direction(0)
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
	
























