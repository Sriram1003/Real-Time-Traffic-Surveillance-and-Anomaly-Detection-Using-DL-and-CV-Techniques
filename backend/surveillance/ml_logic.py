# import cv2
# import numpy as np
# import math
# from ultralytics import YOLO
# from collections import defaultdict, deque
# import os

# class TrafficAnalyzer:
#     def __init__(self):
#         print("--------------------------------------------------")
#         print("  INITIALIZING TRAFFIC AI SYSTEM (YOLOv8)  ")
#         print("--------------------------------------------------")
        
#         # 1. LOAD VEHICLE MODEL
#         print(">> Loading Vehicle Model (yolov8m.pt)...")
#         if os.path.exists('yolov8m.pt'):
#             self.vehicle_model = YOLO('yolov8m.pt')
#         else:
#             print("!! ERROR: yolov8m.pt not found. Downloading standard v8n...")
#             self.vehicle_model = YOLO('yolov8n.pt') 

#         # 2. LOAD HELMET MODEL
#         print(">> Loading Helmet Model (best_helmet.pt)...")
#         try:
#             if os.path.exists('best_helmet.pt'):
#                 self.helmet_model = YOLO('best_helmet.pt')
#             else:
#                 print("!! WARNING: best_helmet.pt not found! Using yolov8n.pt as fallback.")
#                 self.helmet_model = YOLO('yolov8n.pt')
#         except Exception as e:
#             print(f"Error loading helmet model: {e}")
#             self.helmet_model = YOLO('yolov8n.pt')

#         self.target_classes = [2, 3, 5, 7] # Car, Bike, Bus, Truck
        
#         # TRACKING STATE
#         self.track_history = defaultdict(lambda: [])
#         # New: Buffer to smooth out speed jitter
#         self.speed_buffer = defaultdict(lambda: deque(maxlen=5)) 

#     def get_dynamic_ppm(self, y_coord):
#         """
#         Adjusts calibration based on depth (Perspective Correction).
#         Objects lower on screen (higher y) need higher PPM.
#         Objects higher on screen (lower y) need lower PPM.
#         """
#         # TUNING VALUES:
#         # At y=300 (Horizon), 1 meter might be 5 pixels
#         # At y=720 (Bottom), 1 meter might be 25 pixels
#         # Linear interpolation: y * slope + intercept
        
#         # You can tweak these two numbers if speed is still off:
#         ppm_at_top = 8.0    # Lower this if far-away cars are too fast
#         ppm_at_bottom = 30.0 # Raise this if close cars are too fast
        
#         height_of_frame = 720.0
#         slope = (ppm_at_bottom - ppm_at_top) / height_of_frame
        
#         current_ppm = (slope * y_coord) + ppm_at_top
#         return max(current_ppm, 5.0) # Safety minimum

#     def estimate_speed(self, track_id, center_x, center_y):
#         self.track_history[track_id].append((center_x, center_y))
        
#         if len(self.track_history[track_id]) < 2: return 0
#         if len(self.track_history[track_id]) > 30: self.track_history[track_id].pop(0)
            
#         # Look back 5 frames
#         prev_idx = max(0, len(self.track_history[track_id]) - 5)
#         prev_x, prev_y = self.track_history[track_id][prev_idx]
        
#         # Calculate pixel distance
#         dist_pixels = math.sqrt((center_x - prev_x)**2 + (center_y - prev_y)**2)
        
#         # GET DYNAMIC PPM BASED ON DEPTH (Y-Coordinate)
#         ppm = self.get_dynamic_ppm(center_y)
        
#         dist_meters = dist_pixels / ppm
        
#         # Speed Formula
#         # Time = (frames / FPS) -> 5 frames / 30 fps = 0.166s
#         speed_mps = dist_meters / 0.166
#         speed_kmh = speed_mps * 3.6
        
#         # Filter noise: Ignore impossibly low speeds (parking jitter)
#         if speed_kmh < 3:
#             return 0
            
#         # SMOOTHING: Add to buffer and average
#         self.speed_buffer[track_id].append(int(speed_kmh))
#         avg_speed = sum(self.speed_buffer[track_id]) / len(self.speed_buffer[track_id])
        
#         return int(avg_speed)

#     def run_surveillance(self, video_path):
#         cap = cv2.VideoCapture(video_path)
#         window_name = "Traffic Surveillance Output"
#         cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
#         cv2.resizeWindow(window_name, 1280, 720)
        
#         print(f"Processing Video: {video_path}")
        
#         while cap.isOpened():
#             success, frame = cap.read()
#             if not success: break
            
#             frame = cv2.resize(frame, (1280, 720))
            
#             results = self.vehicle_model.track(frame, persist=True, verbose=False)
            
#             if results[0].boxes.id is not None:
#                 boxes = results[0].boxes.xyxy.cpu().numpy()
#                 track_ids = results[0].boxes.id.int().cpu().numpy()
#                 classes = results[0].boxes.cls.int().cpu().numpy()
                
#                 vehicle_count = 0
                
#                 for box, track_id, cls in zip(boxes, track_ids, classes):
#                     if cls not in self.target_classes: continue
                        
#                     vehicle_count += 1
#                     x1, y1, x2, y2 = map(int, box)
#                     cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                    
#                     label_name = self.vehicle_model.names[cls]
                    
#                     # --- IMPROVED SPEED ESTIMATION ---
#                     speed = self.estimate_speed(track_id, cx, cy)
                    
#                     box_color = (255, 120, 0)
#                     status_text = f"{label_name.upper()} {speed} km/h"
                    
#                     # --- HELMET DETECTION ---
#                     if label_name == 'motorcycle':
#                         crop = frame[max(0, y1-50):min(720, y2), max(0, x1):min(1280, x2)]
#                         if crop.size > 0:
#                             h_results = self.helmet_model(crop, verbose=False)
#                             if len(h_results[0].boxes) > 0:
#                                 box_color = (0, 255, 0) # GREEN
#                                 status_text = f"BIKE | HELMET | {speed} km/h"
#                             else:
#                                 box_color = (0, 0, 255) # RED
#                                 status_text = f"BIKE | NO HELMET | {speed} km/h"

#                     # Drawing
#                     cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, 2)
#                     (w, h), _ = cv2.getTextSize(status_text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
#                     cv2.rectangle(frame, (x1, y1 - 25), (x1 + w, y1), box_color, -1)
#                     cv2.putText(frame, status_text, (x1, y1 - 8), 
#                                 cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                                
#                 # UI
#                 cv2.rectangle(frame, (0, 0), (1280, 60), (0, 0, 0), -1)
#                 cv2.putText(frame, f"Vehicles: {vehicle_count}", (1050, 40), 
#                             cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

#             cv2.imshow(window_name, frame)
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break

#         cap.release()
#         cv2.destroyAllWindows()
#------------------------------------------------------------------------------------------------------------------------------------------------------------
# import cv2
# import numpy as np
# import math
# from ultralytics import YOLO
# from collections import defaultdict, deque
# import os
# import easyocr

# class TrafficAnalyzer:
#     def __init__(self):
#         print("--------------------------------------------------")
#         print("  INITIALIZING TRAFFIC AI SYSTEM (UPLOAD MODE)  ")
#         print("--------------------------------------------------")
        
#         # 1. LOAD VEHICLE MODEL (Using 'm' for higher accuracy on Uploads)
#         print(">> Loading Vehicle Model (yolov8m.pt)...")
#         if os.path.exists('yolov8m.pt'):
#             self.vehicle_model = YOLO('yolov8m.pt')
#         else:
#             print("!! WARNING: yolov8m.pt not found. Using yolov8n.pt as fallback.")
#             self.vehicle_model = YOLO('yolov8n.pt') 

#         # 2. LOAD HELMET MODEL
#         print(">> Loading Helmet Model (best_helmet.pt)...")
#         self.helmet_classes = {}
#         try:
#             if os.path.exists('best_helmet.pt'):
#                 self.helmet_model = YOLO('best_helmet.pt')
#                 self.helmet_classes = self.helmet_model.names
#             else:
#                 print("!! WARNING: best_helmet.pt not found! Helmet detection disabled.")
#                 self.helmet_model = None
#         except Exception as e:
#             print(f"Error loading helmet model: {e}")
#             self.helmet_model = None

#         # 3. INITIALIZE OCR FOR LICENSE PLATES
#         print(">> Loading OCR Model (EasyOCR)...")
#         self.reader = easyocr.Reader(['en'], gpu=False)

#         self.target_classes = [2, 3, 5, 7] # Car, Bike, Bus, Truck
        
#         # TRACKING STATE
#         self.track_history = defaultdict(lambda: [])
#         self.speed_buffer = defaultdict(lambda: deque(maxlen=5)) 

#     def get_dynamic_ppm(self, y_coord):
#         """Adjusts pixel-per-meter calibration based on depth."""
#         ppm_at_top = 8.0    
#         ppm_at_bottom = 30.0 
#         height_of_frame = 720.0
#         slope = (ppm_at_bottom - ppm_at_top) / height_of_frame
#         current_ppm = (slope * y_coord) + ppm_at_top
#         return max(current_ppm, 5.0) 

#     def estimate_speed(self, track_id, center_x, center_y):
#         self.track_history[track_id].append((center_x, center_y))
        
#         if len(self.track_history[track_id]) < 2: return 0
#         if len(self.track_history[track_id]) > 30: self.track_history[track_id].pop(0)
            
#         prev_idx = max(0, len(self.track_history[track_id]) - 5)
#         prev_x, prev_y = self.track_history[track_id][prev_idx]
        
#         dist_pixels = math.sqrt((center_x - prev_x)**2 + (center_y - prev_y)**2)
#         ppm = self.get_dynamic_ppm(center_y)
#         dist_meters = dist_pixels / ppm
        
#         speed_mps = dist_meters / 0.166
#         speed_kmh = speed_mps * 3.6
        
#         if speed_kmh < 3:
#             return 0
            
#         self.speed_buffer[track_id].append(int(speed_kmh))
#         avg_speed = sum(self.speed_buffer[track_id]) / len(self.speed_buffer[track_id])
#         return int(avg_speed)

#     def run_surveillance(self, video_path):
#         cap = cv2.VideoCapture(video_path)
#         window_name = "Traffic Surveillance Output"
#         cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
#         cv2.resizeWindow(window_name, 1280, 720)
        
#         print(f"Processing Video: {video_path}")
        
#         frame_count = 0
#         final_vehicle_count = 0

#         while cap.isOpened():
#             success, frame = cap.read()
#             if not success: break
            
#             frame_count += 1
#             frame = cv2.resize(frame, (1280, 720))
            
#             # Using conf=0.3 to ensure we don't miss smaller objects in uploads
#             results = self.vehicle_model.track(frame, persist=True, verbose=False, conf=0.3)
            
#             if results[0].boxes.id is not None:
#                 boxes = results[0].boxes.xyxy.cpu().numpy()
#                 track_ids = results[0].boxes.id.int().cpu().numpy()
#                 classes = results[0].boxes.cls.int().cpu().numpy()
                
#                 current_frame_count = 0
                
#                 for box, track_id, cls in zip(boxes, track_ids, classes):
#                     if cls not in self.target_classes: continue
                        
#                     current_frame_count += 1
#                     x1, y1, x2, y2 = map(int, box)
#                     cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                    
#                     label_name = self.vehicle_model.names[cls]
#                     speed = self.estimate_speed(track_id, cx, cy)
                    
#                     box_color = (255, 120, 0)
#                     status_text = f"{label_name.upper()} {speed} km/h"

#                     # --- 1. OCR LICENSE PLATE RECOGNITION ---
#                     plate_text = ""
#                     # Run OCR every 10 frames for Cars and Trucks
#                     if label_name in ['car', 'truck'] and frame_count % 10 == 0:
#                         try:
#                             roi = frame[max(0,y1):min(y2,720), max(0,x1):min(x2,1280)]
#                             if roi.size > 0:
#                                 gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
#                                 gray = cv2.bilateralFilter(gray, 11, 17, 17)
#                                 ocr_result = self.reader.readtext(gray, detail=0, allowlist='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')
#                                 if len(ocr_result) > 0:
#                                     best_text = max(ocr_result, key=len)
#                                     if len(best_text) > 3:
#                                         plate_text = best_text
#                                         print(f">>> OCR FOUND (UPLOAD): {plate_text}")
#                         except Exception as e:
#                             pass
                    
#                     if plate_text:
#                         status_text += f" [{plate_text}]"
#                         box_color = (255, 0, 255) # Purple for plates
                    
#                     # --- 2. HELMET DETECTION ---
#                     if label_name == 'motorcycle':
#                         box_color = (0, 165, 255) # Default orange for bike
#                         if self.helmet_model:
#                             crop = frame[max(0, y1):min(720, y2), max(0, x1):min(1280, x2)]
#                             if crop.size > 0:
#                                 try:
#                                     # Use a lower confidence threshold to catch helmets better
#                                     h_results = self.helmet_model.predict(crop, verbose=False, conf=0.25)
#                                     helmet_detected = False
                                    
#                                     for h_box in h_results[0].boxes:
#                                         cls_id = int(h_box.cls[0])
#                                         cls_name = self.helmet_classes.get(cls_id, '').lower()
                                        
#                                         # Smart checking based on your model's labels
#                                         if 'with' in cls_name and 'out' not in cls_name:
#                                             helmet_detected = True
#                                             break
                                    
#                                     if helmet_detected:
#                                         box_color = (0, 255, 0) # GREEN
#                                         status_text = f"BIKE | HELMET | {speed} km/h"
#                                     elif len(h_results[0].boxes) > 0:
#                                         box_color = (0, 0, 255) # RED
#                                         status_text = f"BIKE | NO HELMET | {speed} km/h"
#                                 except Exception as e:
#                                     pass

#                     # --- DRAWING ---
#                     cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, 2)
#                     (w, h), _ = cv2.getTextSize(status_text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
#                     cv2.rectangle(frame, (x1, y1 - 25), (x1 + w, y1), box_color, -1)
#                     cv2.putText(frame, status_text, (x1, y1 - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                            
#                 # Update final count tracking
#                 final_vehicle_count = max(final_vehicle_count, track_ids.max() if len(track_ids) > 0 else 0)
                
#                 # UI Overlay
#                 cv2.rectangle(frame, (0, 0), (1280, 60), (0, 0, 0), -1)
#                 cv2.putText(frame, f"Vehicles Present: {current_frame_count}", (50, 40), 
#                             cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

#             cv2.imshow(window_name, frame)
            
#             # Press 'q' to quit early
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break

#         cap.release()
#         cv2.destroyAllWindows()
        
#         return {"total_vehicles_detected": int(final_vehicle_count)}
#--------------------------------------------------------------------------------------------------------------------------------------------------
# import cv2
# import numpy as np
# import math
# from ultralytics import YOLO
# from collections import defaultdict, deque
# import os
# import easyocr

# class TrafficAnalyzer:
#     def __init__(self):
#         print("--------------------------------------------------")
#         print("  INITIALIZING TRAFFIC AI SYSTEM (UPLOAD MODE)  ")
#         print("--------------------------------------------------")
        
#         # 1. LOAD VEHICLE MODEL
#         print(">> Loading Vehicle Model (yolov8m.pt)...")
#         if os.path.exists('yolov8m.pt'):
#             self.vehicle_model = YOLO('yolov8m.pt')
#         else:
#             print("!! WARNING: yolov8m.pt not found. Using yolov8n.pt as fallback.")
#             self.vehicle_model = YOLO('yolov8n.pt') 

#         # 2. LOAD HELMET MODEL
#         print(">> Loading Helmet Model (best_helmet.pt)...")
#         self.helmet_classes = {}
#         try:
#             if os.path.exists('best_helmet.pt'):
#                 self.helmet_model = YOLO('best_helmet.pt')
#                 self.helmet_classes = self.helmet_model.names
#             else:
#                 print("!! WARNING: best_helmet.pt not found! Helmet detection disabled.")
#                 self.helmet_model = None
#         except Exception as e:
#             print(f"Error loading helmet model: {e}")
#             self.helmet_model = None

#         # 3. INITIALIZE OCR 
#         print(">> Loading OCR Model (EasyOCR)...")
#         self.reader = easyocr.Reader(['en'], gpu=False)

#         self.target_classes = [2, 3, 5, 7] # Car, Bike, Bus, Truck
#         self.track_history = defaultdict(lambda: [])
#         self.speed_buffer = defaultdict(lambda: deque(maxlen=5)) 

#     def get_dynamic_ppm(self, y_coord):
#         ppm_at_top = 8.0    
#         ppm_at_bottom = 30.0 
#         slope = (ppm_at_bottom - ppm_at_top) / 720.0
#         return max((slope * y_coord) + ppm_at_top, 5.0) 

#     def estimate_speed(self, track_id, center_x, center_y):
#         self.track_history[track_id].append((center_x, center_y))
#         if len(self.track_history[track_id]) < 2: return 0
#         if len(self.track_history[track_id]) > 30: self.track_history[track_id].pop(0)
            
#         prev_idx = max(0, len(self.track_history[track_id]) - 5)
#         prev_x, prev_y = self.track_history[track_id][prev_idx]
        
#         dist_pixels = math.sqrt((center_x - prev_x)**2 + (center_y - prev_y)**2)
#         dist_meters = dist_pixels / self.get_dynamic_ppm(center_y)
#         speed_kmh = (dist_meters / 0.166) * 3.6
        
#         if speed_kmh < 3: return 0
            
#         self.speed_buffer[track_id].append(int(speed_kmh))
#         return int(sum(self.speed_buffer[track_id]) / len(self.speed_buffer[track_id]))

#     def run_surveillance(self, video_path):
#         cap = cv2.VideoCapture(video_path)
#         window_name = "Traffic Surveillance Output"
#         cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
#         cv2.resizeWindow(window_name, 1280, 720)
        
#         print(f"Processing Video: {video_path}")
#         frame_count = 0
#         final_vehicle_count = 0

#         while cap.isOpened():
#             success, frame = cap.read()
#             if not success: break
            
#             frame_count += 1
#             frame = cv2.resize(frame, (1280, 720))
            
#             # Lower confidence to 0.25 so we don't miss distant cars
#             results = self.vehicle_model.track(frame, persist=True, verbose=False, conf=0.25)
            
#             if results[0].boxes.id is not None:
#                 boxes = results[0].boxes.xyxy.cpu().numpy()
#                 track_ids = results[0].boxes.id.int().cpu().numpy()
#                 classes = results[0].boxes.cls.int().cpu().numpy()
                
#                 current_frame_count = 0
                
#                 for box, track_id, cls in zip(boxes, track_ids, classes):
#                     if cls not in self.target_classes: continue
                        
#                     current_frame_count += 1
#                     x1, y1, x2, y2 = map(int, box)
#                     cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                    
#                     # Box dimensions
#                     box_w = x2 - x1
#                     box_h = y2 - y1
                    
#                     label_name = self.vehicle_model.names[cls]
#                     speed = self.estimate_speed(track_id, cx, cy)
                    
#                     box_color = (255, 120, 0)
#                     status_text = f"{label_name.upper()} {speed} km/h"

#                     # --- 1. OCR LICENSE PLATE RECOGNITION ---
#                     plate_text = ""
#                     # Only run OCR if the vehicle is large enough (close to camera)
#                     if label_name in ['car', 'truck', 'bus'] and frame_count % 10 == 0 and box_h > 60:
#                         try:
#                             # Crop exactly to the vehicle
#                             roi = frame[max(0,y1):min(720,y2), max(0,x1):min(1280,x2)]
#                             if roi.size > 0:
#                                 gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
#                                 gray = cv2.bilateralFilter(gray, 11, 17, 17)
#                                 ocr_result = self.reader.readtext(gray, detail=0, allowlist='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')
#                                 if len(ocr_result) > 0:
#                                     best_text = max(ocr_result, key=len)
#                                     if len(best_text) > 3:
#                                         plate_text = best_text
#                                         print(f">>> OCR FOUND (UPLOAD): {plate_text}")
#                         except: pass
                    
#                     if plate_text:
#                         status_text += f" [{plate_text}]"
#                         box_color = (255, 0, 255) # Purple
                    
#                     # --- 2. HELMET DETECTION (WITH PROPORTIONAL CROP) ---
#                     if label_name == 'motorcycle':
#                         box_color = (0, 165, 255) # Default orange
#                         if self.helmet_model:
#                             # PROPORTIONAL CROP: Expand top by 35% to catch the rider's head
#                             # Expand sides by 10% to catch arms/shoulders
#                             crop_y1 = max(0, y1 - int(box_h * 0.35))
#                             crop_x1 = max(0, x1 - int(box_w * 0.10))
#                             crop_x2 = min(1280, x2 + int(box_w * 0.10))
                            
#                             crop = frame[crop_y1:min(720, y2), crop_x1:crop_x2]
                            
#                             if crop.size > 0:
#                                 try:
#                                     # Very low confidence (0.10) because helmets are tiny objects
#                                     h_results = self.helmet_model.predict(crop, verbose=False, conf=0.10)
#                                     helmet_detected = False
                                    
#                                     for h_box in h_results[0].boxes:
#                                         cls_id = int(h_box.cls[0])
#                                         cls_name = self.helmet_classes.get(cls_id, '').lower()
                                        
#                                         if 'with' in cls_name and 'out' not in cls_name:
#                                             helmet_detected = True
#                                             break
                                    
#                                     if helmet_detected:
#                                         box_color = (0, 255, 0) # GREEN
#                                         status_text = f"BIKE | HELMET | {speed} km/h"
#                                     elif len(h_results[0].boxes) > 0:
#                                         box_color = (0, 0, 255) # RED
#                                         status_text = f"BIKE | NO HELMET | {speed} km/h"
#                                 except: pass

#                     # --- DRAWING ---
#                     cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, 2)
#                     (w, h), _ = cv2.getTextSize(status_text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
#                     cv2.rectangle(frame, (x1, y1 - 25), (x1 + w, y1), box_color, -1)
#                     cv2.putText(frame, status_text, (x1, y1 - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                            
#                 final_vehicle_count = max(final_vehicle_count, track_ids.max() if len(track_ids) > 0 else 0)
                
#                 cv2.rectangle(frame, (0, 0), (1280, 60), (0, 0, 0), -1)
#                 cv2.putText(frame, f"Vehicles Present: {current_frame_count}", (50, 40), 
#                             cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

#             cv2.imshow(window_name, frame)
#             if cv2.waitKey(1) & 0xFF == ord('q'): break

#         cap.release()
#         cv2.destroyAllWindows()
#         return {"total_vehicles_detected": int(final_vehicle_count)}
##--------------------------------------------------------------------------------------------------------------------------------------------------
import cv2
import numpy as np
import math
from ultralytics import YOLO
from collections import defaultdict, deque
import os
import easyocr

class TrafficAnalyzer:
    def __init__(self):
        print("--------------------------------------------------")
        print("  INITIALIZING TRAFFIC AI SYSTEM (UPLOAD MODE)  ")
        print("--------------------------------------------------")
        
        # 1. LOAD VEHICLE MODEL
        print(">> Loading Vehicle Model (yolov8m.pt)...")
        if os.path.exists('yolov8m.pt'):
            self.vehicle_model = YOLO('yolov8m.pt')
        else:
            print("!! WARNING: yolov8m.pt not found. Using yolov8n.pt as fallback.")
            self.vehicle_model = YOLO('yolov8n.pt') 

        # 2. LOAD HELMET MODEL
        print(">> Loading Helmet Model (best_helmet.pt)...")
        self.helmet_classes = {}
        try:
            if os.path.exists('best_helmet.pt'):
                self.helmet_model = YOLO('best_helmet.pt')
                self.helmet_classes = self.helmet_model.names
            else:
                print("!! WARNING: best_helmet.pt not found! Helmet detection disabled.")
                self.helmet_model = None
        except Exception as e:
            print(f"Error loading helmet model: {e}")
            self.helmet_model = None

        # 3. INITIALIZE OCR 
        print(">> Loading OCR Model (EasyOCR)...")
        self.reader = easyocr.Reader(['en'], gpu=False)

        # Target classes: 0=Person (for triple riding), 2=Car, 3=Bike, 5=Bus, 7=Truck
        self.target_classes = [0, 2, 3, 5, 7] 
        self.track_history = defaultdict(lambda: [])
        self.speed_buffer = defaultdict(lambda: deque(maxlen=5)) 

    def get_dynamic_ppm(self, y_coord):
        ppm_at_top = 8.0    
        ppm_at_bottom = 30.0 
        slope = (ppm_at_bottom - ppm_at_top) / 720.0
        return max((slope * y_coord) + ppm_at_top, 5.0) 

    def estimate_speed(self, track_id, center_x, center_y):
        self.track_history[track_id].append((center_x, center_y))
        if len(self.track_history[track_id]) < 2: return 0
        if len(self.track_history[track_id]) > 30: self.track_history[track_id].pop(0)
            
        prev_idx = max(0, len(self.track_history[track_id]) - 5)
        prev_x, prev_y = self.track_history[track_id][prev_idx]
        
        dist_pixels = math.sqrt((center_x - prev_x)**2 + (center_y - prev_y)**2)
        dist_meters = dist_pixels / self.get_dynamic_ppm(center_y)
        speed_kmh = (dist_meters / 0.166) * 3.6
        
        if speed_kmh < 3: return 0
            
        self.speed_buffer[track_id].append(int(speed_kmh))
        return int(sum(self.speed_buffer[track_id]) / len(self.speed_buffer[track_id]))

    # --- TRIPLE RIDING OVERLAP LOGIC ---
    def count_riders(self, bike_box, persons):
        bx1, by1, bx2, by2 = bike_box
        bike_h = by2 - by1
        bike_w = bx2 - bx1
        
        count = 0
        for p_box in persons:
            px1, py1, px2, py2 = p_box
            pcx = (px1 + px2) / 2
            pcy = (py1 + py2) / 2
            
            margin_x = bike_w * 0.2
            margin_y_top = bike_h * 1.5
            
            if (bx1 - margin_x) <= pcx <= (bx2 + margin_x) and \
               (by1 - margin_y_top) <= pcy <= by2:
                count += 1
                
        return count

    def run_surveillance(self, video_path):
        cap = cv2.VideoCapture(video_path)
        window_name = "Traffic Surveillance Output"
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(window_name, 1280, 720)
        
        print(f"Processing Video: {video_path}")
        frame_count = 0
        
        # --- NEW: Use a Set to store Unique Vehicle IDs ---
        unique_vehicles = set()

        while cap.isOpened():
            success, frame = cap.read()
            if not success: break
            
            frame_count += 1
            frame = cv2.resize(frame, (1280, 720))
            
            results = self.vehicle_model.track(frame, persist=True, verbose=False, conf=0.25)
            
            if results[0].boxes.id is not None:
                boxes = results[0].boxes.xyxy.cpu().numpy()
                track_ids = results[0].boxes.id.int().cpu().numpy()
                classes = results[0].boxes.cls.int().cpu().numpy()
                
                # SEPARATE OUT PERSONS FROM VEHICLES
                persons = [box for box, cls in zip(boxes, classes) if cls == 0]
                
                current_frame_count = 0
                
                for box, track_id, cls in zip(boxes, track_ids, classes):
                    if cls not in [2, 3, 5, 7]: continue # Skip standalone pedestrians
                    
                    # Add ID to our set (It only counts actual vehicles)
                    unique_vehicles.add(track_id)
                        
                    current_frame_count += 1
                    x1, y1, x2, y2 = map(int, box)
                    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                    box_w, box_h = x2 - x1, y2 - y1
                    
                    label_name = self.vehicle_model.names[cls]
                    speed = self.estimate_speed(track_id, cx, cy)
                    
                    box_color = (255, 120, 0)
                    status_text = f"{label_name.upper()} {speed} km/h"

                    # --- 1. OCR LICENSE PLATE RECOGNITION ---
                    plate_text = ""
                    if label_name in ['car', 'truck', 'bus'] and frame_count % 10 == 0 and box_h > 30:
                        try:
                            roi = frame[max(0,y1):min(720,y2), max(0,x1):min(1280,x2)]
                            if roi.size > 0:
                                gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                                gray = cv2.bilateralFilter(gray, 11, 17, 17)
                                ocr_result = self.reader.readtext(gray, detail=0, allowlist='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')
                                if len(ocr_result) > 0:
                                    best_text = max(ocr_result, key=len)
                                    if len(best_text) > 3:
                                        plate_text = best_text
                                        print(f">>> OCR FOUND (UPLOAD): {plate_text}")
                        except: pass
                    
                    if plate_text:
                        status_text += f" [{plate_text}]"
                        box_color = (255, 0, 255) 
                    
                    # --- 2. HELMET & TRIPLE RIDING DETECTION ---
                    if label_name == 'motorcycle':
                        box_color = (0, 165, 255) 
                        
                        rider_count = self.count_riders(box, persons)
                        triple_riding = rider_count >= 3
                        
                        helmet_status = ""
                        if self.helmet_model:
                            crop_y1 = max(0, y1 - int(box_h * 0.35))
                            crop_x1 = max(0, x1 - int(box_w * 0.10))
                            crop_x2 = min(1280, x2 + int(box_w * 0.10))
                            
                            crop = frame[crop_y1:min(720, y2), crop_x1:crop_x2]
                            if crop.size > 0:
                                try:
                                    h_results = self.helmet_model.predict(crop, verbose=False, conf=0.10)
                                    helmet_detected = False
                                    
                                    for h_box in h_results[0].boxes:
                                        cls_id = int(h_box.cls[0])
                                        cls_name = self.helmet_classes.get(cls_id, '').lower()
                                        if 'with' in cls_name and 'out' not in cls_name:
                                            helmet_detected = True
                                            break
                                    
                                    if helmet_detected:
                                        box_color = (0, 255, 0)
                                        helmet_status = "HELMET"
                                    elif len(h_results[0].boxes) > 0:
                                        box_color = (0, 0, 255)
                                        helmet_status = "NO HELMET"
                                except: pass

                        status_text = f"BIKE {speed} km/h"
                        if helmet_status:
                            status_text += f" | {helmet_status}"
                        if triple_riding:
                            status_text += " | TRIPLE RIDING!"
                            box_color = (0, 0, 255) 

                    # DRAWING
                    cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, 2)
                    (w, h), _ = cv2.getTextSize(status_text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
                    cv2.rectangle(frame, (x1, y1 - 25), (x1 + w, y1), box_color, -1)
                    cv2.putText(frame, status_text, (x1, y1 - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                            
                cv2.rectangle(frame, (0, 0), (1280, 60), (0, 0, 0), -1)
                cv2.putText(frame, f"Vehicles Present: {current_frame_count}", (50, 40), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

            cv2.imshow(window_name, frame)
            if cv2.waitKey(1) & 0xFF == ord('q'): break

        cap.release()
        cv2.destroyAllWindows()
        
        # --- Return the length of the unique set ---
        return {"total_vehicles_detected": len(unique_vehicles)}