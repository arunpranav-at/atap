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
                            QAction, QSizePolicy, QDockWidget, QListWidget, QFrame, QListWidgetItem)
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
        self.tool_dock = QDockWidget("Tools", self)
        self.tool_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.tool_dock.setFloating(False)  # Ensure it's docked initially

        self.tool_dock.setFeatures(QDockWidget.NoDockWidgetFeatures)
        
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
        
        # Gradient Fill button
        self.btn_gradient = QPushButton("Gradient Fill")
        self.btn_gradient.clicked.connect(lambda: self.canvas.set_tool("gradient"))
        layout.addWidget(self.btn_gradient)

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
        self.tool_dock.setWidget(tools_widget)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.tool_dock)

    def create_color_dock(self):
        """Creates the color selection dock widget"""
        self.color_dock = QDockWidget("Colors", self)
        self.color_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.color_dock.setFloating(False)

        self.color_dock.setFeatures(QDockWidget.NoDockWidgetFeatures)
        
        colors_widget = QWidget()
        layout = QVBoxLayout(colors_widget)

        # 🎨 Color picker with preview in one line
        color_picker_layout = QHBoxLayout()
        
        self.btn_color = QPushButton("Select Color")
        self.btn_color.clicked.connect(self.open_color_dialog)
        
        self.color_preview = QFrame()
        self.color_preview.setFrameShape(QFrame.Box)
        self.color_preview.setFixedSize(40, 20)  # Smaller preview
        self.color_preview.setStyleSheet("background-color: black;")

        # Add button and preview to the same row
        color_picker_layout.addWidget(self.btn_color)
        color_picker_layout.addWidget(self.color_preview)
        
        layout.addLayout(color_picker_layout)  # Add the row layout to main layout

        self.color_dock.setWidget(colors_widget)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.color_dock)

        # 🎨 Gradient color selection
        layout.addWidget(QLabel("Gradient Colors:"))

        # Start Color Selection with Preview
        start_color_layout = QHBoxLayout()
        self.btn_start_color = QPushButton("Start Color")
        self.btn_start_color.clicked.connect(self.select_start_color)
        self.start_color_preview = QFrame()
        self.start_color_preview.setFrameShape(QFrame.Box)
        self.start_color_preview.setFixedSize(40, 20)  # Small preview box
        self.start_color_preview.setStyleSheet("background-color: red;")  # Default Red
        start_color_layout.addWidget(self.btn_start_color)
        start_color_layout.addWidget(self.start_color_preview)
        layout.addLayout(start_color_layout)

        # End Color Selection with Preview
        end_color_layout = QHBoxLayout()
        self.btn_end_color = QPushButton("End Color")
        self.btn_end_color.clicked.connect(self.select_end_color)
        self.end_color_preview = QFrame()
        self.end_color_preview.setFrameShape(QFrame.Box)
        self.end_color_preview.setFixedSize(40, 20)  # Small preview box
        self.end_color_preview.setStyleSheet("background-color: blue;")  # Default Blue
        end_color_layout.addWidget(self.btn_end_color)
        end_color_layout.addWidget(self.end_color_preview)
        layout.addLayout(end_color_layout)
        
        self.palette_layout = QHBoxLayout()
        
        self.custom_colors = []  # Store selected custom colors
        self.update_custom_palette()

        layout.addLayout(self.palette_layout)
        layout.addStretch()

        self.color_dock.setWidget(colors_widget)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.color_dock)

    def select_start_color(self):
        """Opens a color dialog for selecting the start color of the gradient"""
        color = QColorDialog.getColor(self.canvas.gradient_start_color, self)
        if color.isValid():
            self.canvas.set_gradient_colors(color, self.canvas.gradient_end_color)

    def select_end_color(self):
        """Opens a color dialog for selecting the end color of the gradient"""
        color = QColorDialog.getColor(self.canvas.gradient_end_color, self)
        if color.isValid():
            self.canvas.set_gradient_colors(self.canvas.gradient_start_color, color)


    def open_color_dialog(self):
        """Opens a color dialog and allows users to create custom colors"""
        color = QColorDialog.getColor(self.canvas.brush_color, self)
        if color.isValid():
            self.set_brush_color(color)
            self.add_color_to_palette(color)  # Add to custom palette

    def add_color_to_palette(self, color):
        """Adds a new color to the custom palette"""
        if color not in self.custom_colors:
            self.custom_colors.append(color)
            self.update_custom_palette()

    def update_custom_palette(self):
        """Updates the color palette UI with saved colors"""
        # Clear existing buttons
        while self.palette_layout.count():
            item = self.palette_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # Add color buttons
        for color in self.custom_colors:
            color_btn = QPushButton()
            color_btn.setFixedSize(24, 24)
            color_btn.setStyleSheet(f"background-color: {color.name()};")
            color_btn.clicked.connect(lambda checked, c=color: self.set_brush_color(c))
            self.palette_layout.addWidget(color_btn)

    def toggle_tools_dock(self):
        """Toggles the visibility of the Tools dock"""
        if self.tool_dock.isVisible():
            self.tool_dock.hide()
            self.toggle_tools_action.setChecked(False)
        else:
            self.tool_dock.show()
            self.toggle_tools_action.setChecked(True)

    def toggle_colors_dock(self):
        """Toggles the visibility of the Colors dock"""
        if self.color_dock.isVisible():
            self.color_dock.hide()
            self.toggle_colors_action.setChecked(False)
        else:
            self.color_dock.show()
            self.toggle_colors_action.setChecked(True)
    
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
        
        resize_action = QAction("Resize Canvas", self)
        resize_action.triggered.connect(self.resize_canvas_dialog)
        toolbar.addAction(resize_action)

        toolbar.addSeparator()

        # Toggle tools dock
        self.toggle_tools_action = QAction("Toggle Tools", self)
        self.toggle_tools_action.setCheckable(True)
        self.toggle_tools_action.setChecked(True)
        self.toggle_tools_action.triggered.connect(self.toggle_tools_dock)
        toolbar.addAction(self.toggle_tools_action)

        # Toggle colors dock
        self.toggle_colors_action = QAction("Toggle Colors", self)
        self.toggle_colors_action.setCheckable(True)
        self.toggle_colors_action.setChecked(True)
        self.toggle_colors_action.triggered.connect(self.toggle_colors_dock)
        toolbar.addAction(self.toggle_colors_action)

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
        
        # Ensure color_preview exists before using it
        if hasattr(self, 'color_preview'):
            self.color_preview.setStyleSheet(f"background-color: {QColor(color).name()};")

    def play_animation(self):
        """Starts the animation preview playback"""
        self.frame_manager.play_animation()
    
    def stop_animation(self):
        """Stops the animation preview playback"""
        self.frame_manager.stop_animation()
        
    def resize_canvas_dialog(self):
        """Opens a dialog to resize the canvas"""
        width, ok_w = QInputDialog.getInt(self, "Canvas Width", "Enter new width:", self.canvas.width(), 100, 2000, 10)
        height, ok_h = QInputDialog.getInt(self, "Canvas Height", "Enter new height:", self.canvas.height(), 100, 2000, 10)

        if ok_w and ok_h:
            self.canvas.resize_canvas(width, height)
    
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
                # Convert to QPixmap and save
                pixmap = QPixmap.fromImage(frame)
                if not pixmap.save(frame_path, "PNG"):
                    raise Exception(f"Failed to save frame {i} to {frame_path}")
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
            
            # Save project info as JSON
            info_path = os.path.join(temp_dir, "project_info.json")
            with open(info_path, 'w') as f:
                json.dump(project_info, f)
            
            # Create zip archive
            with zipfile.ZipFile(file_path, 'w') as zipf:
                # Add project info file
                zipf.write(info_path, arcname="project_info.json")
                
                # Add all frame images
                for frame_name in frame_paths:
                    frame_path = os.path.join(temp_dir, frame_name)
                    zipf.write(frame_path, arcname=frame_name)
            
            # Clean up temporary directory
            shutil.rmtree(temp_dir)
            
            QMessageBox.information(self, "Save Successful", "Project saved successfully.")
            
        except Exception as e:
            QMessageBox.critical(self, "Save Error", f"Error saving project: {str(e)}")
            # Print the full traceback for debugging
            import traceback
            traceback.print_exc()
    
    def open_project(self):
        """Opens an existing animation project"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Project", "", "ATAP Project Files (*.atap)")
        
        if not file_path:
            return
            
        try:
            # Create a temporary directory for extraction
            temp_dir = tempfile.mkdtemp()
            
            # Verify file exists and is zip-like
            if not os.path.exists(file_path):
                raise Exception(f"File not found: {file_path}")
                
            # Extract zip archive
            import zipfile
            try:
                with zipfile.ZipFile(file_path, 'r') as zipf:
                    zipf.extractall(temp_dir)
            except zipfile.BadZipFile:
                raise Exception(f"Invalid or corrupted project file: {file_path}")
            
            # Verify project info exists
            info_path = os.path.join(temp_dir, "project_info.json")
            if not os.path.exists(info_path):
                raise Exception("Project file is missing required information")
                
            # Load project info
            import json
            with open(info_path, 'r') as f:
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
                frame_count = 0
                for frame_name in project_info.get("frames", []):
                    frame_path = os.path.join(temp_dir, frame_name)
                    
                    # Verify frame file exists
                    if not os.path.exists(frame_path):
                        print(f"Warning: Frame file not found: {frame_path}")
                        continue
                    
                    # Load the image
                    frame = QImage(frame_path)
                    if frame.isNull():
                        print(f"Warning: Could not load frame: {frame_path}")
                        continue
                        
                    # Add to our frames list
                    self.frame_manager.frames.append(frame)
                    
                    # Create thumbnail and add to list
                    thumbnail = self.frame_manager.create_thumbnail(frame)
                    item = QListWidgetItem(f"Frame {len(self.frame_manager.frames)}")
                    item.setIcon(QIcon(QPixmap.fromImage(thumbnail)))
                    self.frame_manager.frame_list.addItem(item)
                    frame_count += 1
                
                # Select the first frame
                if self.frame_manager.frames:
                    self.frame_manager.frame_list.setCurrentRow(0)
                    self.frame_manager.current_frame_index = 0
                    self.canvas.load_image(self.frame_manager.frames[0])
                    self.frame_manager.frame_changed.emit(0)
                    
                    QMessageBox.information(self, "Open Successful", 
                                        f"Project loaded successfully with {frame_count} frames.")
                else:
                    QMessageBox.warning(self, "Open Warning", "No valid frames found in the project.")
            
            # Clean up
            shutil.rmtree(temp_dir)
            
        except Exception as e:
            QMessageBox.critical(self, "Open Error", f"Error opening project: {str(e)}")
            # Print the full traceback for debugging
            import traceback
            traceback.print_exc()

    def closeEvent(self, event):
        """Handles the window close event with a confirmation dialog."""
        reply = QMessageBox.question(
            self,
            "Exit Confirmation",
            "Do you want to save your animation project before closing? You will lose unsaved changes.",
            QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
            QMessageBox.Cancel
        )

        if reply == QMessageBox.Save:
            self.save_project()  # Calls the save function
            event.accept()  # Close the application
        elif reply == QMessageBox.Discard:
            event.accept()  # Close without saving
        else:
            event.ignore()  # Cancel closing the application
