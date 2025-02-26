"""
Canvas module for drawing animation frames
"""

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import (QPixmap, QPainter, QPen, QColor, QImage, 
                        QPainterPath, QBrush, QCursor)
from PyQt5.QtCore import Qt, QPoint, QRect

class Canvas(QWidget):
    """Drawing canvas for creating animation frames"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setFixedSize(800, 600)
        
        # Initialize canvas properties
        self.image = QImage(self.size(), QImage.Format_ARGB32)
        self.image.fill(Qt.white)
        self.backup_image = QImage(self.image)
        
        # Drawing settings
        self.drawing = False
        self.brush_size = 3
        self.brush_color = Qt.black
        self.last_point = QPoint()
        self.current_tool = "pen"
        
        # Eraser is just a white brush
        self.eraser_color = Qt.white
        self.eraser_size = 10
        
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
        self.image.fill(Qt.white)
        self.update()
        
    def load_image(self, image):
        """Loads an image onto the canvas"""
        self.image = image.copy()
        self.update()
        
    def get_image(self):
        """Returns the current canvas image"""
        return self.image.copy()
    
    def mousePressEvent(self, event):
        """Handles mouse press events on the canvas"""
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.last_point = event.pos()
            self.backup_image = self.image.copy()
            
    def mouseMoveEvent(self, event):
        """Handles mouse move events on the canvas"""
        if (event.buttons() & Qt.LeftButton) and self.drawing:
            if self.current_tool == "pen":
                self.draw_line_to(event.pos())
            elif self.current_tool == "eraser":
                self.erase_to(event.pos())
            elif self.current_tool == "fill":
                pass  # Fill is handled in mouseReleaseEvent
    
    def mouseReleaseEvent(self, event):
        """Handles mouse release events on the canvas"""
        if event.button() == Qt.LeftButton and self.drawing:
            if self.current_tool == "pen":
                self.draw_line_to(event.pos())
            elif self.current_tool == "eraser":
                self.erase_to(event.pos())
            elif self.current_tool == "fill":
                self.fill_at(event.pos())
            self.drawing = False
    
    def draw_line_to(self, end_point):
        """Draws a line from the last point to the current point"""
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
        # Convert QImage to a format we can process
        src_image = self.image.copy()
        x, y = point.x(), point.y()
        
        # Get the target color to replace
        if not (0 <= x < self.image.width() and 0 <= y < self.image.height()):
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
    
    def paintEvent(self, event):
        """Handles paint events for the canvas"""
        painter = QPainter(self)
        painter.drawImage(QRect(0, 0, self.width(), self.height()), self.image)