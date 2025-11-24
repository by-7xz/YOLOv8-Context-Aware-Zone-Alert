# YOLOv8-Context-Aware-Zone-Alert

**Contextual Object Entry Alert System based on YOLOv8**

This Program detects a target object(e.g., Cell Phone, Bottle, Cup) entering a defined boundary (ROI) **Only when human presence is confirmed in the frame.** This logic minimizes false positives caused by animals or wind etc.

![Python](https://img.shields.io/badge/Python-3.11-blue) ![YOLOv8](https://img.shields.io/badge/AI-YOLOv8-green) ![License](https://img.shields.io/badge/License-GPLv3-red)

## Features

- **Context-Aware Detection:**  Triggers alarm only when `Person` + `Target` are detected simultaneously.
- **ROI (Region of Interest) Interaction:** Detects when the target object enters the specific zone (e.g., Crosswalk(when target is phone), etc.).
- **Real-time Monitoring:** Supports Every Webcams(default 1080p)
- **Auto-Latch Alarm:** Alarm persists for a set duration (default 3s) even if the object disappears quickly.

## Requirements

- Python 3.10 or 3.11 (Worked on 3.11.9)
- NVIDIA GPU (Recommended for performance, You can try without it)
- Any Webcam
- CUDA (If you use GPU)

## Installation

1. **Clone the repository**
    ```bash
    git clone [https://github.com/by-7xz/YOLOv8-Context-Aware-Zone-Alert.git](https://github.com/by-7xz/YOLOv8-Context-Aware-Zone-Alert.git)
    cd YOLOv8-Context-Aware-Zone-Alert

2. **Instqall Pytorch (Important for RTX50 Users)**
    If you are using RTX 50 Series, or Newer, You must install cu128 or Newer:
    ``pip install --pre torch torchvision torchaudio --index-url [https://download.pytorch.org/whl/cu128](https://download.pytorch.org/whl/cu128)

    For other GPU, Install standard version:
    pip install torch torchvision --index-url [https://download.pytorch.org/whl/cu126](https://download.pytorch.org/whl/cu126)
    
    For CPU, Install CPU Version
    pip install torch torchvision

4. **Install Dependencies**
    pip install =r requirements.txt

## Usage
Run check gpu and check cuda status:
python check_gpu.py

Run main script:
python main.py

Controls
* Drag Mouse For set ROI
* 'S' Key : Start Detection (Set ROI)
* 'R' Key : Reset ROI
* 'Q' Key : Quit Program

## License
This project is licensed under the GPLv3 License - see the LICENSE file for details
