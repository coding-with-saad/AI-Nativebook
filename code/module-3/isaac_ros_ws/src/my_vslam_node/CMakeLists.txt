cmake_minimum_required(VERSION 3.8 FATAL_ERROR)
project(my_vslam_node)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)

add_executable(vslam_node src/vslam_node.cpp)
ament_target_dependencies(vslam_node rclcpp std_msgs sensor_msgs geometry_msgs)
install(TARGETS
  vslam_node
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
