# Cartographer + Gazebo Mapping & Localization Guide

This guide explains how to:

* Build with `catkin_make_isolated`
* Spawn robot in Gazebo
* Control robot & arm
* Create map using Cartographer
* Save `.pbstream`
* Convert to ROS map
* Run localization

---

# 1. Build Workspace (catkin_make_isolated)

Since `cartographer_ros` uses **catkin_make_isolated**, the entire workspace must use it.

After **any change** (config, launch, code):

```bash
catkin_ws_isolated --install
```

If you do NOT want to use `catkin_make_isolated`, you must:

* Split `cartographer_ros` into a **separate workspace**

---

# 2. Launch Gazebo Simulation

Start Gazebo with robot:

```bash
roslaunch my_robot_gazebo spawn_robot.launch
```

### Expected Result
Robot should appear in Gazebo world.

![Gazebo Robot](images/gazebo.png)

---

# 3. Manually Control Robot Arm

Run:

```bash
rosrun wheel_controllers change_joint.py 
```

Example joint values:

```
0.0,0.0,1.7,0.0,-1.3,0.0,0.0,0.0,0.0,0.0
```

### Expected Result

Robot arm moves to configured pose.

![Arm Control](images/02_arm_control.png)

---

# 4. Create Map using Cartographer

### Start Teleop Control

```bash
rosrun wheel_controllers cmd_vel_remote.py
```

Use this to **manually drive robot** for mapping.

![Teleop Movement](images/03_teleop.png)

---

### Record Data

At the same time:

```bash
rosbag record -a
```

This records all topics during mapping.

![Rosbag Recording](images/04_rosbag.png)

---

# 5. Save Cartographer Map (.pbstream)

After mapping finishes:

```bash
rosservice call /write_state "{filename: '$HOME/catkin_ws_base/src/maps/my_map.pbstream', include_unfinished_submaps: true}"
```

This saves:

```
my_map.pbstream
```

![PBStream Saved](images/05_pbstream.png)

---

# 6. Visualize Map

Launch:

```bash
roslaunch cartograph_ros backpack_2d.launch
```

This loads and visualizes the map.

![Cartographer Map](images/06_cartographer_map.png)

---

# 7. Convert pbstream → ROS Map

```bash
rosrun cartographer_ros cartographer_pbstream_to_ros_map \
  -pbstream_filename $HOME/catkin_ws_base/src/maps/my_map.pbstream \
  -map_filestem $HOME/catkin_ws_base/src/maps/my_map
```

This generates:

```
my_map.pgm
my_map.yaml
```

![Map Output](images/07_map_output.png)

---

# 8. Run Localization

Launch localization:

```bash
roslaunch wheel_controllers demo_backpack_2d_localization.launch
```

![Localization Launch](images/08_localization.png)

---

# 9. Set Initial Pose in RViz

You MUST manually set robot initial pose:

RViz → **2D Pose Estimate** → Click on map

![Initial Pose](images/09_initial_pose.png)

Robot should now localize correctly.

---

# Workflow Summary

1. Build workspace
2. Launch Gazebo
3. Control robot
4. Drive to create map
5. Save pbstream
6. Convert to ROS map
7. Launch localization
8. Set initial pose

---

# Output Files

```
maps/
 ├── my_map.pbstream
 ├── my_map.pgm
 └── my_map.yaml
```

---

# Notes

* Always rebuild using `catkin_make_isolated`
* Must set **initial pose** in RViz
* Use slow movement when mapping
* Ensure `/scan` topic is publishing

---
