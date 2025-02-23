cmake_minimum_required(VERSION 3.5)
project(go2_rviz_display)

# Default to C99
if(NOT CMAKE_C_STANDARD)
  set(CMAKE_C_STANDARD 99)
endif()

# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(unitree_go REQUIRED)
find_package(unitree_api REQUIRED)
find_package(sensor_msgs REQUIRED)

include_directories(
  include
  ${rclcpp_INCLUDE_DIRS}
  ${std_msgs_INCLUDE_DIRS}
  ${unitree_go_INCLUDE_DIRS}
  ${unitree_api_INCLUDE_DIRS}
  ${sensor_msgs_INCLUDE_DIRS}
)

link_directories(src)


add_library(${PROJECT_NAME}
  src/Go2JointStatePublisher.cpp
  src/motor_crc.cpp
)

ament_target_dependencies(${PROJECT_NAME}
  rclcpp
  std_msgs
  unitree_go
  unitree_api
  sensor_msgs
)

# Executable
add_executable(${PROJECT_NAME}_node src/go2_joints_state_publisher_node)


target_link_libraries(${PROJECT_NAME}_node
  ${PROJECT_NAME}
)

ament_target_dependencies(${PROJECT_NAME}_node
  rclcpp
  std_msgs
  unitree_go
  unitree_api
  sensor_msgs
)

# Install
install(TARGETS
  ${PROJECT_NAME}
  ${PROJECT_NAME}_node
  DESTINATION lib/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # uncomment the line when a copyright and license is not present in all source files
  #set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # uncomment the line when this package is not in a git repo
  #set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

install(
  DIRECTORY launch urdf dae rviz
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
