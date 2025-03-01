"""
Canvas module for drawing animation frames
"""

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import (QPixmap, QPainter, QPen, QColor, QImage, QLinearGradient, QPainterPath, QBrush, QCursor)
from PyQt5.QtCore import Qt, QPoint, QRect


class Canvas(QWidget):
    """Drawing canvas for creating animation frames"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        
        # Set initial size
        self.setMinimumSize(800, 600)
        
        # Initialize single image with correct size
        self.image = QImage(800, 600, QImage.Format_ARGB32)
        self.image.fill(Qt.white)
        
        # Keep track of canvas size to handle scaling
        self.canvas_width = 800
        self.canvas_height = 600
        
        # Undo/Redo stacks
        self.undo_stack = []
        self.redo_stack = []
        self.max_history = 20
        
        # Drawing settings
        self.drawing = False
        self.brush_size = 3
        self.brush_color = Qt.black
        self.last_point = QPoint()
        self.current_tool = "pen"
        
        # Eraser settings
        self.eraser_color = Qt.white
        self.eraser_size = 10
        
        # Gradient fill settings
        self.gradient_start_color = Qt.red
        self.gradient_end_color = Qt.blue
        
        # Set up the cursor
        self.update_cursor()
    
    def update_cursor(self):
        """Updates the cursor based on current tool and size"""
        if self.current_tool == "pen":
            size = self.brush_size
            color = self.brush_color
        elif self.current_tool == "eraser":
            size = self.eraser_size
            color = self.eraser_color
        else:
            # Default cursor for other tools
            self.setCursor(Qt.ArrowCursor)
            return
        
        # Create a custom cursor for the brush/eraser
        pixmap = QPixmap(size + 2, size + 2)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setPen(Qt.black)
        painter.setBrush(QBrush(color))
        painter.drawEllipse(1, 1, size, size)
        painter.end()
        
        self.setCursor(QCursor(pixmap))
    
    def set_gradient_colors(self, start_color, end_color):
        """Sets the gradient start and end colors"""
        self.gradient_start_color = start_color
        self.gradient_end_color = end_color
    
    def set_brush_size(self, size):
        """Sets the brush size"""
        self.brush_size = size
        self.update_cursor()
    
    def set_brush_color(self, color):
        """Sets the brush color"""
        self.brush_color = color
        self.update_cursor()
    
    def set_tool(self, tool):
        """Sets the current drawing tool"""
        self.current_tool = tool
        self.update_cursor()
    
    def clear(self):
        """Clears the canvas"""
        self.save_state()  # Save current state for undo
        self.image.fill(Qt.white)
        self.update()
    
    def load_image(self, image):
        """Loads an image onto the canvas"""
        self.save_state()  # Save current state for undo
        self.image = image.copy()
        self.canvas_width = self.image.width()
        self.canvas_height = self.image.height()
        self.update()
    
    def get_image(self):
        """Returns the current canvas image"""
        return self.image.copy()
    
    def save_state(self):
        """Saves the current canvas state for undo"""
        self.undo_stack.append(self.image.copy())
        if len(self.undo_stack) > self.max_history:
            self.undo_stack.pop(0)
        self.redo_stack.clear()
    
    def undo(self):
        """Reverts to the previous state"""
        if self.undo_stack:
            self.redo_stack.append(self.image.copy())
            self.image = self.undo_stack.pop()
            self.update()
    
    def redo(self):
        """Restores an undone action"""
        if self.redo_stack:
            self.undo_stack.append(self.image.copy())
            self.image = self.redo_stack.pop()
            self.update()
    
    def resize_canvas(self, width, height):
        """Resizes the canvas while preserving existing drawings"""
        if width == self.canvas_width and height == self.canvas_height:
            return  # No change needed
        
        self.save_state()  # Save current state for undo
        
        # Create a new blank image
        new_image = QImage(width, height, QImage.Format_ARGB32)
        new_image.fill(Qt.white)
        
        # Copy existing drawing into the new image
        painter = QPainter(new_image)
        painter.drawImage(0, 0, self.image)
        painter.end()
        
        self.image = new_image
        self.canvas_width = width
        self.canvas_height = height
        self.setFixedSize(width, height)
        self.update()
    
    def get_image_position(self, widget_pos):
        """Converts widget coordinates to image coordinates"""
        # If widget and image sizes match, just return the position
        # Otherwise, scale to match image coordinates
        x = int(widget_pos.x() * self.canvas_width / self.width())
        y = int(widget_pos.y() * self.canvas_height / self.height())
        return QPoint(x, y)
    
    def mousePressEvent(self, event):
        """Handles mouse press events on the canvas"""
        if event.button() == Qt.LeftButton:
            self.drawing = True
            # Convert widget coordinates to image coordinates
            self.last_point = self.get_image_position(event.pos())
            self.save_state()
    
    def mouseMoveEvent(self, event):
        """Handles mouse move events on the canvas"""
        if (event.buttons() & Qt.LeftButton) and self.drawing:
            # Convert widget coordinates to image coordinates
            current_point = self.get_image_position(event.pos())
            
            if self.current_tool == "pen":
                self.draw_line_to(current_point)
            elif self.current_tool == "eraser":
                self.erase_to(current_point)
    
    def mouseReleaseEvent(self, event):
        """Handles mouse release events on the canvas"""
        if event.button() == Qt.LeftButton and self.drawing:
            # Convert widget coordinates to image coordinates
            current_point = self.get_image_position(event.pos())
            
            if self.current_tool == "pen":
                self.draw_line_to(current_point)
            elif self.current_tool == "eraser":
                self.erase_to(current_point)
            elif self.current_tool == "fill":
                self.fill_at(current_point)
            elif self.current_tool == "gradient":
                self.fill_gradient(current_point)
            
            self.drawing = False
    
    def draw_line_to(self, end_point):
        """Draws a line from the last point to the current point"""
        if self.image.isNull():
            return
        
        painter = QPainter(self.image)
        pen = QPen()
        pen.setWidth(self.brush_size)
        pen.setColor(self.brush_color)
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)
        painter.setPen(pen)
        
        painter.drawLine(self.last_point, end_point)
        self.last_point = end_point
        self.update()
    
    def erase_to(self, end_point):
        """Erases from the last point to the current point"""
        painter = QPainter(self.image)
        pen = QPen()
        pen.setWidth(self.eraser_size)
        pen.setColor(self.eraser_color)
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)
        painter.setPen(pen)
        
        painter.drawLine(self.last_point, end_point)
        self.last_point = end_point
        self.update()
    
    def fill_at(self, point):
        """Fills an area with the current brush color starting at the given point"""
        # Create a copy of the image for processing
        src_image = self.image.copy()
        x, y = point.x(), point.y()
        
        # Get the target color to replace
        if not (0 <= x < self.canvas_width and 0 <= y < self.canvas_height):
            return
        
        target_color = src_image.pixelColor(x, y)
        replacement_color = self.brush_color
        
        # Don't do anything if the colors are the same
        if target_color == replacement_color:
            return
        
        # Simple flood fill algorithm (4-connected)
        stack = [(x, y)]
        width, height = src_image.width(), src_image.height()
        visited = set()
        
        # Create painter
        painter = QPainter(self.image)
        painter.setPen(QPen(replacement_color))
        
        while stack:
            cx, cy = stack.pop()
            if (cx, cy) in visited:
                continue
            
            current_color = src_image.pixelColor(cx, cy)
            if current_color != target_color:
                continue
            
            # Fill this pixel
            painter.drawPoint(cx, cy)
            visited.add((cx, cy))
            
            # Add adjacent pixels
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            for dx, dy in directions:
                nx, ny = cx + dx, cy + dy
                if (0 <= nx < width and 0 <= ny < height and 
                        (nx, ny) not in visited):
                    stack.append((nx, ny))
        
        painter.end()
        self.update()
    
    def fill_gradient(self, point):
        """Fills an enclosed shape with a gradient starting from the clicked point"""
        # Create a copy of the image for processing
        src_image = self.image.copy()
        x, y = point.x(), point.y()
        
        # Ensure the point is within bounds
        if not (0 <= x < self.canvas_width and 0 <= y < self.canvas_height):
            return
        
        target_color = src_image.pixelColor(x, y)
        
        # Don't apply if clicking on the same color
        if target_color == self.gradient_start_color or target_color == self.gradient_end_color:
            return
        
        # Create a mask to track filled area
        width, height = src_image.width(), src_image.height()
        mask = [[False] * height for _ in range(width)]
        
        # Simple flood fill algorithm (4-connected)
        stack = [(x, y)]
        shape_bounds = []  # Store the boundary of the shape
        
        while stack:
            cx, cy = stack.pop()
            if not (0 <= cx < width and 0 <= cy < height) or mask[cx][cy]:
                continue
            
            current_color = src_image.pixelColor(cx, cy)
            if current_color != target_color:
                continue
            
            # Mark this pixel as filled
            mask[cx][cy] = True
            shape_bounds.append((cx, cy))
            
            # Add adjacent pixels to the stack
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            for dx, dy in directions:
                nx, ny = cx + dx, cy + dy
                stack.append((nx, ny))
        
        if not shape_bounds:
            return
        
        # Find bounding box of the shape
        min_x = min(px for px, _ in shape_bounds)
        max_x = max(px for px, _ in shape_bounds)
        min_y = min(py for _, py in shape_bounds)
        max_y = max(py for _, py in shape_bounds)
        
        # Create a gradient inside the detected shape boundary
        gradient = QLinearGradient(min_x, min_y, max_x, max_y)
        gradient.setColorAt(0, self.gradient_start_color)
        gradient.setColorAt(1, self.gradient_end_color)
        
        painter = QPainter(self.image)
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.NoPen)
        
        # Fill the detected shape using a path
        path = QPainterPath()
        for px, py in shape_bounds:
            path.addRect(px, py, 1, 1)  # Fill pixel by pixel
        
        painter.fillPath(path, gradient)
        painter.end()
        
        self.update()
    
    def paintEvent(self, event):
        """Handles paint events for the canvas"""
        painter = QPainter(self)
        # Draw the image scaled to fit the widget
        painter.drawImage(self.rect(), self.image)