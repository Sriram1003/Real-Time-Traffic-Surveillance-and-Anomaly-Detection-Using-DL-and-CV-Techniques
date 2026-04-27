# from django.shortcuts import render

# # Create your views here.
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.parsers import MultiPartParser, FormParser
# from django.core.files.storage import default_storage
# from django.conf import settings
# import os
# import cv2
# import torch
# from .ml_logic import TrafficAnalyzer # We will create this next

# class VideoUploadView(APIView):
#     parser_classes = (MultiPartParser, FormParser)

#     def post(self, request, *args, **kwargs):
#         file_obj = request.FILES['video']
#         file_name = default_storage.save(file_obj.name, file_obj)
#         file_path = os.path.join(settings.MEDIA_ROOT, file_name)

#         # Initialize and Run AI
#         try:
#             # Note: This will open the CV2 window on the SERVER side (your laptop)
#             analyzer = TrafficAnalyzer() 
#             analyzer.run_surveillance(file_path)
            
#             return Response({'status': 'success', 'message': 'Analysis Complete'})
#         except Exception as e:
#             return Response({'status': 'error', 'message': str(e)}, status=500)





# from django.shortcuts import render
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.parsers import MultiPartParser, FormParser
# from django.core.files.storage import default_storage
# from django.conf import settings
# import os
# from .ml_logic import TrafficAnalyzer

# class VideoUploadView(APIView):
#     parser_classes = (MultiPartParser, FormParser)

#     def post(self, request, *args, **kwargs):
#         if 'video' not in request.FILES:
#             return Response({'status': 'error', 'message': 'No video provided'}, status=400)

#         file_obj = request.FILES['video']
#         file_name = default_storage.save(file_obj.name, file_obj)
#         file_path = os.path.join(settings.MEDIA_ROOT, file_name)

#         try:
#             # 1. Initialize AI
#             analyzer = TrafficAnalyzer() 
            
#             # 2. Run Analysis AND Capture the Results (The Counts)
#             counts = analyzer.run_surveillance(file_path)
            
#             # 3. Send the 'counts' back to the Frontend
#             return Response({
#                 'status': 'success', 
#                 'message': 'Analysis Complete',
#                 'results': counts  # <--- THIS IS THE MISSING KEY
#             })
            
#         except Exception as e:
#             print(f"Error: {e}")
#             return Response({'status': 'error', 'message': str(e)}, status=500)
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.parsers import MultiPartParser, FormParser
# from django.core.files.storage import default_storage
# from django.conf import settings
# import os
# from .ml_logic import TrafficAnalyzer

# class VideoUploadView(APIView):
#     parser_classes = (MultiPartParser, FormParser)

#     def post(self, request, *args, **kwargs):
#         if 'video' not in request.FILES:
#             return Response({'status': 'error', 'message': 'No video provided'}, status=400)

#         file_obj = request.FILES['video']
#         file_name = default_storage.save(file_obj.name, file_obj)
#         file_path = os.path.join(settings.MEDIA_ROOT, file_name)

#         try:
#             # 1. Run AI Analysis
#             analyzer = TrafficAnalyzer() 
#             counts = analyzer.run_surveillance(file_path) # <--- GET THE COUNTS
            
#             # 2. Send the counts back to React
#             return Response({
#                 'status': 'success', 
#                 'message': 'Analysis Complete',
#                 'results': counts  # <--- CRITICAL: THIS MUST BE HERE
#             })
            
#         except Exception as e:
#             print(f"Server Error: {e}")
#             return Response({'status': 'error', 'message': str(e)}, status=500)
#-----------------------------------------------------------------------------------------------
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.parsers import MultiPartParser, FormParser
# from django.core.files.storage import default_storage
# from django.conf import settings
# from django.http import StreamingHttpResponse # <--- Added for Live Stream
# import os
# import cv2 # <--- Added for Video Processing
# import yt_dlp # <--- Added for YouTube Link Extraction
# from .ml_logic import TrafficAnalyzer

# # --- 1. EXISTING VIDEO UPLOAD VIEW ---
# class VideoUploadView(APIView):
#     parser_classes = (MultiPartParser, FormParser)

#     def post(self, request, *args, **kwargs):
#         if 'video' not in request.FILES:
#             return Response({'status': 'error', 'message': 'No video provided'}, status=400)

#         file_obj = request.FILES['video']
#         file_name = default_storage.save(file_obj.name, file_obj)
#         file_path = os.path.join(settings.MEDIA_ROOT, file_name)

#         try:
#             # Run AI Analysis
#             analyzer = TrafficAnalyzer() 
#             counts = analyzer.run_surveillance(file_path) 
            
#             # Send the counts back to React
#             return Response({
#                 'status': 'success', 
#                 'message': 'Analysis Complete',
#                 'results': counts  
#             })
            
#         except Exception as e:
#             print(f"Server Error: {e}")
#             return Response({'status': 'error', 'message': str(e)}, status=500)

# # --- 2. NEW LIVE VIDEO FEED VIEW ---
# class LiveVideoFeed(APIView):
#     def get(self, request):
#         # The specific YouTube Live URL you wanted
#         target_url = "https://www.youtube.com/live/y-Os52eW2rg?si=yHFO-ujp2Sbrio9x"
#         return StreamingHttpResponse(self.gen_frames(target_url), content_type='multipart/x-mixed-replace; boundary=frame')

#     def gen_frames(self, youtube_url):
#         # A. Extract the direct video URL using yt-dlp
#         ydl_opts = {
#             'format': 'best[ext=mp4]/best',
#             'quiet': True,
#             'no_warnings': True,
#         }
        
#         try:
#             with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#                 info = ydl.extract_info(youtube_url, download=False)
#                 video_url = info['url'] # The direct stream link
#         except Exception as e:
#             print(f"Error extracting YouTube stream: {e}")
#             return

#         # B. Open the Video Stream
#         cap = cv2.VideoCapture(video_url)
        
#         # C. Initialize AI Model
#         analyzer = TrafficAnalyzer() 

#         while True:
#             success, frame = cap.read()
#             if not success:
#                 break

#             # D. Resize for performance (YouTube 1080p is too slow for CPU)
#             frame = cv2.resize(frame, (1280, 720))

#             # E. Run YOLO Tracking
#             # We filter for specific classes: 2=Car, 3=Bike, 5=Bus, 7=Truck
#             results = analyzer.model.track(frame, persist=True, verbose=False, classes=[2, 3, 5, 7]) 
            
#             # F. Draw the Bounding Boxes
#             annotated_frame = results[0].plot()

#             # G. Encode and Stream
#             ret, buffer = cv2.imencode('.jpg', annotated_frame)
#             frame_bytes = buffer.tobytes()

#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        
#         cap.release()
#------------------------------------------------------------------------------------------------
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.parsers import MultiPartParser, FormParser
# from django.core.files.storage import default_storage
# from django.conf import settings
# from django.http import StreamingHttpResponse
# import os
# import cv2
# import yt_dlp
# from ultralytics import YOLO  # <--- Import YOLO directly
# from .ml_logic import TrafficAnalyzer

# # --- 1. EXISTING VIDEO UPLOAD VIEW ---
# class VideoUploadView(APIView):
#     parser_classes = (MultiPartParser, FormParser)

#     def post(self, request, *args, **kwargs):
#         if 'video' not in request.FILES:
#             return Response({'status': 'error', 'message': 'No video provided'}, status=400)

#         file_obj = request.FILES['video']
#         file_name = default_storage.save(file_obj.name, file_obj)
#         file_path = os.path.join(settings.MEDIA_ROOT, file_name)

#         try:
#             # Keep using TrafficAnalyzer for Uploads (it has the logic for counting)
#             analyzer = TrafficAnalyzer() 
#             counts = analyzer.run_surveillance(file_path) 
            
#             return Response({
#                 'status': 'success', 
#                 'message': 'Analysis Complete',
#                 'results': counts  
#             })
            
#         except Exception as e:
#             print(f"Server Error: {e}")
#             return Response({'status': 'error', 'message': str(e)}, status=500)

# # --- 2. FIXED LIVE VIDEO FEED VIEW ---
# class LiveVideoFeed(APIView):
#     def get(self, request):
#         # We use a stable YouTube Live link (Jackson Hole) to test
#         target_url = "https://www.youtube.com/watch?v=1EiC9bvVGnk" 
#         return StreamingHttpResponse(self.gen_frames(target_url), content_type='multipart/x-mixed-replace; boundary=frame')

#     def gen_frames(self, youtube_url):
#         print(f"DEBUG: Attempting to connect to {youtube_url}")
        
#         # 1. Extract Direct URL
#         ydl_opts = {
#             'format': 'best',
#             'noplaylist': True,
#             'quiet': True,
#         }
        
#         video_url = None
#         try:
#             with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#                 info = ydl.extract_info(youtube_url, download=False)
#                 video_url = info.get('url', None)
#         except Exception as e:
#             print(f"ERROR: yt-dlp failed: {e}")
#             return

#         if not video_url:
#             print("ERROR: No video URL found.")
#             return

#         # 2. Open Video Stream
#         cap = cv2.VideoCapture(video_url)
        
#         # --- THE FIX: Load YOLO directly (Bypassing TrafficAnalyzer) ---
#         print("DEBUG: Loading YOLO model directly...")
#         model = YOLO('yolov8m.pt') 

#         while True:
#             success, frame = cap.read()
#             if not success:
#                 break

#             # Resize for speed
#             frame = cv2.resize(frame, (854, 480))

#             try:
#                 # Use 'model' directly instead of 'analyzer.model'
#                 results = model.track(frame, persist=True, verbose=False, classes=[2, 3, 5, 7])
#                 annotated_frame = results[0].plot()
#             except Exception as e:
#                 print(f"AI Error: {e}")
#                 annotated_frame = frame

#             # Encode and yield
#             ret, buffer = cv2.imencode('.jpg', annotated_frame)
#             if not ret:
#                 continue
            
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        
#         cap.release()
# #------------------------------------------------------------------------------------------------
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.parsers import MultiPartParser, FormParser
# from django.core.files.storage import default_storage
# from django.conf import settings
# from django.http import StreamingHttpResponse
# import os
# import cv2
# import yt_dlp
# import math
# import time
# from ultralytics import YOLO
# from .ml_logic import TrafficAnalyzer

# # --- 1. EXISTING VIDEO UPLOAD VIEW ---
# class VideoUploadView(APIView):
#     parser_classes = (MultiPartParser, FormParser)

#     def post(self, request, *args, **kwargs):
#         if 'video' not in request.FILES:
#             return Response({'status': 'error', 'message': 'No video provided'}, status=400)

#         file_obj = request.FILES['video']
#         file_name = default_storage.save(file_obj.name, file_obj)
#         file_path = os.path.join(settings.MEDIA_ROOT, file_name)

#         try:
#             analyzer = TrafficAnalyzer() 
#             counts = analyzer.run_surveillance(file_path) 
#             return Response({'status': 'success', 'message': 'Analysis Complete', 'results': counts})
#         except Exception as e:
#             print(f"Server Error: {e}")
#             return Response({'status': 'error', 'message': str(e)}, status=500)

# # --- 2. LIVE VIDEO FEED WITH SPEED & HELMETS ---
# class LiveVideoFeed(APIView):
#     def get(self, request):
#         # YouTube URL (Jackson Hole is stable for testing)
#         target_url = "https://www.youtube.com/watch?v=1EiC9bvVGnk"
#         return StreamingHttpResponse(self.gen_frames(target_url), content_type='multipart/x-mixed-replace; boundary=frame')

#     def gen_frames(self, youtube_url):
#         print(f"DEBUG: Connecting to {youtube_url}")
        
#         # 1. Extract URL
#         ydl_opts = {'format': 'best', 'noplaylist': True, 'quiet': True}
#         try:
#             with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#                 info = ydl.extract_info(youtube_url, download=False)
#                 video_url = info.get('url', None)
#         except Exception as e:
#             print(f"ERROR: yt-dlp failed: {e}")
#             return

#         if not video_url: return

#         # 2. Initialize Models
#         cap = cv2.VideoCapture(video_url)
#         model = YOLO('yolov8m.pt') # Vehicle Model
        
#         # Try loading helmet model (Handle error if version is wrong)
#         helmet_model = None
#         try:
#             helmet_model = YOLO('best_helmet.pt')
#         except Exception as e:
#             print(f"WARNING: Helmet model failed to load (Version mismatch?). Skipping helmet detection. Error: {e}")

#         # 3. Speed Tracking Variables
#         track_history = {} # Stores {id: (x, y, timestamp)}
        
#         # Classes: 2=Car, 3=Bike, 5=Bus, 7=Truck
#         CLASS_NAMES = {2: 'Car', 3: 'Bike', 5: 'Bus', 7: 'Truck'}

#         while True:
#             success, frame = cap.read()
#             if not success: break

#             # Resize for performance
#             frame = cv2.resize(frame, (1020, 600))
            
#             # Run Tracking
#             results = model.track(frame, persist=True, verbose=False, classes=[2, 3, 5, 7])
            
#             # --- CUSTOM DRAWING LOGIC ---
#             if results[0].boxes.id is not None:
#                 boxes = results[0].boxes.xyxy.cpu().numpy()
#                 track_ids = results[0].boxes.id.int().cpu().tolist()
#                 clss = results[0].boxes.cls.int().cpu().tolist()

#                 for box, track_id, cls in zip(boxes, track_ids, clss):
#                     x1, y1, x2, y2 = map(int, box)
#                     cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
#                     class_name = CLASS_NAMES.get(cls, 'Vehicle')

#                     # 1. SPEED CALCULATION
#                     speed_label = ""
#                     if track_id in track_history:
#                         prev_cx, prev_cy, prev_time = track_history[track_id]
#                         curr_time = time.time()
                        
#                         # Distance in pixels
#                         distance_px = math.sqrt((cx - prev_cx)**2 + (cy - prev_cy)**2)
                        
#                         # Time elapsed
#                         time_diff = curr_time - prev_time
                        
#                         if time_diff > 0:
#                             # Dynamic Scale (Simple approximation for CCTV view)
#                             # Pixels-per-meter varies by depth (y-axis). 
#                             # Lower in frame (higher y) = more pixels per meter.
#                             ppm = 8 + (cy / 50) 
#                             speed_mps = (distance_px / ppm) / time_diff
#                             speed_kmh = speed_mps * 3.6
                            
#                             # Smoothing
#                             if speed_kmh > 5: # Filter static noise
#                                 speed_label = f"{int(speed_kmh)} km/h"

#                     # Update History
#                     track_history[track_id] = (cx, cy, time.time())

#                     # 2. HELMET DETECTION (Only for Bikes)
#                     color = (255, 0, 0) # Default Blue for vehicles
#                     label = f"{class_name} {speed_label}"

#                     if cls == 3: # Motorcycle
#                         # If we have a working helmet model
#                         if helmet_model:
#                             # Crop ROI
#                             roi = frame[max(0,y1):min(y2,600), max(0,x1):min(x2,1020)]
#                             if roi.size > 0:
#                                 try:
#                                     h_results = helmet_model.predict(roi, verbose=False)
#                                     # Check if 'Helmet' class (usually class 0 or 1 depending on training)
#                                     # We assume logic: If detection found -> Helmet (Green), else No Helmet (Red)
#                                     if len(h_results[0].boxes) > 0:
#                                         color = (0, 255, 0) # Green (Safe)
#                                         label += " [Helmet]"
#                                     else:
#                                         color = (0, 0, 255) # Red (Unsafe)
#                                         label += " [No Helmet]"
#                                 except:
#                                     pass
#                         else:
#                             # Fallback if model is broken
#                             color = (0, 165, 255) # Orange for bikes

#                     # 3. DRAW ON FRAME
#                     cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    
#                     # Draw Label Background
#                     (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
#                     cv2.rectangle(frame, (x1, y1 - 20), (x1 + w, y1), color, -1)
#                     cv2.putText(frame, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

#             # Encode and Yield
#             ret, buffer = cv2.imencode('.jpg', frame)
#             if ret:
#                 yield (b'--frame\r\n'
#                        b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        
#         cap.release()
#------------------------------------------------------------------------------------------------
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.parsers import MultiPartParser, FormParser
# from django.core.files.storage import default_storage
# from django.conf import settings
# from django.http import StreamingHttpResponse
# import os
# import cv2
# import yt_dlp
# import math
# import time
# from ultralytics import YOLO
# from .ml_logic import TrafficAnalyzer

# # --- 1. EXISTING VIDEO UPLOAD VIEW ---
# class VideoUploadView(APIView):
#     parser_classes = (MultiPartParser, FormParser)

#     def post(self, request, *args, **kwargs):
#         if 'video' not in request.FILES:
#             return Response({'status': 'error', 'message': 'No video provided'}, status=400)

#         file_obj = request.FILES['video']
#         file_name = default_storage.save(file_obj.name, file_obj)
#         file_path = os.path.join(settings.MEDIA_ROOT, file_name)

#         try:
#             # We keep the original analyzer for uploads as it handles counting logic well
#             analyzer = TrafficAnalyzer() 
#             counts = analyzer.run_surveillance(file_path) 
#             return Response({'status': 'success', 'message': 'Analysis Complete', 'results': counts})
#         except Exception as e:
#             print(f"Server Error: {e}")
#             return Response({'status': 'error', 'message': str(e)}, status=500)

# # --- 2. OPTIMIZED LIVE VIDEO FEED ---
# class LiveVideoFeed(APIView):
#     def get(self, request):
#         # Using Jackson Hole URL for stable testing
#         target_url = "https://www.youtube.com/watch?v=1EiC9bvVGnk"
#         return StreamingHttpResponse(self.gen_frames(target_url), content_type='multipart/x-mixed-replace; boundary=frame')

#     def gen_frames(self, youtube_url):
#         print(f"DEBUG: Connecting to {youtube_url}")
        
#         # 1. Extract Direct URL using yt-dlp
#         ydl_opts = {'format': 'best', 'noplaylist': True, 'quiet': True}
#         try:
#             with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#                 info = ydl.extract_info(youtube_url, download=False)
#                 video_url = info.get('url', None)
#         except Exception as e:
#             print(f"ERROR: yt-dlp failed: {e}")
#             return

#         if not video_url: return

#         # 2. Initialize Video Capture
#         cap = cv2.VideoCapture(video_url)
        
#         # --- OPTIMIZATION 1: Use Nano Model for Speed (30+ FPS) ---
#         print("DEBUG: Loading YOLOv8 Nano...")
#         model = YOLO('yolov8n.pt') 
        
#         # Try loading helmet model (Graceful fallback if it fails)
#         helmet_model = None
#         try:
#             helmet_model = YOLO('best_helmet.pt')
#         except:
#             print("WARNING: Helmet model failed to load. Showing bikes without helmet status.")

#         # 3. Tracking Variables
#         track_history = {} # Stores {id: (x, y, timestamp)}
#         CLASS_NAMES = {2: 'Car', 3: 'Bike', 5: 'Bus', 7: 'Truck'}
        
#         # FPS Calculation
#         prev_frame_time = 0
#         new_frame_time = 0

#         while True:
#             success, frame = cap.read()
#             if not success: break

#             # --- OPTIMIZATION 2: Lower Resolution (640x360) ---
#             # This is critical for fluency. 1080p is too slow for CPU.
#             frame = cv2.resize(frame, (640, 360))
            
#             # --- OPTIMIZATION 3: Confidence Filtering ---
#             # conf=0.3 skips weak detections to save processing power
#             results = model.track(frame, persist=True, verbose=False, classes=[2, 3, 5, 7], conf=0.3)
            
#             if results[0].boxes.id is not None:
#                 boxes = results[0].boxes.xyxy.cpu().numpy()
#                 track_ids = results[0].boxes.id.int().cpu().tolist()
#                 clss = results[0].boxes.cls.int().cpu().tolist()

#                 for box, track_id, cls in zip(boxes, track_ids, clss):
#                     x1, y1, x2, y2 = map(int, box)
#                     cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
#                     class_name = CLASS_NAMES.get(cls, 'Vehicle')

#                     # A. Speed Calculation
#                     speed_label = ""
#                     if track_id in track_history:
#                         prev_cx, prev_cy, prev_time = track_history[track_id]
#                         curr_time = time.time()
                        
#                         distance_px = math.sqrt((cx - prev_cx)**2 + (cy - prev_cy)**2)
#                         time_diff = curr_time - prev_time
                        
#                         if time_diff > 0:
#                             # Adjusted PPM for 360p resolution
#                             ppm = 4 + (cy / 20) 
#                             speed_kmh = ((distance_px / ppm) / time_diff) * 3.6
                            
#                             if speed_kmh > 3: # Filter noise
#                                 speed_label = f"{int(speed_kmh)} km/h"

#                     track_history[track_id] = (cx, cy, time.time())

#                     # B. Helmet Detection (Only for Bikes)
#                     color = (0, 255, 0) # Default Green
#                     label = f"{class_name} {speed_label}"

#                     if cls == 3: # Motorcycle
#                         color = (0, 165, 255) # Orange default
#                         if helmet_model:
#                             # Crop ROI for helmet check
#                             roi = frame[max(0,y1):min(y2,360), max(0,x1):min(x2,640)]
#                             if roi.size > 0:
#                                 try:
#                                     h_results = helmet_model.predict(roi, verbose=False, conf=0.4)
#                                     if len(h_results[0].boxes) > 0:
#                                         label += " [Helmet]"
#                                         color = (0, 255, 0) # Green
#                                     else:
#                                         label += " [No Helmet]"
#                                         color = (0, 0, 255) # Red
#                                 except: pass

#                     # C. Draw Custom Box & Label
#                     cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    
#                     # Label Background
#                     (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
#                     cv2.rectangle(frame, (x1, y1 - 20), (x1 + w, y1), color, -1)
#                     cv2.putText(frame, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

#             # --- FPS Counter (Top Left) ---
#             new_frame_time = time.time()
#             fps = 1 / (new_frame_time - prev_frame_time) if prev_frame_time > 0 else 0
#             prev_frame_time = new_frame_time
#             cv2.putText(frame, f"FPS: {int(fps)}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

#             # Encode and Yield
#             ret, buffer = cv2.imencode('.jpg', frame)
#             if ret:
#                 yield (b'--frame\r\n'
#                        b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        
#         cap.release()
#-------------------------------------------------------------------------------------------------------------------------------------------      
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.parsers import MultiPartParser, FormParser
# from django.core.files.storage import default_storage
# from django.conf import settings
# from django.http import StreamingHttpResponse
# import os
# import cv2
# import yt_dlp
# import math
# import time
# import easyocr  # <--- NEW LIBRARY
# import numpy as np
# from ultralytics import YOLO
# from .ml_logic import TrafficAnalyzer

# # --- INITIALIZE OCR READER (Load once to save speed) ---
# print("DEBUG: Loading OCR Model... (This may take a moment)")
# reader = easyocr.Reader(['en'], gpu=False) # Set gpu=True if you have NVIDIA CUDA

# # --- 1. EXISTING VIDEO UPLOAD VIEW ---
# class VideoUploadView(APIView):
#     parser_classes = (MultiPartParser, FormParser)

#     def post(self, request, *args, **kwargs):
#         if 'video' not in request.FILES:
#             return Response({'status': 'error', 'message': 'No video provided'}, status=400)

#         file_obj = request.FILES['video']
#         file_name = default_storage.save(file_obj.name, file_obj)
#         file_path = os.path.join(settings.MEDIA_ROOT, file_name)

#         try:
#             # We use the basic analyzer for uploads (Fast counting)
#             # If you want OCR on uploads too, you'd need to modify TrafficAnalyzer class.
#             # For now, let's keep uploads fast and focused on counting.
#             analyzer = TrafficAnalyzer() 
#             counts = analyzer.run_surveillance(file_path) 
#             return Response({'status': 'success', 'message': 'Analysis Complete', 'results': counts})
#         except Exception as e:
#             print(f"Server Error: {e}")
#             return Response({'status': 'error', 'message': str(e)}, status=500)

# # --- 2. LIVE VIDEO FEED WITH SPEED & LICENSE PLATES ---
# class LiveVideoFeed(APIView):
#     def get(self, request):
#         ##target_url = "https://www.youtube.com/watch?v=1EiC9bvVGnk"
#         target_url = "https://www.youtube.com/watch?v=Uuaemo4RwFU"
#         return StreamingHttpResponse(self.gen_frames(target_url), content_type='multipart/x-mixed-replace; boundary=frame')

#     def gen_frames(self, youtube_url):
#         print(f"DEBUG: Connecting to {youtube_url}")
        
#         # 1. Extract URL
#         ydl_opts = {'format': 'best', 'noplaylist': True, 'quiet': True}
#         try:
#             with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#                 info = ydl.extract_info(youtube_url, download=False)
#                 video_url = info.get('url', None)
#         except Exception as e:
#             print(f"ERROR: yt-dlp failed: {e}")
#             return

#         if not video_url: return

#         # 2. Initialize Models
#         cap = cv2.VideoCapture(video_url)
#         print("DEBUG: Loading YOLOv8 Nano...")
#         model = YOLO('yolov8n.pt') 

#         # 3. Tracking Variables
#         track_history = {} 
#         frame_count = 0 
#         CLASS_NAMES = {2: 'Car', 3: 'Bike', 5: 'Bus', 7: 'Truck'}

#         while True:
#             success, frame = cap.read()
#             if not success: break
#             frame_count += 1

#             # Resize (Critical for speed)
#             frame = cv2.resize(frame, (640, 360))
            
#             # Run YOLO
#             results = model.track(frame, persist=True, verbose=False, classes=[2, 3, 5, 7], conf=0.3)
            
#             if results[0].boxes.id is not None:
#                 boxes = results[0].boxes.xyxy.cpu().numpy()
#                 track_ids = results[0].boxes.id.int().cpu().tolist()
#                 clss = results[0].boxes.cls.int().cpu().tolist()

#                 for box, track_id, cls in zip(boxes, track_ids, clss):
#                     x1, y1, x2, y2 = map(int, box)
#                     cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
#                     class_name = CLASS_NAMES.get(cls, 'Vehicle')

#                     # A. Speed Logic
#                     speed_label = ""
#                     if track_id in track_history:
#                         prev_cx, prev_cy, prev_time = track_history[track_id]
#                         curr_time = time.time()
#                         distance = math.sqrt((cx - prev_cx)**2 + (cy - prev_cy)**2)
#                         time_diff = curr_time - prev_time
                        
#                         if time_diff > 0:
#                             ppm = 5 + (cy / 30) 
#                             speed_kmh = ((distance / ppm) / time_diff) * 3.6
#                             if speed_kmh > 3: 
#                                 speed_label = f"{int(speed_kmh)} km/h"
                    
#                     track_history[track_id] = (cx, cy, time.time())

#                     # B. LICENSE PLATE LOGIC (OCR)
#                     # Optimization: Only run OCR every 30 frames AND only on Cars/Trucks
#                     plate_text = ""
#                     if frame_count % 30 == 0 and cls in [2, 7]: 
#                         try:
#                             # 1. Crop the Vehicle
#                             roi = frame[max(0,y1):min(y2,360), max(0,x1):min(x2,640)]
                            
#                             # 2. Simple Image Processing (sharpening for text)
#                             gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                            
#                             # 3. Pass to EasyOCR
#                             # 'allowlist' speeds it up by only looking for numbers/uppercase
#                             ocr_result = reader.readtext(gray, detail=0, allowlist='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')
                            
#                             if len(ocr_result) > 0:
#                                 plate_text = ocr_result[0] # Take first detected text
#                                 print(f"PLATE DETECTED: {plate_text}")
#                         except Exception as e:
#                             pass

#                     # C. Draw
#                     color = (0, 255, 0)
#                     label = f"{class_name} {speed_label}"
#                     if plate_text:
#                         label += f" [{plate_text}]"
#                         color = (255, 0, 255) # Purple if plate found

#                     cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
#                     cv2.putText(frame, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

#             # Encode and Yield
#             ret, buffer = cv2.imencode('.jpg', frame)
#             if ret:
#                 yield (b'--frame\r\n'
#                        b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        
#         cap.release()  
###-------------------------------------------------------------------------------------------------------------------------------------------
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.storage import default_storage
from django.conf import settings
from django.http import StreamingHttpResponse
import os
import cv2
import yt_dlp
import math
import time
import easyocr
import numpy as np
from ultralytics import YOLO
from .ml_logic import TrafficAnalyzer

# --- INITIALIZE OCR READER ---
print("DEBUG: Loading OCR Model...")
reader = easyocr.Reader(['en'], gpu=False) 

# --- 1. EXISTING VIDEO UPLOAD VIEW ---
class VideoUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        if 'video' not in request.FILES:
            return Response({'status': 'error', 'message': 'No video provided'}, status=400)

        file_obj = request.FILES['video']
        file_name = default_storage.save(file_obj.name, file_obj)
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)

        try:
            analyzer = TrafficAnalyzer() 
            counts = analyzer.run_surveillance(file_path) 
            return Response({'status': 'success', 'message': 'Analysis Complete', 'results': counts})
        except Exception as e:
            print(f"Server Error: {e}")
            return Response({'status': 'error', 'message': str(e)}, status=500)

# --- 2. LIVE VIDEO FEED (With Helmet & OCR) ---
class LiveVideoFeed(APIView):
    def get(self, request):
        # Jackson Hole Live Stream (Stable)
        #target_url = "https://www.youtube.com/watch?v=1EiC9bvVGnk"
        #target_url = "https://www.youtube.com/watch?v=Uuaemo4RwFU"
        target_url="https://www.youtube.com/watch?v=rnXIjl_Rzy4"
        return StreamingHttpResponse(self.gen_frames(target_url), content_type='multipart/x-mixed-replace; boundary=frame')

    def gen_frames(self, youtube_url):
        print(f"DEBUG: Connecting to {youtube_url}")
        
        ydl_opts = {'format': 'best', 'noplaylist': True, 'quiet': True}
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(youtube_url, download=False)
                video_url = info.get('url', None)
        except Exception as e:
            print(f"ERROR: yt-dlp failed: {e}")
            return

        if not video_url: return

        # Initialize Video
        cap = cv2.VideoCapture(video_url)
        
        # --- LOAD MODELS ---
        print("DEBUG: Loading YOLOv8 Nano (Vehicles)...")
        vehicle_model = YOLO('yolov8n.pt') 
        
        helmet_model = None
        helmet_classes = {} # To store mapping like {0: 'helmet', 1: 'head'}

        if os.path.exists('best_helmet.pt'):
            try:
                print("DEBUG: Loading Helmet Model (best_helmet.pt)...")
                helmet_model = YOLO('best_helmet.pt')
                print(f"DEBUG: Helmet Classes found: {helmet_model.names}")
                helmet_classes = helmet_model.names
            except Exception as e:
                print(f"!! HELMET MODEL ERROR: {e}")
        else:
            print("!! WARNING: best_helmet.pt not found. Helmet detection disabled.")

        track_history = {} 
        frame_count = 0 
        CLASS_NAMES = {2: 'Car', 3: 'Bike', 5: 'Bus', 7: 'Truck'}

        while True:
            success, frame = cap.read()
            if not success: break
            frame_count += 1

            # Resize (1020x600 for better OCR/Helmet accuracy)
            frame = cv2.resize(frame, (1020, 600))
            
            # Run Vehicle Detection
            results = vehicle_model.track(frame, persist=True, verbose=False, classes=[2, 3, 5, 7], conf=0.25)
            
            if results[0].boxes.id is not None:
                boxes = results[0].boxes.xyxy.cpu().numpy()
                track_ids = results[0].boxes.id.int().cpu().tolist()
                clss = results[0].boxes.cls.int().cpu().tolist()

                for box, track_id, cls in zip(boxes, track_ids, clss):
                    x1, y1, x2, y2 = map(int, box)
                    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                    class_name = CLASS_NAMES.get(cls, 'Vehicle')

                    # Speed Calculation
                    speed_label = ""
                    if track_id in track_history:
                        prev_cx, prev_cy, prev_time = track_history[track_id]
                        curr_time = time.time()
                        distance = math.sqrt((cx - prev_cx)**2 + (cy - prev_cy)**2)
                        time_diff = curr_time - prev_time
                        
                        if time_diff > 0:
                            ppm = 6 + (cy / 40) 
                            speed_kmh = ((distance / ppm) / time_diff) * 3.6
                            if speed_kmh > 3: 
                                speed_label = f"{int(speed_kmh)} km/h"
                    
                    track_history[track_id] = (cx, cy, time.time())

                    # --- LICENSE PLATE OCR (Every 15 frames) ---
                    plate_text = ""
                    if frame_count % 15 == 0 and cls in [2, 7]: # Cars & Trucks
                        try:
                            roi = frame[max(0,y1):min(y2,600), max(0,x1):min(x2,1020)]
                            gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                            gray = cv2.bilateralFilter(gray, 11, 17, 17)
                            ocr_result = reader.readtext(gray, detail=0, allowlist='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')
                            if len(ocr_result) > 0:
                                best_text = max(ocr_result, key=len)
                                if len(best_text) > 3:
                                    plate_text = best_text
                                    print(f">>> OCR FOUND: {plate_text}")
                        except: pass

                    # --- HELMET DETECTION LOGIC ---
                    color = (0, 255, 0) # Default Green
                    label = f"{class_name} {speed_label}"
                    
                    if cls == 3: # If it's a Bike
                        color = (0, 165, 255) # Orange (Unknown status)
                        
                        if helmet_model:
                            # Crop the Biker
                            roi = frame[max(0,y1):min(y2,600), max(0,x1):min(x2,1020)]
                            if roi.size > 0:
                                try:
                                    # Run Helmet Model on Crop
                                    #h_results = helmet_model.predict(roi, verbose=False, conf=0.4)
                                    h_results = helmet_model.predict(roi, verbose=False, conf=0.15)
                                    # Analyze results
                                    helmet_detected = False
                                    for h_box in h_results[0].boxes:
                                        cls_id = int(h_box.cls[0])
                                        cls_name = helmet_classes.get(cls_id, '').lower()
                                        
                                        # Check if the detected class is "helmet"
                                        if 'helmet' in cls_name and 'no' not in cls_name:
                                            helmet_detected = True
                                            break
                                    
                                    if helmet_detected:
                                        label += " [Helmet]"
                                        color = (0, 255, 0) # Green
                                    elif len(h_results[0].boxes) > 0: 
                                        # Objects found but NOT helmet (likely 'head' or 'no-helmet')
                                        label += " [No Helmet]"
                                        color = (0, 0, 255) # Red
                                        
                                except Exception as e: 
                                    pass
                    
                    if plate_text:
                        label += f" [{plate_text}]"
                        color = (255, 0, 255) # Purple for Plate

                    # Draw Box & Label
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(frame, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

            # Encode
            ret, buffer = cv2.imencode('.jpg', frame)
            if ret:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        
        cap.release()