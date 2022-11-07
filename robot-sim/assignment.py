from __future__ import print_function

import time
from sr.robot import *

# Threshold for orientation
a_th = 2.0
# Treshold for distance
d_th = 0.4
# Release distance
r_th = 0.6
# Limited distance
d1 = 1.7
# Bool
silver = True
# Counter number of blocks
counter = 0

R = Robot()

# Function for linear velocity
def drive(speed,seconds):
 R.motors[0].m0.power = speed
 R.motors[0].m1.power = speed
 time.sleep(seconds)
 R.motors[0].m0.power = 0
 R.motors[0].m1.power = 0
 
# Function to change orientaton
def turn(speed,seconds):
 R.motors[0].m0.power = speed
 R.motors[0].m1.power = -speed
 time.sleep(seconds)
 R.motors[0].m0.power = 0
 R.motors[0].m1.power = 0

# Function to find silver token 
def find_silver():
 
 dist = 100
 
 for token in R.see():
 	if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER:
  		dist = token.dist
  		rot_y = token.rot_y
 if dist == 100:
 	return -1, -1
 else:
 	return dist, rot_y
 	
# Function to find gold token 
def find_gold():
 
 dist = 100
 
 for token in R.see():
 	if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD:
  		dist = token.dist
  		rot_y = token.rot_y
 if dist == 100:
 	return -1, -1
 else:
 	return dist, rot_y	
   
 
while (counter < 6):
 
 if silver == True: 			# If silver is true we look for silver token
 	dist, rot_y = find_silver()
 else:					# otherwise golden
 	dist, rot_y = find_gold()
 
 if dist == -1: 			# No token detected
 	print(" I don't see any token: Turning")
 	turn(10,1)
 
 elif silver == True and dist < d_th:  # We are close to silver: grab it
 	print(" Found it")
 	R.grab()
 	print("Gotcha!!")
 	turn(-30,1)
 	silver = not silver 		# now we look for golden token	
 	
 elif silver == False and dist < r_th: # We are close to golden: release it
 	R.release()
 	if R.release:
 		counter = counter +1	# increase counter
 		print("Number of block: " + str(counter))
 	print("Releasing!!!")
 	drive(-60,1)     		# go in the middle and turn
 	turn(30,1)
 	silver = True 			# now we look for silver token
 	
 elif -a_th <= rot_y <= a_th and dist > d1: # Well alligned but very far: big drive
 	print("I'm far... drive fast!!")
 	drive(100,0.5)
 					
 elif -a_th <= rot_y <= a_th and dist < d1: # Well alligned: drive
 	print("Go formaward!!")
 	drive(20,0.5)
 	
 elif dist > d1:    			# Too far: big turn on right
 	print("Too far: turning")
 	turn(20,1)
 	
 elif rot_y < -a_th: 			# Too much on left
 	print("Left a bit..")
 	turn(-2,0.5)
 	
 elif rot_y > a_th: 			# Too much on right
 	print("Right a bit..")
 	turn(2,0.5)
 	
 if counter == 6:  			# Finish work
 	print("Work done... Give me the money")
 	
 
    
