from __future__ import print_function

import math
import time
from sr.robot import *

s_vision=70.0
""" float: Limit angle for the field of view relative to the silver tokens"""

g_vision=30.0
""" float: Limit angle for the field of view relative to the golden tokens"""

d_th = 0.4
""" float: Threshold for the control of the linear distance"""

count=10
""" int: Counter to avoid deadlocks (read below)"""

cruising_speed=50.0
""" float: Cruising speed of the Robot"""

R = Robot()
""" instance of the class Robot"""
    
def set_speed(speed):
   	"""
	Function for setting a linear velocity. It doesn't stop the wheels after it completes its execution allowing
	a smoother movement. It needs a sleep time for code's timing: without it the controller code runs faster than the GUI refresh speed.
    
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
    	dist=1	#max searching distance. With a greater distance the Robot could find a silver box behind a wall (not realistic)
    	for token in R.see():	
        	if token.dist < dist and -s_vision<abs(token.rot_y)<s_vision and token.info.marker_type is MARKER_TOKEN_SILVER:	#Looks for the closest silver token in the field of view described by the angles -/+ s_vision
            		dist=token.dist		#Assign the new token as the closest
	    		rot_y=-round(token.rot_y,2)	#The angle is inverted because token.rot_y returns the angle between the Robot and the box from the latter pov. The opposite is the angle from the robot pov as needed 
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
	dist=10		#max searching distance, farthest boxes don't affect the Robot
	for token in R.see():
		if token.dist < dist and -g_vision<abs(token.rot_y)<g_vision and token.info.marker_type is MARKER_TOKEN_GOLD: #Looks for the closest golden token in the field of view described by the angles -/+ g_vision
			dist=token.dist		#Assign the new token as the closest
			rot_y=-round(token.rot_y,2)	#The angle is inverted because token.rot_y returns the angle between the Robot and the box from the latter pov. The opposite is the angle from the robot pov as needed 
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
	sx=0	#Number of obstacles on the left side
	dx=0	#Numebr of obstacles on the right side
	for token in R.see():			
		if token.dist<=dist and token.info.marker_type is MARKER_TOKEN_GOLD:
			if 40<=round(-token.rot_y)<=110:	#The left side is described by the space between 40 and 110 degrees
				sx=sx+1
			elif -110<=round(-token.rot_y)<=-40:	#The right side is described by the space between -110 and -40 degrees
				dx=dx+1	
	if sx>dx:	#If there are more obstacles on the left side, the Robot must turn right
		out=1.0		
	elif sx==dx and dist==1.0:		#If the number of obstacles on both sides are the same and it wasn't done already 
		out=check_direction(1.5)	#the function is called again with a greater max distance
	else:		#In every other case the Robot should turn left. This according to the necessity to drive around the circuit in the counter-clockwise direction
		out=-1.0		
	return out   
	
def adjust_trajectory(angle):
	"""
	Function to turn the robots of the given angle with a speed that follows a sinusoidal law. The bigger is the angle, the faster the robots turns. 
	If the angle is close to 0 then it is better to avoid to make a turn, let alone a fast one, because it could deviate the route.
	
	Args:
		angle (float): angle between the robot and the object to reach
	"""
	turn(-math.sin(math.radians(angle))*30,0.5) #The angle is in degrees so it needs to be converted in radians to be used by the math.sin function. Since a positve angle means the object is on the left and since 
						    #to turn left the "turn" function needs a negative speed, the speed must be inverted (Same for objects on the right --> negative angle and positive speed)

while 1:  	
	g_dist, g_angle=find_next_golden_token() #Saving the position of the closest golden box in the driving trajectory of the robot
	if g_dist<1.0:		#Obstacle ahead
		set_speed(0)
		if count==0:		#If the robot after 10 turns can't avoid the obstacle it moves backwards
			drive(-10,1)
			count=10	#The robot starts from a new position: counter is set again to 10
		else:
			print("Obstacle detected, turning..\n")
			turnsign=check_direction(1)	#The function returns the best direction to turn into (either +1 or -1)
			turn(turnsign*20,0.5)		#The robot turns according to the direction suggested with a fixed speed for a fixed time
			count=count-1			#The robot is turning so it decrease the counter
	else: 
		count=10	#The robot is able to move freely so the counter can be resetted
		s_dist, s_angle=find_next_silver_token()  #Saving the position of the closest silver box in the driving trajectory of the robot	
		if s_dist<=d_th:	#It's enough close and can be grabbed
			set_speed(0)
			print("Close enough\n")
			if R.grab():  	#Until the box is taken the Robot won't drive (It can only turn)
				print("GRABBED\n")
				turn(30,2)
				R.release()
				turn(-30,2)
			else:	#If the box is close but Robot can't grab it, the Robot adjust its trajectory towards the silver box
				adjust_trajectory(s_angle)
		elif s_dist<100:
			#If the silver box has been detected the Robot approach it with a lower speed and adjusting the trajectory towards the silver box
			set_speed(15)	
			print("Reaching it..\n")
    			adjust_trajectory(s_angle)
    		else:	#if s_dist is equal to 100 than there are not any silver box in the field of view of the Robot, so it continues its search
    			set_speed(cruising_speed)
    			print("Searching.. \n") 
    		
     

















