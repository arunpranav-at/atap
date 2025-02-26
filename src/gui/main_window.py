"""
Main window module for the animation application
"""

import os
import json
import shutil
import tempfile
import zipfile
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QPushButton, QLabel, QSlider, QScrollArea, QColorDialog, 
                            QFileDialog, QInputDialog, QMessageBox, QSpinBox, QToolBar,
                            QAction, QSizePolicy, QDockWidget, QListWidget, QFrame)
from PyQt5.QtGui import QPixmap, QImage, QColor, QIcon
from PyQt5.QtCore import Qt, QRect, QApplication

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
        dock.setAllowe