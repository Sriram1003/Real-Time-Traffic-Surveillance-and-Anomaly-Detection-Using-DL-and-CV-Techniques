# TrafficAI: Real-Time Traffic Surveillance System 🚦

TrafficAI is a full-stack, AI-powered traffic monitoring application. It utilizes state-of-the-art Deep Learning models to process both live camera streams and offline video footage to track vehicles, estimate speeds, and detect traffic violations in real-time.

## 🌟 Key Features

* **Adaptive Object Detection:** Seamlessly switches between **YOLOv8 Nano** (for 30 FPS low-latency live streaming) and **YOLOv8 Medium** (for high-fidelity offline video analysis).
* **Flawless Unique Counting:** Utilizes Multi-Object Tracking (MOT) paired with mathematical `set()` data structures to ensure vehicles are counted exactly once, filtering out tracking glitches and occlusion losses.
* **Dynamic Speed Estimation:** Implements a Perspective-Aware Pixel-Per-Meter (PPM) calibration slope. The system mathematically adjusts speed calculations based on depth (Y-coordinates) to account for camera perspective distortion.
* **Smart ALPR (EasyOCR):** Conditionally triggers Optical Character Recognition only when vehicles meet specific proximity and frame-modulo thresholds, saving CPU/GPU resources while capturing high-quality license plate reads.
* **Advanced Helmet Detection:** Features a custom algorithmic override that proportionally expands the bounding box of detected motorcycles by 35%. This ensures the rider's head is isolated before passing the cropped Region of Interest (ROI) to a custom-trained secondary YOLOv8 helmet model.
* **Triple Riding Detection:** Concurrently tracks pedestrians and motorcycles, utilizing spatial overlap geometry to flag instances where 3 or more human centroids fall within the boundaries of a single motorcycle.

## 🛠️ Technology Stack

**Frontend:**
* React.js
* Tailwind CSS
* Lucide Icons (UI Elements)

**Backend & AI Engine:**
* Django & Django REST Framework
* Ultralytics YOLOv8 (Nano & Medium)
* OpenCV (Computer Vision & Frame Manipulation)
* EasyOCR (Optical Character Recognition)
* yt-dlp (Live Stream Extraction)
