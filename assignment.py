import sys
import psycopg2
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QComboBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        super().__init__(self.fig)
        self.setParent(parent)

    def plot(self, data):
        self.ax.clear()
        self.ax.plot(data, marker='o')
        self.ax.set_title('Plot of Selected Data')
        self.draw()

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.combo = QComboBox(self)
        self.combo.addItem("Table 1")
        self.combo.addItem("Table 2")
        layout.addWidget(self.combo)

        self.plotCanvas = PlotCanvas(self)
        layout.addWidget(self.plotCanvas)

        btn = QPushButton('Show Data', self)
        btn.clicked.connect(self.show_data)
        layout.addWidget(btn)

        self.setLayout(layout)
        self.setWindowTitle('Data Plotter')
        self.show()

    def show_data(self):
        table = self.combo.currentText()
        data = self.get_data(table)
        self.plotCanvas.plot(data)

    def get_data(self, table):
        conn = psycopg2.connect(
            dbname="test_db",
            user="postgres", 
            password="",   # replace with your own password
            
            host="localhost"
        )
        cur = conn.cursor()
        if table == "Table 1":
            cur.execute("SELECT value1 FROM table1;")
        else:
            cur.execute("SELECT value2 FROM table2;")

        rows = cur.fetchall()
        data = [row[0] for row in rows]
        cur.close()
        conn.close()
        return data

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
