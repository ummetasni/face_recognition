# Project Structure

## 📁 Complete File Tree

```
face-recognition-attendance/
│
├── 📄 face_recognition_ui.py          ⭐ Main application (redesigned)
├── 📄 requirements.txt                 Dependencies list
├── 📄 students.csv                     Student ID database
├── 📄 run.bat                          Windows launcher
│
├── 📚 Documentation/
│   ├── README.md                       Quick start guide
│   ├── QUICK_REFERENCE.md              Command reference
│   ├── UI_DESIGN.md                    Design documentation
│   ├── CHANGELOG.md                    Version history
│   ├── REDESIGN_SUMMARY.md             Redesign overview
│   ├── PROJECT_STRUCTURE.md            This file
│   └── FACE_RECOGNITION_UI.md          Original documentation
│
├── 📁 known_faces/                     Registered face images
│   ├── encodings.pkl                   Cached face encodings
│   ├── README.txt                      Instructions
│   └── *.jpg                           Face photos
│
├── 📁 attendance_records/              Session attendance logs
│   └── YYYYMMDD_HHMM_SessionName.csv  Attendance CSVs
│
├── 📁 models/                          Face detection models
│   ├── deploy.prototxt                 Model architecture
│   └── res10_300x300_ssd_iter_140000.caffemodel  Model weights
│
└── 📁 .venv/                           Python virtual environment
```

## 📄 File Descriptions

### Core Application

| File | Purpose | Status |
|------|---------|--------|
| `face_recognition_ui.py` | Main GUI application | ⭐ Redesigned |
| `requirements.txt` | Python dependencies | ✓ Unchanged |
| `run.bat` | Windows launcher script | ⭐ New |

### Documentation

| File | Purpose | Audience |
|------|---------|----------|
| `README.md` | Quick start guide | All users |
| `QUICK_REFERENCE.md` | Command reference | End users |
| `UI_DESIGN.md` | Design documentation | Developers |
| `CHANGELOG.md` | Version history | All users |
| `REDESIGN_SUMMARY.md` | Redesign overview | All users |
| `PROJECT_STRUCTURE.md` | This file | Developers |
| `FACE_RECOGNITION_UI.md` | Original docs | Reference |

### Data Files

| File/Folder | Purpose | Format |
|-------------|---------|--------|
| `students.csv` | Student ID mapping | CSV |
| `known_faces/` | Face images | JPG/PNG |
| `known_faces/encodings.pkl` | Face encoding cache | Pickle |
| `attendance_records/` | Attendance logs | CSV |

### Models

| File | Purpose | Size |
|------|---------|------|
| `deploy.prototxt` | Model architecture | ~28 KB |
| `res10_300x300_ssd_iter_140000.caffemodel` | Model weights | ~10 MB |

## 🗂️ Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    Face Registration                         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    Capture face image
                              │
                              ▼
                    Save to known_faces/
                              │
                              ▼
                    Generate face encoding
                              │
                              ▼
                    Cache in encodings.pkl
                              │
                              ▼
                    Save student info to students.csv

┌─────────────────────────────────────────────────────────────┐
│                    Face Recognition                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    Load encodings from cache
                              │
                              ▼
                    Detect faces in video frame
                              │
                              ▼
                    Match against known encodings
                              │
                              ▼
                    Display results on screen
                              │
                              ▼
                    Log to recognition history
                              │
                              ▼
                    Mark attendance (if session active)
                              │
                              ▼
                    Write to attendance CSV
```

## 📊 File Sizes (Approximate)

| Category | Size |
|----------|------|
| Application code | ~15 KB |
| Documentation | ~50 KB |
| Models | ~10 MB |
| Dependencies | ~500 MB (installed) |
| Face images | ~100 KB per photo |
| Attendance records | ~1 KB per session |

## 🔄 File Lifecycle

### Face Images
1. **Created**: When user registers new person
2. **Read**: On app startup (to build cache)
3. **Cached**: In `encodings.pkl` for faster loading
4. **Updated**: When new photos added
5. **Deleted**: Manually by user (if needed)

### Attendance Records
1. **Created**: When session starts
2. **Written**: Each time person recognized
3. **Closed**: When session ends
4. **Archived**: Kept permanently for records

### Cache Files
1. **Created**: First time faces loaded
2. **Read**: On every app startup
3. **Updated**: When new faces registered
4. **Rebuilt**: When "Rebuild Cache" clicked

## 🎯 Important Paths

### For Users
- **Launch**: `run.bat` or `python face_recognition_ui.py`
- **Add faces**: Put images in `known_faces/`
- **View attendance**: Check `attendance_records/`
- **Student IDs**: Edit `students.csv`

### For Developers
- **Main code**: `face_recognition_ui.py`
- **Dependencies**: `requirements.txt`
- **Design docs**: `UI_DESIGN.md`
- **API reference**: `FACE_RECOGNITION_UI.md`

## 🔒 File Permissions

### Read-Only
- `models/` - Pre-trained models
- `requirements.txt` - Dependency list

### Read-Write
- `known_faces/` - Face images and cache
- `attendance_records/` - Attendance logs
- `students.csv` - Student database

### Executable
- `run.bat` - Windows launcher
- `face_recognition_ui.py` - Python script

## 🗑️ Removed Files

The following files were removed during redesign:

| File | Reason |
|------|--------|
| `main.py` | Replaced by redesigned UI |
| `main_opencv_only.py` | Not needed for main app |

## 📦 Backup Recommendations

### Essential Files
- ✅ `known_faces/` - All face images
- ✅ `students.csv` - Student database
- ✅ `attendance_records/` - All attendance logs

### Optional Files
- ⚠️ `known_faces/encodings.pkl` - Can be rebuilt
- ⚠️ `models/` - Can be re-downloaded

### Not Needed
- ❌ `.venv/` - Virtual environment
- ❌ `__pycache__/` - Python cache
- ❌ `.idea/` - IDE settings

## 🔄 Version Control

### Include in Git
```
face_recognition_ui.py
requirements.txt
students.csv (template)
README.md
*.md (all documentation)
run.bat
known_faces/README.txt
```

### Exclude from Git (.gitignore)
```
.venv/
__pycache__/
.idea/
known_faces/*.jpg
known_faces/*.pkl
attendance_records/*.csv
models/*.caffemodel
```

## 📈 Growth Estimates

### Storage Requirements

| Users | Face Images | Attendance | Total |
|-------|-------------|------------|-------|
| 10 | ~1 MB | ~10 KB/month | ~1 MB |
| 50 | ~5 MB | ~50 KB/month | ~5 MB |
| 100 | ~10 MB | ~100 KB/month | ~10 MB |
| 500 | ~50 MB | ~500 KB/month | ~50 MB |

*Note: Excludes models (~10 MB) and dependencies (~500 MB)*

## 🎓 Usage Patterns

### Typical Session
1. Launch app (reads cache)
2. Start session (creates CSV)
3. Recognize faces (writes to CSV)
4. End session (closes CSV)
5. Close app (releases camera)

### File Access Frequency
- **High**: `encodings.pkl`, video feed
- **Medium**: `students.csv`, attendance CSVs
- **Low**: face images, models
- **Once**: documentation files

---

**Last Updated**: 2025-11-29
**Version**: 2.0 (Modern Redesign)
