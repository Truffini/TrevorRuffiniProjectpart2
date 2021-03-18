import sqlite3
import sys
import requests
from PyQt5 import QtCore, QtWidgets, QtGui
from pandas import read_excel
import math
from PyQt5.QtWebEngineWidgets import QWebEngineView
import plotly
import plotly.express as px

conn = sqlite3.connect("gdata.db")

states = {"Alabama": "AL",
          "Alaska": "AK",
          "Arizona": "AZ",
          "Arkansas": "AR",
          "California": "CA",
          "Colorado": "CO",
          "Connecticut": "CT",
          "Delaware": "DE",
          "Florida": "FL",
          "Georgia": "GA",
          "Hawaii": "HI",
          "Idaho": "ID",
          "Illinois": "IL",
          "Indiana": "IN",
          "Iowa": "IA",
          "Kansas": "KS",
          "Kentucky": "KY",
          "Louisiana": "LA",
          "Maine": "ME",
          "Maryland": "MD",
          "Massachusetts": "MA",
          "Michigan": "MI",
          "Minnesota": "MN",
          "Mississippi": "MS",
          "Missouri": "MO",
          "Montana": "MT",
          "Nebraska": "NE",
          "Nevada": "NV",
          "New Hampshire": "NH",
          "New Jersey": "NJ",
          "New Mexico": "NM",
          "New York": "NY",
          "North Carolina": "NC",
          "North Dakota": "ND",
          "Ohio": "OH",
          "Oklahoma": "OK",
          "Oregon": "OR",
          "Pennsylvania": "PA",
          "Rhode Island": "RI",
          "South Carolina": "SC",
          "South Dakota": "SD",
          "Tennessee": "TN",
          "Texas": "TX",
          "Utah": "UT",
          "Vermont": "VT",
          "Virginia": "VA",
          "Washington": "WA",
          'District of Columbia': "DC",
          "West Virginia": "WV",
          "Wisconsin": "WI",
          "Wyoming": "WY",
          "Guam": "GU",
          "Puerto Rico": "PR",
          "Virgin Islands": "VI"

          }


def show_dialog(title_, msg_):
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Information)

    msg.setText(msg_)
    msg.setInformativeText("This is additional information")
    msg.setWindowTitle(title_)
    msg.setDetailedText("The details are as follows:")
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)

    _ = msg.exec_()


def add_to_data_base(all_data):
    c = conn.cursor()
    print("Data base writing process initiate")
    print("Incoming data count :", len(all_data))

    c.execute('''DROP TABLE IF EXISTS emp_data;''')
    c.execute('''CREATE TABLE IF NOT EXISTS emp_data
                            (
                                state, 
                                occupation_major_title, 
                                total_employment,
                                percentile_salary_25,
                                occ_code
                            )'''
              )
    c.executemany('INSERT OR REPLACE INTO emp_data VALUES (?,?,?,?,?)', all_data)
    conn.commit()
    c = conn.cursor()

    c.execute('SELECT count(*) FROM emp_data')
    print(c.fetchone()[0], "ITEMS inserted to the data base")


def load_data(file_name, sheet_name):
    all_data = []
    df = read_excel(file_name, sheet_name=sheet_name)
    total_fetch_result = 0
    for index, row in df.iterrows():
        if row['o_group'] == 'major':
            item_data = (row['area_title'], row['occ_title'], row['tot_emp'], row['h_pct25'], row['occ_code'])
            total_fetch_result += 1
            all_data.append(item_data)
    print("[FETCHED REPORT]: ", total_fetch_result, " ITEMS")
    show_dialog("success", "Successfully fetch details")
    add_to_data_base(all_data)


class DataLoad(QtWidgets.QMainWindow):
    switch_window = QtCore.pyqtSignal(str)

    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        self.main_CF = QtWidgets.QFrame(self)
        self.setCentralWidget(self.main_CF)
        self.main_CL = QtWidgets.QVBoxLayout(self.main_CF)

        self.file_name = None
        self.sheet_name = None
        self.setWindowTitle('Data Loading')
        self.setGeometry(200, 200, 400, 200)

        form = QtWidgets.QFrame(self.main_CF)
        self.main_CL.addWidget(form)
        layout1 = QtWidgets.QFormLayout(form)
        self.sheetNames = QtWidgets.QComboBox()
        self.sheetNames.currentIndexChanged.connect(self.selection_change)
        layout1.addRow("Sheet Name :", self.sheetNames)

        form2 = QtWidgets.QFrame(self.main_CF)
        self.main_CL.addWidget(form2)
        layout = QtWidgets.QGridLayout(form2)
        self.button1 = QtWidgets.QPushButton('Open Excel File')
        self.button1.clicked.connect(self.select_file)
        self.button = QtWidgets.QPushButton('Load Data')

        self.note = QtWidgets.QLabel("No File Open")
        self.button.clicked.connect(self.load_data_function)

        layout.addWidget(self.button1)
        layout.addWidget(self.button)
        layout.addWidget(self.note)

        if not self.sheet_name or not self.file_name:
            self.sheetNames.setEnabled(False)
            self.button.setEnabled(False)

        self.main_CL.addWidget(form2)
        self.main_CL.addWidget(form)

    def select_file(self):
        self.button1.setEnabled(False)
        self.button1.setText("Loading ... ")
        self.file_name, value = QtWidgets.QFileDialog.getOpenFileName(self, "Select one or more files to open",
                                                                      "",
                                                                      "Excel Files (*.xlsx)")
        self.button1.setEnabled(True)
        self.button1.setText('Open Excel File')
        if not self.file_name:
            print("Not selected file")
            return
        xl = read_excel(self.file_name, None)
        added = False
        for i in xl.keys():
            print(i)
            added = True
            self.sheetNames.addItem(i)
        if added:
            self.sheetNames.setEnabled(True)

        self.note.setText("File was Opened, Please select Sheet Name")
        print(self.file_name)

    def load_data_function(self):
        self.button.setEnabled(False)
        self.button.setText("Loading ... ")
        print("ok")
        load_data(self.file_name, self.sheet_name)
        self.button.setEnabled(True)
        self.button.setText("Load Data")

    def selection_change(self, i):
        print("Items in the list are :")

        for count in range(self.sheetNames.count()):
            print(self.sheetNames.itemText(count))
        print("Current index", i, "selection changed ", self.sheetNames.currentText())
        self.sheet_name = self.sheetNames.currentText()
        self.button.setEnabled(True)

    def switch(self):
        self.switch_window.emit(self.line_edit.text())


class WindowTwo(QtWidgets.QMainWindow):

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Data Visualization')
        self.setGeometry(200, 200, 1000, 500)
        layout = QtWidgets.QGridLayout()

        c = conn.cursor()
        c.execute(
            """SELECT count(state) as total FROM emp_data where occ_code not like '3%-%' or occ_code not like '4%-%' 
              Group by state""")
        if c.fetchone():
            self.setLayout(layout)
            tabwidget = QtWidgets.QTabWidget()
            layout.addWidget(tabwidget, 0, 0)
            table_frame = QtWidgets.QFrame()

            table_header = []

            c = conn.cursor()
            self.data = {'abr state': [],
                         'state': [],
                         'total emp': [],
                         'top 25 sal': [],
                         'graduates students count': [],
                         'three_year_declining_balance': []
                         }

            c.execute(
                """SELECT state,sum(total_employment) as total , max(percentile_salary_25) as sal_25  FROM emp_data
                 where occ_code not like '3%' or occ_code not like '4%'   Group by state""")

            size_tb = 0
            for i in c.fetchall():
                size_tb += 1
                if i[0] in states.keys():
                    self.data['abr state'].append(states[i[0]])
                else:
                    self.data['abr state'].append(any("-"))
                self.data['state'].append(i[0])
                self.data['total emp'].append(int(i[1]))
                self.data['top 25 sal'].append(int(i[2]))

            self.data['graduates students count'] = [0] * size_tb
            self.data['three_year_declining_balance'] = [0] * size_tb

            table_layout = QtWidgets.QHBoxLayout(table_frame)
            table = QtWidgets.QTableWidget(3000, 5)
            table.resizeColumnsToContents()
            table.resizeRowsToContents()

            form = QtWidgets.QFrame()
            layout1 = QtWidgets.QGridLayout(form)

            form1 = QtWidgets.QFrame()
            layout2 = QtWidgets.QGridLayout(form1)

            form2 = QtWidgets.QFrame()
            layout3 = QtWidgets.QGridLayout(form2)

            form3 = QtWidgets.QFrame()
            layout4 = QtWidgets.QGridLayout(form3)

            c = conn.cursor()
            c.execute(
                """SELECT state,sum(total_employment),max(percentile_salary_25) as sal_25 FROM emp_data where occ_code 
                not like '3%-%' or occ_code not like '4%-%'   Group by state""")
            data = c.fetchall()
            s = []
            c = []
            top_25_sal = []
            for i in data:
                if i[0] in states.keys():
                    top_25_sal.append(i[2])
                    s.append(states[i[0]])
                    c.append(i[1])

            cn = conn.cursor()
            cn.execute(
                """SELECT state,avg(three_year_declining_balance), sum(size) FROM school_data Group by state""")
            st_data = cn.fetchall()
            for i in st_data:
                if i[0] in self.data['abr state']:
                    self.data['graduates students count'][self.data['abr state'].index(i[0])] = int(i[2] / 4)
                    self.data['three_year_declining_balance'][int(self.data['abr state'].index(i[0]))] = float(i[1])

            print(self.data['graduates students count'])
            fig = px.choropleth(locations=s, locationmode="USA-states", color=c, title="Number Of Employees In A State",
                                scope="usa")

            fig.update_layout(coloraxis_colorbar=dict(
                title="Total Number of Employees"
            ))

            fig1 = px.choropleth(locations=s, locationmode="USA-states", color=top_25_sal,
                                 title="Top 25% Salary In A State",
                                 scope="usa")

            fig1.update_layout(coloraxis_colorbar=dict(
                title="Top 25% Salary"
            ))
            print(len(self.data['three_year_declining_balance']) == len(self.data['state']))
            fig2 = px.choropleth(locations=s, locationmode="USA-states",
                                 color=[i * j / j for i, j in
                                        zip(self.data['three_year_declining_balance'], top_25_sal)],
                                 title="Compare Three Year Declining  Balance With Top 25% Salary in a State",
                                 scope="usa")

            fig2.update_layout(coloraxis_colorbar=dict(
                title="AVG three year declining"
            ))

            fig3 = px.choropleth(locations=s, locationmode="USA-states",
                                 color=[i / j for i, j in zip(self.data['three_year_declining_balance'], c)],
                                 title="Compare Graduates count with job count",
                                 scope="usa")

            fig3.update_layout(coloraxis_colorbar=dict(
                title="Graduates ratio to grad jobs"
            ))

            print(fig.layout.coloraxis.colorscale)
            named_colorscales = fig.layout.coloraxis.colorscale

            cn = conn.cursor()

            cn.execute("""SELECT   state, 
                                        occupation_major_title, 
                                        total_employment,
                                        percentile_salary_25,
                                        occ_code FROM emp_data 
                        where occ_code not like '3%' AND occ_code not like '4%' """)
            st_data = cn.fetchall()
            self.data = {
                'state': [],
                'occupations': [],
                'occ_code': [],
                'total emp': [],
                'top 25 sal': [],

            }

            for i in st_data:
                self.data['state'].append(i[0])
                self.data['occupations'].append(i[1])
                self.data['total emp'].append(i[2])
                self.data['occ_code'].append(i[4])
                self.data['top 25 sal'].append(int(i[3]))

            for n, key in enumerate(sorted(self.data.keys())):
                table_header.append(key)
                for m, item in enumerate(self.data[key]):
                    newitem = QtWidgets.QTableWidgetItem(str(item))
                    newitem.setForeground(QtGui.QColor("rgb(255,255,255)"))

                    if key in ['total emp']:
                        idx = int(item / max(self.data["total emp"]) * 10)
                        idx = idx - 1 if idx == 10 else idx
                        newitem.setBackground(QtGui.QColor(named_colorscales[idx][1]))
                        newitem.setTextAlignment(2)

                    if key in ['top 25 sal']:
                        newitem.setTextAlignment(2)
                    table.setItem(m, n, newitem)

            table.setSortingEnabled(True)
            table.setHorizontalHeaderLabels(table_header)
            table.resizeColumnsToContents()
            table_layout.addWidget(table)

            tabwidget.addTab(table_frame, "Table")

            html = '<html><body>'
            html += plotly.offline.plot(fig, output_type='div', include_plotlyjs='cdn')
            html += '</body></html>'

            plot_widget = QWebEngineView()
            plot_widget.setHtml(html)
            layout1.addWidget(plot_widget)

            html1 = '<html><body>'
            html1 += plotly.offline.plot(fig1, output_type='div', include_plotlyjs='cdn')
            html1 += '</body></html>'

            plot_widget1 = QWebEngineView()
            plot_widget1.setHtml(html1)
            layout2.addWidget(plot_widget1)

            html2 = '<html><body>'
            html2 += plotly.offline.plot(fig2, output_type='div', include_plotlyjs='cdn')
            html2 += '</body></html>'

            plot_widget2 = QWebEngineView()
            plot_widget2.setHtml(html2)
            layout3.addWidget(plot_widget2)

            html3 = '<html><body>'
            html3 += plotly.offline.plot(fig3, output_type='div', include_plotlyjs='cdn')
            html3 += '</body></html>'

            plot_widget3 = QWebEngineView()
            plot_widget3.setHtml(html3)
            layout4.addWidget(plot_widget3)

            tabwidget.addTab(form, "Employees")
            tabwidget.addTab(form1, "Top 25% salary")
            tabwidget.addTab(form2, "Compare 3 year declining balance ")
            tabwidget.addTab(form3, "Compare graduates count with employees count")

            self.setCentralWidget(tabwidget)
        else:
            lable = QtWidgets.QLabel("              Need Excel Data For Visualizing Data : Please Load Excel data   ")
            layout.addWidget(lable)
            self.setCentralWidget(lable)
            print("ERROR")


class Main(QtWidgets.QWidget):
    switch_window = QtCore.pyqtSignal(str)

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Menu')
        self.setGeometry(200, 200, 400, 200)

        layout = QtWidgets.QVBoxLayout()

        self.button1 = QtWidgets.QPushButton('Load Data')
        self.button2 = QtWidgets.QPushButton('Data Visualization')

        self.button1.clicked.connect(self.but1)
        self.button2.clicked.connect(self.but2)

        layout.addWidget(self.button1)
        layout.addWidget(self.button2)

        self.setLayout(layout)

    def but1(self):
        self.switch_window.emit("a")

    def but2(self):
        self.switch_window.emit("b")


class Controller:

    def __init__(self):
        self.window_two = WindowTwo()
        self.window = DataLoad()
        self.login = Main()
        self.window_two = WindowTwo()

    def show_menu(self):
        self.login.switch_window.connect(self.show_main)
        self.login.show()

    def show_main(self, a):

        if a == "a":
            self.window.switch_window.connect(self.show_window_two)
            self.window.show()
        else:
            self.window_two.show()

    def show_window_two(self):
        self.window.close()
        self.window_two.show()


def get_data(update):
    cur = conn.cursor()
    result = cur.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    table_names = []
    if len(result) > 0:
        table_names = sorted(list(zip(*result))[0])
    if 'school_data' not in table_names or update:

        api_key = "XlTqdPm10c8nEmo2BXSAoagG6Bj0cukrBg4GWPci"
        url = "https://api.data.gov/ed/collegescorecard/v1/schools.json?school.degrees_awarded.predominant=2,3"
        fields = ",".join([
            "school.state",
            "2016.student.size",
            "2016.repayment.repayment_cohort.3_year_declining_balance",
        ])

        all_data = []
        response = requests.get(f"{url}&fields={fields}&api_key={api_key}&per_page={100}")
        page_of_data = response.json()
        total_res = page_of_data['metadata']['total']
        items_per_page = page_of_data['metadata']['per_page']

        total_pages = math.ceil(total_res / items_per_page)
        total_fetch_result = 0
        for page in range(0, total_pages):
            response = requests.get(f"{url}&fields={fields}&api_key={api_key}&page={page}&per_page={100}")
            if response.status_code != 200:
                print("Error with data syncing process")
                exit(-1)

            page_of_data = response.json()
            result = page_of_data['results']
            print(f"[INFO] Syncing Page {page + 1:02} of {total_pages} | {len(result):03} Data Items Exist")
            for item in page_of_data['results']:
                item_data = (
                    item["school.state"],
                    item["2016.student.size"],
                    item["2016.repayment.repayment_cohort.3_year_declining_balance"]
                )
                total_fetch_result += 1
                all_data.append(item_data)
        print("[FETCHED REPORT]: ", total_fetch_result, " ITEMS")
        c = conn.cursor()
        print("Data base writing process initiate")
        print("Incoming data count :", len(all_data))
        c.execute('''CREATE TABLE IF NOT EXISTS school_data
                                    (
                                        state, 
                                        size,
                                        three_year_declining_balance
                                    )'''
                  )

        c.executemany('INSERT OR REPLACE INTO school_data VALUES (?,?,?)', all_data)
        conn.commit()
        c = conn.cursor()

        c.execute('SELECT count(*) FROM school_data')
        print(c.fetchone()[0], "ITEMS inserted to the data base")


def init():
    c = conn.cursor()
    print("Data base writing process initiate")
    c.execute('''CREATE TABLE IF NOT EXISTS emp_data
                                      (
                                          state, 
                                          occupation_major_title, 
                                          total_employment,
                                          percentile_salary_25,
                                          occ_code
                                      )'''
              )
    conn.commit()


def main():
    init()
    get_data(False)
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.show_menu()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
