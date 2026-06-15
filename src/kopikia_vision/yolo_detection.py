#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from ultralytics import YOLO
import cv2

class YoloDetectionNode(Node):
    def __init__(self):
        super().__init__('yolo_detection_node')
        
        # Subscribe to the raw image from camera_setup.py
        self.subscription = self.create_subscription(
            Image,
            '/camera/color/image_raw',
            self.listener_callback,
            10)
            
        # Publisher for the debug image with bounding boxes
        self.publisher_ = self.create_publisher(Image, '/camera/yolo/debug_image', 10)
        
        self.br = CvBridge()
        
        # Load YOLO11 model (n is for nano, best for Jetson performance)
        # It will download the .pt file on the first run
        self.model = YOLO('yolo11n.pt') 
        
        self.get_logger().info("YOLO11 Detection Node has started.")

    def listener_callback(self, data):
        try:
            # Convert ROS Image to OpenCV BGR format
            cv_image = self.br.imgmsg_to_cv2(data, "bgr8")
            
            # Run YOLO inference
            # device='0' uses the Jetson GPU
            results = self.model(cv_image, stream=True, device='0', verbose=False)
            
            for r in results:
                # Draw results on the image
                annotated_frame = r.plot()
                
                # Convert back to ROS Image and publish
                self.publisher_.publish(self.br.cv2_to_imgmsg(annotated_frame, "bgr8"))
                
        except Exception as e:
            self.get_logger().error(f"YOLO Processing Error: {e}")

def main(args=None):
    rclpy.init(args=args)
    node = YoloDetectionNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()