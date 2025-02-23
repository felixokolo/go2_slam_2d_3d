# SLAM setup for unitree GO2 robot

## Overview

This setup contains all necessary ROS2 nodes to run and visualize ascynchronous SLAM from the SLAM_toolbox. It contains the following nodes;
1. go2_joint_state_publisher - Subscribes to the /lowstate topic from the go2 robot and republishes it to the /joint_states topic for the robot_state_publisher node.

2. go2_rviz_display - Setup all necessary nodes for the visualization of the GO2 robot on RViz.
3. HesaiLidar_General_ROS - Cloned from the [Hesai git repo](https://github.com/HesaiTechnology/HesaiLidar_General_ROS)
4. odom_to_tf_ros2 - Modified from the [gstavrinos repo](https://github.com/gstavrinos/odom_to_tf_ros2). Subscribes to /dog_odom provided by dog_control node included in unitree's [Expansion Dock Module](https://unitree-firmware.oss-cn-hangzhou.aliyuncs.com/tool/GO2_SLAM20240920.zip).
5. pointcloud_to_laserscan - Modified from [DiegoCarvajal98 pointcloud_to_laserscan repo](https://github.com/ros-perception/pointcloud_to_laserscan)
6. LIO-SAM-ros2 - Modified from [robot mania Creating a Point Cloud Using LIO-SAM with ROS2 and Gazebo](https://www.youtube.com/watch?v=NNR9RUNz5Pg)

## Installation

To get started with the Go2 SLAM, follow these steps:

### Prerequisites

- [ROS2 foxx (Robot Operating System 2)](https://docs.ros.org/en/foxy/Installation.html)
- [Unitree_ros2](https://github.com/unitreerobotics/unitree_ros2)
- Git

### Clone the Repository

```bash
git clone https://github.com/felixokolo/go2_slam_2d_3d
```

### Build
```bash
cd go2_slam_2d_3d
sudo chmod +x build.sh
source /opt/ros/foxy/setup.bash
source ~/unitree_ros2/cyclonedds_ws/install/setup.bash # Change according to your installation path
./build.sh
```

### Launch
```bash
# In the project directory
source /opt/ros/foxy/setup.bash
ros2 launch go2_rviz_display go2_rviz_display.launch.py
```