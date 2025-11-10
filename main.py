import sys
from pathlib import Path

# Pastikan folder file ini ada di sys.path untuk import modul-modul lain
BASE = Path(__file__).resolve().parent
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

from PySide6 import QtWidgets, QtUiTools
from PySide6.QtCore import QFile, Qt

# Import form per tabel (pastikan file2 ini ada di folder yang sama)
from officers import OfficersForm
from vehicles import VehiclesForm
from drives import DrivesForm
from cycles import CyclesForm
from activities import ActivitiesForm
from queues import QueuesForm

UI_FILE = "main.ui"

def load_ui_anywhere(ui_name: str):
    """Load UI (QWidget atau QMainWindow) dari folder file ini berada."""
    ui_path = BASE / ui_name
    if not ui_path.exists():
        return None
    f = QFile(str(ui_path))
    if not f.open(QFile.ReadOnly):
        return None
    loader = QtUiTools.QUiLoader()
    w = loader.load(f, None)
    f.close()
    return w

def wire_buttons(win):
    """Sambungkan tombol berdasarkan objectName atau text."""
    mapping_by_name = {
        "btnOfficers": open_officers,
        "btnVehicles": open_vehicles,
        "btnDrives": open_drives,
        "btnCycles": open_cycles,
        "btnActivities": open_activities,
        "btnQueues": open_queues,
    }
    found = False
    for name, handler in mapping_by_name.items():
        btn = win.findChild(QtWidgets.QPushButton, name)
        if btn:
            btn.clicked.connect(lambda _=False, h=handler: h(win))
            found = True

    if not found:
        text_map = {
            "officers": open_officers,
            "vehicles": open_vehicles,
            "drives": open_drives,
            "cycles": open_cycles,
            "activities": open_activities,
            "queues": open_queues,
            "petugas": open_officers,
            "kendaraan": open_vehicles,
            "siklus": open_cycles,
            "aktivitas": open_activities,
            "antrian": open_queues,
            "antrean": open_queues,
        }
        for btn in win.findChildren(QtWidgets.QPushButton):
            t = (btn.text() or "").strip().lower()
            if t in text_map:
                btn.clicked.connect(lambda _=False, h=text_map[t]: h(win))
                found = True
    return found

def _open_child(parent_win, cls):
    child = cls()
    child.setAttribute(Qt.WA_DeleteOnClose, True)
    child.show()
    if not hasattr(parent_win, "_children"):
        parent_win._children = []
    parent_win._children.append(child)

def open_officers(parent): _open_child(parent, OfficersForm)
def open_vehicles(parent): _open_child(parent, VehiclesForm)
def open_drives(parent): _open_child(parent, DrivesForm)
def open_cycles(parent): _open_child(parent, CyclesForm)
def open_activities(parent): _open_child(parent, ActivitiesForm)
def open_queues(parent): _open_child(parent, QueuesForm)

def build_fallback():
    win = QtWidgets.QMainWindow()
    central = QtWidgets.QWidget()
    win.setCentralWidget(central)
    grid = QtWidgets.QGridLayout(central)
    buttons = [
        ("Officers", open_officers),
        ("Vehicles", open_vehicles),
        ("Drives", open_drives),
        ("Cycles", open_cycles),
        ("Activities", open_activities),
        ("Queues", open_queues),
    ]
    for i, (text, handler) in enumerate(buttons):
        b = QtWidgets.QPushButton(text)
        b.setMinimumSize(160, 60)
        b.clicked.connect(lambda _=False, h=handler: h(win))
        grid.addWidget(b, i // 3, i % 3)
    win.setWindowTitle("Home — Menu Tabel (Fallback)")
    win.resize(900, 560)
    return win

def main():
    app = QtWidgets.QApplication(sys.argv)

    win = load_ui_anywhere(UI_FILE)
    if win is None:
        win = build_fallback()
    else:
        # Pastikan ukuran/judul enak
        if not win.windowTitle():
            win.setWindowTitle("Home — Menu Tabel")
        if win.width() < 820 or win.height() < 520:
            win.resize(900, 560)
        # Sambungkan tombol
        if not wire_buttons(win):
            # Kalau tombol tidak terdeteksi, tambahkan toolbar sederhana agar tetap bisa dibuka
            tb = QtWidgets.QToolBar("Menu")
            win.addToolBar(tb)
            acts = [
                ("Officers", open_officers),
                ("Vehicles", open_vehicles),
                ("Drives", open_drives),
                ("Cycles", open_cycles),
                ("Activities", open_activities),
                ("Queues", open_queues),
            ]
            for text, handler in acts:
                act = tb.addAction(text)
                act.triggered.connect(lambda _=False, h=handler: h(win))

    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
