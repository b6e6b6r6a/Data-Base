import sqlite3
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem
from form_staff import Ui_Form

STAFF_POSTS = ['менеджер', 'бухгалтер', 'экономист', 'логист']

class MyWidget(QWidget, Ui_Form):
    def __init__(self):
        super(MyWidget, self).__init__()
        self.setupUi(self)
        self.comboBox.addItems(STAFF_POSTS)
        self.pbOpen.clicked.connect(self.open_file)
        self.pbInsert.clicked.connect(self.insert)

    def open_file(self):
        try:
            self.conn = sqlite3.connect('staff_db.db')
            cur = self.conn.cursor()
            data = cur.execute("select * from staff")
            col_name = [i[0] for i in data.description]
            data_rows = data.fetchall()
        except Exception as e:
            print(f"Проблемы с подключением к БД. {e}")
            return e
        self.twStaffs.setColumnCount(len(col_name))
        self.twStaffs.setHorizontalHeaderLabels(col_name)
        self.twStaffs.setRowCount(0)
        #self.cbColNames.addItems(col_name)
        for i, row in enumerate(data_rows):
            self.twStaffs.setRowCount(self.twStaffs.rowCount() + 1)
            for j, elem in enumerate(row):
                self.twStaffs.setItem(i, j, QTableWidgetItem(str(elem)))
        self.twStaffs.resizeColumnsToContents()

    def update(self, query="select * from staff"):
        try:
            cur= self.conn.cursor()
            data = cur.execute(query).fetchall()
        except Exception as e:
            print = (f"Проблемы с подключением к бд {e}")
            return e
        self.twStaffs.setRowCount(0)
        for i, row in enumerate(data):
            self.twStaffs.setRowCount(self.twStaffs.rowCount() + 1)
            for j, elen in enumerate(row):
                self.twStaffs.setItem(i,j,QTableWidgetItem(str(elen)))
        self.twStaffs.resizeColumnsToContents()

    def insert(self):
        row = [self.leFio.text(), 'М' if self.rbMale.isChecked() else 'Ж', self.spAge.text(),
               self.lePhone.text(), self.leEmail.text(), self.comboBox.itemText(self.comboBox.currentIndex()),
               self.sbExp.text()]
        try:
            cur = self.conn.cursor()
            cur.execute(f"""insert into staff(fio, sex, phone, email, positioms, exp, age)
            values ('{row[0]}', '{row[1]}', {row[2]}, '{row[3]}', '{row[4]}', '{row[5]}', {row[6]})""")
            self.conn.commit()
            cur.close()
        except Exception as e:
            print(f"Исключение: {e}")
            return e
        self.update()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
