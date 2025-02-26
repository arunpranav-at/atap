"""
ATAP - Animation Tool for Adorable Preschoolers
Main application entry point
"""

import sys
from PyQt5.QtWidgets import QApplication
from src.gui.main_window import MainWindow

def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()