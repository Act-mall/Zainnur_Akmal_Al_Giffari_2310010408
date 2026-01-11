# This Python file uses the following encoding: utf-8
import os
from PySide6.QtWidgets import QWidget, QTableWidgetItem, QMessageBox
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader

from crud import crud_2310010408


class form_drives(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        ui_path = os.path.join(os.path.dirname(__file__), "drives.ui")
        filenya = QFile(ui_path)
        if not filenya.open(QFile.ReadOnly):
            raise RuntimeError(f"Gagal membuka UI: {ui_path}")

        muatfile = QUiLoader()
        self.formdrives = muatfile.load(filenya, self)
        self.setWindowTitle(self.formdrives.windowTitle())
        filenya.close()

        try:
            self.resize(self.formdrives.size())
        except Exception:
            pass

        self.aksi = crud_2310010408()

        self._load_fk_options()

        self.formdrives.BtnSimpan.clicked.connect(self.simpanDrives)
        self.formdrives.BtnUbah.clicked.connect(self.ubahDrives)
        self.formdrives.BtnHapus.clicked.connect(self.hapusDrives)

        if hasattr(self.formdrives, "lineCari"):
            self.formdrives.lineCari.textChanged.connect(self.cariDataDrives)

        self.formdrives.btnCetak.clicked.connect(self.laporanDrives)
        self.formdrives.tblDrives.cellClicked.connect(self.pilihBaris)

        self.tampilDataDrives()

    # ===== helper dropdown =====
    def _combo_get_id(self, widget):
        """Ambil id dari QComboBox (userData). Fallback ke text bila QLineEdit."""
        if hasattr(widget, "currentData"):
            return widget.currentData()
        if hasattr(widget, "text"):
            t = widget.text().strip()
            return t if t else None
        return None

    def _combo_set_by_id(self, widget, id_value):
        """Set QComboBox currentIndex berdasarkan userData (id)."""
        if not hasattr(widget, "count"):
            if hasattr(widget, "setText"):
                widget.setText("" if id_value is None else str(id_value))
            return

        try:
            id_val = int(str(id_value).strip())
        except Exception:
            id_val = None

        if id_val is None:
            widget.setCurrentIndex(0)
            return

        for i in range(widget.count()):
            if widget.itemData(i) == id_val:
                widget.setCurrentIndex(i)
                return

        widget.addItem(str(id_val), id_val)
        widget.setCurrentIndex(widget.count() - 1)

    def _load_fk_options(self):
        """Muat pilihan Officer & Vehicle untuk dropdown."""
        # Officers
        cb_off = self.formdrives.EditOfficerId
        if hasattr(cb_off, "clear"):
            cb_off.clear()
            cb_off.addItem("-- pilih officer --", None)
            try:
                for o in self.aksi.dataOfficers():
                    label = f"{o.get('id')} - {o.get('name', '')}".strip()
                    cb_off.addItem(label, o.get("id"))
            except Exception:
                pass

        cb_veh = self.formdrives.EditVehicleId
        if hasattr(cb_veh, "clear"):
            cb_veh.clear()
            cb_veh.addItem("-- pilih vehicle --", None)
            try:
                for v in self.aksi.dataVehicles():
                    label = f"{v.get('id')} - {v.get('serial_number','')} {v.get('model','')} ({v.get('production_year','')})".strip()
                    cb_veh.addItem(label, v.get("id"))
            except Exception:
                pass

    def simpanDrives(self):
        officer_id = self._combo_get_id(self.formdrives.EditOfficerId)
        vehicle_id = self._combo_get_id(self.formdrives.EditVehicleId)

        if officer_id is None:
            QMessageBox.information(None, "Informasi", "Officer ID belum dipilih")
            return
        if vehicle_id is None:
            QMessageBox.information(None, "Informasi", "Vehicle ID belum dipilih")
            return

        active = self.formdrives.ComboActive.currentText()
        latitude = self.formdrives.EditLatitude.text()
        longitude = self.formdrives.EditLongitude.text()
        date_ = self.formdrives.EditDate.text()

        try:
            self.aksi.tambahDrives(officer_id, vehicle_id, active, latitude, longitude, date_)
            self.tampilDataDrives()
            QMessageBox.information(None, "Informasi", "Data berhasil disimpan")
        except Exception as e:
            QMessageBox.information(None, "Informasi", f"Gagal simpan: {e}")

    def ubahDrives(self):
        if not self.formdrives.EditId.text().strip():
            QMessageBox.information(None, "Informasi", "ID belum diisi (pilih data di tabel)")
            self.formdrives.EditId.setFocus()
            return

        id_ = self.formdrives.EditId.text()
        officer_id = self._combo_get_id(self.formdrives.EditOfficerId)
        vehicle_id = self._combo_get_id(self.formdrives.EditVehicleId)
        active = self.formdrives.ComboActive.currentText()
        latitude = self.formdrives.EditLatitude.text()
        longitude = self.formdrives.EditLongitude.text()
        date_ = self.formdrives.EditDate.text()

        if officer_id is None or vehicle_id is None:
            QMessageBox.information(None, "Informasi", "Officer ID / Vehicle ID belum dipilih")
            return

        try:
            self.aksi.gantiDrives(id_, officer_id, vehicle_id, active, latitude, longitude, date_)
            self.tampilDataDrives()
            QMessageBox.information(None, "Informasi", "Data berhasil diubah")
        except Exception as e:
            QMessageBox.information(None, "Informasi", f"Gagal ubah: {e}")

    def hapusDrives(self):
        if not self.formdrives.EditId.text().strip():
            QMessageBox.information(None, "Informasi", "ID belum diisi (pilih data di tabel)")
            return

        pesan = QMessageBox.information(
            None, "Informasi", "Apakah yakin menghapus data ini?", QMessageBox.Yes | QMessageBox.No
        )
        if pesan != QMessageBox.Yes:
            return

        id_ = self.formdrives.EditId.text()
        try:
            self.aksi.kurangDrives(id_)
            self.tampilDataDrives()
            QMessageBox.information(None, "Informasi", "Data berhasil dihapus")
        except Exception as e:
            QMessageBox.information(None, "Informasi", f"Gagal hapus: {e}")

    def tampilDataDrives(self):
        self.formdrives.tblDrives.setRowCount(0)
        data = self.aksi.dataDrives()
        for i, baris in enumerate(data):
            self.formdrives.tblDrives.insertRow(i)
            self.formdrives.tblDrives.setItem(i, 0, QTableWidgetItem(str(baris["id"])))
            self.formdrives.tblDrives.setItem(i, 1, QTableWidgetItem(str(baris["officer_id"])))
            self.formdrives.tblDrives.setItem(i, 2, QTableWidgetItem(str(baris["vehicle_id"])))
            self.formdrives.tblDrives.setItem(i, 3, QTableWidgetItem(str(baris["active"])))
            self.formdrives.tblDrives.setItem(i, 4, QTableWidgetItem(str(baris.get("latitude", "") or "")))
            self.formdrives.tblDrives.setItem(i, 5, QTableWidgetItem(str(baris.get("longitude", "") or "")))
            self.formdrives.tblDrives.setItem(i, 6, QTableWidgetItem(str(baris.get("date", "") or "")))

    def cariDataDrives(self):
        varCari = self.formdrives.lineCari.text() if hasattr(self.formdrives, "lineCari") else ""
        self.formdrives.tblDrives.setRowCount(0)
        data = self.aksi.filterDrives(varCari) if varCari else self.aksi.dataDrives()
        for i, baris in enumerate(data):
            self.formdrives.tblDrives.insertRow(i)
            self.formdrives.tblDrives.setItem(i, 0, QTableWidgetItem(str(baris["id"])))
            self.formdrives.tblDrives.setItem(i, 1, QTableWidgetItem(str(baris["officer_id"])))
            self.formdrives.tblDrives.setItem(i, 2, QTableWidgetItem(str(baris["vehicle_id"])))
            self.formdrives.tblDrives.setItem(i, 3, QTableWidgetItem(str(baris["active"])))
            self.formdrives.tblDrives.setItem(i, 4, QTableWidgetItem(str(baris.get("latitude", "") or "")))
            self.formdrives.tblDrives.setItem(i, 5, QTableWidgetItem(str(baris.get("longitude", "") or "")))
            self.formdrives.tblDrives.setItem(i, 6, QTableWidgetItem(str(baris.get("date", "") or "")))

    def laporanDrives(self):
        cari = self.formdrives.txtFilter.text().strip() if hasattr(self.formdrives, "txtFilter") else ""
        filter_ = self.formdrives.comboFilter.currentText() if hasattr(self.formdrives, "comboFilter") else "Semua"
        try:
            if filter_ == "Semua" or not cari:
                self.aksi.cetakDrives()
            else:
                self.aksi.cetakFilterDrives(cari)  # active 0/1
            QMessageBox.information(None, "Informasi", "Laporan berhasil dibuat: Laporan Drives.pdf")
        except Exception as e:
            QMessageBox.information(None, "Informasi", f"Gagal cetak: {e}")

    def pilihBaris(self, row, col):
        _ = col

        def item(c):
            it = self.formdrives.tblDrives.item(row, c)
            return it.text() if it else ""

        self.formdrives.EditId.setText(item(0))
        self._combo_set_by_id(self.formdrives.EditOfficerId, item(1))
        self._combo_set_by_id(self.formdrives.EditVehicleId, item(2))

        val = item(3)
        idx = self.formdrives.ComboActive.findText(val)
        if idx >= 0:
            self.formdrives.ComboActive.setCurrentIndex(idx)

        self.formdrives.EditLatitude.setText(item(4))
        self.formdrives.EditLongitude.setText(item(5))
        self.formdrives.EditDate.setText(item(6))
