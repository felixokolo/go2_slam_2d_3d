cmake_minimum_required(VERSION 3.5)
project(go2_joints_state_publisher)

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(unitree_go REQUIRED)
find_package(unitree_api REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(rosidl_default_runtime REQUIRED)
find_package(trajectory_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)


# Include directories
include_directories(
  include
  ${rclcpp_INCLUDE_DIRS}
  ${std_msgs_INCLUDE_DIRS}
  ${unitree_go_INCLUDE_DIRS}
  
)
link_directories(src)

# Library
add_library(${PROJECT_NAME}
  src/Go2JointStatePublisher.cpp
  src/motor_crc.cpp
)

ament_target_dependencies(${PROJECT_NAME}
  rclcpp
  std_msgs
  unitree_go
  unitree_api
  trajectory_msgs
  sensor_msgs
)

# Executable
add_executable(${PROJECT_NAME}_node src/${PROJECT_NAME}_node.cpp)


target_link_libraries(${PROJECT_NAME}_node
  ${PROJECT_NAME}
)

ament_target_dependencies(${PROJECT_NAME}_node
  rclcpp
  std_msgs
  unitree_go
  unitree_api
  trajectory_msgs
)

# Install
install(TARGETS
  ${PROJECT_NAME}
  ${PROJECT_NAME}_node
  DESTINATION lib/${PROJECT_NAME}
)

install(DIRECTORY include/
  DESTINATION include/
)

install(DIRECTORY
DESTINATION share/${PROJECT_NAME}
)

ament_package()
