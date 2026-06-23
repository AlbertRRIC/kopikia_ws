#!/usr/bin/env python3
import rclpy
from pathlib import Path
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String  # Imported for the new topic
from cv_bridge import CvBridge
from ultralytics import YOLO
import cv2
import numpy as np
import json  # Used to structure the published data cleanly

# Import message filters for strict topic synchronization
import message_filters

class YoloDetectionNode(Node):
    def __init__(self):
        super().__init__('yolo_detection_node')
        
        self.br = CvBridge()
        
        # --- Model Initialization ---
        MODEL_DIR = Path(__file__).parent / 'model'
        best_weights = MODEL_DIR / 'cup_detector' / 'weights' / 'best.pt'
        if best_weights.exists():
            self.model = YOLO(str(best_weights))
            self.get_logger().info(f"YOLO11 Detection Node started with custom model: {best_weights.name}")
        else:
            self.model = YOLO(str(MODEL_DIR / 'yolo11n.pt'))
            self.get_logger().info("YOLO11 Detection Node started with pretrained yolo11n.pt")
            
        # --- Publishers ---
        self.image_pub = self.create_publisher(Image, '/camera/yolo/debug_image', 10)
        # Added the requested data publisher
        self.position_pub = self.create_publisher(String, '/barista/cup_position', 10)
        
        # --- Synchronized Subscriptions ---
        self.color_sub = message_filters.Subscriber(self, Image, '/camera/color/image_raw')
        self.depth_sub = message_filters.Subscriber(self, Image, '/camera/depth/image_raw')
        
        self.ts = message_filters.ApproximateTimeSynchronizer(
            [self.color_sub, self.depth_sub], 
            queue_size=10, 
            slop=0.05
        )
        self.ts.registerCallback(self.synchronized_callback)
        
        self.get_logger().info("YOLO11 Detection Node completely initialized.")

    def synchronized_callback(self, color_msg, depth_msg):
        try:
            cv_image = self.br.imgmsg_to_cv2(color_msg, "bgr8")
            depth_image = self.br.imgmsg_to_cv2(depth_msg, desired_encoding="passthrough")
            
            # --- Establish the Central Reference Point ---
            frame_width = cv_image.shape[1]
            frame_center_x = frame_width // 2
            
            # Run inference
            results = self.model(cv_image, device='0', verbose=False)
            
            # This list will hold the position data for all cups found in this frame
            frame_cup_data = []
            
            for r in results:
                # Plot bounding boxes without original labels so we can add custom text
                annotated_frame = r.plot(labels=False)
                
                if r.boxes is not None and len(r.boxes) > 0:
                    detected_objects = []
                    
                    # 1. Parse detections and extract model-defined labels
                    for box in r.boxes:
                        class_id = int(box.cls[0].cpu().numpy())
                        
                        # Extract the true name string assigned to this class by the model
                        model_label = self.model.names[class_id]
                        
                        x1, y1, x2, y2 = map(int, box.xyxy[0].cpu().numpy())
                        cx = (x1 + x2) // 2
                        cy = (y1 + y2) // 2
                        
                        detected_objects.append({
                            'label': model_label,
                            'box': (x1, y1, x2, y2),
                            'cx': cx,
                            'cy': cy
                        })
                    
                    # 2. Process each object relative to the frame center
                    for obj in detected_objects:
                        x1, y1, x2, y2 = obj['box']
                        cx, cy = obj['cx'], obj['cy']
                        
                        object_name = obj['label']
                        
                        # --- Dynamic Left/Right Detection Relative to Screen Center ---
                        if cx < frame_center_x:
                            side_label = "Left"
                            text_color = (255, 0, 0)  # Blue text for Left side
                        else:
                            side_label = "Right"
                            text_color = (0, 0, 255)  # Red text for Right side
                        
                        # Fetch Distance data from Depth Map
                        dist_meters = 0.0
                        if 0 <= cx < depth_image.shape[1] and 0 <= cy < depth_image.shape[0]:
                            raw_dist = depth_image[cy, cx]
                            if depth_image.dtype == np.uint16:
                                dist_meters = float(raw_dist) / 1000.0
                            else:
                                dist_meters = float(raw_dist)
                        
                        # Save the localized data for publishing
                        frame_cup_data.append({
                            "object": object_name,
                            "position": side_label,
                            "distance_m": round(dist_meters, 2) if dist_meters > 0.0 else None
                        })
                        
                        # Assemble the final bounding box annotation text
                        if dist_meters > 0.0:
                            final_text = f"{object_name} ({side_label}) | {dist_meters:.2f}m"
                        else:
                            final_text = f"{object_name} ({side_label})"
                            
                        # Draw custom text above the target bounding box
                        cv2.putText(annotated_frame, final_text, (x1, y1 - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 2)
                
                # Draw a vertical center line guide to visually verify left vs right splits
                cv2.line(annotated_frame, (frame_center_x, 0), (frame_center_x, cv_image.shape[0]), (0, 255, 255), 1)
                
                # Publish the annotated image stream
                self.image_pub.publish(self.br.cv2_to_imgmsg(annotated_frame, "bgr8"))
            
            # 3. Publish the text position data as a JSON string if any cups were detected
            if frame_cup_data:
                string_msg = String()
                string_msg.data = json.dumps(frame_cup_data)
                self.position_pub.publish(string_msg)
                
        except Exception as e:
            self.get_logger().error(f"Error in synchronized processing loop: {e}")

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