import mysql.connector
from mysql.connector import Error

class crud:
    def _init_(self):
        try:
            self.koneksi = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='db_2310010408'
            )
            self.koneksi.autocommit = True
        except Error as e:
            raise RuntimeError(f"Gagal koneksi DB: {e}")

    __init__ = _init_

    def cursor(self):
        if not getattr(self, "koneksi", None) or not self.koneksi.is_connected():
            self._init_()
        return self.koneksi.cursor(dictionary=True)

    def fetch_all(self, table):
        cur = self.cursor()
        cur.execute(f"SELECT * FROM `{table}`")
        return cur.fetchall()

    def fetch_by_id(self, table, id_value):
        cur = self.cursor()
        cur.execute(f"SELECT * FROM `{table}` WHERE id=%s", (id_value,))
        return cur.fetchone()

    def show_columns(self, table):
        cur = self.cursor()
        cur.execute(f"SHOW COLUMNS FROM `{table}`")
        return cur.fetchall()

    def insert(self, table, data: dict):
        cols = [k for k,v in data.items() if v is not None]
        vals = [data[k] for k in cols]
        placeholders = ", ".join(["%s"] * len(cols))
        colnames = ", ".join([f"`{c}`" for c in cols])
        sql = f"INSERT INTO `{table}` ({colnames}) VALUES ({placeholders})"
        cur = self.cursor()
        cur.execute(sql, tuple(vals))
        return cur.lastrowid

    def update(self, table, id_value, data: dict):
        sets = []
        vals = []
        for k, v in data.items():
            if k == "id": 
                continue
            sets.append(f"`{k}`=%s")
            vals.append(v)
        if not sets:
            return False
        vals.append(id_value)
        sql = f"UPDATE `{table}` SET {', '.join(sets)} WHERE id=%s"
        cur = self.cursor()
        cur.execute(sql, tuple(vals))
        return cur.rowcount > 0

    def delete(self, table, id_value):
        cur = self.cursor()
        cur.execute(f"DELETE FROM `{table}` WHERE id=%s", (id_value,))
        return cur.rowcount > 0

    def search(self, table, keyword):
        cols_info = self.show_columns(table)
        text_cols = [c['Field'] for c in cols_info if 'char' in c['Type'] or 'text' in c['Type']]
        if not text_cols:
            return self.fetch_all(table)
        where = " OR ".join([f"`{c}` LIKE %s" for c in text_cols])
        params = tuple([f"%{keyword}%"] * len(text_cols))
        cur = self.cursor()
        cur.execute(f"SELECT * FROM `{table}` WHERE {where}", params)
        return cur.fetchall()

    def fetch_options(self, table, id_col='id', label_col=None):
        if label_col is None:
            try_candidates = ['name','model','official_reg_number','serial_number','email','id']
            cols = [c['Field'] for c in self.show_columns(table)]
            for c in try_candidates:
                if c in cols:
                    label_col = c
                    break
            if label_col is None:
                label_col = 'id'
        cur = self.cursor()
        cur.execute(f"SELECT `{id_col}` AS id, `{label_col}` AS label FROM `{table}` ORDER BY `{label_col}` ASC")
        return cur.fetchall()
