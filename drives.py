from common import BaseForm
from PySide6.QtWidgets import QComboBox

class DrivesForm(BaseForm):
    TABLE = "drives"
    UI_FILE = "drives.ui"
    FIELD_WIDGETS = {
        "id": ("spin", "spinId"),
        "officer_id": ("combo", "comboOfficer"),
        "vehicle_id": ("combo", "comboVehicle"),
        "active": ("check", "checkActive"),
        "latitude": ("line", "editLatitude"),
        "longitude": ("line", "editLongitude"),
        "date": ("date", "dateDrive"),
        "created_at": ("line", "editCreatedAt"),
        "updated_at": ("line", "editUpdatedAt"),
    }

    def setup_fk_options(self):
        comboOfficer = self.ui.findChild(QComboBox, "comboOfficer")
        if comboOfficer:
            comboOfficer.clear()
            for row in self.db.fetch_options("officers", "id", "name"):
                comboOfficer.addItem(str(row["label"]), row["id"])

        comboVehicle = self.ui.findChild(QComboBox, "comboVehicle")
        if comboVehicle:
            comboVehicle.clear()
            for row in self.db.fetch_options("vehicles", "id", "model"):
                comboVehicle.addItem(str(row["label"]), row["id"])
