# Project Structure Guide

## 📁 Complete Project Structure

```
face-recognition-attendance/
│
├── 📄 Main Program File
│   └── face_recognition_ui.py          # The entire application (1200+ lines)
│
├── 📄 Configuration Files
│   ├── requirements.txt                # Python libraries needed
│   └── students.csv                    # Student name and ID database
│
├── 📁 Data Folders
│   ├── known_faces/                    # Registered face images
│   │   ├── encodings.pkl              # Cached face encodings (auto-generated)
│   │   ├── README.txt                 # Instructions for adding faces
│   │   └── *.jpg                      # Face photos (e.g., John.jpg, Mary.jpg)
│   │
│   ├── attendance_records/             # Attendance CSV files
│   │   └── YYYYMMDD_HHMM_SessionName.csv
│   │
│   └── models/                         # AI models for face detection
│       ├── deploy.prototxt            # Model architecture
│       └── res10_300x300_ssd_iter_140000.caffemodel  # Model weights
│
└── 📚 Documentation Files
    ├── README.md                       # Main readme
    ├── README_FOR_BEGINNERS.md         # Beginner's guide
    └── PROJECT_STRUCTURE_GUIDE.md      # This file
```

---

## 📄 File Descriptions

### Main Program File

**face_recognition_ui.py** (1200+ lines)
- **Purpose:** The entire application in one file
- **Contains:**
  - User interface code
  - Face recognition logic
  - Attendance tracking
  - Session management
  - Student database management
- **Run with:** `python face_recognition_ui.py`

### Configuration Files

**requirements.txt**
- **Purpose:** Lists all Python libraries needed
- **Contents:**
  ```
  cmake>=3.25.0
  numpy>=1.26.0
  opencv-python>=4.8.0
  dlib>=19.24.0
  face-recognition>=1.3.0
  ```
- **Used for:** Installation (`pip install -r requirements.txt`)

**students.csv**
- **Purpose:** Database of student names and IDs
- **Format:**
  ```csv
  name,student_id
  John Smith,12345
  Mary Johnson,67890
  ```
- **Can edit with:** Excel, Notepad, any text editor
- **Auto-created:** If doesn't exist

---

## 📁 Folder Descriptions

### known_faces/

**Purpose:** Stores registered face images and cache

**Files inside:**

1. **Person photos** (e.g., John.jpg, Mary.jpg)
   - Format: PersonName.jpg
   - Multiple photos per person allowed (John.jpg, John2.jpg, John3.jpg)
   - Supported formats: .jpg, .jpeg, .png, .bmp

2. **encodings.pkl**
   - Auto-generated cache file
   - Stores face encodings for faster loading
   - Binary file (can't read with text editor)
   - Safe to delete (will be regenerated)

3. **README.txt**
   - Instructions for adding face photos manually
   - Explains naming convention

**Size:** Grows with number of registered people (~100KB per person)

### attendance_records/

**Purpose:** Stores attendance session records

**File naming:** `YYYYMMDD_HHMM_SessionName.csv`
- YYYY = Year (e.g., 2025)
- MM = Month (e.g., 11)
- DD = Day (e.g., 29)
- HH = Hour (e.g., 14)
- MM = Minute (e.g., 30)
- SessionName = Your session name (e.g., MathClass)

**Example:** `20251129_1430_MathClass.csv`

**File format:**
```csv
session_name,date,time,person,student_id,confidence
Math Class,2025-11-29,14:30:15,John Smith,12345,95.2%
Math Class,2025-11-29,14:30:20,Mary Johnson,67890,92.8%
```

**Can open with:** Excel, Google Sheets, any CSV reader

**Size:** Small (~1KB per session)

### models/

**Purpose:** Contains AI models for face detection

**Files:**

1. **deploy.prototxt** (~28 KB)
   - Model architecture definition
   - Describes how the neural network is structured

2. **res10_300x300_ssd_iter_140000.caffemodel** (~10 MB)
   - Pre-trained model weights
   - The "brain" that detects faces

**Important:** 
- Don't delete these files!
- Auto-downloaded if missing
- Used by OpenCV for face detection

---

## 🔄 Data Flow Diagram

### Registration Flow
```
User clicks "Register New Person"
        ↓
Camera captures video
        ↓
User presses SPACE
        ↓
Face detected in frame
        ↓
Face image extracted and saved
        ↓
User enters name and ID
        ↓
Saved to known_faces/Name.jpg
        ↓
Added to students.csv
        ↓
Face encoding generated
        ↓
Cached in encodings.pkl
```

### Recognition Flow
```
User clicks "Start Recognition"
        ↓
Camera captures video frames
        ↓
Each frame processed:
  ├─> Face detected
  ├─> Face encoding generated
  ├─> Compared with known encodings
  └─> Best match found
        ↓
If match found:
  ├─> Name displayed on screen
  ├─> Welcome message shown
  ├─> Added to recognition history
  └─> If session active: marked present
```

### Attendance Flow
```
User starts session
        ↓
CSV file created in attendance_records/
        ↓
Recognition mode active
        ↓
Person recognized
        ↓
Check if already marked present
        ↓
If not present:
  ├─> Add to present list
  ├─> Write to CSV file
  └─> Update display
        ↓
User ends session
        ↓
CSV file closed
```

---

## 💾 Data Storage Details

### How Face Data is Stored

1. **Original Image**
   - Location: `known_faces/Name.jpg`
   - Format: JPEG image
   - Size: ~50-200 KB per image
   - Used for: Display, re-encoding

2. **Face Encoding**
   - Location: `known_faces/encodings.pkl`
   - Format: Binary pickle file
   - Size: ~1 KB per face
   - Used for: Fast recognition
   - Contains: 128-dimensional face vectors

3. **Student Info**
   - Location: `students.csv`
   - Format: CSV text file
   - Size: ~50 bytes per student
   - Used for: Name-to-ID mapping

### How Attendance is Stored

**File:** `attendance_records/YYYYMMDD_HHMM_SessionName.csv`

**Columns:**
- `session_name` - Name of the session
- `date` - Date in YYYY-MM-DD format
- `time` - Time in HH:MM:SS format
- `person` - Person's name
- `student_id` - Student ID number
- `confidence` - Recognition confidence (0-100%)

**Example row:**
```
Math Class,2025-11-29,14:30:15,John Smith,12345,95.2%
```

---

## 🔧 File Lifecycle

### When Program Starts

1. **Check folders exist**
   - Creates `known_faces/` if missing
   - Creates `attendance_records/` if missing

2. **Load face encodings**
   - Tries to load `encodings.pkl` (fast)
   - If missing/corrupt: loads from images (slow)

3. **Load student info**
   - Reads `students.csv`
   - Creates empty file if missing

4. **Initialize camera**
   - Opens camera device
   - Starts video feed

### During Registration

1. **Capture face image**
   - Extract face from video frame
   - Add padding around face

2. **Save image**
   - Find unique filename (Name.jpg, Name2.jpg, etc.)
   - Save to `known_faces/`

3. **Update student info**
   - Add/update entry in `students.csv`

4. **Rebuild cache**
   - Generate face encoding
   - Save to `encodings.pkl`

### During Recognition

1. **Process video frames**
   - Detect faces in frame
   - Generate face encodings
   - Compare with known encodings

2. **Log recognition**
   - Add to in-memory history
   - Display on screen

3. **Mark attendance** (if session active)
   - Check if already present
   - If new: write to CSV file
   - Update present list

### When Program Closes

1. **Release camera**
   - Stops video capture
   - Frees camera for other apps

2. **Save any pending data**
   - Ensures all CSV writes complete

3. **Clean up**
   - Close all files
   - Exit gracefully

---

## 📊 Storage Requirements

### Minimum Space Needed

| Component | Size | Notes |
|-----------|------|-------|
| Program files | ~50 KB | Python code |
| Models | ~10 MB | Face detection AI |
| Python libraries | ~500 MB | Installed once |
| **Total minimum** | **~510 MB** | Before any data |

### Per User Data

| Data Type | Size per Person | Example (100 people) |
|-----------|----------------|---------------------|
| Face images | ~100 KB | ~10 MB |
| Face encodings | ~1 KB | ~100 KB |
| Student info | ~50 bytes | ~5 KB |
| **Total per person** | **~101 KB** | **~10 MB** |

### Per Session Data

| Data Type | Size | Notes |
|-----------|------|-------|
| Attendance CSV | ~1 KB | ~50 bytes per student |
| Example: 30 students | ~1.5 KB | Very small |

### Growth Estimates

**For a school with 500 students:**
- Face data: ~50 MB
- 1 year of daily attendance (200 days): ~300 KB
- **Total: ~50 MB** (very manageable!)

---

## 🔐 File Permissions

### Read-Only Files
- `models/` - Don't modify
- `requirements.txt` - Don't modify

### Read-Write Files
- `face_recognition_ui.py` - Can modify (advanced users)
- `students.csv` - Can edit manually
- `known_faces/` - Can add/remove images
- `attendance_records/` - Can view/export

### Auto-Generated Files
- `encodings.pkl` - Auto-created, safe to delete
- Attendance CSVs - Auto-created during sessions

---

## 🗂️ Backup Recommendations

### Essential Files (Must Backup)
✅ `known_faces/*.jpg` - Face images
✅ `students.csv` - Student database
✅ `attendance_records/*.csv` - Attendance records

### Optional Files (Can Regenerate)
⚠️ `encodings.pkl` - Can rebuild from images
⚠️ `models/` - Can re-download

### Don't Need to Backup
❌ `__pycache__/` - Python cache
❌ `.venv/` - Virtual environment

---

## 📈 Scalability

### Small Scale (1-50 people)
- Works perfectly
- Fast recognition
- No performance issues

### Medium Scale (50-200 people)
- Still works well
- Slightly slower recognition
- May need better computer

### Large Scale (200+ people)
- May be slow
- Consider database instead of CSV
- Consider server-based solution

---

## 🔄 File Maintenance

### Regular Tasks

**Weekly:**
- Check attendance records folder
- Export important CSVs to backup

**Monthly:**
- Review registered people
- Remove old/unused faces
- Clean up attendance records

**As Needed:**
- Delete `encodings.pkl` and rebuild if issues
- Update `students.csv` for new students
- Archive old attendance records

### Troubleshooting Files

**If recognition is slow:**
1. Delete `encodings.pkl`
2. Restart program (rebuilds cache)

**If student IDs are wrong:**
1. Edit `students.csv` in Excel
2. Save file
3. Restart program

**If faces not recognized:**
1. Check `known_faces/` folder
2. Ensure images are clear
3. Add more photos per person

---

## 📝 Summary

### Key Points

1. **One main file:** `face_recognition_ui.py` contains everything
2. **Three data folders:** known_faces, attendance_records, models
3. **Two config files:** requirements.txt, students.csv
4. **Auto-generated:** encodings.pkl, attendance CSVs
5. **Small storage:** ~50 MB for 500 people
6. **Easy backup:** Just copy known_faces and attendance_records

### File Hierarchy

```
Most Important:
  1. face_recognition_ui.py (the program)
  2. known_faces/ (face images)
  3. students.csv (student data)
  4. attendance_records/ (attendance data)

Important:
  5. requirements.txt (for installation)
  6. models/ (for face detection)

Auto-Generated:
  7. encodings.pkl (cache)
  8. __pycache__/ (Python cache)
```

Now you understand the complete project structure! 🎉
