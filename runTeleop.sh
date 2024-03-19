# Starts the keyboard controller and pipes message to topic /zamboni/cmd_vel
ros2 run keyboard_controller keyboard_controller speed:=5 turn:=250 --ros-args --remap cmd_vel:=/zamboni/cmd_vel
