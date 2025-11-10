from common import BaseForm

class OfficersForm(BaseForm):
    TABLE = "officers"
    UI_FILE = "officers.ui"
    FIELD_WIDGETS = {
        "id": ("spin", "spinId"),
        "official_reg_number": ("line", "editOfficialRegNumber"),
        "name": ("line", "editName"),
        "photo": ("line", "editPhoto"),
        "email": ("line", "editEmail"),
        "password": ("pwd", "editPassword"),
        "segment": ("line", "editSegment"),
        "license_expired": ("date", "dateLicenseExpired"),
        "onesignal": ("line", "editOneSignal"),
        "created_at": ("line", "editCreatedAt"),
        "updated_at": ("line", "editUpdatedAt"),
    }
