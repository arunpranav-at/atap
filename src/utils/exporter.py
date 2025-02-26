"""
Animation exporter module for saving animations as video files
"""

import os
import shutil
import tempfile
import subprocess

class AnimationExporter:
    """Handles exporting animation frames to a video file"""
    
    def __init__(self, parent=None):
        self.parent = parent
        self.temp_dir = None
    
    def export_animation(self, frames, fps, output_path):
        """Exports animation frames to a video file"""
        try:
            # Create temporary directory for frames
            self.temp_dir = tempfile.mkdtemp()
            
            # Save frames as individual images
            for i, frame in enumerate(frames):
                frame_path = os.path.join(self.temp_dir, f"frame_{i:04d}.png")
                frame.copy().save(frame_path)  # <-- Ensure each frame is a separate file
            
            try:
                # First, try running FFmpeg normally (if it's in the PATH)
                # Construct FFmpeg command to create video
                input_pattern = os.path.join(self.temp_dir, "frame_%04d.png")
                ffmpeg_cmd = [
                    "ffmpeg",
                    "-y",  # Overwrite output file if it exists
                    "-framerate", str(fps),
                    "-i", input_pattern,
                    "-c:v", "libx264",
                    "-pix_fmt", "yuv420p",
                    "-crf", "18",  # Quality (lower is better)
                    output_path
                ]
                
                # Run FFmpeg
                subprocess.run(ffmpeg_cmd, check=True)
                
            except (subprocess.CalledProcessError, FileNotFoundError):
                # FFmpeg not found in PATH, show error with instructions
                self.cleanup()
                return False, ("FFmpeg is not installed or not found in the system PATH. "
                              "Please install FFmpeg from https://ffmpeg.org/download.html "
                              "or specify the full path to the FFmpeg executable in the code.")
            
            # Clean up temporary files
            self.cleanup()
            
            return True, "Animation exported successfully."
            
        except Exception as e:
            self.cleanup()
            return False, f"Export error: {str(e)}"
    
    def cleanup(self):
        """Cleans up temporary files"""
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)