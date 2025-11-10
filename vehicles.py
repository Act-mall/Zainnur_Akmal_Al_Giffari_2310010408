from common import BaseForm  # atau 'from common import BaseForm' kalau file kamu bernama common.py
from PySide6.QtWidgets import QComboBox

class VehiclesForm(BaseForm):
    TABLE = "vehicles"
    UI_FILE = "vehicles.ui"
    FIELD_WIDGETS = {
        "id": ("spin", "spinId"),
        "serial_number": ("line", "editSerialNumber"),
        "model": ("line", "editModel"),
        "production_year": ("line", "editProductionYear"),
        "created_at": ("line", "editCreatedAt"),
        "updated_at": ("line", "editUpdatedAt"),
    }
