sudo route add -net 239.255.42.99 netmask 255.255.255.255 eno1
source ros_ws/devel/setup.bash
roslaunch crazyswarm hover_swarm.launch
