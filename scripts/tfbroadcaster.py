#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

from nav_msgs.msg import Odometry
from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped

class OdomTimerFix(Node):
    
    def __init__(self):
        super().__init__('OdomTimerFix')
        self.publisher_ = self.create_publisher(Odometry, '/odom', 10)
        timer_period = 0.05  # seconds
        self.tf_broadcaster = TransformBroadcaster(self)
        

        self.subscription = self.create_subscription(
            Odometry,
            'robot_odom',
            self.subscriber_callback,
            10)
        self.subscription  #prevent unused variable warning

    def subscriber_callback(self,msg):
        newOdom = Odometry()
        newOdom = msg
        newOdom.header.stamp = self.get_clock().now().to_msg()
        self.publisher_.publish(newOdom)
        
        t = TransformStamped()
        t.header.frame_id = 'odom'
        t.child_frame_id = 'base_footprint'
        t.header.stamp = self.get_clock().now().to_msg()
        t.transform.translation.x = newOdom.pose.pose.position.x
        t.transform.translation.y = newOdom.pose.pose.position.y
        t.transform.translation.z = newOdom.pose.pose.position.z
        t.transform.rotation.x = newOdom.pose.pose.orientation.x
        t.transform.rotation.y = newOdom.pose.pose.orientation.y
        t.transform.rotation.z = newOdom.pose.pose.orientation.z
        t.transform.rotation.w = newOdom.pose.pose.orientation.w
        self.tf_broadcaster.sendTransform(t)
        
        newOdom.child_frame_id = 'base_footprint'
        newOdom.header.stamp = self.get_clock().now().to_msg()
        self.publisher_.publish(newOdom)
def main(args=None):
    rclpy.init(args=args)

    run = OdomTimerFix()

    rclpy.spin(run)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
        
    

