# This Python file uses the following encoding: utf-8
import os
from PySide6.QtWidgets import QWidget, QTableWidgetItem, QMessageBox
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader

from crud import crud_2310010408


class form_activities(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        ui_path = os.path.join(os.path.dirname(__file__), "activities.ui")
        filenya = QFile(ui_path)
        if not filenya.open(QFile.ReadOnly):
            raise RuntimeError(f"Gagal membuka UI: {ui_path}")

        muatfile = QUiLoader()
        self.formactivities = muatfile.load(filenya, self)
        self.setWindowTitle(self.formactivities.windowTitle())
        filenya.close()

        try:
            self.resize(self.formactivities.size())
        except Exception:
            pass

        self.aksi = crud_2310010408()

        self._load_cycle_options()

        self.formactivities.BtnSimpan.clicked.connect(self.simpanActivities)
        self.formactivities.BtnUbah.clicked.connect(self.ubahActivities)
        self.formactivities.BtnHapus.clicked.connect(self.hapusActivities)

        if hasattr(self.formactivities, "lineCari"):
            self.formactivities.lineCari.textChanged.connect(self.cariDataActivities)

        self.formactivities.btnCetak.clicked.connect(self.laporanActivities)
        self.formactivities.tblActivities.cellClicked.connect(self.pilihBaris)

        self.tampilDataActivities()

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

    def _load_cycle_options(self):
        cb = self.formactivities.EditCycleId
        if not hasattr(cb, "clear"):
            return
        cb.clear()
        cb.addItem("-- pilih cycle --", None)
        try:
            for c in self.aksi.dataCycles():
                label = f"{c.get('id')} - drive {c.get('drive_id')} ({c.get('date','')})"
                cb.addItem(label.strip(), c.get("id"))
        except Exception:
            pass

    def simpanActivities(self):
        cycle_id = self._combo_get_id(self.formactivities.EditCycleId)
        if cycle_id is None:
            QMessageBox.information(None, "Informasi", "Cycle ID belum dipilih")
            return
        if not self.formactivities.EditName.text().strip():
            QMessageBox.information(None, "Informasi", "Name belum diisi")
            self.formactivities.EditName.setFocus()
            return

        name = self.formactivities.EditName.text()
        start_time = self.formactivities.EditStart.text()
        finish_time = self.formactivities.EditFinish.text()

        try:
            self.aksi.tambahActivities(cycle_id, name, start_time, finish_time)
            self.tampilDataActivities()
            QMessageBox.information(None, "Informasi", "Data berhasil disimpan")
        except Exception as e:
            QMessageBox.information(None, "Informasi", f"Gagal simpan: {e}")

    def ubahActivities(self):
        if not self.formactivities.EditId.text().strip():
            QMessageBox.information(None, "Informasi", "ID belum diisi (pilih data di tabel)")
            self.formactivities.EditId.setFocus()
            return

        id_ = self.formactivities.EditId.text()
        cycle_id = self._combo_get_id(self.formactivities.EditCycleId)
        name = self.formactivities.EditName.text()
        start_time = self.formactivities.EditStart.text()
        finish_time = self.formactivities.EditFinish.text()

        if cycle_id is None:
            QMessageBox.information(None, "Informasi", "Cycle ID belum dipilih")
            return
        if not name.strip():
            QMessageBox.information(None, "Informasi", "Name belum diisi")
            return

        try:
            self.aksi.gantiActivities(id_, cycle_id, name, start_time, finish_time)
            self.tampilDataActivities()
            QMessageBox.information(None, "Informasi", "Data berhasil diubah")
        except Exception as e:
            QMessageBox.information(None, "Informasi", f"Gagal ubah: {e}")

    def hapusActivities(self):
        if not self.formactivities.EditId.text().strip():
            QMessageBox.information(None, "Informasi", "ID belum diisi (pilih data di tabel)")
            return

        pesan = QMessageBox.information(
            None, "Informasi", "Apakah yakin menghapus data ini?", QMessageBox.Yes | QMessageBox.No
        )
        if pesan != QMessageBox.Yes:
            return

        id_ = self.formactivities.EditId.text()
        try:
            self.aksi.kurangActivities(id_)
            self.tampilDataActivities()
            QMessageBox.information(None, "Informasi", "Data berhasil dihapus")
        except Exception as e:
            QMessageBox.information(None, "Informasi", f"Gagal hapus: {e}")

    def tampilDataActivities(self):
        self.formactivities.tblActivities.setRowCount(0)
        data = self.aksi.dataActivities()
        for i, baris in enumerate(data):
            self.formactivities.tblActivities.insertRow(i)
            self.formactivities.tblActivities.setItem(i, 0, QTableWidgetItem(str(baris["id"])))
            self.formactivities.tblActivities.setItem(i, 1, QTableWidgetItem(str(baris["cycle_id"])))
            self.formactivities.tblActivities.setItem(i, 2, QTableWidgetItem(str(baris["name"])))
            self.formactivities.tblActivities.setItem(i, 3, QTableWidgetItem(str(baris.get("start_time", "") or "")))
            self.formactivities.tblActivities.setItem(i, 4, QTableWidgetItem(str(baris.get("finish_time", "") or "")))

    def cariDataActivities(self):
        varCari = self.formactivities.lineCari.text() if hasattr(self.formactivities, "lineCari") else ""
        self.formactivities.tblActivities.setRowCount(0)
        data = self.aksi.filterActivities(varCari) if varCari else self.aksi.dataActivities()
        for i, baris in enumerate(data):
            self.formactivities.tblActivities.insertRow(i)
            self.formactivities.tblActivities.setItem(i, 0, QTableWidgetItem(str(baris["id"])))
            self.formactivities.tblActivities.setItem(i, 1, QTableWidgetItem(str(baris["cycle_id"])))
            self.formactivities.tblActivities.setItem(i, 2, QTableWidgetItem(str(baris["name"])))
            self.formactivities.tblActivities.setItem(i, 3, QTableWidgetItem(str(baris.get("start_time", "") or "")))
            self.formactivities.tblActivities.setItem(i, 4, QTableWidgetItem(str(baris.get("finish_time", "") or "")))

    def laporanActivities(self):
        cari = self.formactivities.txtFilter.text().strip() if hasattr(self.formactivities, "txtFilter") else ""
        filter_ = self.formactivities.comboFilter.currentText() if hasattr(self.formactivities, "comboFilter") else "Semua"
        try:
            if filter_ == "Semua" or not cari:
                self.aksi.cetakActivities()
            else:
                self.aksi.cetakFilterActivities(cari)  # cycle_id
            QMessageBox.information(None, "Informasi", "Laporan berhasil dibuat: Laporan Activities.pdf")
        except Exception as e:
            QMessageBox.information(None, "Informasi", f"Gagal cetak: {e}")

    def pilihBaris(self, row, col):
        _ = col

        def item(c):
            it = self.formactivities.tblActivities.item(row, c)
            return it.text() if it else ""

        self.formactivities.EditId.setText(item(0))
        self._combo_set_by_id(self.formactivities.EditCycleId, item(1))
        self.formactivities.EditName.setText(item(2))
        self.formactivities.EditStart.setText(item(3))
        self.formactivities.EditFinish.setText(item(4))
