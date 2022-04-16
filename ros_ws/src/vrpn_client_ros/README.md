#安装
mkdir vrpn
cd vrpn
git clone git://github.com/ros-drivers/vrpn_client_ros.git  #或者直接复制此安装包到/vrpn下
sudo apt-get install ros-noetic-vrpn-client-ros
catkin_make          #删除CmakeLists.txt和package.xml文件后再编译

#修改 launch/sample.launch文件
localhost 改为 169.254.0.223（Optitrack多播地址）

#使用
cd vrpn_client_ros
source devel/setup.bash
roslaunch launch/sample.launch

#看到Motive中定义的刚体
