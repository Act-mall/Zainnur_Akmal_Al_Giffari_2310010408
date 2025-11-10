from common import BaseForm
from PySide6.QtWidgets import QComboBox

class QueuesForm(BaseForm):
    TABLE = "queues"
    UI_FILE = "queues.ui"
    FIELD_WIDGETS = {
        "id": ("spin", "spinId"),
        "excavator_id": ("combo", "comboExcavator"),
        "truck_id": ("combo", "comboTruck"),
        "waiting": ("check", "checkWaiting"),
        "created_at": ("line", "editCreatedAt"),
        "updated_at": ("line", "editUpdatedAt"),
    }

    def setup_fk_options(self):
        comboExc = self.ui.findChild(QComboBox, "comboExcavator")
        if comboExc:
            comboExc.clear()
            for row in self.db.fetch_options("vehicles", "id", "model"):
                comboExc.addItem(str(row["label"]), row["id"])
        comboTruck = self.ui.findChild(QComboBox, "comboTruck")
        if comboTruck:
            comboTruck.clear()
            for row in self.db.fetch_options("vehicles", "id", "serial_number"):
                comboTruck.addItem(str(row["label"]), row["id"])
