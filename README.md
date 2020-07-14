# MacBot // McMaster's MacBot ROS Stack

### macbot_description
Contains RViz configuration files, URDFs, and meshes. Textured and textureless variants. Textureless variant does not have sensors attached. 

### macbot_gazebo
Package for Gazebo Simulations. Contains world and their model files. Script for killall Gazebo launch. 
* default.launch - Main launch file for launching Gazebo and RViz
    - model: robot_textured (default), robot_texturesless
    - world: empty (default), maze, contact_stability
    - rviz_config: sensors (default), mapping, navigation, robot
* teleop.launch - Keyboard teleop controls for driving the robot around

```
roslaunch macbot_gazebo default.launch world:= maze rviz_config:=navigation
```

### macbot_navigation
Navigation package utilizing ROS navigation stack. Contains configuration / parameter files for move_base package and maps.
* amcl.launch
* gmap.launch
* localization.launch