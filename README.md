# Python Robotics Simulator
This is a simple robot simulator that replace and improves the [Original](https://github.com/CarmineD8/python_simulator) one developed by [Student Robotics](https://studentrobotics.org/) and modified for the Research Track I course.  
The robot is able to constantly drive in the arena avoiding the golden boxes.
Occasionally, when they are close, it is capable of grabbing and releasing the silver ones.  

## How to run the code  
The simulator requires a Python 2.7 installation, the [pygame](http://pygame.org/) library, [PyPyBox2D](https://pypi.python.org/pypi/pypybox2d/2.1-r331), and [PyYAML](https://pypi.python.org/pypi/PyYAML/).  

Pygame, unfortunately, can be tricky (though [not impossible](http://askubuntu.com/q/312767)) to install in virtual environments.  
If you are using `pip`, you might try `pip install hg+https://bitbucket.org/pygame/pygame`, or you could use your operating system's package manager. Windows users could use [Portable Python](http://portablepython.com/).  

PyPyBox2D and PyYAML are more forgiving, and should install just fine using `pip` or `easy_install`.  

To run the script in the simulator, use `python2 run.py assignment1.py`.  

For further questions and/or problems read [here](https://github.com/CarmineD8/python_simulator/tree/master/robot-sim).

## What the code does  
The code implements the following algorithm:  
<pre>
<b>while</b> the program is running
	retrieve the position of the closest golden box   
	<b>if</b> its distance is less than an arbitrary one  
		stop the robot  
		<b>if</b> the robot has been trying to avoid obstacles for 10 timesteps/turns   
			move the robot backward a little   
		<b>else</b>  
			search for the best direction to turn into  
			turn  
	<b>else</b>  
 		retrieve the position of the closest silver box  
		<b>if</b> its distance is less than an arbitrary one  
			stop the robot  
			grab the silver box  
			<b>if</b> the action was succesful  
				turn by 180° degrees  
				release the silver box  
				turn by 180° degrees   
			<b>else</b>   
				adjust the trajectory according to the angle of the silver box with respect to the robot direction  
		<b>else</b> <b>if</b> the silver box is in sight  
			set a slower speed  
			adjust the trajectory according to the angle of the silver box with respect to the robot direction  
		<b>else</b>   
			set cruising speed
</pre>

 
 The code uses some new functions and improves others:
 + The **drive** function has been replaced by the **set_speed** function. The latter doesn't stop the robot at the end of its execution in order 
 to have a smoother ride.  
 + The functions to which the search for boxes is assigned are:  
 	- The **find_next_silver_token** that filters, among all the tokens that the robot can see, the nearest silver token in the preset viewing angle  
 	- The **find_next_golden_token** that does the same thing as the find_next_silver_token function, but with a smaller viewing angle  
 + The **check_direction** function compares the number of obstacles on the right of the robot with the ones on the left and decides into which direction to turn. If the numbers match the searching restarts with a greater searching distance  
 + The **adjust_trajectory** turns the robot of the given angle with a speed that follows a sinusoidal law: the bigger is the angle, the faster the robots turns. If the angle is close to zero then it is better to avoid to make a turn, let alone a fast one, because it could deviate the route.
 


## Further improvement


 
