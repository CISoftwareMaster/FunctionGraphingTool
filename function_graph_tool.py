#!/usr/bin/python3
"""
    Function Graphing Tool
    By: Charles Ivan Mozar

    contact:
    cisoftwaremaster@gmail.com
"""
import sys
from PyQt5.QtCore import Qt, QPointF, QRect
from PyQt5.QtWidgets import QApplication, qApp, QWidget, QMainWindow, QAction, QLineEdit, QVBoxLayout, QHBoxLayout, QLabel, QMessageBox, QSlider
from PyQt5.QtGui import QPainter, QColor


# the graphing widget
class Paper(QWidget):
    def __init__(self):
        # initialise Paper as a subclass of QWidget
        super().__init__()

        # zoom factor
        self.zoom = 25

        # initialise the list of points
        self.points = []
        self.setMinimumSize(400, 200)

    def paintEvent(self, event):
        painter = QPainter(self)

        # set painter properties
        painter.setRenderHint(QPainter.Antialiasing)

        # draw the graph background
        painter.fillRect(QRect(0, 0, self.width(), self.height()), QColor(230, 230, 230))

        # draw the axis lines
        painter.setPen(Qt.DotLine)
        painter.drawLine(self.width()/2, 0, self.width()/2, self.height())
        painter.drawLine(0, self.height()/2, self.width(), self.height()/2)

        # draw the graph
        painter.setPen(Qt.SolidLine)

        # centre of graph
        cw = self.width()/2
        ch = self.height()/2

        for i in range(len(self.points)-1):
            A = self.points[i] * self.zoom
            B = self.points[i+1] * self.zoom
            # draw a line segment connecting point A to B
            painter.drawLine(cw + A.x(), ch - A.y(), cw + B.x(), ch - B.y())

        # set font size
        font = painter.font()
        font.setPointSize(6)
        painter.setFont(font)

        # draw zoom level
        painter.drawText(QPointF(self.width() - 60, self.height() - 10),
                         "Zoom level: %i" % self.zoom)

    def draw_graph(self, points):
        # clear the list of points
        self.points = []

        # insert the new points
        for point in points:
            self.points.append(point)

        # update the graph
        self.repaint()


class Graphing(QMainWindow):
    def __init__(self):
        # initialise Graphing as a subclass of QMainWindow
        super().__init__()

        # initialise the user interface
        self.init_ui()

        # show this window
        self.show()

    def init_ui(self):
        # initialise menus
        self.init_menu()

        # initialise the view and layout
        layout = QVBoxLayout()
        self.view = QWidget()
        self.view.setLayout(layout)
        self.setCentralWidget(self.view)

        # initialise the graphing paper
        self.graph = Paper()

        # initialise the function input
        self.function = QLineEdit()
        fbar_view = QWidget()
        fbar_view_layout = QHBoxLayout()
        fbar_view.setLayout(fbar_view_layout)
        fbar_label = QLabel("f(x) = ")

        # update function input layout
        fbar_view_layout.addWidget(fbar_label)
        fbar_view_layout.addWidget(self.function)

        # zoom control for the graph
        zoom = QSlider()
        zoom.setOrientation(Qt.Horizontal)
        zoom.setValue(self.graph.zoom)
        zoom.setMinimum(1)
        zoom.setMaximum(50)
        zoom.setTickInterval(1)
        zoom.setTickPosition(QSlider.TicksBelow)
        zoom.valueChanged.connect(self._update_zoom)

        # set function input properties
        self.function.setPlaceholderText("x + 3")
        self.function.returnPressed.connect(self.resolve_formula)

        # update layout
        layout.addWidget(self.graph, 1)
        layout.addWidget(zoom)
        layout.addWidget(fbar_view)

        # set window geometry
        self.setMinimumSize(400, 300)
        self.setWindowTitle("Function Graph Tool")

    def init_menu(self):
        # initialise the menubar
        self.menubar = self.menuBar()

        # create the file menu
        m_file = self.menubar.addMenu("&File")

        # the quit action
        a_file_quit = QAction("&Quit Graph", self)
        a_file_quit.setShortcut("Ctrl+Q")
        a_file_quit.triggered.connect(qApp.quit)
        m_file.addAction(a_file_quit)

    def resolve_formula(self):
        formula = self.function.text()

        # prepare formula for evaluation
        formula = formula.replace(" ", "")
        formula = formula.replace("+", "@+")
        formula = formula.replace("-", "@-")

        # split the formula into steps
        steps = formula.split("@")

        # store the resulting coordinates in this list
        points = []

        try:
            for x in range(-1000, 1000):
                y = 0
                # execute each step
                for step in steps:
                    if step != "":
                        # handle terms with no coefficients
                        if step.find("x") == 0 or (step.find("x") == 1 and "-" in step):
                            step = step.replace("x", "1x")

                        # is negative
                        n = False
                        # should multiply
                        m = False
                        # exponent
                        e = 1

                        if "+" in step:
                            a = step.replace("+", "")

                        # handle x-variable
                        if "x" in step:
                            m = True
                            step = step.replace("x", "")

                        # check for exponents
                        if "^" in step:
                            # extract exponent
                            e = step[step.find("^")+1:len(step)]
                            step = step.replace("^%s" % e, "")
                        else:
                            # default exponent is 1
                            e = 1

                        # extract the numerical coefficient
                        c = float(step)

                        # apply multiplication and exponent
                        if m:
                            c = c * x ** float(e)

                        # update y
                        y += c

                # insert this point to the list
                points.append(QPointF(x, y))
        except:
            QMessageBox.warning(self, "Error", "There was a problem resolving your function...")
            return

        # update graph
        self.graph.draw_graph(points)

    def _update_zoom(self, x):
        # update zoom level
        self.graph.zoom = x

        # update graph
        self.graph.repaint()


if __name__ == "__main__":
    # initialise Qt application
    app = QApplication(sys.argv)

    # initialise window
    window = Graphing()

    # enter main loop
    sys.exit(app.exec_())
