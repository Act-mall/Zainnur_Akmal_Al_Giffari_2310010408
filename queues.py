# This Python file uses the following encoding: utf-8
import os
from PySide6.QtWidgets import QWidget, QTableWidgetItem, QMessageBox
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader

from crud import crud_2310010408


class form_queues(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        ui_path = os.path.join(os.path.dirname(__file__), "queues.ui")
        filenya = QFile(ui_path)
        if not filenya.open(QFile.ReadOnly):
            raise RuntimeError(f"Gagal membuka UI: {ui_path}")

        muatfile = QUiLoader()
        self.formqueues = muatfile.load(filenya, self)
        self.setWindowTitle(self.formqueues.windowTitle())
        filenya.close()

        try:
            self.resize(self.formqueues.size())
        except Exception:
            pass

        self.aksi = crud_2310010408()

        self._load_vehicle_options()

        self.formqueues.BtnSimpan.clicked.connect(self.simpanQueues)
        self.formqueues.BtnUbah.clicked.connect(self.ubahQueues)
        self.formqueues.BtnHapus.clicked.connect(self.hapusQueues)

        if hasattr(self.formqueues, "lineCari"):
            self.formqueues.lineCari.textChanged.connect(self.cariDataQueues)

        self.formqueues.btnCetak.clicked.connect(self.laporanQueues)
        self.formqueues.tblQueues.cellClicked.connect(self.pilihBaris)

        self.tampilDataQueues()

    def _combo_get_id(self, widget):
        if hasattr(widget, "currentData"):
            return widget.currentData()
        if hasattr(widget, "text"):
            t = widget.text().strip()
            return t if t else None
        return None

    def _combo_set_by_id(self, widget, id_value):
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

    def _load_vehicle_options(self):
        """Muat pilihan Vehicle untuk dropdown excavator & truck."""
        cb_ex = self.formqueues.EditExcavatorId
        cb_tr = self.formqueues.EditTruckId

        vehicles = []
        try:
            vehicles = self.aksi.dataVehicles()
        except Exception:
            vehicles = []

        if hasattr(cb_ex, "clear"):
            cb_ex.clear()
            cb_ex.addItem("-- pilih excavator --", None)
            for v in vehicles:
                label = f"{v.get('id')} - {v.get('serial_number','')} {v.get('model','')} ({v.get('production_year','')})".strip()
                cb_ex.addItem(label, v.get("id"))

        if hasattr(cb_tr, "clear"):
            cb_tr.clear()
            cb_tr.addItem("-- pilih truck --", None)
            for v in vehicles:
                label = f"{v.get('id')} - {v.get('serial_number','')} {v.get('model','')} ({v.get('production_year','')})".strip()
                cb_tr.addItem(label, v.get("id"))

    def simpanQueues(self):
        excavator_id = self._combo_get_id(self.formqueues.EditExcavatorId)
        truck_id = self._combo_get_id(self.formqueues.EditTruckId)

        if excavator_id is None:
            QMessageBox.information(None, "Informasi", "Excavator ID belum dipilih")
            return
        if truck_id is None:
            QMessageBox.information(None, "Informasi", "Truck ID belum dipilih")
            return

        waiting = self.formqueues.ComboWaiting.currentText()

        try:
            self.aksi.tambahQueues(excavator_id, truck_id, waiting)
            self.tampilDataQueues()
            QMessageBox.information(None, "Informasi", "Data berhasil disimpan")
        except Exception as e:
            QMessageBox.information(None, "Informasi", f"Gagal simpan: {e}")

    def ubahQueues(self):
        if not self.formqueues.EditId.text().strip():
            QMessageBox.information(None, "Informasi", "ID belum diisi (pilih data di tabel)")
            self.formqueues.EditId.setFocus()
            return

        id_ = self.formqueues.EditId.text()
        excavator_id = self._combo_get_id(self.formqueues.EditExcavatorId)
        truck_id = self._combo_get_id(self.formqueues.EditTruckId)
        waiting = self.formqueues.ComboWaiting.currentText()

        if excavator_id is None or truck_id is None:
            QMessageBox.information(None, "Informasi", "Excavator/Truck ID belum dipilih")
            return

        try:
            self.aksi.gantiQueues(id_, excavator_id, truck_id, waiting)
            self.tampilDataQueues()
            QMessageBox.information(None, "Informasi", "Data berhasil diubah")
        except Exception as e:
            QMessageBox.information(None, "Informasi", f"Gagal ubah: {e}")

    def hapusQueues(self):
        if not self.formqueues.EditId.text().strip():
            QMessageBox.information(None, "Informasi", "ID belum diisi (pilih data di tabel)")
            return

        pesan = QMessageBox.information(
            None, "Informasi", "Apakah yakin menghapus data ini?", QMessageBox.Yes | QMessageBox.No
        )
        if pesan != QMessageBox.Yes:
            return

        id_ = self.formqueues.EditId.text()
        try:
            self.aksi.kurangQueues(id_)
            self.tampilDataQueues()
            QMessageBox.information(None, "Informasi", "Data berhasil dihapus")
        except Exception as e:
            QMessageBox.information(None, "Informasi", f"Gagal hapus: {e}")

    def tampilDataQueues(self):
        self.formqueues.tblQueues.setRowCount(0)
        data = self.aksi.dataQueues()
        for i, baris in enumerate(data):
            self.formqueues.tblQueues.insertRow(i)
            self.formqueues.tblQueues.setItem(i, 0, QTableWidgetItem(str(baris["id"])))
            self.formqueues.tblQueues.setItem(i, 1, QTableWidgetItem(str(baris["excavator_id"])))
            self.formqueues.tblQueues.setItem(i, 2, QTableWidgetItem(str(baris["truck_id"])))
            self.formqueues.tblQueues.setItem(i, 3, QTableWidgetItem(str(baris["waiting"])))

    def cariDataQueues(self):
        varCari = self.formqueues.lineCari.text() if hasattr(self.formqueues, "lineCari") else ""
        self.formqueues.tblQueues.setRowCount(0)
        data = self.aksi.filterQueues(varCari) if varCari else self.aksi.dataQueues()
        for i, baris in enumerate(data):
            self.formqueues.tblQueues.insertRow(i)
            self.formqueues.tblQueues.setItem(i, 0, QTableWidgetItem(str(baris["id"])))
            self.formqueues.tblQueues.setItem(i, 1, QTableWidgetItem(str(baris["excavator_id"])))
            self.formqueues.tblQueues.setItem(i, 2, QTableWidgetItem(str(baris["truck_id"])))
            self.formqueues.tblQueues.setItem(i, 3, QTableWidgetItem(str(baris["waiting"])))

    def laporanQueues(self):
        cari = self.formqueues.txtFilter.text().strip() if hasattr(self.formqueues, "txtFilter") else ""
        filter_ = self.formqueues.comboFilter.currentText() if hasattr(self.formqueues, "comboFilter") else "Semua"
        try:
            if filter_ == "Semua" or not cari:
                self.aksi.cetakQueues()
            else:
                self.aksi.cetakFilterQueues(cari)  # waiting 0/1
            QMessageBox.information(None, "Informasi", "Laporan berhasil dibuat: Laporan Queues.pdf")
        except Exception as e:
            QMessageBox.information(None, "Informasi", f"Gagal cetak: {e}")

    def pilihBaris(self, row, col):
        _ = col

        def item(c):
            it = self.formqueues.tblQueues.item(row, c)
            return it.text() if it else ""

        self.formqueues.EditId.setText(item(0))
        self._combo_set_by_id(self.formqueues.EditExcavatorId, item(1))
        self._combo_set_by_id(self.formqueues.EditTruckId, item(2))

        val = item(3)
        idx = self.formqueues.ComboWaiting.findText(val)
        if idx >= 0:
            self.formqueues.ComboWaiting.setCurrentIndex(idx)
