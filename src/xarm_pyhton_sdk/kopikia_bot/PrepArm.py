#!/usr/bin/env python3

"""
Description: functions to change tools
"""
import os
import sys
import time
import math
import json
from xarm.wrapper import XArmAPI
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

ARMPresent = False

#######################################################
#kopikia home J1 0 J2 0 J3 0 J4 0 J5 -90 j6 0

#####################ARRAYS#############################
HomeToReady_list = [
			   [30, 0, 0, 0, -90, 0],
			   #[-90, -25, -100, 0, 122, 0],
			   #[0, -25, -100, 0, 122, 0]
			   ]

HomeToCup_list = [
			   [-26.1, 56.3, -57.5, -1.5, -88.7, 0],
			   [-26.1, 56.3, -57.5, -1.5, -85.7, 0],
			   [-26.1, 56.3, -57.5, -1.5, -88.7, 0]
			   ]

Cup1ToAlign_list = [
			   [-10, 0, 0, 0, -90, 0],
			   [-10, 39.5, -38.6, 0, -90, 0],
			   [-10, 39.5, -38.6, 51.4, -90, 0]
			   ]

Cup1ToAlignReverse_list = [
			   [-10, 39.5, -38.6, 51.4, -90, 0],
			   [-10, 39.5, -38.6, 0, -90, 0],
			   [-10, 0, 0, 0, -90, 0]
			   ]

Cup1Adjust_list = [
			   [-27.2, 48, -60.6, 30.8, -78.5, -6.1],
			   [-27.7, 50, -60.6, 30.8, -78.5, -6.1],
			   ]

Cup1AdjustReverse_list = [
			   [-27.7, 50, -60.6, 30.8, -78.5, -6.1],
			   ]

Cup2ToAlign_list = [
			   [-10, 0, 0, 0, -90, 0],
			   [-10, 39.5, -38.6, 0, -90, 0],
			   [-10, 39.5, -38.6, 51.4, -90, 0]
			   ]

Cup2ToAlignReverse_list = [
			   [-10, 39.5, -38.6, 51.4, -90, 0],
			   [-10, 39.5, -38.6, 0, -90, 0],
			   [-10, 0, 0, 0, -90, 0]
			   ]

Cup2Adjust_list = [
			   [-27.2, 48, -60.6, 30.8, -78.5, -6.1],
			   [-27.7, 50, -60.6, 30.8, -78.5, -6.1],
				]

Cup2AdjustReverse_list = [
			   [-27.7, 50, -60.6, 30.8, -78.5, -6.1],
				]

Cup1Release_list = [
			   [-27.7, 43.3, -60.6, 30.8, -78.6, -6.1],
			   [-21.2, 27.7, -32.7, 30.9, -84.3, -6.1],
			   ]

Cup1ToHome_list = [
			   [-10, 27.7, -32.7, 30.9, -84.3, -6.1],
			   [30, 0, 0, 0, -90, 0],
			   ]

Cup2ToHome_list = [
			   [-10, 27.7, -32.7, 30.9, -84.3, -6.1],
			   [30, 0, 0, 0, -90, 0],
				]
	
Cup2Release_list = [
			   [-27.7, 43.3, -60.6, 30.8, -78.6, -6.1],
			   [-21.2, 27.7, -32.7, 30.9, -84.3, -6.1],
			   ]

Cup1ReleaseReverse_list = [
			   [-21.2, 27.7, -32.7, 30.9, -84.3, -6.1],
			   [-27.7, 43.3, -60.6, 30.8, -78.6, -6.1],
			   ]

Cup2ReleaseReverse_list = [
			   [-21.2, 27.7, -32.7, 30.9, -84.3, -6.1],
			   [-27.7, 43.3, -60.6, 30.8, -78.6, -6.1],
			   ]

ArmToCup1Release_list = [
			   [15.6, 26, -52.9, 0, -91.9, 0],
			   [30, 0, 0, 0, -90, 0],
			   ]

ArmToCup2Release_list = [
			   [33.8, 12.4, -40, -12, -87.8, -6],
			   [30, 0, 0, 0, -90, 00],
			   ]

ArmToScreen_list = [
			   [0.4, -13.1, -55.4, 82.2, -63.7, -63.8],
			   #[-90, -25, -100, 0, 122, 0],
			   #[-90, -60, -30, 0, 90, 0]
			   ]

ArmLatteOnScreen_list = [
			   [-5.4, -16.3, -58, 82.1, -52.6, -72.3],
			   [-9.8, -16.3, -58, 82.1, -52.6, -72.3],
			   [-5.4, -16.3, -58, 82.1, -52.6, -72.3],
			   ]

ArmLatteOffScreen_list = [
			   [-9.8, -16.3, -58, 82.1, -52.6, -72.3],
			   [-5.4, -16.3, -58, 82.1, -52.6, -72.3],
			   ]

ArmCappuccinoOnScreen_list = [
			   [-5, -12.9, -62.7, 85.1, -51.9, -72.2],
			   [-6.8, -12.9, -62.7, 85.1, -51.9, -72.2],
			   [-5, -12.9, -62.7, 85.1, -51.9, -72.2],
			   ]

ArmCappuccinoOffScreen_list = [
			   [-6.8, -12.9, -62.7, 85.1, -51.9, -72.2],
			   [-5, -12.9, -62.7, 85.1, -51.9, -72.2],
			   ]

ArmAmericanoOnScreen_list = [
			   [-2.4, -7.4, -67.5, 85.1, -55.2, -72.2],
			   [-3.2, -12.9, -62.7, 85.1, -51.9, -72.2],
			   [-2.4, -7.4, -67.5, 85.1, -55.2, -72.2],
			   ]

ArmAmericanoOffScreen_list = [
			   [-3.2, -12.9, -62.7, 85.1, -51.9, -72.2],
			   [-2.4, -7.4, -67.5, 85.1, -55.2, -72.2],
			   ]

ArmEspressoOnScreen_list = [
			   [0.1, -4, -71.4, 85.1, -55.5, -72.2],
			   [-1.5, -4, -71.4, 85.1, -55.5, -72.2],
			   [0.1, -4, -71.4, 85.1, -55.5, -72.2],
			   ]

ArmEspressoOffScreen_list = [
			   [-1.5, -4, -71.4, 85.1, -55.5, -72.2],
			   [0.1, -4, -71.4, 85.1, -55.5, -72.2],
			   ]

ArmMochaOnScreen_list = [
			   [-0.8, -5.3, -67.8, 85, -53.3, -71.6],
			   [-1.9, -5.3, -67.8, 85, -53.3, -71.6],
			   [-0.8, -5.3, -67.8, 85, -53.3, -71.6],
			   ]

ArmMochaOffScreen_list = [
			   [-1.9, -5.3, -67.8, 85, -53.3, -71.6],
			   [-0.8, -5.3, -67.8, 85, -53.3, -71.6],
			   ]

ArmMiloOnScreen_list = [
			   [-3.9, -11.1, -62.8, 85.6, -50, -71.6],
			   [-5.2, -11.1, -62.8, 85.6, -50, -71.6],
			   [-3.9, -11.1, -62.8, 85.6, -50, -71.6],
			   ]

ArmMiloOffScreen_list = [
			   [-5.2, -11.1, -62.8, 85.6, -50, -71.6],
			   [-3.9, -11.1, -62.8, 85.6, -50, -71.6],
			   ]
ArmSaltedCaramelOnScreen_list = [
			   [-9.7, -21.1, -54.3, 83.5, -39.8, -71.7],
			   [-11.4, -21.1, -54.3, 83.5, -39.8, -71.7],
			   [-9.7, -21.1, -54.3, 83.5, -39.8, -71.7],
			   ]

ArmSaltedCaramelOffScreen_list = [
			   [-11.4, -21.1, -54.3, 83.5, -39.8, -71.7],
			   [-9.7, -21.1, -54.3, 83.5, -39.8, -71.7],
			   ]

ArmMatchaOnScreen_list = [
			   [-13.3, -24.4, -51.3, 83.5, -38.2, -71.7],
			   [-14.4, -24.4, -51.3, 83.5, -38.2, -71.7],
			   [-13.3, -24.4, -51.3, 83.5, -38.2, -71.7],
			   ]

ArmMatchaOffScreen_list = [
			   [-14.4, -24.4, -51.3, 83.5, -38.2, -71.7],
			   [-13.3, -24.4, -51.3, 83.5, -38.2, -71.7],
			   ]

ArmDirtyOnScreen_list = [
			   [-8.1, -17.2, -56.4, 83.5, -34.7, -71.7],
			   [-9.1, -17.2, -56.4, 83.5, -34.7, -71.7],
			   [-8.1, -17.2, -56.4, 83.5, -34.7, -71.7],
			   ]

ArmDirtyOffScreen_list = [
			   [-9.1, -17.2, -56.4, 83.5, -34.7, -71.7],
			   [-8.1, -17.2, -56.4, 83.5, -34.7, -71.7],
			   ]

CoffeeToServe_list = [
			   [31.2, 42.3, -44.1, 0, -90.4, 0],
			   #[-90, -25, -100, 0, 122, 0],
			   #[-90, -60, -30, 0, 90, 0]
			   ]

ArmToLeftCup_list = [
				[32.4, 26.2, -21.8, -12, -90, -6],		#Arm infront of cups
				[33.8, 33.7, -38.4, -12, -82.8, -6],	#Arm in left cup
			   ]		

ArmLiftLeftCup_list = [
				[33.8, 33.7, -38.4, -12, -87.8, -6], 	#Arm lift left cup
				[21.8, 33.7, -38.4, -12, -87.8, -6], 	#Arm beside left cup holder
				[30, 0, 0, 0, -90, 0]					#Arm home
			   ]	

ArmLiftLeftCupReverse_list = [
				[30, 0, 0, 0, -90, 0], 					#Arm beside left cup holder
				[21.8, 33.7, -38.4, -12, -87.8, -6], 	#Arm lift left cup
				[33.8, 33.7, -38.4, -12, -87.8, -6],	#Arm infront of cups
			   ]
  
ArmToRightCup_list = [
				[15.6, 28.8, -21.7, 0, -95, 0],		#Arm infront of cups
				[15.6, 37.6, -40.8, 0, -87.2, 0],	#Arm in right cup
			   ]

ArmLiftRightCup_list = [
				[15.6, 37.6, -40.8, 0, -92.2, 0], 		#Arm lift right cup
				[26.8, 37.6, -40.8, 0, -92.2, 0], 		#Arm beside right cup holder
				[30, 0, 0, 0, -90, 0]					#Arm home
			   ]

ARmLiftRightCupReverse_list = [
				[30, 0, 0, 0, -90, 0],					#Arm home
				[26.8, 37.6, -40.8, 0, -92.2, 0], 		#Arm beside right cup holder
				[15.6, 37.6, -40.8, 0, -92.2, 0], 		#Arm lift right cup
				#[15.8, 31.3, -37.1, 0.2, -80.7, 0]		#Cup in holder
			   ]

#############################TOOL 1###################################
BeforeTool1_list = [  
				[0, -25, -100, 0, 122, 0],
				[-54.2,-25, -100, 0.8, 89.9, 0],
				[-107, -51.8, -38.2, -0.4, 89.8, -56.5]
				]
AfterTool1_list = [
				[-87.4, -37.1, -37.1, -0.6, 74.4, -36.8],
				[-87.4, -25, -100, 0, 122, 0],
				[0, -25, -100, 0, 122, 0]
				]       

UnequipTool1_list = [
				[0, -25, -100, 0, 122, 0],
				[-87.4, -25, -100, 0, 122, 0],
				[-87.4, -37.1, -37.1, -0.6, 74.4, -36.8]
				]

Tool1ToReady_list = [
				[-107, -51.8, -38.2, -0.4, 89.8, -56.5],
				[-54.2, -25, -100, 0.8, 89.9, 0],
				[0, -25, -100, 0, 122, 0]
				]
ToolToClean_list = [
				[0, -25, -100, 0, 122, 0],
				[0.4, -21.8, -76.3, 1, 115.9, -90],
				[0.3,-26.4,-48.5, 1.7, 92.7, -90]
				]

CleanToReady_list = [
				[0.3,-26.4,-48.5, 1.7, 92.7, -90],
				[0.4, -21.8, -76.3, 1, 115.9, -90],
				[0, -25, -100, 0, 122, 0],	
				]

#############################TOOL 2###################################
BeforeTool2_list = [  
				[0, -25, -100, 0, 122, 0],
				[50.8, -25, -100, 0.7, 91.2, 0],
				[101, -63.1, -26.7, 0.7, 90.2, -118.7]
				]
AfterTool2_list = [
				[75.3, -48.5, -34, 0.6, 82.8, -144.3],
				[75.3, -25, -100, 0, 122, -72],
				[0, -25, -100, 0, 122, 0]
				]       

UnequipTool2_list = [
				[0, -25, -100, 0, 122, 0],
				[75.3, -25, -100, 0, 122, -72],
				[76.3, -46.1, -35.2, 0.7, 81.6, -143.3]
				]

Tool2ToReady_list = [
				[101, -63.1, -26.7, 0.7, 90.2, -118.7],
				[50.8, -25, -100, 0.7, 91.2, 0],
				[0, -25, -100, 0, 122, 0]
				]
ArmToLeftCup_list = [
				[32.4, 26.2, -21.8, -12, -90, -6],		#Arm infront of cups
				[33.8, 33.7, -38.4, -12, -82.8, -6],	#Arm in left cup
			   ]		
				


#############################TOOL 3###################################
BeforeTool3_list = [
				[0, -25, -100, 0, 122, 0],
				[-40.5, -13.3, -98.2, -110, 133.2, -118.6]
				]

AfterTool3_list = [
				[-70.6, -15.9, -111.2, -99.6, 103.7, -127.6],
				[0, -25, -100, -99.6, 103.7, -127.6],
				[0, -25, -100, 0, 122, -180]
				]

UnequipTool3_list = [
				[0, -25, -100, 0, 122, -180],
				[0, -25, -100, -99.6, 103.7, -127.6],
				[-70.6, -15.9, -111.2, -99.6, 103.7, -127.6],
				]

Tool3ToReady_list = [
				[-40.5, -13.3, -98.2, -110, 133.2, -118.6],
				[0, -25, -100, 0, 122, 0]
				]

########################################################


def GripperControl(arm, state):
	arm.set_mode(0)
	arm.set_state(0)
	time.sleep(0.1)
	code = arm.set_gripper_mode(0)
	code = arm.set_gripper_enable(True)
	code = arm.set_gripper_speed(5000)
	if(state == "close"):
		code = arm.set_gripper_position(-10, wait=True)
	elif(state ==  "open"):
		code = arm.set_gripper_position(800, wait=True)
	else:
		raise ValueError("Invalid state. Use 'close' or 'open'.")




def HomeToReady(arm, speed, is_radian, wait, angles_list=HomeToReady_list):
	GripperControl(arm, "close")
	time.sleep(0.1)
	for angles in angles_list:
		arm.set_servo_angle(angle=angles, speed=speed, is_radian=is_radian, wait=wait)

def ArmToLeftCup(arm, speed, is_radian, wait, angles_list=HomeToReady_list):
	GripperControl(arm, "open")
	time.sleep(0.1)
	for angles in angles_list:
		arm.set_servo_angle(angle=angles, speed=speed, is_radian=is_radian, wait=wait)

def ArmLiftLeftCup(arm, speed, is_radian, wait, angles_list=HomeToReady_list):
	GripperControl(arm, "close")
	time.sleep(0.1)
	for angles in angles_list:
		arm.set_servo_angle(angle=angles, speed=speed, is_radian=is_radian, wait=wait)

def ArmToRightCup(arm, speed, is_radian, wait, angles_list=HomeToReady_list):
	GripperControl(arm, "open")
	time.sleep(0.1)
	for angles in angles_list:
		arm.set_servo_angle(angle=angles, speed=speed, is_radian=is_radian, wait=wait)

def Cup1Adjust(arm, speed, is_radian, wait, angles_list=Cup1Adjust_list):
	for angles in angles_list:
		arm.set_servo_angle(angle=angles, speed=speed, is_radian=is_radian, wait=wait)		

def Cup1AdjustReverse(arm, speed, is_radian, wait, angles_list=Cup1AdjustReverse_list):
	for angles in angles_list:
		arm.set_servo_angle(angle=angles, speed=speed, is_radian=is_radian, wait=wait)

def Cup2Adjust(arm, speed, is_radian, wait, angles_list=Cup2Adjust_list):
	for angles in angles_list:
		arm.set_servo_angle(angle=angles, speed=speed, is_radian=is_radian, wait=wait)		

def Cup2AdjustReverse(arm, speed, is_radian, wait, angles_list=Cup2AdjustReverse_list):
	for angles in angles_list:
		arm.set_servo_angle(angle=angles, speed=speed, is_radian=is_radian, wait=wait)
		
def ArmLiftRightCup(arm, speed, is_radian, wait, angles_list=HomeToReady_list):
	GripperControl(arm, "close")
	time.sleep(0.1)
	for angles in angles_list:
		arm.set_servo_angle(angle=angles, speed=speed, is_radian=is_radian, wait=wait)

def Cup1ReleaseReverse(arm, speed, is_radian, wait, angles_list=Cup1ReleaseReverse_list):
	for angles in angles_list:
		arm.set_servo_angle(angle=angles, speed=speed, is_radian=is_radian, wait=wait)

def Cup2ReleaseReverse(arm, speed, is_radian, wait, angles_list=Cup2ReleaseReverse_list):
	for angles in angles_list:
		arm.set_servo_angle(angle=angles, speed=speed, is_radian=is_radian, wait=wait)

def HomeToCup(arm, speed, is_radian, wait, angles_list=HomeToCup_list):
	arm.set_mode(0)
	arm.set_state(0)   
	time.sleep(0.1)
	for angles in angles_list:
		arm.set_servo_angle(angle=angles, speed=speed, is_radian=is_radian, wait=wait)

def Cup1ToAlign(arm, speed, is_radian, wait, angles_list=Cup1ToAlign_list):
	arm.set_mode(0)
	arm.set_state(0)   
	time.sleep(0.1)
	for angles in angles_list:
		arm.set_servo_angle(angle=angles, speed=speed, is_radian=is_radian, wait=wait)

def Cup2ToAlign(arm, speed, is_radian, wait, angles_list=Cup2ToAlign_list):
	arm.set_mode(0)
	arm.set_state(0)   
	time.sleep(0.1)
	for angles in angles_list:
		arm.set_servo_angle(angle=angles, speed=speed, is_radian=is_radian, wait=wait)

def Cup1Release(arm, speed, is_radian, wait, angles_list=Cup1Release_list):
	arm.set_mode(0)
	arm.set_state(0)   
	time.sleep(0.1)
	for angles in angles_list:
		arm.set_servo_angle(angle=angles, speed=speed, is_radian=is_radian, wait=wait)	

def Cup2Release(arm, speed, is_radian, wait, angles_list=Cup2Release_list):
	arm.set_mode(0)
	arm.set_state(0)   
	time.sleep(0.1)
	for angles in angles_list:
		arm.set_servo_angle(angle=angles, speed=speed, is_radian=is_radian, wait=wait)	

def Cup1ToHome(arm, speed, is_radian, wait, angles_list=Cup1ToHome_list):
	arm.set_mode(0)
	arm.set_state(0)   
	time.sleep(0.1)
	for angles in angles_list:
		arm.set_servo_angle(angle=angles, speed=speed, is_radian=is_radian, wait=wait)

def Cup2ToHome(arm, speed, is_radian, wait, angles_list=Cup2ToHome_list):
	arm.set_mode(0)
	arm.set_state(0)   
	time.sleep(0.1)
	for angles in angles_list:
		arm.set_servo_angle(angle=angles, speed=speed, is_radian=is_radian, wait=wait)	



def ArmToRelease(arm, speed, is_radian, wait, angles_list=ArmToCup1Release_list):
	arm.set_mode(0)
	arm.set_state(0)   
	time.sleep(0.1)
	for angles in angles_list:
		arm.set_servo_angle(angle=angles, speed=speed, is_radian=is_radian, wait=wait)

def CoffeeToServe(arm, speed, is_radian, wait, angles_list=CoffeeToServe_list):
	arm.set_mode(0)
	arm.set_state(0)   
	time.sleep(0.1)
	for angles in angles_list:
		arm.set_servo_angle(angle=angles, speed=speed, is_radian=is_radian, wait=wait)

def ArmToScreen(arm, speed, is_radian, wait, angles_list=ArmToScreen_list):
	arm.set_mode(0)
	arm.set_state(0)   
	time.sleep(0.1)
	for angles in angles_list:
		arm.set_servo_angle(angle=angles, speed=speed, is_radian=is_radian, wait=wait)
		
def ArmSelectDrink(arm, speed, is_radian, wait, angles_list=ArmLatteOnScreen_list):
	arm.set_mode(0)
	arm.set_state(0)   
	time.sleep(0.1)
	for angles in angles_list:
		arm.set_servo_angle(angle=angles, speed=speed, is_radian=is_radian, wait=wait)

def EquipTool1(arm, speed, is_radian, wait,angles_list1=BeforeTool1_list, angles_list2=AfterTool1_list):
	arm.set_mode(0)
	arm.set_state(0)   
	time.sleep(0.1)
	for angles in angles_list1:
		arm.set_servo_angle(angle=angles, speed=speed, is_radian=is_radian, wait=wait)
	arm.set_position(x=None, y=None, z=-165.1, relative=True, is_radian=False, wait=True)
	GripperControl(arm, "open")
	arm.set_position(x=None, y=None, z=110.1, relative=True, is_radian=False, wait=True)
	arm.set_position(x=80, y=-80, z=None, relative=True, is_radian=False, wait=True)
	for angles in angles_list2:
		arm.set_servo_angle(angle=angles, speed=speed, is_radian=is_radian, wait=wait)

def UnequipTool1(arm, speed, is_radian, wait, angles_list1=UnequipTool1_list, angles_list2=Tool1ToReady_list):
	arm.set_mode(0)
	arm.set_state(0)   
			   #[10, 0, 0, 0, -90, 0],
	time.sleep(0.1)
	for angles in angles_list1:
		arm.set_servo_angle(angle=angles, speed=speed, is_radian=is_radian, wait=wait)
	time.sleep(0.1)
	arm.set_position(x=-80, y=80, z=None, relative=True, is_radian=False, wait=True)
	arm.set_position(x=None, y=None, z=-110.1, relative=True, is_radian=False, wait=True)
	GripperControl(arm, "close")
	time.sleep(1)
	arm.set_position(x=None, y=None, z=165.1, relative=True, is_radian=False, wait=True)
	for angles in angles_list2:
		arm.set_servo_angle(angle=angles, speed=speed, is_radian=is_radian, wait=wait)
		
		

def EquipTool2(arm, speed, is_radian, wait, angles_list1=BeforeTool2_list, angles_list2=AfterTool2_list):
	arm.set_mode(0)
	arm.set_state(0)   
	time.sleep(0.1)
	for angles in angles_list1:
		arm.set_servo_angle(angle=angles, speed=speed, is_radian=is_radian, wait=wait)
	arm.set_position(x=None, y=None, z=-105.2, relative=True, is_radian=False, wait=True)
	time.sleep(0.1)
	GripperControl(arm, "open")
	arm.set_position(x=None, y=None, z=112.9, relative=True, is_radian=False, wait=True)
	arm.set_position(x=100, y=60, z=None, relative=True, is_radian=False, wait=True)
	for angles in angles_list2:
		arm.set_servo_angle(angle=angles, speed=speed, is_radian=is_radian, wait=wait)

def UnequipTool2(arm, speed, is_radian, wait, angles_list1=UnequipTool2_list, angles_list2=Tool2ToReady_list):
	arm.set_mode(0)
	arm.set_state(0)   
	time.sleep(0.1)
	for angles in angles_list1:
		arm.set_servo_angle(angle=angles, speed=speed, is_radian=is_radian, wait=wait)
	time.sleep(0.1)
	arm.set_position(x=-96, y=-65, z=None, relative=True, is_radian=False, wait=True)
	arm.set_position(x=None, y=None, z=-112.9, relative=True, is_radian=False, wait=True)
	GripperControl(arm, "close")
	time.sleep(1)
	arm.set_position(x=None, y=None, z=105.2, relative=True, is_radian=False, wait=True)
	for angles in angles_list2:
		arm.set_servo_angle(angle=angles, speed=speed, is_radian=is_radian, wait=wait)



def EquipTool3(arm, speed, is_radian, wait, angles_list1=BeforeTool3_list,angles_list2=AfterTool3_list):
	arm.set_mode(0)
	arm.set_state(0)
	time.sleep(0.1)
	for angles in angles_list1:
		arm.set_servo_angle(angle=angles, speed=speed, is_radian=is_radian, wait=wait)
	time.sleep(0.1)
	arm.set_position(x=-145, relative=True, is_radian=False, wait=True)
	GripperControl(arm, "open")
	arm.set_position(z=80, relative=True, is_radian=False, wait=True)
	for angles in angles_list2:
		arm.set_servo_angle(angle=angles, speed=speed, is_radian=is_radian, wait=wait)
	time.sleep(0.1)

def UnequipTool3(arm, speed, is_radian, wait, angles_list1=UnequipTool3_list, angles_list2=Tool3ToReady_list):
	arm.set_mode(0)
	arm.set_state(0)   
	time.sleep(0.1)
	for angles in angles_list1:
		arm.set_servo_angle(angle=angles, speed=speed, is_radian=is_radian, wait=wait)
	time.sleep(0.1)
	arm.set_position(z=-80, relative=True, is_radian=False, wait=True)
	GripperControl(arm, "close")
	arm.set_position(x=145, relative=True, is_radian=False, wait=True)
	for angles in angles_list2:
		arm.set_servo_angle(angle=angles, speed=speed, is_radian=is_radian, wait=wait)

def ToolToContainer(arm, speed, is_radian, wait, angles_list=ToolToClean_list):
	arm.set_mode(0)
	arm.set_state(0)   
	time.sleep(0.1)
	for angles in angles_list:
		arm.set_servo_angle(angle=angles, speed=speed, is_radian=is_radian, wait=wait)

	
def ContainerToReady(arm, speed, is_radian, wait, angles_list=CleanToReady_list):
	arm.set_mode(0)
	arm.set_state(0)  
	time.sleep(0.1) 
	for angles in angles_list:
		arm.set_servo_angle(angle=angles, speed=speed, is_radian=is_radian, wait=wait)


class ArmROSNode(Node):
	def __init__(self, arm=None):
		super().__init__('arm_control_node')
		self.arm = arm
		self.status_pub = self.create_publisher(String, '/barista/status', 10)
		self.cmd_sub = self.create_subscription(String, '/barista/cmd', self.cmd_callback, 10)
		self.cup_pos_sub = self.create_subscription(String, '/barista/cup_position', self.cup_pos_callback, 10)
		self.cup_selection = None
		self.lastest_cup_position = []
		self.get_logger().info('ArmROSNode initialized')

	def cup_pos_callback(self, msg: String):
			"""Callback that continuously updates the arm with tracking data from YOLO"""
			try:
				self.latest_cup_data = json.loads(msg.data)
				self.get_logger().debug(f"Updated cup position data: {self.latest_cup_data}")
			except Exception as e:
				self.get_logger().error(f"Failed to parse cup position JSON data: {e}")

	def publish_status(self, status: str):
		msg = String()
		msg.data = status
		self.status_pub.publish(msg)
		self.get_logger().info(f'Published status: {status}')

	def find_physical_side(self) -> str:
		"""
		Cross-references self.cup_selection (e.g., 'cup1' or 'cup2') 
		with the active YOLO tracking array to find its absolute layout position.
		"""
		self.get_logger().info(f"Finding physical side for cup selection: {self.cup_selection}")
		self.get_logger().info(f"Latest cup data: {self.latest_cup_data}")
		
		if not self.latest_cup_data:
			self.get_logger().warning("No vision data tracking stream active.")
			return None
			
		for item in self.latest_cup_data:
			detected_object = item.get("object", "").lower().strip()
			
			# Match if 'cup_1' or 'cup_2' is contained within the detected string name
			if self.cup_selection and self.cup_selection in detected_object:
				side = item.get("position")  # Returns "Left" or "Right"
				self.get_logger().info(f"Matched target {self.cup_selection} to physical side: {side}")
				return side
				
		return None
	
	def cmd_callback(self, msg: String):
		self.get_logger().info(f'Received command: {msg.data}')
		#if not self.arm:
		#	self.get_logger().warning('No arm instance available to execute commands')
		#	return
		cmd = msg.data.lower().strip()
		if cmd == 'cup1' or cmd == 'cup2':
			self.cup_selection = cmd
			self.get_logger().info(f'Cup selected: {self.cup_selection}')
		# Basic command handling - extend as needed
		elif cmd == 'espresso' or cmd == 'americano' or cmd == 'latte' or cmd == 'cappuccino' or cmd == 'latte' \
			or cmd == 'milo' or cmd == 'milo_mocha' or cmd == 'salted_caramel_latte' or cmd == 'matcha_latte' or cmd == 'dirty_matcha':

			# Fallback if a drink was triggered before selecting a specific target type
			if self.cup_selection is None:
				self.cup_selection = 'cup1'
				self.get_logger().info("No cup selection specified. Defaulting to cup_1 tracking.")

			# COMBINE BOTH: Query YOLO data to find where the specific requested cup is sitting
			detected_side = self.find_physical_side()
			
			# Fallback if camera stream is offline or the target is obscured
			if detected_side is None:
				self.get_logger().warning(f"YOLO could not find {self.cup_selection}! Using default layout mapping.")
				detected_side = "Right" if self.cup_selection == 'cup_1' else "Left"

			self.get_logger().info(f"Proceeding with detected side for {self.cup_selection}: {detected_side}")	
			
			self.publish_status('KopiKia:getting cup')
			if ARMPresent:
				if detected_side == 'Right':
					ArmToRightCup(self.arm, 15, False, True, ArmToRightCup_list)

				elif detected_side == 'Left':
					ArmToLeftCup(self.arm, 15, False, True, ArmToLeftCup_list)

			else:		
				time.sleep(5)
		
			self.publish_status('KopiKia:cup acquired')
			if ARMPresent:
				if detected_side == 'Right':
					ArmLiftRightCup(self.arm, 15, False, True, ArmLiftRightCup_list)

				elif detected_side == 'Left':
					ArmLiftLeftCup(self.arm, 15, False, True, ArmLiftLeftCup_list)
				else:	
					time.sleep(5)
			else:		
				time.sleep(5)
		
			self.publish_status('KopiKia:position cup')
			if ARMPresent:
				if detected_side == 'Right':
					Cup1ToAlign(self.arm, 15, False, True, Cup1ToAlign_list)
				elif detected_side == 'Left':
					Cup2ToAlign(self.arm, 15, False, True, Cup2ToAlign_list)
				else:
					time.sleep(5)	
			else:
				time.sleep(5)
		
			self.publish_status('KopiKia:cup aligned')
			if ARMPresent:
				if detected_side == 'Right':
					Cup1Adjust(self.arm, 15, False, True, Cup1Adjust_list)
					GripperControl(self.arm, "open")
					Cup1Release(self.arm, 15, False, True, Cup1Release_list)
					GripperControl(self.arm, "close")
					Cup1ToHome(self.arm, 15, False, True, Cup1ToHome_list)

				elif detected_side == 'Left':
					Cup2Adjust(self.arm, 15, False, True, Cup2Adjust_list)			
					GripperControl(self.arm, "open")
					Cup2Release(self.arm, 15, False, True, Cup2Release_list)
					GripperControl(self.arm, "close")
					Cup2ToHome(self.arm, 15, False, True, Cup2ToHome_list)			
			else:
				time.sleep(5)
	
			self.publish_status('KopiKia:select drink')
			if ARMPresent:
				ArmToScreen(self.arm, 15, False, True, ArmToScreen_list)
				if cmd == 'latte':
					ArmSelectDrink(self.arm, 15, False, True, ArmLatteOnScreen_list)
					ArmSelectDrink(self.arm, 15, False, True, ArmLatteOffScreen_list)
				
				elif cmd == 'cappuccino':
					ArmSelectDrink(self.arm, 15, False, True, ArmCappuccinoOnScreen_list)
					ArmSelectDrink(self.arm, 15, False, True, ArmCappuccinoOffScreen_list)
				
				elif cmd == 'milo':
					ArmSelectDrink(self.arm, 15, False, True, ArmMiloOnScreen_list)
					ArmSelectDrink(self.arm, 15, False, True, ArmMiloOffScreen_list)

				elif cmd == 'milo_mocha':
					ArmSelectDrink(self.arm, 15, False, True, ArmMochaOnScreen_list)
					ArmSelectDrink(self.arm, 15, False, True, ArmMochaOffScreen_list)	

				elif cmd == 'salted_caramel_latte':
					ArmSelectDrink(self.arm, 15, False, True, ArmSaltedCaramelOnScreen_list)
					ArmSelectDrink(self.arm, 15, False, True, ArmSaltedCaramelOffScreen_list)	

				elif cmd == 'matcha_latte':
					ArmSelectDrink(self.arm, 15, False, True, ArmMatchaOnScreen_list)
					ArmSelectDrink(self.arm, 15, False, True, ArmMatchaOffScreen_list)

				elif cmd == 'dirty_matcha':
					ArmSelectDrink(self.arm, 15, False, True, ArmDirtyOnScreen_list)
					ArmSelectDrink(self.arm, 15, False, True, ArmDirtyOffScreen_list)	

				elif cmd == 'espresso':
					ArmSelectDrink(self.arm, 15, False, True, ArmEspressoOnScreen_list)
					ArmSelectDrink(self.arm, 15, False, True, ArmEspressoOffScreen_list)

				elif cmd == 'americano':
					ArmSelectDrink(self.arm, 15, False, True, ArmAmericanoOnScreen_list)
					ArmSelectDrink(self.arm, 15, False, True, ArmAmericanoOffScreen_list)
						
				else:
					time.sleep(5)

			else:
				time.sleep(5)

			self.publish_status('KopiKia:drink started')
			if ARMPresent:
				HomeToReady(self.arm, 15, False, True, HomeToReady_list)
			else:	
				time.sleep(5)

			self.publish_status('KopiKia:drink ready')
			time.sleep(5)
			self.publish_status('KopiKia:grap cup')
			if ARMPresent:
				if detected_side == 'Right':
					GripperControl(self.arm, "open")
					Cup1ReleaseReverse(self.arm, 15, False, True, Cup1ReleaseReverse_list)
					Cup1AdjustReverse(self.arm, 15, False, True, Cup1AdjustReverse_list)
					GripperControl(self.arm, "close")

				elif detected_side == 'Left':
					GripperControl(self.arm, "open")
					Cup2ReleaseReverse(self.arm, 15, False, True, Cup2ReleaseReverse_list)
					Cup2AdjustReverse(self.arm, 15, False, True, Cup2AdjustReverse_list)
					GripperControl(self.arm, "close")


				else:
					time.sleep(5)
			time.sleep(5)
			self.publish_status('KopiKia:cup transition')
			if ARMPresent:
				if detected_side == 'Right':
					Cup1ToAlign(self.arm, 15, False, True, Cup1ToAlignReverse_list)
					ArmLiftRightCup(self.arm, 15, False, True, ARmLiftRightCupReverse_list)

				elif detected_side == 'Left':
					Cup2ToAlign(self.arm, 15, False, True, Cup2ToAlignReverse_list)
					ArmLiftLeftCup(self.arm, 15, False, True, ArmLiftLeftCupReverse_list)

				else:
					time.sleep(5)

			self.publish_status('KopiKia:serve cup')
			time.sleep(5)
			if ARMPresent:	
				if detected_side == 'Right':
					GripperControl(self.arm, "open")
					ArmToRelease(self.arm, 15, False, True, ArmToCup1Release_list)
					GripperControl(self.arm, "close")

				elif detected_side == 'Left':
					GripperControl(self.arm, "open")
					ArmToRelease(self.arm, 15, False, True, ArmToCup2Release_list)
					GripperControl(self.arm, "close")

			self.publish_status('KopiKia:returned home')


def main():
	sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
	#######################################################
	"""
	Just for test example
	"""
	if len(sys.argv) >= 2:
		ip = sys.argv[1]
	else:
		try:
			from configparser import ConfigParser
			parser = ConfigParser()
			parser.read('../robot.conf')
			ip = parser.get('xArm', 'ip')
		except:
			ip = '192.168.1.223'
			if not ip:
				print('input error, exit')
				sys.exit(1)
	########################################################

	
	if ARMPresent:
		arm = XArmAPI(ip)
		arm.motion_enable(enable=True)
		arm.set_mode(0)
		arm.set_state(state=0)

	# If run with `--ros`, start ROS2 node to publish/subscribe
	if '--ros' in sys.argv:
		rclpy.init()
		# Pass the initialized arm instance to the ROS node
		arm_instance = arm if ARMPresent else None
		node = ArmROSNode(arm_instance)
		try:
			rclpy.spin(node)
		except KeyboardInterrupt:
			pass
		finally:
			node.destroy_node()
			rclpy.shutdown()
		return

	#if ARMPresent:
	#	HomeToReady(arm, 15, False, True, HomeToReady_list)
	#	HomeToCup(arm, 15, False, True, HomeToCup_list)
	#	CupToAlign(arm, 15, False, True, CupToAlign_list)   
	#	CupToCoffee(arm, 15, False, True, CupToCoffee_list)	 
	#	CupToAlign(arm, 15, False, True, CupToAlign_list)
	#	CoffeeToScreen(arm, 15, False, True, CoffeeToScreen_list)
	#	CupToAlign(arm, 15, False, True, CupToAlign_list)
	#	CupToCoffee(arm, 15, False, True, CupToCoffee_list)	 
	#	CoffeeToReady(arm, 15, False, True, CoffeeToReady_list)	 
	#	HomeToReady(arm, 15, False, True, HomeToReady_list)
	#	CoffeeToServe(arm, 15, False, True, CoffeeToServe_list)
	#	HomeToReady(arm, 15, False, True, HomeToReady_list)

if __name__ == '__main__':
	main()
