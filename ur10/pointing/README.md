# Development instructions

These instructions are meant to help run the demo in simulation or an a real
robot.

## Before running the demo on the real robot

1. Turn the robot on, click on the red button in the lower left part of the
   tablet, click on "ON", verify that the two first steps on the screen turn
   green. Click on "START". The remaining states should turn green.
2. Load the file ros.urp on the tablet.
3. Verify that the robot is in the home position. The robot can automatically
   move to the position by entering "Home" and hold the button
   "Move robot to New Position".
   Sometime,the robot will go the protective state to prevent collision.
   In that case, rotate the wrist to a safe state and try again.
4. In the Installation tab, check the Safety => Robot Limits section to ensure
   the robot is in the least restricted conifiguration.
5. All the terminals should begin with

```bash
source /root/catkin_ws/ur10_robot.sh
```
to point the ROS_MASTER_URI, HPP_HOST, ROS_IP to the right configuration.
6. The computer connected to robot should have the Ethernet configuration as following
    IPv4 addr: 192.168.56.1
    Netmask  : 255.255.255.0
    Gateway  : 192.168.56.1

## Steps to run the demo


Open several tabs in a terminal, go to directory
`/root/catkin_ws/src/agimus-demos/ur10/pointing` and type the following
instructions

1. in terminal 1
```bash
hppcorbaserver
```

2. in terminal 2
```bash
ipython -i script_hpp.py
```

3. in terminal 3
```bash
source /root/setup_ld.sh
gepetto-gui
```

### Generate a trajectory from the initial configuration

4. in terminal 4

To run the simulation:
```bash
roslaunch ./simulation.launch
```

To run the robot instead:
```bash
roslaunch ur_robot_driver ur10e_bringup.launch robot_ip:=192.168.56.5 robot_description_file:=/root/catkin_ws/install/share/agimus_demos/launch/ur10_pointing_load_ur10e.launch
```

After ROS is launched successfully, press the "play" icon in the tablet
and select "Play from beginning Robot Program". In the terminal you should
read
```bash
[ INFO] [1634638700.530389390]: Robot connected to reverse interface. Ready to receive control commands.
```

5. in terminal 2
```python
from tools_hpp import ConfigGenerator, RosInterface

ri = RosInterface(robot)
cg = ConfigGenerator(graph)
q_init = ri.getCurrentConfig(q0)
res = False
while not res:
    res, q_goal, qg = cg.generateValidConfigForHandle('part/handle_0', q0)

ps.setInitialConfig(q_init)
ps.addGoalConfig(q_goal)
ps.solve()
```

6. in terminal 5
```bash
roslaunch ./demo.launch
```
On the robot, after the file is run, the robot should have a lock sound of the joint.

7. in terminal 6
``` bash
rostopic pub /hpp/target/position dynamic_graph_bridge_msgs/Vector [0,0,0,0,0,0]
```

8. in terminal 7
``` bash
rostopic pub /hpp/target/velocity dynamic_graph_bridge_msgs/Vector [0,0,0,0,0,0]
```

9. in terminal 8
```bash
rosrun dynamic_graph_bridge run_command
```
then
```python
from dynamic_graph.sot.core.task import Task
from dynamic_graph.sot.core.feature_posture import FeaturePosture
from dynamic_graph.sot.universal_robot.sot_universal_robot_device \
    import DeviceUniversalRobot

supervisor.sots["Loop | f"].sot.setMaxControlIncrementSquaredNorm(1e8)
robot.initializeTracer()
robot.tracer.setBufferSize(2**24)
robot.addTrace('___posture_task', 'controlGain')
robot.addTrace('___posture_task', 'task')
robot.addTrace('___posture_task', 'error')
robot.addTrace('___posture_feature_', 'error')
robot.addTrace('___posture_feature_','posture')
robot.addTrace('___posture_feature_','postureDot')
robot.addTrace('___posture_feature_','state')
robot.addTrace('ros_queued_subscribe', 'posture')
robot.addTrace('UniversalRobot', 'state')
robot.addTrace('UniversalRobot', 'robotState')
robot.addTrace('UniversalRobot', 'control')
robot.addTrace('ur_dynamic', 'position')

robot.startTracer()
```


10. in terminal 6
stop rostopic pub commands in terminal 6 and 7, then
```bash
rosrun agimus rqt_path_execution 
```
then select path 2 and type execute path.

11. in terminal 8, once the path is executed;
```
python
robot.stopTracer()
```