# This Python file uses the following encoding: utf-8
import datetime
import mysql.connector
from reportlab.platypus import SimpleDocTemplate, Table
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors

class crud_2310010408:
    def __init__(self):
        self.koneksi = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='db_2310010408'
        )

    def _now(self):
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def _cetak_pdf(self, judul, headers, data_rows, file_laporan):

        baris_data = [headers] + list(data_rows)
        pagesize = landscape(A4) if len(headers) > 6 else A4
        pdf = SimpleDocTemplate(file_laporan, pagesize=pagesize)
        tabel = Table(baris_data)
        pdf.build([tabel])

    def tambahVehicles(self, serial, model, year):
        aksi = self.koneksi.cursor()
        aksi.execute(
            "insert into vehicles (serial_number, model, production_year, created_at, updated_at) values(%s, %s, %s, %s, %s)",
            (serial, model, year, self._now(), self._now())
        )
        self.koneksi.commit()
        aksi.close()

    def gantiVehicles(self, id_, serial, model, year):
        aksi = self.koneksi.cursor()
        aksi.execute(
            "update vehicles set serial_number=%s, model=%s, production_year=%s, updated_at=%s where id=%s",
            (serial, model, year, self._now(), id_)
        )
        self.koneksi.commit()
        aksi.close()

    def kurangVehicles(self, id_):
        aksi = self.koneksi.cursor()
        aksi.execute("delete from vehicles where id=%s", (id_,))
        self.koneksi.commit()
        aksi.close()

    def dataVehicles(self):
        aksi = self.koneksi.cursor(dictionary=True)
        aksi.execute("select id, serial_number, model, production_year from vehicles order by id asc")
        data = aksi.fetchall()
        aksi.close()
        return data

    def filterVehicles(self, cari):
        aksi = self.koneksi.cursor(dictionary=True)
        aksi.execute(
            "select id, serial_number, model, production_year from vehicles where id like %s or serial_number like %s or model like %s or production_year like %s order by id asc",
            ([f"%{cari}%", f"%{cari}%", f"%{cari}%", f"%{cari}%"])
        )
        data = aksi.fetchall()
        aksi.close()
        return data

    def cetakVehicles(self):
        aksi = self.koneksi.cursor()
        aksi.execute("select id, serial_number, model, production_year from vehicles order by id asc")
        data = aksi.fetchall()
        aksi.close()
        self._cetak_pdf(
            "Vehicles",
            ["ID", "Serial Number", "Model", "Production Year"],
            data,
            "Laporan Vehicles.pdf"
        )

    def cetakFilterVehicles(self, year):
        aksi = self.koneksi.cursor()
        aksi.execute(
            "select id, serial_number, model, production_year from vehicles where production_year=%s order by id asc",
            (year,)
        )
        data = aksi.fetchall()
        aksi.close()
        self._cetak_pdf(
            "Vehicles",
            ["ID", "Serial Number", "Model", "Production Year"],
            data,
            "Laporan Vehicles.pdf"
        )

    def tambahOfficers(self, reg, name, email, password, segment, license_expired):
        aksi = self.koneksi.cursor()
        aksi.execute(
            "insert into officers (official_reg_number, name, email, password, segment, license_expired, created_at, updated_at) values(%s, %s, %s, %s, %s, %s, %s, %s)",
            (reg, name, email, password, segment or None, license_expired or None, self._now(), self._now())
        )
        self.koneksi.commit()
        aksi.close()

    def gantiOfficers(self, id_, reg, name, email, password, segment, license_expired):
        aksi = self.koneksi.cursor()
        aksi.execute(
            "update officers set official_reg_number=%s, name=%s, email=%s, password=%s, segment=%s, license_expired=%s, updated_at=%s where id=%s",
            (reg, name, email, password, segment or None, license_expired or None, self._now(), id_)
        )
        self.koneksi.commit()
        aksi.close()

    def kurangOfficers(self, id_):
        aksi = self.koneksi.cursor()
        aksi.execute("delete from officers where id=%s", (id_,))
        self.koneksi.commit()
        aksi.close()

    def dataOfficers(self):
        aksi = self.koneksi.cursor(dictionary=True)
        aksi.execute("select id, official_reg_number, name, email, segment, license_expired from officers order by id asc")
        data = aksi.fetchall()
        aksi.close()
        return data

    def filterOfficers(self, cari):
        aksi = self.koneksi.cursor(dictionary=True)
        aksi.execute(
            "select id, official_reg_number, name, email, segment, license_expired from officers where id like %s or official_reg_number like %s or name like %s or email like %s or segment like %s order by id asc",
            ([f"%{cari}%", f"%{cari}%", f"%{cari}%", f"%{cari}%", f"%{cari}%"])
        )
        data = aksi.fetchall()
        aksi.close()
        return data


    def getPasswordOfficer(self, id_):
        aksi = self.koneksi.cursor()
        aksi.execute("select password from officers where id=%s", (id_,))
        row = aksi.fetchone()
        aksi.close()
        return row[0] if row else ""

    def cetakOfficers(self):
        aksi = self.koneksi.cursor()
        aksi.execute("select id, official_reg_number, name, email, segment, license_expired from officers order by id asc")
        data = aksi.fetchall()
        aksi.close()
        self._cetak_pdf(
            "Officers",
            ["ID", "Reg Number", "Name", "Email", "Segment", "License Expired"],
            data,
            "Laporan Officers.pdf"
        )

    def cetakFilterOfficers(self, segment):
        aksi = self.koneksi.cursor()
        aksi.execute(
            "select id, official_reg_number, name, email, segment, license_expired from officers where segment=%s order by id asc",
            (segment,)
        )
        data = aksi.fetchall()
        aksi.close()
        self._cetak_pdf(
            "Officers",
            ["ID", "Reg Number", "Name", "Email", "Segment", "License Expired"],
            data,
            "Laporan Officers.pdf"
        )

    def tambahDrives(self, officer_id, vehicle_id, active, latitude, longitude, date_):
        aksi = self.koneksi.cursor()
        aksi.execute(
            "insert into drives (officer_id, vehicle_id, active, latitude, longitude, date, created_at, updated_at) values(%s, %s, %s, %s, %s, %s, %s, %s)",
            (int(officer_id), int(vehicle_id), int(active), latitude or None, longitude or None, date_ or None, self._now(), self._now())
        )
        self.koneksi.commit()
        aksi.close()

    def gantiDrives(self, id_, officer_id, vehicle_id, active, latitude, longitude, date_):
        aksi = self.koneksi.cursor()
        aksi.execute(
            "update drives set officer_id=%s, vehicle_id=%s, active=%s, latitude=%s, longitude=%s, date=%s, updated_at=%s where id=%s",
            (int(officer_id), int(vehicle_id), int(active), latitude or None, longitude or None, date_ or None, self._now(), id_)
        )
        self.koneksi.commit()
        aksi.close()

    def kurangDrives(self, id_):
        aksi = self.koneksi.cursor()
        aksi.execute("delete from drives where id=%s", (id_,))
        self.koneksi.commit()
        aksi.close()

    def dataDrives(self):
        aksi = self.koneksi.cursor(dictionary=True)
        aksi.execute("select id, officer_id, vehicle_id, active, latitude, longitude, date from drives order by id asc")
        data = aksi.fetchall()
        aksi.close()
        return data

    def filterDrives(self, cari):
        aksi = self.koneksi.cursor(dictionary=True)
        aksi.execute(
            "select id, officer_id, vehicle_id, active, latitude, longitude, date from drives where id like %s or officer_id like %s or vehicle_id like %s or active like %s or date like %s order by id asc",
            ([f"%{cari}%", f"%{cari}%", f"%{cari}%", f"%{cari}%", f"%{cari}%"])
        )
        data = aksi.fetchall()
        aksi.close()
        return data

    def cetakDrives(self):
        aksi = self.koneksi.cursor()
        aksi.execute("select id, officer_id, vehicle_id, active, latitude, longitude, date from drives order by id asc")
        data = aksi.fetchall()
        aksi.close()
        self._cetak_pdf(
            "Drives",
            ["ID", "Officer ID", "Vehicle ID", "Active", "Latitude", "Longitude", "Date"],
            data,
            "Laporan Drives.pdf"
        )

    def cetakFilterDrives(self, active):
        aksi = self.koneksi.cursor()
        aksi.execute(
            "select id, officer_id, vehicle_id, active, latitude, longitude, date from drives where active=%s order by id asc",
            (int(active),)
        )
        data = aksi.fetchall()
        aksi.close()
        self._cetak_pdf(
            "Drives",
            ["ID", "Officer ID", "Vehicle ID", "Active", "Latitude", "Longitude", "Date"],
            data,
            "Laporan Drives.pdf"
        )

    def tambahCycles(self, drive_id, start_time, finish_time, date_):
        aksi = self.koneksi.cursor()
        aksi.execute(
            "insert into cycles (drive_id, start_time, finish_time, date, created_at, updated_at) values(%s, %s, %s, %s, %s, %s)",
            (int(drive_id), start_time, finish_time or None, date_ or None, self._now(), self._now())
        )
        self.koneksi.commit()
        aksi.close()

    def gantiCycles(self, id_, drive_id, start_time, finish_time, date_):
        aksi = self.koneksi.cursor()
        aksi.execute(
            "update cycles set drive_id=%s, start_time=%s, finish_time=%s, date=%s, updated_at=%s where id=%s",
            (int(drive_id), start_time, finish_time or None, date_ or None, self._now(), id_)
        )
        self.koneksi.commit()
        aksi.close()

    def kurangCycles(self, id_):
        aksi = self.koneksi.cursor()
        aksi.execute("delete from cycles where id=%s", (id_,))
        self.koneksi.commit()
        aksi.close()

    def dataCycles(self):
        aksi = self.koneksi.cursor(dictionary=True)
        aksi.execute("select id, drive_id, start_time, finish_time, date from cycles order by id asc")
        data = aksi.fetchall()
        aksi.close()
        return data

    def filterCycles(self, cari):
        aksi = self.koneksi.cursor(dictionary=True)
        aksi.execute(
            "select id, drive_id, start_time, finish_time, date from cycles where id like %s or drive_id like %s or start_time like %s or finish_time like %s or date like %s order by id asc",
            ([f"%{cari}%", f"%{cari}%", f"%{cari}%", f"%{cari}%", f"%{cari}%"])
        )
        data = aksi.fetchall()
        aksi.close()
        return data

    def cetakCycles(self):
        aksi = self.koneksi.cursor()
        aksi.execute("select id, drive_id, start_time, finish_time, date from cycles order by id asc")
        data = aksi.fetchall()
        aksi.close()
        self._cetak_pdf(
            "Cycles",
            ["ID", "Drive ID", "Start Time", "Finish Time", "Date"],
            data,
            "Laporan Cycles.pdf"
        )

    def cetakFilterCycles(self, date_):
        aksi = self.koneksi.cursor()
        aksi.execute(
            "select id, drive_id, start_time, finish_time, date from cycles where date=%s order by id asc",
            (date_,)
        )
        data = aksi.fetchall()
        aksi.close()
        self._cetak_pdf(
            "Cycles",
            ["ID", "Drive ID", "Start Time", "Finish Time", "Date"],
            data,
            "Laporan Cycles.pdf"
        )

    def tambahActivities(self, cycle_id, name, start_time, finish_time):
        aksi = self.koneksi.cursor()
        aksi.execute(
            "insert into activities (cycle_id, name, start_time, finish_time, created_at, updated_at) values(%s, %s, %s, %s, %s, %s)",
            (int(cycle_id), name, start_time or None, finish_time or None, self._now(), self._now())
        )
        self.koneksi.commit()
        aksi.close()

    def gantiActivities(self, id_, cycle_id, name, start_time, finish_time):
        aksi = self.koneksi.cursor()
        aksi.execute(
            "update activities set cycle_id=%s, name=%s, start_time=%s, finish_time=%s, updated_at=%s where id=%s",
            (int(cycle_id), name, start_time or None, finish_time or None, self._now(), id_)
        )
        self.koneksi.commit()
        aksi.close()

    def kurangActivities(self, id_):
        aksi = self.koneksi.cursor()
        aksi.execute("delete from activities where id=%s", (id_,))
        self.koneksi.commit()
        aksi.close()

    def dataActivities(self):
        aksi = self.koneksi.cursor(dictionary=True)
        aksi.execute("select id, cycle_id, name, start_time, finish_time from activities order by id asc")
        data = aksi.fetchall()
        aksi.close()
        return data

    def filterActivities(self, cari):
        aksi = self.koneksi.cursor(dictionary=True)
        aksi.execute(
            "select id, cycle_id, name, start_time, finish_time from activities where id like %s or cycle_id like %s or name like %s order by id asc",
            ([f"%{cari}%", f"%{cari}%", f"%{cari}%"])
        )
        data = aksi.fetchall()
        aksi.close()
        return data

    def cetakActivities(self):
        aksi = self.koneksi.cursor()
        aksi.execute("select id, cycle_id, name, start_time, finish_time from activities order by id asc")
        data = aksi.fetchall()
        aksi.close()
        self._cetak_pdf(
            "Activities",
            ["ID", "Cycle ID", "Name", "Start Time", "Finish Time"],
            data,
            "Laporan Activities.pdf"
        )

    def cetakFilterActivities(self, cycle_id):
        aksi = self.koneksi.cursor()
        aksi.execute(
            "select id, cycle_id, name, start_time, finish_time from activities where cycle_id=%s order by id asc",
            (int(cycle_id),)
        )
        data = aksi.fetchall()
        aksi.close()
        self._cetak_pdf(
            "Activities",
            ["ID", "Cycle ID", "Name", "Start Time", "Finish Time"],
            data,
            "Laporan Activities.pdf"
        )

    def tambahQueues(self, excavator_id, truck_id, waiting):
        aksi = self.koneksi.cursor()
        aksi.execute(
            "insert into queues (excavator_id, truck_id, waiting, created_at, updated_at) values(%s, %s, %s, %s, %s)",
            (int(excavator_id), int(truck_id), int(waiting), self._now(), self._now())
        )
        self.koneksi.commit()
        aksi.close()

    def gantiQueues(self, id_, excavator_id, truck_id, waiting):
        aksi = self.koneksi.cursor()
        aksi.execute(
            "update queues set excavator_id=%s, truck_id=%s, waiting=%s, updated_at=%s where id=%s",
            (int(excavator_id), int(truck_id), int(waiting), self._now(), id_)
        )
        self.koneksi.commit()
        aksi.close()

    def kurangQueues(self, id_):
        aksi = self.koneksi.cursor()
        aksi.execute("delete from queues where id=%s", (id_,))
        self.koneksi.commit()
        aksi.close()

    def dataQueues(self):
        aksi = self.koneksi.cursor(dictionary=True)
        aksi.execute("select id, excavator_id, truck_id, waiting from queues order by id asc")
        data = aksi.fetchall()
        aksi.close()
        return data

    def filterQueues(self, cari):
        aksi = self.koneksi.cursor(dictionary=True)
        aksi.execute(
            "select id, excavator_id, truck_id, waiting from queues where id like %s or excavator_id like %s or truck_id like %s or waiting like %s order by id asc",
            ([f"%{cari}%", f"%{cari}%", f"%{cari}%", f"%{cari}%"])
        )
        data = aksi.fetchall()
        aksi.close()
        return data

    def cetakQueues(self):
        aksi = self.koneksi.cursor()
        aksi.execute("select id, excavator_id, truck_id, waiting from queues order by id asc")
        data = aksi.fetchall()
        aksi.close()
        self._cetak_pdf(
            "Queues",
            ["ID", "Excavator ID", "Truck ID", "Waiting"],
            data,
            "Laporan Queues.pdf"
        )

    def cetakFilterQueues(self, waiting):
        aksi = self.koneksi.cursor()
        aksi.execute(
            "select id, excavator_id, truck_id, waiting from queues where waiting=%s order by id asc",
            (int(waiting),)
        )
        data = aksi.fetchall()
        aksi.close()
        self._cetak_pdf(
            "Queues",
            ["ID", "Excavator ID", "Truck ID", "Waiting"],
            data,
            "Laporan Queues.pdf"
        )
