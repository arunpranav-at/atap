"""
Main window module for the animation application
"""

import os
import json
import shutil
import tempfile
import zipfile
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QApplication,
                            QPushButton, QLabel, QSlider, QScrollArea, QColorDialog, 
                            QFileDialog, QInputDialog, QMessageBox, QSpinBox, QToolBar,
                            QAction, QSizePolicy, QDockWidget, QListWidget, QFrame)
from PyQt5.QtGui import QPixmap, QImage, QColor, QIcon
from PyQt5.QtCore import Qt, QRect

from src.gui.canvas import Canvas
from src.gui.frame_manager import FrameManager
from src.utils.exporter import AnimationExporter

class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        
        # Set up the main window
        self.setWindowTitle("ATAP - Animation Tool for Adorable Preschoolers")
        self.setMinimumSize(1200, 800)
        
        # Set up central widget and main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        
        # Create Canvas
        self.canvas = Canvas(self)
        
        # Create Frame Manager
        self.frame_manager = FrameManager(self)
        
        # Create Animation Exporter
        self.exporter = AnimationExporter(self)
        
        # Create Tool Dock
        self.create_tool_dock()
        
        # Create Color Dock
        self.create_color_dock()
        
        # Create main toolbar
        self.create_toolbar()
        
        # Set up main layout
        canvas_container = QWidget()
        canvas_layout = QVBoxLayout(canvas_container)
        canvas_scroll = QScrollArea()
        canvas_scroll.setWidget(self.canvas)
        canvas_scroll.setWidgetResizable(False)
        canvas_scroll.setAlignment(Qt.AlignCenter)
        canvas_layout.addWidget(canvas_scroll)
        
        # Animation controls
        anim_controls = QHBoxLayout()
        self.btn_play = QPushButton("Play")
        self.btn_play.clicked.connect(self.play_animation)
        self.btn_stop = QPushButton("Stop")
        self.btn_stop.clicked.connect(self.stop_animation)
        anim_controls.addWidget(self.btn_play)
        anim_controls.addWidget(self.btn_stop)
        canvas_layout.addLayout(anim_controls)
        
        # Add main components to layout
        self.main_layout.addWidget(canvas_container, 3)
        
        # Create a right panel for the frame manager
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.addWidget(QLabel("Frames:"))
        right_layout.addWidget(self.frame_manager)
        
        # Add export button to right panel
        self.btn_export = QPushButton("Export Animation")
        self.btn_export.clicked.connect(self.export_animation)
        right_layout.addWidget(self.btn_export)
        
        self.main_layout.addWidget(right_panel, 1)
    
    def create_tool_dock(self):
        """Creates the tools dock widget"""
        dock = QDockWidget("Tools", self)
        dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        
        tools_widget = QWidget()
        layout = QVBoxLayout(tools_widget)
        
        # Brush tool button
        self.btn_brush = QPushButton("Pen")
        self.btn_brush.clicked.connect(lambda: self.canvas.set_tool("pen"))
        layout.addWidget(self.btn_brush)
        
        # Eraser tool button
        self.btn_eraser = QPushButton("Eraser")
        self.btn_eraser.clicked.connect(lambda: self.canvas.set_tool("eraser"))
        layout.addWidget(self.btn_eraser)
        
        # Fill tool button
        self.btn_fill = QPushButton("Fill")
        self.btn_fill.clicked.connect(lambda: self.canvas.set_tool("fill"))
        layout.addWidget(self.btn_fill)
        
        # Clear canvas button
        self.btn_clear = QPushButton("Clear")
        self.btn_clear.clicked.connect(self.canvas.clear)
        layout.addWidget(self.btn_clear)
        
        # Brush size slider
        layout.addWidget(QLabel("Brush Size:"))
        self.brush_slider = QSlider(Qt.Horizontal)
        self.brush_slider.setRange(1, 50)
        self.brush_slider.setValue(3)
        self.brush_slider.valueChanged.connect(self.canvas.set_brush_size)
        layout.addWidget(self.brush_slider)
        
        # Eraser size slider
        layout.addWidget(QLabel("Eraser Size:"))
        self.eraser_slider = QSlider(Qt.Horizontal)
        self.eraser_slider.setRange(1, 50)
        self.eraser_slider.setValue(10)
        self.eraser_slider.valueChanged.connect(lambda x: setattr(self.canvas, 'eraser_size', x))
        layout.addWidget(self.eraser_slider)
        
        layout.addStretch()
        dock.setWidget(tools_widget)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock)
    
    def create_color_dock(self):
        """Creates the color selection dock widget"""
        dock = QDockWidget("Colors", self)
        dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        
        colors_widget = QWidget()
        layout = QVBoxLayout(colors_widget)
        
        # Color picker button
        self.btn_color = QPushButton("Select Color")
        self.btn_color.clicked.connect(self.open_color_dialog)
        layout.addWidget(self.btn_color)
        
        # Color preview
        self.color_preview = QFrame()
        self.color_preview.setFrameShape(QFrame.Box)
        self.color_preview.setFixedSize(100, 50)
        self.color_preview.setStyleSheet("background-color: black;")
        layout.addWidget(self.color_preview)
        
        # Common colors palette
        layout.addWidget(QLabel("Common Colors:"))
        palette_layout = QHBoxLayout()
        
        common_colors = [
            Qt.black, Qt.white, Qt.red, Qt.green, Qt.blue,
            Qt.cyan, Qt.magenta, Qt.yellow, Qt.gray
        ]
        
        for color in common_colors:
            color_btn = QPushButton()
            color_btn.setFixedSize(24, 24)
            color_btn.setStyleSheet(f"background-color: {QColor(color).name()};")
            color_btn.clicked.connect(lambda checked, c=color: self.set_brush_color(QColor(c)))
            palette_layout.addWidget(color_btn)
        
        layout.addLayout(palette_layout)
        layout.addStretch()
        dock.setWidget(colors_widget)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock)
    
    def create_toolbar(self):
        """Creates the main application toolbar"""
        toolbar = QToolBar("Main Toolbar", self)
        self.addToolBar(toolbar)
        
        # File operations
        new_action = QAction("New Project", self)
        new_action.triggered.connect(self.new_project)
        toolbar.addAction(new_action)
        
        save_action = QAction("Save Project", self)
        save_action.triggered.connect(self.save_project)
        toolbar.addAction(save_action)
        
        load_action = QAction("Open Project", self)
        load_action.triggered.connect(self.open_project)
        toolbar.addAction(load_action)
        
        toolbar.addSeparator()
        
        # Animation operations
        export_action = QAction("Export Video", self)
        export_action.triggered.connect(self.export_animation)
        toolbar.addAction(export_action)
    
    def open_color_dialog(self):
        """Opens a color dialog and sets the selected color"""
        color = QColorDialog.getColor(self.canvas.brush_color, self)
        if color.isValid():
            self.set_brush_color(color)
    
    def set_brush_color(self, color):
        """Sets the brush color and updates the color preview"""
        self.canvas.set_brush_color(color)
        self.color_preview.setStyleSheet(f"background-color: {QColor(color).name()};")
    
    def play_animation(self):
        """Starts the animation preview playback"""
        self.frame_manager.play_animation()
    
    def stop_animation(self):
        """Stops the animation preview playback"""
        self.frame_manager.stop_animation()
    
    def export_animation(self):
        """Exports the animation as a video file"""
        # Get all frames and FPS
        frames = self.frame_manager.frames
        fps = self.frame_manager.fps
        
        # Check if we have frames to export
        if not frames:
            QMessageBox.warning(self, "Export Error", "No frames to export.")
            return
        
        # Ask for output file location
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Animation", "", "MP4 Files (*.mp4)")
        
        if not file_path:
            return
        
        # Add extension if not provided
        if not file_path.lower().endswith('.mp4'):
            file_path += '.mp4'
        
        # Show a "please wait" message
        msg = QMessageBox()
        msg.setText("Exporting animation. Please wait...")
        msg.setStandardButtons(QMessageBox.NoButton)
        msg.show()
        QApplication.processEvents()
        
        # Export animation
        success, message = self.exporter.export_animation(frames, fps, file_path)
        
        # Close the "please wait" message
        msg.close()
        
        # Show result
        if success:
            QMessageBox.information(self, "Export Successful", message)
        else:
            QMessageBox.critical(self, "Export Failed", message)
    
    def new_project(self):
        """Creates a new animation project"""
        reply = QMessageBox.question(
            self, "New Project", 
            "This will clear your current project. Continue?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            # Reset the frame manager
            self.frame_manager.frames = []
            self.frame_manager.frame_list.clear()
            self.frame_manager.add_frame()
            
            # Clear the canvas
            self.canvas.clear()
    
    def save_project(self):
        """Saves the current animation project"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Project", "", "ATAP Project Files (*.atap)")
        
        if not file_path:
            return
            
        # Add extension if not provided
        if not file_path.lower().endswith('.atap'):
            file_path += '.atap'
        
        try:
            # Create a temporary directory for frames
            temp_dir = tempfile.mkdtemp()
            
            # Save all frames as individual images
            frame_paths = []
            for i, frame in enumerate(self.frame_manager.frames):
                frame_path = os.path.join(temp_dir, f"frame_{i:04d}.png")
                frame.save(frame_path)
                frame_paths.append(os.path.basename(frame_path))
            
            # Create a project info dictionary
            project_info = {
                "fps": self.frame_manager.fps,
                "frame_count": len(self.frame_manager.frames),
                "frames": frame_paths,
                "canvas_size": {
                    "width": self.canvas.width(),
                    "height": self.canvas.height()
                }
            }
            
            # Save as a zip file
            with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
                info_path = f.name
                import json
                json.dump(project_info, f)
            
            # Create zip archive
            import zipfile
            with zipfile.ZipFile(file_path, 'w') as zipf:
                # Add project info file
                zipf.write(info_path, arcname="project_info.json")
                
                # Add all frame images
                for frame_name in frame_paths:
                    frame_path = os.path.join(temp_dir, frame_name)
                    zipf.write(frame_path, arcname=frame_name)
            
            # Clean up
            os.unlink(info_path)
            shutil.rmtree(temp_dir)
            
            QMessageBox.information(self, "Save Successful", "Project saved successfully.")
            
        except Exception as e:
            QMessageBox.critical(self, "Save Error", f"Error saving project: {str(e)}")
    
    def open_project(self):
        """Opens an existing animation project"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Project", "", "ATAP Project Files (*.atap)")
        
        if not file_path:
            return
            
        try:
            # Create a temporary directory for extraction
            temp_dir = tempfile.mkdtemp()
            
            # Extract zip archive
            import zipfile
            with zipfile.ZipFile(file_path, 'r') as zipf:
                zipf.extractall(temp_dir)
            
            # Load project info
            import json
            with open(os.path.join(temp_dir, "project_info.json"), 'r') as f:
                project_info = json.load(f)
            
            # Ask for confirmation before loading
            reply = QMessageBox.question(
                self, "Open Project", 
                "This will replace your current project. Continue?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            
            if reply == QMessageBox.Yes:
                # Reset the frame manager
                self.frame_manager.frames = []
                self.frame_manager.frame_list.clear()
                
                # Set FPS
                self.frame_manager.fps = project_info.get("fps", 12)
                self.frame_manager.fps_spinner.setValue(self.frame_manager.fps)
                
                # Load frames
                for frame_name in project_info.get("frames", []):
                    frame_path = os.path.join(temp_dir, frame_name)
                    frame = QImage(frame_path)
                    
                    # Add to our frames list
                    self.frame_manager.frames.append(frame)
                    
                    # Create thumbnail and add to list
                    thumbnail = self.frame_manager.create_thumbnail(frame)
                    item = QListWidgetItem(f"Frame {len(self.frame_manager.frames)}")
                    item.setIcon(QIcon(QPixmap.fromImage(thumbnail)))
                    self.frame_manager.frame_list.addItem(item)
                
                # Select the first frame
                if self.frame_manager.frames:
                    self.frame_manager.frame_list.setCurrentRow(0)
                    self.frame_manager.current_frame_index = 0
                    self.frame_manager.frame_changed.emit(0)
                    
                QMessageBox.information(self, "Open Successful", "Project loaded successfully.")
            
            # Clean up
            shutil.rmtree(temp_dir)
            
        except Exception as e:
            QMessageBox.critical(self, "Open Error", f"Error opening project: {str(e)}")
