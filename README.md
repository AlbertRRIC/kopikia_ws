# kopikia work space

# this is for the text to speech installation steps flutter TTS (very machine)
# sudo apt update
# sudo apt install -y espeak espeak-ng speech-dispatcher libspeechd-dev

# piper is better
# cd ~/ros2_ws/src
# git clone https://github.com/mgonzs13/piper_ros.git
# git clone https://github.com/ros-drivers/audio_common.git -b ros2
# remove sound_play of already install ros2
# sudo apt update
# sudo apt install ros-${ROS_DISTRO}-ament-cmake-clang-format
# sudo apt update
# sudo apt install pkg-config libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev

# colcon build
# source install/setup.bash
# ros2 run piper_ros tts_node


#ros2 run rqt_image_view rqt_image_view
