import os
import subprocess

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument, ExecuteProcess, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    gazebo = 'zamboni_gazebo'
    description = 'zamboni_description'

    # set the world
    world = os.path.join(get_package_share_directory(gazebo), 'worlds', 'ice_rink.world')
    urdf = os.path.join(get_package_share_directory(description),'urdf', 'zamboni.urdf')
    rviz = os.path.join(get_package_share_directory(description), 'rviz', 'view.rviz')
    
    print(f"using urdf: {urdf}")
    print(f"using rviz: {rviz}")

    # Prevent 
    subprocess.run(['killall', 'gzserver'])
    subprocess.run(['killall', 'gzclient'])

    sim_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation (Gazebo) clock if true'
    )

    launch_gazebo = ExecuteProcess(
            cmd=['gazebo', world],#'libgazebo_ros_factory'],
        )

    launch_rviz = Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz],
            output={'both': 'log'}
        )

    rcutils_output = SetEnvironmentVariable(
            'RCUTILS_CONSOLE_OUTPUT_FORMAT', '[{severity}]: {message}'
        )

    rcutils = SetEnvironmentVariable(
            'RCUTILS_COLORIZED_OUTPUT', '1'
        )

    robot_state_publisher = Node(
            package='robot_state_publisher',
            name='robot_state_publisher',
            executable='robot_state_publisher',
            output='screen', #{'both':'log'},
            parameters=[{'use_sim_time': True}], 
            arguments=[urdf]
        )

    # RTABMap = IncludeLaunchDescription(
    #         PythonLaunchDescriptionSource([
    #             FindPackageShare("rtabmap_ros"), '/launch', '/rtabmap.launch.py']),
    #         launch_arguments={'use_sim_time': use_sim_time,
    #         "rgb_topic":"/depth_camera/color/image_raw", 
    #         "depth_topic":"/depth_camera/depth/image_raw",
    #         "camera_info_topic":"/depth_camera/color/camera_info",
    #         "odom_topic":"/zamboni/odom",
    #         "frame_id":"base_link", 
    #         "approx_sync":"true", 
    #         "wait_imu_to_init":"true", 
    #         "imu_topic":"/imu/data",
    #         "visual_odometry":"false",
    #         "qos":"2"}.items()
    #    )

    return LaunchDescription([
        rcutils_output,
        rcutils,
        launch_gazebo,
        sim_time,
        robot_state_publisher,
        launch_rviz,
        #RTABMap
    ])

def main():
    generate_launch_description()

if __name__ == '__main__':
    main()