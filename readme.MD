# 🚀 End-to-End Object Detection Web App — Setup & Run Guide

This guide explains **exactly how to set up and run this project after cloning the repository from GitHub**.

The project is a **full-stack, end-to-end object detection system** supporting:
- Image detection
- Video detection (browser-safe playback)
- Live webcam detection

Frontend is built with **React**, backend with **FastAPI + YOLOv8 (PyTorch)**.

---

## 📁 Repository Structure

After cloning, your repository should look like this:

```
E2E-project/
 ├── backend/
 └── frontend/
```

---

## 1️⃣ System Requirements

### Operating System
- Windows 10 / 11 (fully tested)
- Linux (Ubuntu 20.04+)
- macOS (CPU-only)

### Hardware
**Minimum:**
- 8 GB RAM
- 4-core CPU

**Recommended:**
- NVIDIA GPU (6 GB+ VRAM)
- 16 GB RAM

Webcam required for webcam mode.

---

## 2️⃣ Required Software (Install These First)

### ✅ Python
- Python **3.10 or 3.11** (recommended)

Check:
```bash
python --version
```

---

### ✅ Node.js
- Node.js **v18 or newer**

Check:
```bash
node -v
npm -v
```

Download:
https://nodejs.org/

---

### ✅ FFmpeg (MANDATORY for video playback)

#### Windows
1. Download from:
   https://www.gyan.dev/ffmpeg/builds/
2. Download **ffmpeg-release-essentials.zip**
3. Extract to:
   ```
   C:\ffmpeg
   ```
4. Add this to **System PATH**:
   ```
   C:\ffmpeg\bin
   ```
5. Verify:
   ```powershell
   ffmpeg -version
   ```

#### Linux
```bash
sudo apt install ffmpeg
```

#### macOS
```bash
brew install ffmpeg
```

---

## 3️⃣ Backend Setup (FastAPI + YOLOv8)

### Step 1: Go to Backend Folder

```bash
cd backend
```

---

### Step 2: Create Virtual Environment

```bash
python -m venv .venv
```

Activate:

**Windows**
```bash
.venv\Scripts\activate
```

**Linux / macOS**
```bash
source .venv/bin/activate
```

---

### Step 3: Install Backend Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

### Step 4: Install PyTorch

#### CPU-only
```bash
pip install torch torchvision torchaudio
```

#### GPU (example: CUDA 12.1)
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

Verify:
```bash
python -c "import torch; print(torch.cuda.is_available())"
```

---

### Step 5: Download YOLO Models (IMPORTANT)

Run **once** to avoid runtime download issues:

```bash
python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
python -c "from ultralytics import YOLO; YOLO('yolov8s.pt')"
python -c "from ultralytics import YOLO; YOLO('yolov8m.pt')"
python -c "from ultralytics import YOLO; YOLO('yolov8l.pt')"
```

Models are cached automatically.

---

### Step 6: Run Backend Server

```bash
uvicorn main:app --reload --port 8000
```

Verify:
- Open browser
- Go to: `http://localhost:8000/docs`
- Swagger UI should open

---

## 4️⃣ Frontend Setup (React + Vite)

### Step 1: Go to Frontend Folder

```bash
cd frontend
```

---

### Step 2: Install Dependencies

```bash
npm install
```

---

### Step 3: Run Frontend

```bash
npm run dev
```

You will see:
```
Local: http://localhost:5173/
```

Open this URL in your browser.

---

## 5️⃣ Running the Full Application

### Terminal 1 — Backend
```bash
cd backend
.venv\Scripts\activate   # Windows
uvicorn main:app --reload --port 8000
```

### Terminal 2 — Frontend
```bash
cd frontend
npm run dev
```

Both must be running at the same time.

---

## 6️⃣ How to Use the App

1. Open `http://localhost:5173`
2. Select detection mode:
   - Image
   - Video
   - Webcam
3. Select model complexity:
   - Nano (fast)
   - Small
   - Medium
   - Large (accurate)
4. Upload file or start webcam
5. View live progress and results

---

## 7️⃣ Important Behavior (By Design)

### Webcam
- Only **one webcam session** allowed
- Stops automatically when:
  - Mode changes
  - Reset is clicked
  - Job is cancelled

### Files
- Uploaded files and results are **auto-cleaned**
- No disk clutter

---

## 8️⃣ Common Issues & Fixes

### ❌ Small model (`yolov8s`) error
Cause: corrupted model file

Fix:
```bash
delete yolov8s.pt
python -c "from ultralytics import YOLO; YOLO('yolov8s.pt')"
```

---

### ❌ Video plays in VLC but not browser
Cause: FFmpeg missing

Fix:
- Install FFmpeg
- Ensure `ffmpeg -version` works

---

## 9️⃣ Project Highlights

- End-to-end ML pipeline
- Browser-safe video streaming
- Real-time webcam inference
- Clean lifecycle & resource management
- Production-style architecture

---

## ✅ You’re Ready to Go!

If everything above is completed:
- Backend runs without errors
- Frontend opens in browser
- Image / Video / Webcam detection works

🎉 **Project setup complete.**

