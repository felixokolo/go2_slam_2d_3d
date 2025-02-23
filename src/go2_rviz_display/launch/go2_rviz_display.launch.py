from launch import LaunchDescription
from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import Command, LaunchConfiguration
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():

    go2_rviz_display_shared = get_package_share_directory("go2_rviz_display")
    lio_sam_pkg_share = FindPackageShare(package='lio_sam').find('lio_sam')
    urdf_file_path = os.path.join(go2_rviz_display_shared,
                                  'urdf', 'go2_description.urdf')
    hesai_lidar_pkg_share = FindPackageShare(package='hesai_lidar').find('hesai_lidar')
    scanner_arg = DeclareLaunchArgument(
            name='scanner', default_value='',
            description='Namespace for sample topics'
        )
    with open(urdf_file_path, 'r') as infp:
        robot_desc = infp.read()

    robot_state_pub = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'use_sim_time': False, 'robot_description': robot_desc}],
        arguments=[urdf_file_path])
    
    go2_joints_pub = Node(
        package='go2_rviz_display',
        executable='go2_rviz_display_node',
        name='go2_rviz_display'
    )

    hesai_lidar_launch_include = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(hesai_lidar_pkg_share, 'launch/hesai_lidar_launch.py')
        )
    )

    joints_state_node = Node(
        package='go2_joints_state_publisher',
        executable='go2_joints_state_publisher_node',
        name='go2_joints_state_publisher'
    )

    pointcloud_to_laserscan_node2 = Node(
        package='pointcloud_to_laserscan', executable='pointcloud_to_laserscan_node',
        remappings=[('cloud_in', [LaunchConfiguration(variable_name='scanner'), '/rslidar_points']),
                    ('scan', [LaunchConfiguration(variable_name='scanner'), '/scan'])],
        parameters=[{
            'target_frame': 'rslidar',
            'transform_tolerance': 0.01,
            'min_height': -0.3,
            'max_height': 3.0,
            'angle_min': -3.142, #-1.5708,  # -M_PI/2
            'angle_max': 3.142, #1.5708,  # M_PI/2
            'angle_increment': 0.003141593, #0.0087,  # M_PI/360.0
            'scan_time': 0.1, #0.3333,
            'range_min': 0.1,
            'range_max': 8.0,
            'use_inf': False,
            'inf_epsilon': 1.0
        }],
        name='pointcloud_to_laserscan_rslidar'
    )

    odom_to_tf_node = Node(
        package='odom_to_tf_ros2',
        executable='odom_to_tf',
        name='odom_to_tf',
        #parameters=[odom_to_tf_params_file]
    )

    lio_sam_launch_include = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(lio_sam_pkg_share, 'launch/run.launch.py')
        )
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', [os.path.join(go2_rviz_display_shared, 'rviz', 'go2_rviz_config.rviz')]]
        )
    

    return LaunchDescription([
        scanner_arg,
        go2_joints_pub,
        robot_state_pub,
        pointcloud_to_laserscan_node2,
        odom_to_tf_node,
        joints_state_node,
        # hesai_lidar_launch_include, # Uncomment when using pointcloud from HESAI Lidar
        lio_sam_launch_include,
        rviz_node
    ])