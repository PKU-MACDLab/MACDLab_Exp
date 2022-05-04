# Install script for directory: /home/ica/MACDLab_Exp/ros_ws/src/ugv_ros

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/ica/MACDLab_Exp/ros_ws/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/ugv_ros/msg" TYPE FILE FILES "/home/ica/MACDLab_Exp/ros_ws/src/ugv_ros/msg/xyyaw_pose.msg")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/ugv_ros/srv" TYPE FILE FILES
    "/home/ica/MACDLab_Exp/ros_ws/src/ugv_ros/srv/GoTo.srv"
    "/home/ica/MACDLab_Exp/ros_ws/src/ugv_ros/srv/Stop.srv"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/ugv_ros/action" TYPE FILE FILES
    "/home/ica/MACDLab_Exp/ros_ws/src/ugv_ros/action/GoTo.action"
    "/home/ica/MACDLab_Exp/ros_ws/src/ugv_ros/action/Stop.action"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/ugv_ros/msg" TYPE FILE FILES
    "/home/ica/MACDLab_Exp/ros_ws/devel/share/ugv_ros/msg/GoToAction.msg"
    "/home/ica/MACDLab_Exp/ros_ws/devel/share/ugv_ros/msg/GoToActionGoal.msg"
    "/home/ica/MACDLab_Exp/ros_ws/devel/share/ugv_ros/msg/GoToActionResult.msg"
    "/home/ica/MACDLab_Exp/ros_ws/devel/share/ugv_ros/msg/GoToActionFeedback.msg"
    "/home/ica/MACDLab_Exp/ros_ws/devel/share/ugv_ros/msg/GoToGoal.msg"
    "/home/ica/MACDLab_Exp/ros_ws/devel/share/ugv_ros/msg/GoToResult.msg"
    "/home/ica/MACDLab_Exp/ros_ws/devel/share/ugv_ros/msg/GoToFeedback.msg"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/ugv_ros/msg" TYPE FILE FILES
    "/home/ica/MACDLab_Exp/ros_ws/devel/share/ugv_ros/msg/StopAction.msg"
    "/home/ica/MACDLab_Exp/ros_ws/devel/share/ugv_ros/msg/StopActionGoal.msg"
    "/home/ica/MACDLab_Exp/ros_ws/devel/share/ugv_ros/msg/StopActionResult.msg"
    "/home/ica/MACDLab_Exp/ros_ws/devel/share/ugv_ros/msg/StopActionFeedback.msg"
    "/home/ica/MACDLab_Exp/ros_ws/devel/share/ugv_ros/msg/StopGoal.msg"
    "/home/ica/MACDLab_Exp/ros_ws/devel/share/ugv_ros/msg/StopResult.msg"
    "/home/ica/MACDLab_Exp/ros_ws/devel/share/ugv_ros/msg/StopFeedback.msg"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/ugv_ros/cmake" TYPE FILE FILES "/home/ica/MACDLab_Exp/ros_ws/build/ugv_ros/catkin_generated/installspace/ugv_ros-msg-paths.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include" TYPE DIRECTORY FILES "/home/ica/MACDLab_Exp/ros_ws/devel/include/ugv_ros")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/roseus/ros" TYPE DIRECTORY FILES "/home/ica/MACDLab_Exp/ros_ws/devel/share/roseus/ros/ugv_ros")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/common-lisp/ros" TYPE DIRECTORY FILES "/home/ica/MACDLab_Exp/ros_ws/devel/share/common-lisp/ros/ugv_ros")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/gennodejs/ros" TYPE DIRECTORY FILES "/home/ica/MACDLab_Exp/ros_ws/devel/share/gennodejs/ros/ugv_ros")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  execute_process(COMMAND "/usr/bin/python3" -m compileall "/home/ica/MACDLab_Exp/ros_ws/devel/lib/python3/dist-packages/ugv_ros")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python3/dist-packages" TYPE DIRECTORY FILES "/home/ica/MACDLab_Exp/ros_ws/devel/lib/python3/dist-packages/ugv_ros")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/ica/MACDLab_Exp/ros_ws/build/ugv_ros/catkin_generated/installspace/ugv_ros.pc")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/ugv_ros/cmake" TYPE FILE FILES "/home/ica/MACDLab_Exp/ros_ws/build/ugv_ros/catkin_generated/installspace/ugv_ros-msg-extras.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/ugv_ros/cmake" TYPE FILE FILES
    "/home/ica/MACDLab_Exp/ros_ws/build/ugv_ros/catkin_generated/installspace/ugv_rosConfig.cmake"
    "/home/ica/MACDLab_Exp/ros_ws/build/ugv_ros/catkin_generated/installspace/ugv_rosConfig-version.cmake"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/ugv_ros" TYPE FILE FILES "/home/ica/MACDLab_Exp/ros_ws/src/ugv_ros/package.xml")
endif()

