#!/usr/bin/env python3
"""
Modern Face Recognition Attendance System
A redesigned, clean UI for face registration and attendance tracking
"""

import csv
import cv2
import face_recognition
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import pickle
from PIL import Image, ImageTk
from typing import Optional, List, Dict
from datetime import datetime

try:
    import winsound
except ImportError:
    winsound = None


class ModernFaceRecognitionUI:
    """Modern GUI for face recognition and attendance tracking."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition Attendance System")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)
        
        # Paths
        self.known_faces_dir = Path("known_faces")
        self.known_faces_dir.mkdir(exist_ok=True)
        self.attendance_dir = Path("attendance_records")
        self.attendance_dir.mkdir(exist_ok=True)
        self.student_info_file = Path("students.csv")
        
        # Data
        self.known_face_encodings: List[np.ndarray] = []
        self.known_face_names: List[str] = []
        self.student_info: Dict[str, Dict[str, str]] = {}
        self.present_students: Dict[str, Dict] = {}
        self.recognition_history: List[dict] = []
        
        # State
        self.video_capture: Optional[cv2.VideoCapture] = None
        self.current_frame = None
        self.is_running = False
        self.mode = "idle"  # idle, register, recognize
        self.captured_face = None
        self.captured_location = None
        
        # Session
        self.session_active = False
        self.session_name = ""
        self.session_file: Optional[Path] = None
        self.session_start: Optional[datetime] = None
        
        # Settings
        self.tolerance = 0.6
        self.last_recognition = {}
        self.last_welcome = {}
        
        # Load data
        self.load_known_faces()
        self.load_student_info()
        
        # Setup UI
        self.setup_modern_ui()
        
        # Start camera
        self.start_camera()
    
    def setup_modern_ui(self):
        """Create modern, clean UI layout."""
        # Color scheme - Light theme
        self.colors = {
            'bg': '#f0f4f8',
            'card': '#ffffff',
            'accent': '#4a90e2',
            'primary': '#2563eb',
            'success': '#10b981',
            'danger': '#ef4444',
            'text': '#1f2937',
            'text_dim': '#6b7280'
        }
        
        self.root.configure(bg=self.colors['bg'])
        
        # Configure styles
        style = ttk.Style()
        style.theme_use('clam')
        
        # Main container with padding
        main_container = tk.Frame(self.root, bg=self.colors['bg'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        self.create_header(main_container)
        
        # Content area (3 columns)
        content = tk.Frame(main_container, bg=self.colors['bg'])
        content.pack(fill=tk.BOTH, expand=True, pady=(20, 0))
        
        # Left panel - Camera feed
        self.create_camera_panel(content)
        
        # Middle panel - Controls
        self.create_control_panel(content)
        
        # Right panel - Data
        self.create_data_panel(content)
    
    def create_header(self, parent):
        """Create header with title and stats."""
        header = tk.Frame(parent, bg=self.colors['bg'])
        header.pack(fill=tk.X, pady=(0, 10))
        
        # Title
        title = tk.Label(
            header,
            text="🎓 Face Recognition Attendance",
            font=("Segoe UI", 28, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['primary']
        )
        title.pack(side=tk.LEFT)
        
        # Stats
        stats_frame = tk.Frame(header, bg=self.colors['bg'])
        stats_frame.pack(side=tk.RIGHT)
        
        self.stat_registered = self.create_stat_badge(stats_frame, "Registered", "0", 0)
        self.stat_present = self.create_stat_badge(stats_frame, "Present", "0", 1)
        self.stat_session = self.create_stat_badge(stats_frame, "Session", "Inactive", 2)
    
    def create_stat_badge(self, parent, label, value, col):
        """Create a stat badge."""
        frame = tk.Frame(parent, bg=self.colors['card'], padx=15, pady=8, relief=tk.SOLID, borderwidth=1, highlightbackground='#e5e7eb', highlightthickness=1)
        frame.grid(row=0, column=col, padx=5)
        
        tk.Label(
            frame,
            text=label,
            font=("Segoe UI", 9),
            bg=self.colors['card'],
            fg=self.colors['text_dim']
        ).pack()
        
        value_label = tk.Label(
            frame,
            text=value,
            font=("Segoe UI", 16, "bold"),
            bg=self.colors['card'],
            fg=self.colors['text']
        )
        value_label.pack()
        
        return value_label
    
    def create_camera_panel(self, parent):
        """Create camera feed panel."""
        panel = tk.Frame(parent, bg=self.colors['bg'])
        panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Card
        card = tk.Frame(panel, bg=self.colors['card'], padx=2, pady=2, relief=tk.SOLID, borderwidth=1, highlightbackground='#e5e7eb', highlightthickness=1)
        card.pack(fill=tk.BOTH, expand=True)
        
        # Video label
        self.video_label = tk.Label(
            card,
            text="📷 Initializing camera...",
            font=("Segoe UI", 14),
            bg='#2c3e50',
            fg='white'
        )
        self.video_label.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Overlay for messages
        self.overlay_label = tk.Label(
            self.video_label,
            text="",
            font=("Segoe UI", 18, "bold"),
            bg=self.colors['success'],
            fg='white',
            padx=30,
            pady=15
        )
    
    def create_control_panel(self, parent):
        """Create control panel with buttons and forms."""
        panel = tk.Frame(parent, bg=self.colors['bg'], width=350)
        panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))
        panel.pack_propagate(False)
        
        # Mode buttons
        self.create_card(panel, "Actions", self.create_action_buttons)
        
        # Session control
        self.create_card(panel, "Session", self.create_session_controls)
        
        # Registration form (hidden initially)
        self.register_card = self.create_card(panel, "Register Person", self.create_register_form)
        self.register_card.pack_forget()
        
        # Status
        self.create_card(panel, "Status", self.create_status_display)
    
    def create_card(self, parent, title, content_func):
        """Create a card container."""
        card = tk.Frame(parent, bg=self.colors['card'], relief=tk.SOLID, borderwidth=1, highlightbackground='#e5e7eb', highlightthickness=1)
        card.pack(fill=tk.X, pady=(0, 15))
        
        # Title
        title_frame = tk.Frame(card, bg=self.colors['accent'])
        title_frame.pack(fill=tk.X)
        
        tk.Label(
            title_frame,
            text=title,
            font=("Segoe UI", 12, "bold"),
            bg=self.colors['accent'],
            fg=self.colors['text'],
            anchor=tk.W,
            padx=15,
            pady=10
        ).pack(fill=tk.X)
        
        # Content
        content = tk.Frame(card, bg=self.colors['card'], padx=15, pady=15)
        content.pack(fill=tk.BOTH, expand=True)
        
        content_func(content)
        
        return card
    
    def create_action_buttons(self, parent):
        """Create action buttons."""
        self.btn_register = self.create_button(
            parent,
            "➕ Register New Person",
            self.start_registration,
            self.colors['primary']
        )
        self.btn_register.pack(fill=tk.X, pady=(0, 10))
        
        self.btn_recognize = self.create_button(
            parent,
            "🔍 Start Recognition",
            self.start_recognition,
            self.colors['success']
        )
        self.btn_recognize.pack(fill=tk.X, pady=(0, 10))
        
        self.btn_stop = self.create_button(
            parent,
            "⏹ Stop",
            self.stop_mode,
            self.colors['danger'],
            state=tk.DISABLED
        )
        self.btn_stop.pack(fill=tk.X)
    
    def create_button(self, parent, text, command, color, state=tk.NORMAL):
        """Create a styled button."""
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            font=("Segoe UI", 11, "bold"),
            bg=color,
            fg='white',
            activebackground=color,
            activeforeground='white',
            relief=tk.FLAT,
            cursor='hand2',
            padx=20,
            pady=12,
            state=state
        )
        return btn
    
    def create_session_controls(self, parent):
        """Create session management controls."""
        # Session name input
        tk.Label(
            parent,
            text="Session Name:",
            font=("Segoe UI", 10),
            bg=self.colors['card'],
            fg=self.colors['text_dim']
        ).pack(anchor=tk.W, pady=(0, 5))
        
        self.session_entry = tk.Entry(
            parent,
            font=("Segoe UI", 11),
            bg='white',
            fg=self.colors['text'],
            insertbackground=self.colors['text'],
            relief=tk.SOLID,
            borderwidth=1,
            highlightthickness=1,
            highlightbackground=self.colors['accent'],
            highlightcolor=self.colors['primary']
        )
        self.session_entry.insert(0, "Class A")
        self.session_entry.pack(fill=tk.X, pady=(0, 10), ipady=8)
        
        # Buttons
        btn_frame = tk.Frame(parent, bg=self.colors['card'])
        btn_frame.pack(fill=tk.X)
        
        self.btn_start_session = self.create_button(
            btn_frame,
            "▶ Start",
            self.start_session,
            self.colors['success']
        )
        self.btn_start_session.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        self.btn_end_session = self.create_button(
            btn_frame,
            "⏸ End",
            self.end_session,
            self.colors['danger'],
            state=tk.DISABLED
        )
        self.btn_end_session.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    def create_register_form(self, parent):
        """Create registration form."""
        # Name
        tk.Label(
            parent,
            text="Full Name:",
            font=("Segoe UI", 10),
            bg=self.colors['card'],
            fg=self.colors['text_dim']
        ).pack(anchor=tk.W, pady=(0, 5))
        
        self.name_entry = tk.Entry(
            parent,
            font=("Segoe UI", 11),
            bg='white',
            fg=self.colors['text'],
            insertbackground=self.colors['text'],
            relief=tk.SOLID,
            borderwidth=1
        )
        self.name_entry.pack(fill=tk.X, pady=(0, 10), ipady=8)
        
        # Student ID
        tk.Label(
            parent,
            text="Student ID:",
            font=("Segoe UI", 10),
            bg=self.colors['card'],
            fg=self.colors['text_dim']
        ).pack(anchor=tk.W, pady=(0, 5))
        
        self.student_id_entry = tk.Entry(
            parent,
            font=("Segoe UI", 11),
            bg='white',
            fg=self.colors['text'],
            insertbackground=self.colors['text'],
            relief=tk.SOLID,
            borderwidth=1
        )
        self.student_id_entry.pack(fill=tk.X, pady=(0, 15), ipady=8)
        
        # Save button
        self.btn_save = self.create_button(
            parent,
            "💾 Save Face",
            self.save_face,
            self.colors['success']
        )
        self.btn_save.pack(fill=tk.X)
        
        # Hint
        tk.Label(
            parent,
            text="Press SPACE to capture face",
            font=("Segoe UI", 9, "italic"),
            bg=self.colors['card'],
            fg=self.colors['text_dim']
        ).pack(pady=(10, 0))
    
    def create_status_display(self, parent):
        """Create status display."""
        self.status_label = tk.Label(
            parent,
            text="Ready",
            font=("Segoe UI", 10),
            bg=self.colors['card'],
            fg=self.colors['text'],
            wraplength=300,
            justify=tk.LEFT
        )
        self.status_label.pack(fill=tk.X)
    
    def create_data_panel(self, parent):
        """Create data display panel."""
        panel = tk.Frame(parent, bg=self.colors['bg'], width=400)
        panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        panel.pack_propagate(False)
        
        # Recognition history
        self.create_card(panel, "Recognition History", self.create_history_table)
        
        # Present students
        self.create_card(panel, "Present Students", self.create_attendance_list)
        
        # Registered people
        self.create_card(panel, "Registered People", self.create_people_list)
    
    def create_history_table(self, parent):
        """Create recognition history table."""
        # Scrollbar
        scroll = tk.Scrollbar(parent)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview
        self.history_tree = ttk.Treeview(
            parent,
            columns=("time", "name", "id", "conf"),
            show="headings",
            height=6,
            yscrollcommand=scroll.set
        )
        
        self.history_tree.heading("time", text="Time")
        self.history_tree.heading("name", text="Name")
        self.history_tree.heading("id", text="ID")
        self.history_tree.heading("conf", text="Confidence")
        
        self.history_tree.column("time", width=80, anchor=tk.CENTER)
        self.history_tree.column("name", width=120)
        self.history_tree.column("id", width=80, anchor=tk.CENTER)
        self.history_tree.column("conf", width=80, anchor=tk.CENTER)
        
        self.history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.config(command=self.history_tree.yview)
    
    def create_attendance_list(self, parent):
        """Create attendance list."""
        scroll = tk.Scrollbar(parent)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.attendance_list = tk.Listbox(
            parent,
            font=("Segoe UI", 10),
            bg='white',
            fg=self.colors['text'],
            selectbackground=self.colors['primary'],
            selectforeground='white',
            relief=tk.SOLID,
            borderwidth=1,
            height=6,
            yscrollcommand=scroll.set
        )
        self.attendance_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.config(command=self.attendance_list.yview)
        
        self.attendance_list.insert(0, "No students present")
    
    def create_people_list(self, parent):
        """Create registered people list."""
        scroll = tk.Scrollbar(parent)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.people_list = tk.Listbox(
            parent,
            font=("Segoe UI", 10),
            bg='white',
            fg=self.colors['text'],
            selectbackground=self.colors['primary'],
            selectforeground='white',
            relief=tk.SOLID,
            borderwidth=1,
            height=8,
            yscrollcommand=scroll.set
        )
        self.people_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.config(command=self.people_list.yview)
        
        self.update_people_list()
    
    # Data Management
    
    def load_known_faces(self, force_rebuild=False):
        """Load face encodings from cache or rebuild."""
        pickle_file = self.known_faces_dir / "encodings.pkl"
        
        if not force_rebuild and pickle_file.exists():
            try:
                with open(pickle_file, 'rb') as f:
                    data = pickle.load(f)
                    self.known_face_encodings = data['encodings']
                    self.known_face_names = data['names']
                return
            except Exception as e:
                print(f"Cache error: {e}")
        
        # Rebuild from images
        self.known_face_encodings = []
        self.known_face_names = []
        
        for ext in ['.jpg', '.jpeg', '.png', '.bmp']:
            for img_file in self.known_faces_dir.glob(f"*{ext}"):
                try:
                    name = img_file.stem
                    image = face_recognition.load_image_file(str(img_file))
                    encodings = face_recognition.face_encodings(image)
                    
                    if encodings:
                        self.known_face_encodings.append(encodings[0])
                        self.known_face_names.append(name)
                except Exception as e:
                    print(f"Error loading {img_file}: {e}")
        
        # Save cache
        if self.known_face_encodings:
            try:
                with open(pickle_file, 'wb') as f:
                    pickle.dump({
                        'encodings': self.known_face_encodings,
                        'names': self.known_face_names
                    }, f)
            except Exception as e:
                print(f"Cache save error: {e}")
    
    def load_student_info(self):
        """Load student information from CSV."""
        if not self.student_info_file.exists():
            return
        
        try:
            with open(self.student_info_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    name = row.get('name', '').strip()
                    student_id = row.get('student_id', '').strip()
                    if name:
                        self.student_info[name] = {'student_id': student_id}
        except Exception as e:
            print(f"Error loading student info: {e}")
    
    def save_student_info(self):
        """Save student information to CSV."""
        try:
            with open(self.student_info_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['name', 'student_id'])
                for name, data in sorted(self.student_info.items()):
                    writer.writerow([name, data.get('student_id', '')])
        except Exception as e:
            print(f"Error saving student info: {e}")
    
    def update_people_list(self):
        """Update registered people list."""
        self.people_list.delete(0, tk.END)
        
        unique_names = sorted(set(self.known_face_names))
        
        if not unique_names:
            self.people_list.insert(0, "No registered people")
            self.stat_registered.config(text="0")
            return
        
        for name in unique_names:
            count = self.known_face_names.count(name)
            student_id = self.student_info.get(name, {}).get('student_id', 'N/A')
            self.people_list.insert(tk.END, f"{name} (ID: {student_id}) - {count} photo(s)")
        
        self.stat_registered.config(text=str(len(unique_names)))
    
    def update_attendance_list(self):
        """Update present students list."""
        self.attendance_list.delete(0, tk.END)
        
        if not self.present_students:
            self.attendance_list.insert(0, "No students present")
            self.stat_present.config(text="0")
            return
        
        for info in sorted(self.present_students.values(), key=lambda x: x['name']):
            student_id = info.get('student_id', 'N/A')
            time_str = info.get('time', '')
            self.attendance_list.insert(
                tk.END,
                f"{info['name']} (ID: {student_id}) - {time_str}"
            )
        
        self.stat_present.config(text=str(len(self.present_students)))
    
    def add_to_history(self, name, student_id, confidence):
        """Add recognition event to history."""
        now = datetime.now()
        
        # Throttle duplicates
        key = f"{name}_{student_id}"
        if key in self.last_recognition:
            if (now - self.last_recognition[key]).total_seconds() < 2:
                return
        
        self.last_recognition[key] = now
        
        time_str = now.strftime("%H:%M:%S")
        conf_str = f"{confidence:.1f}%" if confidence else "-"
        
        self.history_tree.insert(
            "", 0,
            values=(time_str, name, student_id or "-", conf_str)
        )
        
        # Keep only last 50 entries
        children = self.history_tree.get_children()
        if len(children) > 50:
            self.history_tree.delete(children[-1])
    
    # Session Management
    
    def start_session(self):
        """Start attendance session."""
        if self.session_active:
            messagebox.showinfo("Session Active", "A session is already running.")
            return
        
        session_name = self.session_entry.get().strip()
        if not session_name:
            messagebox.showwarning("Missing Name", "Please enter a session name.")
            return
        
        self.session_active = True
        self.session_name = session_name
        self.session_start = datetime.now()
        
        # Create CSV file
        timestamp = self.session_start.strftime("%Y%m%d_%H%M")
        safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in session_name)
        self.session_file = self.attendance_dir / f"{timestamp}_{safe_name}.csv"
        
        # Write header
        with open(self.session_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['session_name', 'date', 'time', 'person', 'student_id', 'confidence'])
        
        self.present_students.clear()
        self.update_attendance_list()
        
        self.btn_start_session.config(state=tk.DISABLED)
        self.btn_end_session.config(state=tk.NORMAL)
        self.stat_session.config(text="Active", fg=self.colors['success'])
        
        self.status_label.config(text=f"Session '{session_name}' started")
        messagebox.showinfo("Session Started", f"Attendance session '{session_name}' is now active.")
    
    def end_session(self):
        """End attendance session."""
        if not self.session_active:
            return
        
        count = len(self.present_students)
        session_name = self.session_name
        
        self.session_active = False
        self.session_name = ""
        self.session_file = None
        self.session_start = None
        
        self.btn_start_session.config(state=tk.NORMAL)
        self.btn_end_session.config(state=tk.DISABLED)
        self.stat_session.config(text="Inactive", fg=self.colors['text_dim'])
        
        self.status_label.config(text=f"Session ended: {count} student(s) present")
        messagebox.showinfo("Session Ended", f"Session '{session_name}' ended.\n{count} student(s) were present.")
    
    def mark_attendance(self, name, student_id, confidence):
        """Mark student as present."""
        if not self.session_active or name == "Unknown":
            return
        
        key = student_id or name
        if key in self.present_students:
            return
        
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M:%S")
        
        self.present_students[key] = {
            'name': name,
            'student_id': student_id,
            'date': date_str,
            'time': time_str,
            'confidence': confidence
        }
        
        # Write to CSV
        if self.session_file:
            with open(self.session_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                conf_str = f"{confidence:.1f}%" if confidence else "-"
                writer.writerow([self.session_name, date_str, time_str, name, student_id or "", conf_str])
        
        self.update_attendance_list()
        self.show_welcome(name, confidence)
    
    def show_welcome(self, name, confidence):
        """Show welcome message."""
        now = datetime.now()
        
        # Throttle welcomes
        if name in self.last_welcome:
            if (now - self.last_welcome[name]).total_seconds() < 5:
                return
        
        self.last_welcome[name] = now
        
        # Show overlay
        conf_text = f" ({confidence:.1f}%)" if confidence else ""
        self.overlay_label.config(text=f"Welcome {name}! 👋{conf_text}")
        self.overlay_label.place(relx=0.5, rely=0.05, anchor='n')
        
        # Play sound
        try:
            if winsound:
                winsound.MessageBeep(winsound.MB_ICONASTERISK)
            else:
                self.root.bell()
        except:
            pass
        
        # Hide after 3 seconds
        self.root.after(3000, lambda: self.overlay_label.place_forget())
    
    # Camera and Video Processing
    
    def start_camera(self):
        """Initialize camera."""
        self.video_capture = cv2.VideoCapture(0)
        if not self.video_capture.isOpened():
            messagebox.showerror("Camera Error", "Could not open camera.")
            return
        
        self.is_running = True
        self.update_frame()
    
    def update_frame(self):
        """Update video frame."""
        if not self.is_running:
            return
        
        ret, frame = self.video_capture.read()
        if not ret:
            self.root.after(30, self.update_frame)
            return
        
        # Process based on mode
        if self.mode == "register":
            frame = self.process_register_frame(frame)
        elif self.mode == "recognize":
            frame = self.process_recognize_frame(frame)
        else:
            frame = self.process_idle_frame(frame)
        
        # Display
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_rgb = cv2.resize(frame_rgb, (800, 600))
        
        img = Image.fromarray(frame_rgb)
        photo = ImageTk.PhotoImage(image=img)
        
        self.video_label.configure(image=photo, text="")
        self.video_label.image = photo
        
        self.root.after(30, self.update_frame)
    
    def process_idle_frame(self, frame):
        """Process frame in idle mode."""
        cv2.putText(
            frame,
            "Select an action to begin",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )
        return frame
    
    def process_register_frame(self, frame):
        """Process frame in registration mode."""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        
        if self.captured_face is not None:
            # Show captured face
            if self.captured_location:
                top, right, bottom, left = self.captured_location
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 255), 3)
            
            cv2.putText(
                frame,
                "Face captured! Enter details and save",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 255),
                2
            )
        else:
            # Show detected faces
            for (top, right, bottom, left) in face_locations:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(
                    frame,
                    "Press SPACE to capture",
                    (left, top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2
                )
            
            cv2.putText(
                frame,
                "Registration Mode - Press SPACE to capture",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )
        
        return frame
    
    def process_recognize_frame(self, frame):
        """Process frame in recognition mode."""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        small_frame = cv2.resize(rgb_frame, (0, 0), fx=0.25, fy=0.25)
        
        face_locations = face_recognition.face_locations(small_frame)
        face_encodings = face_recognition.face_encodings(small_frame, face_locations)
        
        for face_encoding, (top, right, bottom, left) in zip(face_encodings, face_locations):
            # Scale back up
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            
            name = "Unknown"
            confidence = None
            student_id = ""
            color = (0, 0, 255)
            
            if self.known_face_encodings:
                matches = face_recognition.compare_faces(
                    self.known_face_encodings,
                    face_encoding,
                    tolerance=self.tolerance
                )
                face_distances = face_recognition.face_distance(
                    self.known_face_encodings,
                    face_encoding
                )
                
                if len(face_distances) > 0:
                    best_idx = np.argmin(face_distances)
                    if matches[best_idx]:
                        name = self.known_face_names[best_idx]
                        confidence = (1 - face_distances[best_idx]) * 100
                        student_id = self.student_info.get(name, {}).get('student_id', '')
                        color = (0, 255, 0)
            
            # Draw box
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            
            # Draw label
            label = name
            if student_id:
                label += f" (ID: {student_id})"
            if confidence:
                label += f" {confidence:.1f}%"
            
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
            cv2.putText(
                frame,
                label,
                (left + 6, bottom - 6),
                cv2.FONT_HERSHEY_DUPLEX,
                0.5,
                (255, 255, 255),
                1
            )
            
            # Log and mark attendance
            if name != "Unknown":
                self.add_to_history(name, student_id, confidence)
                self.mark_attendance(name, student_id, confidence)
        
        cv2.putText(
            frame,
            f"Recognition Mode - Detecting faces...",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )
        
        return frame
    
    # Mode Control
    
    def start_registration(self):
        """Start registration mode."""
        self.mode = "register"
        self.captured_face = None
        self.captured_location = None
        self.name_entry.delete(0, tk.END)
        self.student_id_entry.delete(0, tk.END)
        
        self.register_card.pack(fill=tk.X, pady=(0, 15), before=self.status_label.master.master)
        
        self.btn_register.config(state=tk.DISABLED)
        self.btn_recognize.config(state=tk.DISABLED)
        self.btn_stop.config(state=tk.NORMAL)
        
        self.status_label.config(text="Registration mode: Position face and press SPACE")
        
        self.root.bind('<space>', lambda e: self.capture_face())
    
    def start_recognition(self):
        """Start recognition mode."""
        if not self.known_face_encodings:
            messagebox.showwarning("No Faces", "Please register at least one person first.")
            return
        
        self.mode = "recognize"
        
        self.btn_register.config(state=tk.DISABLED)
        self.btn_recognize.config(state=tk.DISABLED)
        self.btn_stop.config(state=tk.NORMAL)
        
        count = len(set(self.known_face_names))
        self.status_label.config(text=f"Recognition mode: Detecting {count} registered person(s)")
    
    def stop_mode(self):
        """Stop current mode."""
        self.mode = "idle"
        self.captured_face = None
        self.captured_location = None
        
        self.register_card.pack_forget()
        
        self.btn_register.config(state=tk.NORMAL)
        self.btn_recognize.config(state=tk.NORMAL)
        self.btn_stop.config(state=tk.DISABLED)
        
        self.status_label.config(text="Ready")
        
        self.root.unbind('<space>')
    
    def capture_face(self):
        """Capture face for registration."""
        if not self.video_capture:
            return
        
        ret, frame = self.video_capture.read()
        if not ret:
            return
        
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        
        if not face_locations:
            messagebox.showwarning("No Face", "No face detected. Please position your face clearly.")
            return
        
        # Capture first face
        top, right, bottom, left = face_locations[0]
        self.captured_location = (top, right, bottom, left)
        
        padding = 20
        self.captured_face = rgb_frame[
            max(0, top-padding):min(rgb_frame.shape[0], bottom+padding),
            max(0, left-padding):min(rgb_frame.shape[1], right+padding)
        ].copy()
        
        self.name_entry.focus()
        self.status_label.config(text="Face captured! Enter name and student ID, then save")
    
    def save_face(self):
        """Save captured face."""
        if self.captured_face is None:
            messagebox.showwarning("No Face", "Please capture a face first.")
            return
        
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("Missing Name", "Please enter a name.")
            return
        
        student_id = self.student_id_entry.get().strip()
        if not student_id:
            messagebox.showwarning("Missing ID", "Please enter a student ID.")
            return
        
        # Find unique filename
        counter = 1
        while True:
            filename = self.known_faces_dir / f"{name}{'' if counter == 1 else counter}.jpg"
            if not filename.exists():
                break
            counter += 1
        
        # Save image
        face_bgr = cv2.cvtColor(self.captured_face, cv2.COLOR_RGB2BGR)
        cv2.imwrite(str(filename), face_bgr)
        
        # Save student info
        self.student_info[name] = {'student_id': student_id}
        self.save_student_info()
        
        # Reload faces
        self.load_known_faces(force_rebuild=True)
        self.update_people_list()
        
        # Reset
        self.captured_face = None
        self.captured_location = None
        self.name_entry.delete(0, tk.END)
        self.student_id_entry.delete(0, tk.END)
        
        messagebox.showinfo("Success", f"Face registered!\n\nName: {name}\nID: {student_id}")
        self.status_label.config(text=f"Registered: {name} ({student_id})")
    
    def on_closing(self):
        """Handle window close."""
        self.is_running = False
        if self.video_capture:
            self.video_capture.release()
        self.root.destroy()


def main():
    """Main entry point."""
    root = tk.Tk()
    app = ModernFaceRecognitionUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
