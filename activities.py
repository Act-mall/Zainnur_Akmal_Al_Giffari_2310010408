from common import BaseForm
from PySide6.QtWidgets import QComboBox

class ActivitiesForm(BaseForm):
    TABLE = "activities"
    UI_FILE = "activities.ui"
    FIELD_WIDGETS = {
        "id": ("spin", "spinId"),
        "cycle_id": ("combo", "comboCycle"),
        "name": ("line", "editName"),
        "start_time": ("time", "timeStart"),
        "finish_time": ("time", "timeFinish"),
        "created_at": ("line", "editCreatedAt"),
        "updated_at": ("line", "editUpdatedAt"),
    }

    def setup_fk_options(self):
        comboCycle = self.ui.findChild(QComboBox, "comboCycle")
        if comboCycle:
            comboCycle.clear()
            for row in self.db.fetch_options("cycles", "id", None):
                comboCycle.addItem(str(row["id"]) if "id" in row else str(row["label"]), row["id"])
