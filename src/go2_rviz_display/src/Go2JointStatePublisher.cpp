#include "Go2JointStatePublisher.h"


Go2JointStatePublisher::Go2JointStatePublisher(std::string nodeName)
: Node(nodeName), // clock(RCL_ROS_TIME)
  steady_clock(RCL_STEADY_TIME)
{
    lowState_sub = this->create_subscription<unitree_go::msg::LowState>(
        lowStateTopic, 10, std::bind(&Go2JointStatePublisher::lowStateCallback, this, std::placeholders::_1));

    
    jointsState_pub = this->create_publisher<sensor_msgs::msg::JointState>(jointsStateTopic, 500);

    jointState.name.resize(NUM_OF_JOINTS);     // Names of the joints
    jointState.position.resize(NUM_OF_JOINTS); // Joint positions

    freqDivCount = 0;
    clock_ptr = this->get_clock();

    for (size_t i = 0; i < NUM_OF_JOINTS; ++i)
    { 
        jointState.name[i] = jointNames[i];
        jointState.position[i] = 0.0;
    }

    // Publish initial transforms
    this->publishJointsState();

}

void Go2JointStatePublisher::publishJointsState()
{

    jointState.header.stamp.sec = sec;
    jointState.header.stamp.nanosec = nanosec;

    jointsState_pub->publish(jointState); 
}

void Go2JointStatePublisher::lowStateCallback(const unitree_go::msg::LowState::SharedPtr msg)
{
    ++freqDivCount;

    if (freqDivCount < FREQ_DIV)
        return;

    for (int i = 0; i < NUM_OF_JOINTS; i++)
        jointState.position[i] = msg->motor_state[i].q;

    rclcpp::Time now = clock_ptr->now();
    sec = now.seconds();
    nanosec = now.nanoseconds() % 1000000000; // get only the nano seconds part of the returned value
    publishJointsState();
    freqDivCount = 0;
}
