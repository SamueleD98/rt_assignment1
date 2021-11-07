from __future__ import print_function

import math
import time
from sr.robot import *

s_vision=70.0
""" float: limit angle for the field of view relative to the silver tokens"""

g_vision=30.0
""" float: limit angle for the field of view relative to the golden tokens"""

d_th = 0.4
""" float: Threshold for the control of the linear distance"""

count=10
""" int: Counter to avoid deadlocks"""

R = Robot()
""" instance of the class Robot"""

def drive(speed, seconds):
	"""
    	Function for setting a linear velocity
    
   	Args:   
   		speed (int): the speed of the wheels
		seconds (int): the time interval
    	"""    
    	R.motors[0].m0.power = speed
    	R.motors[0].m1.power = speed
    	time.sleep(seconds)
    	R.motors[0].m0.power = 0
    	R.motors[0].m1.power = 0
    
def set_speed(speed):
   	"""
	Function for setting a linear velocity. It doesn't stop the wheels after it completes its execution allowing
	a smoother movement. 
    
	Args: 
		speed (int): the speed of the wheels
	"""
	R.motors[0].m0.power = speed
	R.motors[0].m1.power = speed
	time.sleep(0.5)    

def turn(speed, seconds):
    	"""
    	Function for setting an angular velocity
    
    	Args:   
    		speed (int): the speed of the wheels
		seconds (int): the time interval
    	"""
    	R.motors[0].m0.power = speed
    	R.motors[0].m1.power = -speed
    	time.sleep(seconds)
    	R.motors[0].m0.power = 0
    	R.motors[0].m1.power = 0
    
def find_next_silver_token():
    	"""
    	Function to find the closest silver token in the specified field of view

    	Returns:
		dist (float): distance of the closest silver token (100 if no silver token is detected)
		rot_y (float): angle between the silver token and  the robot (0 if no silver token is detected)
    	"""
    	dist=1
    	for token in R.see():	
        	if token.dist < dist and -s_vision<abs(token.rot_y)<s_vision and token.info.marker_type is MARKER_TOKEN_SILVER:
            		dist=token.dist
	    		rot_y=-round(token.rot_y,2)
    	if dist==1:
		return 100, 0
    	else: 
   		return dist, rot_y    

def find_next_golden_token():
    	"""
	Function to find the closest golden token in the specified field of view

	Returns:
		dist (float): distance of the closest golden token (100 if no golden token is detected)
		rot_y (float): angle between the golden token and  the robot (0 if no golden token is detected)
    	"""
	dist=10
	for token in R.see():
		if token.dist < dist and -g_vision<abs(token.rot_y)<g_vision and token.info.marker_type is MARKER_TOKEN_GOLD:
			dist=token.dist
			rot_y=-round(token.rot_y,2)
	if dist==10:
		return 100, 0
	else: 
		return dist, rot_y    
   	
def check_direction(dist):
   	"""
  	Function to find the best direction to turn into (left or right, where the left one is preferred to assure an anti-clock wise turning). The function counts the obstacles the robots
  	will find turning right or left and it decides the best direction. If the number of obstacles are the same then it will increase the searching distance. 		It is preferable to start with a smaller distance to avoid uncertainties due to a wider field of view.
  	
    	Returns:
		out (int): 1 if is preferrable to turn right or -1 if is preferrable to turn left
   	"""
	sx=0
	dx=0
	for token in R.see():			
		if token.dist<=dist and token.info.marker_type is MARKER_TOKEN_GOLD:
			if 40<=round(-token.rot_y)<=110:
				sx=sx+1
			elif -110<=round(-token.rot_y)<=-40:
				dx=dx+1	
	if sx>dx:
		out=1.0		
	elif sx==dx and dist==1.0:		
		out=check_direction(1.5)
	else:
		out=-1.0		
	return out   
	
def adjust_trajectory(angle):
	"""
	Function to turn the robots of the given angle with a speed that follows a sinusoidal law. The bigger is the angle, the faster the robots turns. 
	If the angle is close to 0 then it is better to avoid to make a turn, let alone a fast one, because it could deviate the route.
	
	Args:
		angle (float): angle between the robot and the object to reach
	"""
	turn(-math.sin(math.radians(angle))*30,0.5) 

while 1:  	
	g_dist, g_angle=find_next_golden_token() #Saving the position of the closest golden box in the driving trajectory of the robot
	if g_dist<1.0:		#Minace impelling
		set_speed(0)
		if count==0:	#If the robots after 10 turns can't avoid the obstacle it moves backwards
			drive(-10,1)
			count=10
		else:
			print("Object detected, turning..\n")
			turnsign=check_direction(1)	#The function returns the best direction to turn into
			turn(turnsign*20,0.5)
	else: 
		count=10	#The robots is able to move freely so the counter can be resetted
		s_dist, s_angle=find_next_silver_token()  #Saving the position of the closest silver box in the driving trajectory of the robot	
		if s_dist<=d_th:	#It's enough close and can be grabbed
			set_speed(0)
			print("Close enough\n")
			if R.grab():  	#Until the box is taken the robot won't drive (It can only turn)
				print("GRABBED\n")
				turn(30,2)
				R.release()
				turn(-30,2)
			else:	#If the box is close but it can't grab it than it adjust its trajectory 
				adjust_trajectory(s_angle)
		elif s_dist<100:
			#If the silver box has been detected the robots approach it with a lower speed and adjusting the trajectory 
			set_speed(15)	
			print("Reaching it..\n")
    			adjust_trajectory(s_angle)
    		else:
    			set_speed(50)
    			print("Searching.. \n") 
    		
     

















