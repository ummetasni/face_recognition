# Quick Reference Guide

## 🚀 Launch Application

**Windows:**
```bash
run.bat
```

**Mac/Linux:**
```bash
python face_recognition_ui.py
```

## 🎯 Main Actions

### Register New Person
1. Click **"➕ Register New Person"**
2. Position face in camera
3. Press **SPACE** to capture
4. Enter **Full Name**
5. Enter **Student ID**
6. Click **"💾 Save Face"**

### Start Recognition
1. Click **"🔍 Start Recognition"**
2. System detects faces automatically
3. Green box = Known person
4. Red box = Unknown person

### Manage Session
1. Enter session name (e.g., "Class A")
2. Click **"▶ Start"**
3. Recognition auto-marks attendance
4. Click **"⏸ End"** when done

### Stop Current Mode
- Click **"⏹ Stop"** anytime

## ⌨️ Keyboard Shortcuts

| Key | Action |
|-----|--------|
| **SPACE** | Capture face (in registration mode) |

## 📊 Understanding the Interface

### Header Stats
- **Registered**: Total unique people registered
- **Present**: Students marked present in current session
- **Session**: Active/Inactive status

### Camera Feed (Left)
- Live video from webcam
- Face detection boxes
- Welcome overlay for recognized faces

### Controls (Middle)
- **Actions**: Main mode buttons
- **Session**: Start/end attendance sessions
- **Register**: Form for new person (when capturing)
- **Status**: Current mode and messages

### Data Display (Right)
- **History**: Recent recognition events
- **Present**: Students in current session
- **People**: All registered individuals

## 🎨 Visual Indicators

### Face Detection Boxes
- 🟢 **Green**: Known person (recognized)
- 🔴 **Red**: Unknown person

### Button Colors
- 🔵 **Blue**: Primary actions (Register, Recognize)
- 🟢 **Cyan**: Success actions (Start, Save)
- 🔴 **Red**: Stop/End actions

### Session Status
- 🟢 **Active**: Session running
- ⚪ **Inactive**: No session

## 📁 File Locations

### Input Files
- `known_faces/*.jpg` - Registered face photos
- `students.csv` - Student ID database

### Output Files
- `attendance_records/*.csv` - Session attendance logs
- `known_faces/encodings.pkl` - Face encoding cache

## 🔧 Common Tasks

### Add Multiple Photos for One Person
1. Register person first time: `John.jpg`
2. Register same person again: `John2.jpg`
3. System automatically numbers duplicates
4. More photos = better accuracy

### View Attendance Records
1. Open `attendance_records/` folder
2. Files named: `YYYYMMDD_HHMM_SessionName.csv`
3. Open in Excel or any CSV viewer

### Check Who's Registered
- Look at **"Registered People"** list (bottom right)
- Shows: Name (ID: xxx) - N photo(s)

### Clear Recognition History
- History auto-clears after 50 entries
- Restart app to clear completely

## ⚠️ Troubleshooting

### Camera Not Working
- Close other apps using camera
- Check camera permissions
- Try restarting application

### Face Not Detected
- Ensure good lighting
- Face camera directly
- Move closer to camera
- Remove glasses/hat if needed

### Low Recognition Accuracy
- Register multiple photos per person
- Use clear, well-lit photos
- Ensure face is clearly visible
- Try adjusting tolerance in code

### Person Not Recognized
- Check if registered (see People list)
- Try registering additional photos
- Ensure good lighting conditions
- Face camera directly

## 💡 Tips for Best Results

### Registration
- ✅ Good lighting
- ✅ Face camera directly
- ✅ Neutral expression
- ✅ Remove obstructions
- ✅ Register 2-3 photos per person

### Recognition
- ✅ Same lighting as registration
- ✅ Face camera clearly
- ✅ Stay still for a moment
- ✅ Remove glasses if not in registration photo

### Sessions
- ✅ Start session before recognition
- ✅ Use descriptive names ("Monday Class A")
- ✅ End session when done
- ✅ Check CSV file after session

## 📊 Data Format

### students.csv
```csv
name,student_id
John Doe,12345
Jane Smith,67890
```

### Attendance CSV
```csv
session_name,date,time,person,student_id,confidence
Class A,2025-11-29,14:30:15,John Doe,12345,95.2%
```

## 🎓 Workflow Example

### Typical Class Session

1. **Before Class:**
   - Launch application
   - Enter session name: "Monday Morning - Class A"
   - Click "▶ Start"

2. **During Class:**
   - Click "🔍 Start Recognition"
   - Students face camera as they enter
   - System auto-marks attendance
   - Watch "Present Students" list grow

3. **After Class:**
   - Click "⏹ Stop" (stop recognition)
   - Click "⏸ End" (end session)
   - Check attendance CSV in `attendance_records/`

4. **New Student Arrives:**
   - Click "⏹ Stop" (if recognizing)
   - Click "➕ Register New Person"
   - Capture face with SPACE
   - Enter name and ID
   - Click "💾 Save Face"
   - Click "🔍 Start Recognition" (resume)

## 🔗 More Information

- **README.md** - Installation and setup
- **UI_DESIGN.md** - Design documentation
- **CHANGELOG.md** - Version history
- **REDESIGN_SUMMARY.md** - What changed

---

**Need Help?** Check the documentation files or review error messages in the Status panel.
