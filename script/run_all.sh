# ROSBridge terminal
gnome-terminal --title="ROSBridge" -- bash -c "
ros2 run rosbridge_server rosbridge_websocket
exec bash
"

# Prearm node terminal
gnome-terminal --title="Preparm" -- bash -c "
source ~/MyProject/kopikia_ws/install/setup.bash
ros2 run kopikia_bot preparm --ros
exec bash
"

# Flutter GUI terminal
gnome-terminal --title="Flutter GUI" -- bash -c "
cd ~/MyProject/kopikia_ws/kopikia_gui_ws/kopikia_gui_ros2
flutter run -d linux
exec bash
"
