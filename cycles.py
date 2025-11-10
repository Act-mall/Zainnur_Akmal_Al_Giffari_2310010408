from common import BaseForm
from PySide6.QtWidgets import QComboBox

class CyclesForm(BaseForm):
    TABLE = "cycles"
    UI_FILE = "cycles.ui"
    FIELD_WIDGETS = {
        "id": ("spin", "spinId"),
        "drive_id": ("combo", "comboDrive"),
        "start_time": ("time", "timeStart"),
        "finish_time": ("time", "timeFinish"),
        "date": ("date", "dateCycle"),
        "created_at": ("line", "editCreatedAt"),
        "updated_at": ("line", "editUpdatedAt"),
    }

    def setup_fk_options(self):
        comboDrive = self.ui.findChild(QComboBox, "comboDrive")
        if comboDrive:
            comboDrive.clear()
            for row in self.db.fetch_options("drives", "id", None):
                comboDrive.addItem(str(row["id"]) if "id" in row else str(row["label"]), row["id"])
