# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "ugv_ros: 1 messages, 0 services")

set(MSG_I_FLAGS "-Iugv_ros:/home/ica/MACDLab_Exp/ros_ws/src/ugv_ros/msg;-Istd_msgs:/opt/ros/noetic/share/std_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(geneus REQUIRED)
find_package(genlisp REQUIRED)
find_package(gennodejs REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(ugv_ros_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/home/ica/MACDLab_Exp/ros_ws/src/ugv_ros/msg/xyyaw_pose.msg" NAME_WE)
add_custom_target(_ugv_ros_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "ugv_ros" "/home/ica/MACDLab_Exp/ros_ws/src/ugv_ros/msg/xyyaw_pose.msg" ""
)

#
#  langs = gencpp;geneus;genlisp;gennodejs;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(ugv_ros
  "/home/ica/MACDLab_Exp/ros_ws/src/ugv_ros/msg/xyyaw_pose.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/ugv_ros
)

### Generating Services

### Generating Module File
_generate_module_cpp(ugv_ros
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/ugv_ros
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(ugv_ros_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(ugv_ros_generate_messages ugv_ros_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/ica/MACDLab_Exp/ros_ws/src/ugv_ros/msg/xyyaw_pose.msg" NAME_WE)
add_dependencies(ugv_ros_generate_messages_cpp _ugv_ros_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(ugv_ros_gencpp)
add_dependencies(ugv_ros_gencpp ugv_ros_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS ugv_ros_generate_messages_cpp)

### Section generating for lang: geneus
### Generating Messages
_generate_msg_eus(ugv_ros
  "/home/ica/MACDLab_Exp/ros_ws/src/ugv_ros/msg/xyyaw_pose.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/ugv_ros
)

### Generating Services

### Generating Module File
_generate_module_eus(ugv_ros
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/ugv_ros
  "${ALL_GEN_OUTPUT_FILES_eus}"
)

add_custom_target(ugv_ros_generate_messages_eus
  DEPENDS ${ALL_GEN_OUTPUT_FILES_eus}
)
add_dependencies(ugv_ros_generate_messages ugv_ros_generate_messages_eus)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/ica/MACDLab_Exp/ros_ws/src/ugv_ros/msg/xyyaw_pose.msg" NAME_WE)
add_dependencies(ugv_ros_generate_messages_eus _ugv_ros_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(ugv_ros_geneus)
add_dependencies(ugv_ros_geneus ugv_ros_generate_messages_eus)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS ugv_ros_generate_messages_eus)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(ugv_ros
  "/home/ica/MACDLab_Exp/ros_ws/src/ugv_ros/msg/xyyaw_pose.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/ugv_ros
)

### Generating Services

### Generating Module File
_generate_module_lisp(ugv_ros
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/ugv_ros
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(ugv_ros_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(ugv_ros_generate_messages ugv_ros_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/ica/MACDLab_Exp/ros_ws/src/ugv_ros/msg/xyyaw_pose.msg" NAME_WE)
add_dependencies(ugv_ros_generate_messages_lisp _ugv_ros_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(ugv_ros_genlisp)
add_dependencies(ugv_ros_genlisp ugv_ros_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS ugv_ros_generate_messages_lisp)

### Section generating for lang: gennodejs
### Generating Messages
_generate_msg_nodejs(ugv_ros
  "/home/ica/MACDLab_Exp/ros_ws/src/ugv_ros/msg/xyyaw_pose.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/ugv_ros
)

### Generating Services

### Generating Module File
_generate_module_nodejs(ugv_ros
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/ugv_ros
  "${ALL_GEN_OUTPUT_FILES_nodejs}"
)

add_custom_target(ugv_ros_generate_messages_nodejs
  DEPENDS ${ALL_GEN_OUTPUT_FILES_nodejs}
)
add_dependencies(ugv_ros_generate_messages ugv_ros_generate_messages_nodejs)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/ica/MACDLab_Exp/ros_ws/src/ugv_ros/msg/xyyaw_pose.msg" NAME_WE)
add_dependencies(ugv_ros_generate_messages_nodejs _ugv_ros_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(ugv_ros_gennodejs)
add_dependencies(ugv_ros_gennodejs ugv_ros_generate_messages_nodejs)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS ugv_ros_generate_messages_nodejs)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(ugv_ros
  "/home/ica/MACDLab_Exp/ros_ws/src/ugv_ros/msg/xyyaw_pose.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/ugv_ros
)

### Generating Services

### Generating Module File
_generate_module_py(ugv_ros
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/ugv_ros
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(ugv_ros_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(ugv_ros_generate_messages ugv_ros_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/ica/MACDLab_Exp/ros_ws/src/ugv_ros/msg/xyyaw_pose.msg" NAME_WE)
add_dependencies(ugv_ros_generate_messages_py _ugv_ros_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(ugv_ros_genpy)
add_dependencies(ugv_ros_genpy ugv_ros_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS ugv_ros_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/ugv_ros)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/ugv_ros
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_cpp)
  add_dependencies(ugv_ros_generate_messages_cpp std_msgs_generate_messages_cpp)
endif()

if(geneus_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/ugv_ros)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/ugv_ros
    DESTINATION ${geneus_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_eus)
  add_dependencies(ugv_ros_generate_messages_eus std_msgs_generate_messages_eus)
endif()

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/ugv_ros)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/ugv_ros
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_lisp)
  add_dependencies(ugv_ros_generate_messages_lisp std_msgs_generate_messages_lisp)
endif()

if(gennodejs_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/ugv_ros)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/ugv_ros
    DESTINATION ${gennodejs_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_nodejs)
  add_dependencies(ugv_ros_generate_messages_nodejs std_msgs_generate_messages_nodejs)
endif()

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/ugv_ros)
  install(CODE "execute_process(COMMAND \"/usr/bin/python3\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/ugv_ros\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/ugv_ros
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_py)
  add_dependencies(ugv_ros_generate_messages_py std_msgs_generate_messages_py)
endif()
