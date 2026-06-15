#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from sensor_msgs.msg import Image
import pyrealsense2 as rs
import numpy as np
from cv_bridge import CvBridge

class RealSenseNode(Node):
    def __init__(self):
        super().__init__('realsense_node')
        # Create a publisher for the distance data
        self.publisher_ = self.create_publisher(Float32, 'camera/distance', 10)
        # Create a publisher for the color image stream for YOLO integration
        self.image_publisher_ = self.create_publisher(Image, 'camera/color/image_raw', 10)
        self.br = CvBridge()
        
        # Align object: ensures depth and color frames share the same coordinate system
        # This is critical for YOLO to accurately measure distance to detected objects.
        self.align = rs.align(rs.stream.color)

        # Initialize the RealSense pipeline
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        self.config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

        try:
            self.pipeline.start(self.config)
            self.get_logger().info("RealSense Camera Node has started with Depth and Color streams.")
        except Exception as e:
            self.get_logger().error(f"Failed to start RealSense pipeline: {e}")
            return

        # Create a timer to process frames at 10Hz (0.1s interval)
        self.timer = self.create_timer(0.1, self.timer_callback)

    def timer_callback(self):
        try:
            # Increased timeout to 1000ms to allow for hardware jitter and startup lag
            frames = self.pipeline.wait_for_frames(timeout_ms=1000)
            
            # Process alignment
            aligned_frames = self.align.process(frames)
            depth_frame = aligned_frames.get_depth_frame()
            color_frame = aligned_frames.get_color_frame()
            
            if not depth_frame or not color_frame:
                return

            # Get distance at the center of the frame
            width, height = depth_frame.get_width(), depth_frame.get_height()
            dist = depth_frame.get_distance(width // 2, height // 2)
            
            # Publish the distance
            msg = Float32()
            msg.data = float(dist)
            self.publisher_.publish(msg)
            
            # Convert color frame to numpy array and publish as ROS Image
            color_image = np.asanyarray(color_frame.get_data())
            self.image_publisher_.publish(self.br.cv2_to_imgmsg(color_image, encoding="bgr8"))

        except Exception as e:
            self.get_logger().warn(f"Could not read frame: {e}")

def main(args=None):
    rclpy.init(args=args)
    node = RealSenseNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.pipeline.stop()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()