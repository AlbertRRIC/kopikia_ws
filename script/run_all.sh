# Kill any existing instances to prevent port binding issues
killall -9 rosbridge_websocket 2>/dev/null

# ROSBridge terminal
gnome-terminal --title="ROSBridge" -- bash -c "
source ~/MyProject/kopikia_ws/install/setup.bash
ros2 run rosbridge_server rosbridge_websocket --ros-args -p address:='0.0.0.0' -p default_call_service_timeout:=5.0 -p call_services_in_new_thread:=true -p send_action_goals_in_new_thread:=true
exec bash
"

# Prearm node terminal
gnome-terminal --title="Preparm" -- bash -c "
source ~/MyProject/kopikia_ws/install/setup.bash
ros2 run kopikia_bot preparm 192.168.1.223 --ros
exec bash
"

# Flutter GUI terminal
gnome-terminal --title="Flutter GUI" -- bash -c "
cd ~/MyProject/kopikia_ws/kopikia_gui_ws/kopikia_gui_ros2
sleep 10
flutter run -d linux
exec bash
"
