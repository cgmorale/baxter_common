import xml.etree.ElementTree as ET

baxter_robot = ET.parse('baxter_robot.urdf')
baxter_moveit = ET.parse('baxter_moveit.urdf')

robot_root = baxter_robot.getroot()
moveit_root = baxter_moveit.getroot()

float_fields = ['radius',
'mass',
'value', 
'ix',
'ixx',
'ixy',
'ixz',
'iyy',
'iyz',
'izz',
'length']

for element in robot_root.iter():
	for key,value in element.attrib.iteritems():
		if key in float_fields:
			element.set(key, str(float(value)))
		else:
			element.set(key, value.strip())

robot_links = baxter_robot.findall('link')
robot_joints = baxter_robot.findall('joint')

moveit_links = baxter_moveit.findall('link')
moveit_joints = baxter_moveit.findall('joint')

for m_link in moveit_links:
	found = False
	for r_link in robot_links:
		if r_link.get('name') == m_link.get('name'):
			found = True
	if not found:
		robot_root.append(m_link)

for m_joint in moveit_joints:
	found = False
	for r_joint in robot_joints:
		if r_joint.get('name') == m_joint.get('name'):
			found = True
	if not found:
		robot_root.append(m_joint)

baxter_robot.write('baxter_combined.urdf')