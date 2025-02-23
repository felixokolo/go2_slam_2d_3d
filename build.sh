colcon build --packages-select go2_joints_state_publisher --cmake-args -DCMAKE_BUILD_TYPE=Release
colcon build --packages-select go2_rviz_display
colcon build --packages-select pointcloud_to_laserscan --cmake-args -DCMAKE_BUILD_TYPE=Release
colcon build --packages-select odom_to_tf_ros2 --cmake-args -DCMAKE_BUILD_TYPE=Release
colcon build --packages-select lio_sam