#!/usr/bin/env python3

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import LogInfo
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    
    return LaunchDescription([
        Node(
            package='rplidar_ros',
            executable='rplidar_node',
            name='rplidar_node',
            parameters=[{'channel_type':'serial',
                         'serial_port': '/dev/ttyUSB0',
                         'serial_baudrate': 256000,
                         'frame_id': 'laser_frame',
                         'inverted': False,
                         'angle_compensate': True}],
            output='screen'
            ),
            
            
            
    ])

