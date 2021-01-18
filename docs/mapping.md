# Mapping

## Simulation (gmapping)
To map solely in the Gazebo simulation, specify the world argument in the following launch command:

```
roslaunch macbot_gazebo default.launch world:=maze rviz_config:=mapping
```

In a separate tab, start the gmapping node so that can begin to build the map:

```
roslaunch macbot_navigation gmap.launch
```

To drive the robot in simulation with teleop, launch the following in the third tab:

```
roslaunch macbot_gazebo teleop.launch
```

When you're done mapping, save your map with the following command:
```
rosrun map_server map_saver -f ~/catkin_ws/src/macbot_navigation/map/mapname
```