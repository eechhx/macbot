# MacBot - McMaster's Autonomous Robot ROS Stack

### If you are looking for detailed documentation, **[check the Wiki](https://github.com/eechhx/macbot/wiki)**.

![macbot_rviz](mbot_rviz.png)


## macbot_description
Contains RViz configuration files, URDFs, and meshes. Textured and textureless variants. Textureless variant does not have sensors attached. 



## macbot_gazebo
Package for Gazebo Simulations. Contains world and their model files. Script for killall Gazebo launch.

**Models**
* maze
* maze_short_textured
* maze_textured

**Launch**
* default.launch - Main launch file for launching Gazebo and RViz
    - `model` (default: `robot_textured`), `robot_texturesless`
    - `world` (default: `empty`), `maze`, `contact_stability`
    - `rviz_config` (default: `sensors`), `mapping`, `navigation`, `robot`
* teleop.launch - Keyboard teleop controls for driving the robot around

```
roslaunch macbot_gazebo default.launch world:=maze rviz_config:=navigation
```



## macbot_navigation
Navigation package utilizing ROS navigation stack. Contains configuration / parameter files for move_base package and maps. Launch files with `_macbot` are specific for the actual robot. The ones without are used for Gazebo simulated environments.

**Maps**
* `enviro` (mapped environment from ydlidar)
* `gmap_map` (maze)

**Launch**
* amcl_macbot.launch
    - `map_arg` (default: `enviro`)
* amcl.launch
    - `map_arg` (default: `gmap_map`)
* gmap_macbot.launch
* gmap.launch
* localization.launch
    - `map_arg` (default: `gmap_map`)


## macbot_physical
Physical package for interfacing with the MacBot. 

**Launch**
* diff_drive.launch - diff_drive node required for driving MacBot.

**Nodes**
* macbot_node.py - Communicating with the various nodes on the CAN bus.
* tf_broadcaster.py - Broadcasting the transforms of the left and right motorized wheels. 



## macbot_sensors
Package for launching one of the various sensors on the MacBot. 

**Launch**
* camera.launch - Intel RealSense
* lidar.launch - ydlidar
    - `pub_tf` (default: `false`) - Publishes the TF link between `odom` and `base_link`.
* sensors.launch - Launch all sensors

**Nodes**
* pose_odom.py - Publishes `nav_msgs/Odometry` messages from `geometry_msgs/PoseStamped` messages outputted by [laser_scan_matcher](http://wiki.ros.org/laser_scan_matcher) 