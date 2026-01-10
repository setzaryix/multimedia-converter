import os
import sys
import json

from PySide6.QtWidgets import QApplication, QMainWindow
from ui.ConversionTab import ConversionTab
from managers.PresetManager import PresetManager

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Multimedia Converter")
        self.resize(400, 300)

        self.preset_manager = PresetManager()
        self.conversion_preset = self.preset_manager.load_conversion_preset()

        self.ui = ConversionTab(self.conversion_preset, self)
        self.setCentralWidget(self.ui)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())