# This Python file uses the following encoding: utf-8
from PySide6.QtWidgets import QWidget, QTableWidgetItem, QMessageBox
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader

from crud import crud_2310010408


class form_vehicles(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        filenya = QFile('vehicles.ui')
        filenya.open(QFile.ReadOnly)
        muatfile = QUiLoader()
        self.formvehicles = muatfile.load(filenya, self)
        self.setWindowTitle(self.formvehicles.windowTitle())

        self.aksi = crud_2310010408()

        self.formvehicles.BtnSimpan.clicked.connect(self.simpanVehicles)
        self.formvehicles.BtnUbah.clicked.connect(self.ubahVehicles)
        self.formvehicles.BtnHapus.clicked.connect(self.hapusVehicles)

        self.formvehicles.lineCari.textChanged.connect(self.cariDataVehicles)
        self.formvehicles.btnCetak.clicked.connect(self.laporanVehicles)
        self.formvehicles.tblVehicles.cellClicked.connect(self.pilihBaris)

        self.tampilDataVehicles()

    def simpanVehicles(self):
        if not self.formvehicles.EditSerial.text().strip():
            QMessageBox.information(None, 'Informasi', 'Serial Number belum diisi')
            self.formvehicles.EditSerial.setFocus()
        elif not self.formvehicles.EditModel.text().strip():
            QMessageBox.information(None, 'Informasi', 'Model belum diisi')
            self.formvehicles.EditModel.setFocus()
        elif not self.formvehicles.EditYear.text().strip():
            QMessageBox.information(None, 'Informasi', 'Production Year belum diisi')
            self.formvehicles.EditYear.setFocus()
        else:
            serial = self.formvehicles.EditSerial.text()
            model = self.formvehicles.EditModel.text()
            year = self.formvehicles.EditYear.text()
            try:
                self.aksi.tambahVehicles(serial, model, year)
                self.tampilDataVehicles()
                QMessageBox.information(None, 'Informasi', 'Data berhasil disimpan')
            except Exception as e:
                QMessageBox.information(None, 'Informasi', f'Gagal simpan: {e}')

    def ubahVehicles(self):
        if not self.formvehicles.EditId.text().strip():
            QMessageBox.information(None, 'Informasi', 'ID belum diisi (pilih data di tabel atau isi manual)')
            self.formvehicles.EditId.setFocus()
            return

        id_ = self.formvehicles.EditId.text()
        serial = self.formvehicles.EditSerial.text()
        model = self.formvehicles.EditModel.text()
        year = self.formvehicles.EditYear.text()
        try:
            self.aksi.gantiVehicles(id_, serial, model, year)
            self.tampilDataVehicles()
            QMessageBox.information(None, 'Informasi', 'Data berhasil diubah')
        except Exception as e:
            QMessageBox.information(None, 'Informasi', f'Gagal ubah: {e}')

    def hapusVehicles(self):
        if not self.formvehicles.EditId.text().strip():
            QMessageBox.information(None, 'Informasi', 'ID belum diisi (pilih data di tabel atau isi manual)')
            return

        pesan = QMessageBox.information(
            None,
            'Informasi',
            'Apakah yakin menghapus data ini?',
            QMessageBox.Yes | QMessageBox.No
        )

        if pesan == QMessageBox.Yes:
            id_ = self.formvehicles.EditId.text()
            try:
                self.aksi.kurangVehicles(id_)
                self.tampilDataVehicles()
                QMessageBox.information(None, 'Informasi', 'Data berhasil dihapus')
            except Exception as e:
                QMessageBox.information(None, 'Informasi', f'Gagal hapus: {e}')

    def tampilDataVehicles(self):
        self.formvehicles.tblVehicles.setRowCount(0)
        data = self.aksi.dataVehicles()
        for i, baris in enumerate(data):
            self.formvehicles.tblVehicles.insertRow(i)
            self.formvehicles.tblVehicles.setItem(i, 0, QTableWidgetItem(str(baris['id'])))
            self.formvehicles.tblVehicles.setItem(i, 1, QTableWidgetItem(str(baris['serial_number'])))
            self.formvehicles.tblVehicles.setItem(i, 2, QTableWidgetItem(str(baris['model'])))
            self.formvehicles.tblVehicles.setItem(i, 3, QTableWidgetItem(str(baris['production_year'])))

    def cariDataVehicles(self):
        varCari = self.formvehicles.lineCari.text()
        self.formvehicles.tblVehicles.setRowCount(0)
        data = self.aksi.filterVehicles(varCari) if varCari else self.aksi.dataVehicles()
        for i, baris in enumerate(data):
            self.formvehicles.tblVehicles.insertRow(i)
            self.formvehicles.tblVehicles.setItem(i, 0, QTableWidgetItem(str(baris['id'])))
            self.formvehicles.tblVehicles.setItem(i, 1, QTableWidgetItem(str(baris['serial_number'])))
            self.formvehicles.tblVehicles.setItem(i, 2, QTableWidgetItem(str(baris['model'])))
            self.formvehicles.tblVehicles.setItem(i, 3, QTableWidgetItem(str(baris['production_year'])))

    def laporanVehicles(self):
        cari = self.formvehicles.txtFilter.text().strip()
        filter_ = self.formvehicles.comboFilter.currentText()
        try:
            if filter_ == 'Semua' or not cari:
                self.aksi.cetakVehicles()
            else:
                self.aksi.cetakFilterVehicles(cari)
            QMessageBox.information(None, 'Informasi', 'Laporan berhasil dibuat: Laporan Vehicles.pdf')
        except Exception as e:
            QMessageBox.information(None, 'Informasi', f'Gagal cetak: {e}')

    def pilihBaris(self, row, col):
        _ = col
        def item(c):
            it = self.formvehicles.tblVehicles.item(row, c)
            return it.text() if it else ''

        self.formvehicles.EditId.setText(item(0))
        self.formvehicles.EditSerial.setText(item(1))
        self.formvehicles.EditModel.setText(item(2))
        self.formvehicles.EditYear.setText(item(3))
