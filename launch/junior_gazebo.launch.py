from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node
from launch.substitutions import Command
from launch_ros.parameter_descriptions import ParameterValue

def generate_launch_description():
    ld = LaunchDescription()

    ld.add_action(
        ExecuteProcess(
            cmd=[
                'gazebo',
                '--verbose',
                '-s',
                'libgazebo_ros_factory.so'
            ],
            output='screen'
        )
    )
    packagePath = FindPackageShare('junior_model')

    ld.add_action(
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{
                'robot_description': ParameterValue(
                    Command([
                        'xacro ',
                        PathJoinSubstitution([packagePath,'urdf', 'junior.urdf'])
                    ]), 
                    value_type=str
                ),
            }]
        )
    )
    ld.add_action(
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui'
        )
    )
    ld.add_action(
        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            output='screen',
            arguments=[
                '-topic', '/robot_description',
                '-entity', 'junior'
            ]
        )
    )

    return ld