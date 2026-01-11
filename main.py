# This Python file uses the following encoding: utf-8
import sys

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader

from officers import form_officers
from vehicles import form_vehicles
from drives import form_drives
from cycles import form_cycles
from activities import form_activities
from queues import form_queues


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        filenya = QFile("form.ui")
        filenya.open(QFile.ReadOnly)
        muatfile = QUiLoader()
        self.formutama = muatfile.load(filenya, self)
        self.setWindowTitle(self.formutama.windowTitle())
        self.resize(self.formutama.size())
        self.setMenuBar(self.formutama.menuBar())

        self.formutama.actionDATA_OFFICERS.triggered.connect(self.buka_officers)
        self.formutama.actionDATA_VEHICLES.triggered.connect(self.buka_vehicles)
        self.formutama.actionDATA_DRIVES.triggered.connect(self.buka_drives)
        self.formutama.actionDATA_CYCLES.triggered.connect(self.buka_cycles)
        self.formutama.actionDATA_ACTIVITIES.triggered.connect(self.buka_activities)
        self.formutama.actionDATA_QUEUES.triggered.connect(self.buka_queues)

    def buka_officers(self):
        self.w_officers = form_officers()
        self.w_officers.show()

    def buka_vehicles(self):
        self.w_vehicles = form_vehicles()
        self.w_vehicles.show()

    def buka_drives(self):
        self.w_drives = form_drives()
        self.w_drives.show()

    def buka_cycles(self):
        self.w_cycles = form_cycles()
        self.w_cycles.show()

    def buka_activities(self):
        self.w_activities = form_activities()
        self.w_activities.show()

    def buka_queues(self):
        self.w_queues = form_queues()
        self.w_queues.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("SITAMBANG")
    jendela = MainWindow()
    jendela.show()
    sys.exit(app.exec())
