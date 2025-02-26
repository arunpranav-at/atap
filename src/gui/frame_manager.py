"""
Frame Manager module for handling animation frames
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                           QLabel, QListWidget, QListWidgetItem, QSpinBox, QMessageBox)
from PyQt5.QtGui import QPixmap, QImage, QIcon
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QTimer

class FrameManager(QWidget):
    """Widget to manage animation frames"""
    frame_changed = pyqtSignal(int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.frames = []
        self.current_frame_index = -1
        self.fps = 12
        
        # UI Setup
        self.layout = QVBoxLayout(self)
        
        # Frame list
        self.frame_list = QListWidget()
        self.frame_list.setIconSize(QSize(80, 60))
        self.frame_list.setViewMode(QListWidget.IconMode)
        self.frame_list.setFlow(QListWidget.LeftToRight)
        self.frame_list.setResizeMode(QListWidget.Adjust)
        self.frame_list.setSelectionMode(QListWidget.SingleSelection)
        self.frame_list.itemClicked.connect(self.on_frame_selected)
        
        # Frame control buttons
        btn_layout = QHBoxLayout()
        
        self.btn_add = QPushButton("Add Frame")
        self.btn_add.clicked.connect(self.add_frame)
        
        self.btn_duplicate = QPushButton("Duplicate")
        self.btn_duplicate.clicked.connect(self.duplicate_frame)
        
        self.btn_delete = QPushButton("Delete")
        self.btn_delete.clicked.connect(self.delete_frame)
        
        self.btn_move_left = QPushButton("←")
        self.btn_move_left.clicked.connect(self.move_frame_left)
        
        self.btn_move_right = QPushButton("→")
        self.btn_move_right.clicked.connect(self.move_frame_right)
        
        # FPS settings
        fps_layout = QHBoxLayout()
        fps_layout.addWidget(QLabel("FPS:"))
        self.fps_spinner = QSpinBox()
        self.fps_spinner.setRange(1, 60)
        self.fps_spinner.setValue(self.fps)
        self.fps_spinner.valueChanged.connect(self.set_fps)
        fps_layout.addWidget(self.fps_spinner)
        
        # Add widgets to layouts
        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_duplicate)
        btn_layout.addWidget(self.btn_delete)
        btn_layout.addWidget(self.btn_move_left)
        btn_layout.addWidget(self.btn_move_right)
        
        self.layout.addWidget(self.frame_list)
        self.layout.addLayout(btn_layout)
        self.layout.addLayout(fps_layout)
        
        # Initialize with one empty frame
        self.add_frame()
    
    def set_fps(self, fps):
        """Sets the animation frames per second"""
        self.fps = fps  
    
    def add_frame(self):
        """Adds a new blank frame to the animation"""
        if self.current_frame_index >= 0 and self.frames:
            # Save the current canvas image as a deep copy
            current_image = self.parent.canvas.get_image()
            self.frames[self.current_frame_index] = current_image.copy()
        
        # Create a blank white frame
        new_frame = QImage(800, 600, QImage.Format_ARGB32)
        new_frame.fill(Qt.white)
        
        # Store a new independent frame copy
        self.frames.append(new_frame.copy())
        
        # Update UI
        index = len(self.frames) - 1
        thumbnail = self.create_thumbnail(new_frame)
        item = QListWidgetItem(f"Frame {index + 1}")
        item.setIcon(QIcon(QPixmap.fromImage(thumbnail)))
        self.frame_list.addItem(item)
        
        # Select the new frame
        self.frame_list.setCurrentRow(index)
        self.current_frame_index = index
        
        # Load the blank frame onto the canvas
        self.parent.canvas.load_image(new_frame.copy())
        self.frame_changed.emit(index)
    
    def duplicate_frame(self):
        """Duplicates the current frame"""
        if not self.frames or self.current_frame_index < 0:
            return
            
        # Save the current canvas state to the current frame
        current_image = self.parent.canvas.get_image()
        self.frames[self.current_frame_index] = current_image.copy()
            
        # Create a deep copy of the current frame
        frame_copy = self.frames[self.current_frame_index].copy()
        
        # Insert after the current frame
        insert_position = self.current_frame_index + 1
        self.frames.insert(insert_position, frame_copy)
        
        # Create thumbnail and add to list
        thumbnail = self.create_thumbnail(frame_copy)
        item = QListWidgetItem(f"Frame {insert_position + 1}")
        item.setIcon(QIcon(QPixmap.fromImage(thumbnail)))
        self.frame_list.insertItem(insert_position, item)
        
        # Update frame numbering
        self.renumber_frames()
        
        # Select the new frame
        self.frame_list.setCurrentRow(insert_position)
        self.current_frame_index = insert_position
        self.parent.canvas.load_image(frame_copy.copy())
        self.frame_changed.emit(insert_position)
    
    def delete_frame(self):
        """Deletes the current frame"""
        if not self.frames or self.current_frame_index < 0:
            return
            
        # Don't delete the last frame
        if len(self.frames) <= 1:
            QMessageBox.warning(self, "Warning", "Cannot delete the last frame.")
            return
            
        # Remove from list and frames
        self.frames.pop(self.current_frame_index)
        self.frame_list.takeItem(self.current_frame_index)
        
        # Update frame numbering
        self.renumber_frames()
        
        # Select an appropriate frame
        new_index = min(self.current_frame_index, len(self.frames) - 1)
        self.frame_list.setCurrentRow(new_index)
        self.current_frame_index = new_index
        
        # Load the new current frame onto the canvas
        if self.frames:
            self.parent.canvas.load_image(self.frames[new_index].copy())
        self.frame_changed.emit(new_index)
    
    def move_frame_left(self):
        """Moves the current frame one position to the left"""
        if (not self.frames or self.current_frame_index <= 0 or
            self.current_frame_index >= len(self.frames)):
            return
        
        # Save the current canvas state to the current frame
        current_image = self.parent.canvas.get_image()
        self.frames[self.current_frame_index] = current_image.copy()
            
        # Swap frames
        new_index = self.current_frame_index - 1
        self.frames[new_index], self.frames[self.current_frame_index] = \
            self.frames[self.current_frame_index].copy(), self.frames[new_index].copy()
            
        # Update UI to reflect changes
        self.refresh_frame_list()
        
        # Select the moved frame
        self.frame_list.setCurrentRow(new_index)
        self.current_frame_index = new_index
        self.parent.canvas.load_image(self.frames[new_index].copy())
        self.frame_changed.emit(new_index)
    
    def move_frame_right(self):
        """Moves the current frame one position to the right"""
        if (not self.frames or self.current_frame_index < 0 or
            self.current_frame_index >= len(self.frames) - 1):
            return
        
        # Save the current canvas state to the current frame
        current_image = self.parent.canvas.get_image()
        self.frames[self.current_frame_index] = current_image.copy()
            
        # Swap frames
        new_index = self.current_frame_index + 1
        self.frames[new_index], self.frames[self.current_frame_index] = \
            self.frames[self.current_frame_index].copy(), self.frames[new_index].copy()
            
        # Update UI to reflect changes
        self.refresh_frame_list()
        
        # Select the moved frame
        self.frame_list.setCurrentRow(new_index)
        self.current_frame_index = new_index
        self.parent.canvas.load_image(self.frames[new_index].copy())
        self.frame_changed.emit(new_index)
    
    def refresh_frame_list(self):
        """Refreshes the frame list to reflect the current state of frames"""
        self.frame_list.clear()
        
        for i, frame in enumerate(self.frames):
            thumbnail = self.create_thumbnail(frame)
            item = QListWidgetItem(f"Frame {i + 1}")
            item.setIcon(QIcon(QPixmap.fromImage(thumbnail)))
            self.frame_list.addItem(item)
    
    def renumber_frames(self):
        """Updates frame numbers in the list widget"""
        for i in range(self.frame_list.count()):
            self.frame_list.item(i).setText(f"Frame {i + 1}")
    
    def on_frame_selected(self, item):
        """Handles frame selection from the list"""
        # Save the current frame before switching
        if self.current_frame_index >= 0 and self.current_frame_index < len(self.frames):
            current_image = self.parent.canvas.get_image()
            self.frames[self.current_frame_index] = current_image.copy()
            
        # Switch to the selected frame
        index = self.frame_list.row(item)
        self.current_frame_index = index
        
        # Load the selected frame onto the canvas
        if index >= 0 and index < len(self.frames):
            self.parent.canvas.load_image(self.frames[index].copy())
            
        self.frame_changed.emit(index)
    
    def create_thumbnail(self, image):
        """Creates a thumbnail from a frame image"""
        return image.scaled(80, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    
    def update_current_frame(self, image):
        """Updates the current frame with a new image"""
        if not self.frames or self.current_frame_index < 0:
            return
            
        self.frames[self.current_frame_index] = image.copy()
        
        # Update thumbnail
        thumbnail = self.create_thumbnail(image)
        self.frame_list.item(self.current_frame_index).setIcon(
            QIcon(QPixmap.fromImage(thumbnail)))
    
    def get_current_frame(self):
        """Returns the current frame image"""
        if not self.frames or self.current_frame_index < 0:
            return None
        return self.frames[self.current_frame_index].copy()
    
    def play_animation(self):
        """Starts playing the animation preview"""
        # Save the current frame before starting playback
        if self.current_frame_index >= 0 and self.frames:
            current_image = self.parent.canvas.get_image()
            self.frames[self.current_frame_index] = current_image.copy()
            
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.advance_frame)
        self.animation_timer.start(1000 // self.fps)
        self.playback_index = 0
        self.old_index = self.current_frame_index
        
        # Load the first frame for playback
        if self.frames:
            self.parent.canvas.load_image(self.frames[0].copy())
    
    def stop_animation(self):
        """Stops the animation preview"""
        if hasattr(self, 'animation_timer'):
            self.animation_timer.stop()
            # Restore the originally selected frame
            self.frame_list.setCurrentRow(self.old_index)
            self.current_frame_index = self.old_index
            if self.old_index >= 0 and self.old_index < len(self.frames):
                self.parent.canvas.load_image(self.frames[self.old_index].copy())
            self.frame_changed.emit(self.old_index)
    
    def advance_frame(self):
        """Advances to the next frame during animation playback"""
        if not self.frames:
            return
            
        self.playback_index = (self.playback_index + 1) % len(self.frames)
        self.frame_list.setCurrentRow(self.playback_index)
        # During playback, don't save frames, just display them
        self.parent.canvas.load_image(self.frames[self.playback_index].copy())
        self.current_frame_index = self.playback_index
        self.frame_changed.emit(self.playback_index)