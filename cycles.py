# This Python file uses the following encoding: utf-8
import os
from PySide6.QtWidgets import QWidget, QTableWidgetItem, QMessageBox
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader

from crud import crud_2310010408


class form_cycles(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        ui_path = os.path.join(os.path.dirname(__file__), "cycles.ui")
        filenya = QFile(ui_path)
        if not filenya.open(QFile.ReadOnly):
            raise RuntimeError(f"Gagal membuka UI: {ui_path}")

        muatfile = QUiLoader()
        self.formcycles = muatfile.load(filenya, self)
        self.setWindowTitle(self.formcycles.windowTitle())
        filenya.close()

        try:
            self.resize(self.formcycles.size())
        except Exception:
            pass

        self.aksi = crud_2310010408()

        self._load_drive_options()

        self.formcycles.BtnSimpan.clicked.connect(self.simpanCycles)
        self.formcycles.BtnUbah.clicked.connect(self.ubahCycles)
        self.formcycles.BtnHapus.clicked.connect(self.hapusCycles)

        if hasattr(self.formcycles, "lineCari"):
            self.formcycles.lineCari.textChanged.connect(self.cariDataCycles)

        self.formcycles.btnCetak.clicked.connect(self.laporanCycles)
        self.formcycles.tblCycles.cellClicked.connect(self.pilihBaris)

        self.tampilDataCycles()

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

    def _load_drive_options(self):
        cb = self.formcycles.EditDriveId
        if not hasattr(cb, "clear"):
            return
        cb.clear()
        cb.addItem("-- pilih drive --", None)
        try:
            for d in self.aksi.dataDrives():
                label = f"{d.get('id')} - officer {d.get('officer_id')} / vehicle {d.get('vehicle_id')} ({d.get('date','')})"
                cb.addItem(label.strip(), d.get("id"))
        except Exception:
            pass

    def simpanCycles(self):
        drive_id = self._combo_get_id(self.formcycles.EditDriveId)
        if drive_id is None:
            QMessageBox.information(None, "Informasi", "Drive ID belum dipilih")
            return
        if not self.formcycles.EditStart.text().strip():
            QMessageBox.information(None, "Informasi", "Start Time belum diisi")
            self.formcycles.EditStart.setFocus()
            return

        start_time = self.formcycles.EditStart.text()
        finish_time = self.formcycles.EditFinish.text()
        date_ = self.formcycles.EditDate.text()

        try:
            self.aksi.tambahCycles(drive_id, start_time, finish_time, date_)
            self.tampilDataCycles()
            QMessageBox.information(None, "Informasi", "Data berhasil disimpan")
        except Exception as e:
            QMessageBox.information(None, "Informasi", f"Gagal simpan: {e}")

    def ubahCycles(self):
        if not self.formcycles.EditId.text().strip():
            QMessageBox.information(None, "Informasi", "ID belum diisi (pilih data di tabel)")
            self.formcycles.EditId.setFocus()
            return

        id_ = self.formcycles.EditId.text()
        drive_id = self._combo_get_id(self.formcycles.EditDriveId)
        start_time = self.formcycles.EditStart.text()
        finish_time = self.formcycles.EditFinish.text()
        date_ = self.formcycles.EditDate.text()

        if drive_id is None:
            QMessageBox.information(None, "Informasi", "Drive ID belum dipilih")
            return
        if not start_time.strip():
            QMessageBox.information(None, "Informasi", "Start Time belum diisi")
            return

        try:
            self.aksi.gantiCycles(id_, drive_id, start_time, finish_time, date_)
            self.tampilDataCycles()
            QMessageBox.information(None, "Informasi", "Data berhasil diubah")
        except Exception as e:
            QMessageBox.information(None, "Informasi", f"Gagal ubah: {e}")

    def hapusCycles(self):
        if not self.formcycles.EditId.text().strip():
            QMessageBox.information(None, "Informasi", "ID belum diisi (pilih data di tabel)")
            return

        pesan = QMessageBox.information(
            None, "Informasi", "Apakah yakin menghapus data ini?", QMessageBox.Yes | QMessageBox.No
        )
        if pesan != QMessageBox.Yes:
            return

        id_ = self.formcycles.EditId.text()
        try:
            self.aksi.kurangCycles(id_)
            self.tampilDataCycles()
            QMessageBox.information(None, "Informasi", "Data berhasil dihapus")
        except Exception as e:
            QMessageBox.information(None, "Informasi", f"Gagal hapus: {e}")

    def tampilDataCycles(self):
        self.formcycles.tblCycles.setRowCount(0)
        data = self.aksi.dataCycles()
        for i, baris in enumerate(data):
            self.formcycles.tblCycles.insertRow(i)
            self.formcycles.tblCycles.setItem(i, 0, QTableWidgetItem(str(baris["id"])))
            self.formcycles.tblCycles.setItem(i, 1, QTableWidgetItem(str(baris["drive_id"])))
            self.formcycles.tblCycles.setItem(i, 2, QTableWidgetItem(str(baris["start_time"])))
            self.formcycles.tblCycles.setItem(i, 3, QTableWidgetItem(str(baris.get("finish_time", "") or "")))
            self.formcycles.tblCycles.setItem(i, 4, QTableWidgetItem(str(baris.get("date", "") or "")))

    def cariDataCycles(self):
        varCari = self.formcycles.lineCari.text() if hasattr(self.formcycles, "lineCari") else ""
        self.formcycles.tblCycles.setRowCount(0)
        data = self.aksi.filterCycles(varCari) if varCari else self.aksi.dataCycles()
        for i, baris in enumerate(data):
            self.formcycles.tblCycles.insertRow(i)
            self.formcycles.tblCycles.setItem(i, 0, QTableWidgetItem(str(baris["id"])))
            self.formcycles.tblCycles.setItem(i, 1, QTableWidgetItem(str(baris["drive_id"])))
            self.formcycles.tblCycles.setItem(i, 2, QTableWidgetItem(str(baris["start_time"])))
            self.formcycles.tblCycles.setItem(i, 3, QTableWidgetItem(str(baris.get("finish_time", "") or "")))
            self.formcycles.tblCycles.setItem(i, 4, QTableWidgetItem(str(baris.get("date", "") or "")))

    def laporanCycles(self):
        cari = self.formcycles.txtFilter.text().strip() if hasattr(self.formcycles, "txtFilter") else ""
        filter_ = self.formcycles.comboFilter.currentText() if hasattr(self.formcycles, "comboFilter") else "Semua"
        try:
            if filter_ == "Semua" or not cari:
                self.aksi.cetakCycles()
            else:
                self.aksi.cetakFilterCycles(cari)  # date YYYY-MM-DD
            QMessageBox.information(None, "Informasi", "Laporan berhasil dibuat: Laporan Cycles.pdf")
        except Exception as e:
            QMessageBox.information(None, "Informasi", f"Gagal cetak: {e}")

    def pilihBaris(self, row, col):
        _ = col

        def item(c):
            it = self.formcycles.tblCycles.item(row, c)
            return it.text() if it else ""

        self.formcycles.EditId.setText(item(0))
        self._combo_set_by_id(self.formcycles.EditDriveId, item(1))
        self.formcycles.EditStart.setText(item(2))
        self.formcycles.EditFinish.setText(item(3))
        self.formcycles.EditDate.setText(item(4))
