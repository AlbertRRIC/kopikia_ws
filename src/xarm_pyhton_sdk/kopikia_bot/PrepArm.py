#!/usr/bin/env python3

"""
Description: functions to change tools
"""
import os
import sys
import time
import math
from xarm.wrapper import XArmAPI
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

ARMPresent = True

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

CupToAlign_list = [
			   [-2, 46.4, -38, -1.5, -95, 0],
			   #[-90, -25, -100, 0, 122, 0],
			   #[-90, -60, -30, 0, 90, 0]
			   ]

CupToCoffee_list = [
			   [0, 66.1, -93.1, -1.5, -58.8, 0],
			   #[-90, -25, -100, 0, 122, 0],
			   #[-90, -60, -30, 0, 90, 0]
			   ]

CoffeeToReady_list = [
			   [-0.2, 50.9, -50.5, 1.6, -90.1, -0.1],
			   #[-90, -25, -100, 0, 122, 0],
			   #[-90, -60, -30, 0, 90, 0]
			   ]

CoffeeToScreen_list = [
			   [-2.5, 9.4, -57.4, -1.5, -43.8, 0],
			   #[-90, -25, -100, 0, 122, 0],
			   #[-90, -60, -30, 0, 90, 0]
			   ]

CoffeeToServe_list = [
			   [31.2, 42.3, -44.1, 0, -90.4, 0],
			   #[-90, -25, -100, 0, 122, 0],
			   #[-90, -60, -30, 0, 90, 0]
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
		code = arm.set_gripper_position(500, wait=True)
	else:
		raise ValueError("Invalid state. Use 'close' or 'open'.")




def HomeToReady(arm, speed, is_radian, wait, angles_list=HomeToReady_list):
	GripperControl(arm, "open")
	time.sleep(0.1)
	for angles in angles_list:
		arm.set_servo_angle(angle=angles, speed=speed, is_radian=is_radian, wait=wait)

def HomeToCup(arm, speed, is_radian, wait, angles_list=HomeToCup_list):
	arm.set_mode(0)
	arm.set_state(0)   
	time.sleep(0.1)
	for angles in angles_list:
		arm.set_servo_angle(angle=angles, speed=speed, is_radian=is_radian, wait=wait)

def CupToAlign(arm, speed, is_radian, wait, angles_list=CupToAlign_list):
	arm.set_mode(0)
	arm.set_state(0)   
	time.sleep(0.1)
	for angles in angles_list:
		arm.set_servo_angle(angle=angles, speed=speed, is_radian=is_radian, wait=wait)

def CupToCoffee(arm, speed, is_radian, wait, angles_list=CupToCoffee_list):
	arm.set_mode(0)
	arm.set_state(0)   
	time.sleep(0.1)
	for angles in angles_list:
		arm.set_servo_angle(angle=angles, speed=speed, is_radian=is_radian, wait=wait)		

def CoffeeToScreen(arm, speed, is_radian, wait, angles_list=CoffeeToScreen_list):
	arm.set_mode(0)
	arm.set_state(0)   
	time.sleep(0.1)
	for angles in angles_list:
		arm.set_servo_angle(angle=angles, speed=speed, is_radian=is_radian, wait=wait)	

def CoffeeToReady(arm, speed, is_radian, wait, angles_list=CoffeeToReady_list):
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
		self.get_logger().info('ArmROSNode initialized')

	def publish_status(self, status: str):
		msg = String()
		msg.data = status
		self.status_pub.publish(msg)
		self.get_logger().info(f'Published status: {status}')

	def cmd_callback(self, msg: String):
		self.get_logger().info(f'Received command: {msg.data}')
		#if not self.arm:
		#	self.get_logger().warning('No arm instance available to execute commands')
		#	return
		cmd = msg.data.lower().strip()
		# Basic command handling - extend as needed
		if cmd == 'espresso' or cmd == 'americano' or cmd == 'latte' or cmd == 'cappuccino' or cmd == 'latte' \
			or cmd == 'milo' or cmd == 'milo_mocha' or cmd == 'salted_caramel_latte' or cmd == 'matcha_latte' or cmd == 'dirty_matcha':

			#HomeToReady(self.arm, 15, False, True, HomeToReady_list)
			self.publish_status('KopiKia:getting cup')
			time.sleep(5)
			self.publish_status('KopiKia:cup acquired')
			time.sleep(5)
			self.publish_status('KopiKia:position cup')
			time.sleep(5)
			self.publish_status('KopiKia:select drink')
			time.sleep(5)
			self.publish_status('KopiKia:drink started')
			time.sleep(5)
			self.publish_status('KopiKia:drink ready')
			time.sleep(5)
			self.publish_status('KopiKia:grap cup')
			time.sleep(5)
			self.publish_status('KopiKia:cup transition')
			time.sleep(5)
			self.publish_status('KopiKia:serve cup')
			time.sleep(5)
			HomeToReady(self.arm, 15, False, True, HomeToReady_list)
			self.publish_status('KopiKia:returned home')
		else:
			self.get_logger().info(f'Unknown command: {cmd}')
			self.publish_status(f'unknown:{cmd}')

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
