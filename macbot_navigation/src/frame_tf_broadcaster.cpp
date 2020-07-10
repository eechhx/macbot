#include <ros/ros.h>
#include <tf/transform_listener.h>
#include <tf/transform_broadcaster.h>
#include <geometry_msgs/TransformStamped.h>
#include <geometry_msgs/Twist.h>
#include <ros/duration.h>

int main(int argc, char** argv) {
    ros::init(argc, argv, "tf_time");
    ros::NodeHandle node;

    tf::TransformListener listener;

    ros::Rate rate(10.0);
    while (node.ok()){
        tf::StampedTransform transform;
        try{


            // now = now - ros::Duration(0.01);

            // ros::Time tomorrow = ros::Time::now() + ros::Duration(60*60*60);
            // ros::spinOnce();

            ros::Time now = ros::Time::now();
            listener.waitForTransform("/odom", "/map",
                                (now+ros::Duration(1.0)), ros::Duration(10.0));
            listener.lookupTransform("/odom", "/map",
                                now, transform);
        }
        catch (tf::TransformException &ex) {
            ROS_ERROR("%s",ex.what());
            ros::Duration(1.0).sleep();
            continue;
        }
        rate.sleep();
    }

    return 0;
};

