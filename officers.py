# This Python file uses the following encoding: utf-8
from PySide6.QtWidgets import QWidget, QTableWidgetItem, QMessageBox
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader

from crud import crud_2310010408


class form_officers(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        filenya = QFile('officers.ui')
        filenya.open(QFile.ReadOnly)
        muatfile = QUiLoader()
        self.formofficers = muatfile.load(filenya, self)
        self.setWindowTitle(self.formofficers.windowTitle())


        self.aksi = crud_2310010408()

        self.formofficers.BtnSimpan.clicked.connect(self.simpanOfficers)
        self.formofficers.BtnUbah.clicked.connect(self.ubahOfficers)
        self.formofficers.BtnHapus.clicked.connect(self.hapusOfficers)

        self.formofficers.lineCari.textChanged.connect(self.cariDataOfficers)
        self.formofficers.btnCetak.clicked.connect(self.laporanOfficers)
        self.formofficers.tblOfficers.cellClicked.connect(self.pilihBaris)

        self.tampilDataOfficers()

    def simpanOfficers(self):
        if not self.formofficers.EditReg.text().strip():
            QMessageBox.information(None, 'Informasi', 'Official Reg Number belum diisi')
            self.formofficers.EditReg.setFocus()
        elif not self.formofficers.EditName.text().strip():
            QMessageBox.information(None, 'Informasi', 'Name belum diisi')
            self.formofficers.EditName.setFocus()
        elif not self.formofficers.EditEmail.text().strip():
            QMessageBox.information(None, 'Informasi', 'Email belum diisi')
            self.formofficers.EditEmail.setFocus()
        elif not self.formofficers.EditPassword.text().strip():
            QMessageBox.information(None, 'Informasi', 'Password belum diisi')
            self.formofficers.EditPassword.setFocus()
        else:
            reg = self.formofficers.EditReg.text()
            name = self.formofficers.EditName.text()
            email = self.formofficers.EditEmail.text()
            password = self.formofficers.EditPassword.text()
            segment = self.formofficers.EditSegment.text()
            license_expired = self.formofficers.EditLicense.text()
            try:
                self.aksi.tambahOfficers(reg, name, email, password, segment, license_expired)
                self.tampilDataOfficers()
                QMessageBox.information(None, 'Informasi', 'Data berhasil disimpan')
            except Exception as e:
                QMessageBox.information(None, 'Informasi', f'Gagal simpan: {e}')

    def ubahOfficers(self):
        if not self.formofficers.EditId.text().strip():
            QMessageBox.information(None, 'Informasi', 'ID belum diisi (pilih data di tabel atau isi manual)')
            self.formofficers.EditId.setFocus()
            return

        id_ = self.formofficers.EditId.text()
        reg = self.formofficers.EditReg.text()
        name = self.formofficers.EditName.text()
        email = self.formofficers.EditEmail.text()
        password = self.formofficers.EditPassword.text().strip()
        segment = self.formofficers.EditSegment.text()
        license_expired = self.formofficers.EditLicense.text()

        if not password:
            try:
                lama = self.aksi.getPasswordOfficer(id_)
                password = lama
            except Exception:
                password = ''

        try:
            self.aksi.gantiOfficers(id_, reg, name, email, password, segment, license_expired)
            self.tampilDataOfficers()
            QMessageBox.information(None, 'Informasi', 'Data berhasil diubah')
        except Exception as e:
            QMessageBox.information(None, 'Informasi', f'Gagal ubah: {e}')

    def hapusOfficers(self):
        if not self.formofficers.EditId.text().strip():
            QMessageBox.information(None, 'Informasi', 'ID belum diisi (pilih data di tabel atau isi manual)')
            return

        pesan = QMessageBox.information(
            None,
            'Informasi',
            'Apakah yakin menghapus data ini?',
            QMessageBox.Yes | QMessageBox.No
        )

        if pesan == QMessageBox.Yes:
            id_ = self.formofficers.EditId.text()
            try:
                self.aksi.kurangOfficers(id_)
                self.tampilDataOfficers()
                QMessageBox.information(None, 'Informasi', 'Data berhasil dihapus')
            except Exception as e:
                QMessageBox.information(None, 'Informasi', f'Gagal hapus: {e}')

    def tampilDataOfficers(self):
        self.formofficers.tblOfficers.setRowCount(0)
        data = self.aksi.dataOfficers()
        for i, baris in enumerate(data):
            self.formofficers.tblOfficers.insertRow(i)
            self.formofficers.tblOfficers.setItem(i, 0, QTableWidgetItem(str(baris['id'])))
            self.formofficers.tblOfficers.setItem(i, 1, QTableWidgetItem(str(baris['official_reg_number'])))
            self.formofficers.tblOfficers.setItem(i, 2, QTableWidgetItem(str(baris['name'])))
            self.formofficers.tblOfficers.setItem(i, 3, QTableWidgetItem(str(baris['email'])))
            self.formofficers.tblOfficers.setItem(i, 4, QTableWidgetItem(str(baris.get('segment', '') or '')))
            self.formofficers.tblOfficers.setItem(i, 5, QTableWidgetItem(str(baris.get('license_expired', '') or '')))

    def cariDataOfficers(self):
        varCari = self.formofficers.lineCari.text()
        self.formofficers.tblOfficers.setRowCount(0)
        data = self.aksi.filterOfficers(varCari) if varCari else self.aksi.dataOfficers()
        for i, baris in enumerate(data):
            self.formofficers.tblOfficers.insertRow(i)
            self.formofficers.tblOfficers.setItem(i, 0, QTableWidgetItem(str(baris['id'])))
            self.formofficers.tblOfficers.setItem(i, 1, QTableWidgetItem(str(baris['official_reg_number'])))
            self.formofficers.tblOfficers.setItem(i, 2, QTableWidgetItem(str(baris['name'])))
            self.formofficers.tblOfficers.setItem(i, 3, QTableWidgetItem(str(baris['email'])))
            self.formofficers.tblOfficers.setItem(i, 4, QTableWidgetItem(str(baris.get('segment', '') or '')))
            self.formofficers.tblOfficers.setItem(i, 5, QTableWidgetItem(str(baris.get('license_expired', '') or '')))

    def laporanOfficers(self):
        cari = self.formofficers.txtFilter.text().strip()
        filter_ = self.formofficers.comboFilter.currentText()
        try:
            if filter_ == 'Semua' or not cari:
                self.aksi.cetakOfficers()
            else:
                self.aksi.cetakFilterOfficers(cari)
            QMessageBox.information(None, 'Informasi', 'Laporan berhasil dibuat: Laporan Officers.pdf')
        except Exception as e:
            QMessageBox.information(None, 'Informasi', f'Gagal cetak: {e}')

    def pilihBaris(self, row, col):
        _ = col
        def item(c):
            it = self.formofficers.tblOfficers.item(row, c)
            return it.text() if it else ''

        self.formofficers.EditId.setText(item(0))
        self.formofficers.EditReg.setText(item(1))
        self.formofficers.EditName.setText(item(2))
        self.formofficers.EditEmail.setText(item(3))
        self.formofficers.EditSegment.setText(item(4))
        self.formofficers.EditLicense.setText(item(5))
        self.formofficers.EditPassword.setText('')
