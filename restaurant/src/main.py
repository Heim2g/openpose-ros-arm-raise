#!/usr/bin/env python
import time
import rospy
import roslib
from std_msgs.msg import Int16, Bool, String
from geometry_msgs.msg import Twist
from sound_play.libsoundplay import SoundClient
from tfpose_ros.msg import Persons, Person, BodyPartElm

Nose = 0
Neck = 1
RShoulder = 2
RElbow = 3
RWrist = 4
LShoulder = 5
LElbow = 6
LWrist = 7
RHip = 8
RKnee = 9
RAnkle = 10
LHip = 11
LKnee = 12
LAnkle = 13
REye = 14
LEye = 15
REar = 16
LEar = 17
Background = 18

number_of_person = 0
detected_person = Person()
body_part = BodyPartElm()
minimun_person = 0
maximun_person = 0

person_pose = [0,[0,0,0],[0,0,0],[0,0,0]]
# first is person number : second is wrist, third is elbow, shoulder
sentence=""
def raise_hand(wrist_y, elbow_y, person_number):
	if wrist_y < elbow_y:
		rospy.loginfo(str(wrist_y) + " and " + str(elbow_y))
		rospy.loginfo(str(person_number) + " is raising his hand")
		return True
emergency = False
class arduino_f:
	def run(self):
		arduino_pub = rospy.Subscriber('/pushed', Person ,self.function)
		
	def function(msg):
		emergency  = msg.data
		

def func(msg):
	#rospy.loginfo("sdfhv")
	detected_person = msg
	body_part = detected_person.body_part
	person_pose[0] = detected_person.person_number
	#rospy.loginfo(len(body_part))
	for k in range(len(body_part)) :
		#rospy.loginfo(detected_person.body_part[k].part_id)
		if detected_person.body_part[k].part_id == RWrist:
			if detected_person.body_part[k].part_id >= 0.7:
				person_pose[1][0] = detected_person.body_part[k].x
				person_pose[1][1] = detected_person.body_part[k].y
			
			
		elif detected_person.body_part[k].part_id == RElbow:
			if detected_person.body_part[k].part_id >= 0.7:
				person_pose[2][0] = detected_person.body_part[k].x
				person_pose[2][1] = detected_person.body_part[k].y
			
			
		elif detected_person.body_part[k].part_id == RShoulder:
			if detected_person.body_part[k].part_id >= 0.7:
				person_pose[3][0] = detected_person.body_part[k].x
				person_pose[3][1] = detected_person.body_part[k].y
	pub = rospy.Publisher('cmd_vel_mux/input/teleop', Twist, queue_size=5)
	
	twist = Twist()
	#rospy.loginfo(raise_hand(person_pose[1][1],person_pose[2][1],person_pose[0]))
	rospy.loginfo(emergency)
	if emergency:
		twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
		pub.publish(twist)
	else:
		if raise_hand(person_pose[1][1],person_pose[2][1],person_pose[0]):
			
			if person_pose[3][0] < 0.5 and person_pose[3][0] > 0.4:
				twist.linear.x = 0.2; twist.linear.y = 0; twist.linear.z = 0
			elif person_pose[3][0] > 0.5 :
				twist.linear.x = 0.2; twist.linear.y = 0; twist.linear.z = -0.4
			elif person_pose[3][0] < 0.4 :
				twist.linear.x = 0.2; twist.linear.y = 0; twist.linear.z = 0.4
			rospy.loginfo("published")
			pub.publish(twist)
		
		

	
		
	
	


if __name__ == "__main__":
	#init_all()
	
	rospy.init_node('restaurant', anonymous=True)
	rospy.loginfo("started")
	
	rospy.sleep(5)
	emer_button = arduino_f()
	emer_button.run()
	person = rospy.Subscriber('/pose_estimator/pose_body', Person ,func)
	
	rospy.loginfo("started subscribe")

	
	rospy.spin()
