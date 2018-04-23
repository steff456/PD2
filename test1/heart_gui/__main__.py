# -*- coding: utf-8 -*-

"""Main Heart Visualizer GUI."""

# Standard Library imports
import os
import sys
import locale
import os.path as osp

# Matplotlib imports
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# Qt imports
from qtpy.QtCore import Qt
from qtpy.compat import to_qvariant, getopenfilename
from qtpy.QtWidgets import (QMenu, QVBoxLayout, QWidget, QApplication, QSizePolicy,
                            QLabel,  QLineEdit, QHBoxLayout)

# Numpy imports
import numpy as np

# # Local imports
from heart_gui.utils import (let_the_magic_work_pleth, let_the_magic_work_HR,
                             let_the_magic_work_SO2, let_the_magic_work_CO, let_the_magic_work_HRV) 
# import lux_qt.gui.icons as ima
# from lux_qt.views.utils import ColorMap
# from lux_qt.views.view_gui import GeneralView
# from lux_qt.gui.dialogs import ViewCreateDialog
# from lux_qt.gui.base import create_toolbutton, add_actions, Tabs, create_action


class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        self.compute_initial_figure()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass



class MyStaticMplCanvas(MyMplCanvas):
    """Simple canvas with a sine plot."""

    def __init__(self, parent, x, y=None, width=5, height=4, dpi=100):
        self.x = x
        self.y = y
        MyMplCanvas.__init__(self, parent, width, height, dpi)

    def compute_initial_figure(self):
        # t = np.arange(0.0, 3.0, 0.01)
        # s = np.sin(2*np.pi*t)
        self.y = np.arange(0, len(self.x))
        self.axes.plot(self.y, self.x)



class AngelaApp(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        graph_layout = QVBoxLayout()
        filename, _ = getopenfilename(self, caption="Select a file")
        v_values = let_the_magic_work_pleth(filename)
        v_HRV = let_the_magic_work_HRV(filename)
        # HRV
        hr_values = let_the_magic_work_HR(filename)
        hr_value = np.mean(hr_values)
        so2_value = np.mean(let_the_magic_work_SO2(filename))
        co_value = np.mean(let_the_magic_work_CO(filename, hr_values))
        self.pleth = MyStaticMplCanvas(self,x=v_values, width=650, height=900)
        self.hrv = MyStaticMplCanvas(self, x=v_HRV, width=650, height=900)
        graph_layout.addWidget(self.pleth)
        graph_layout.addWidget(self.hrv)
        layout = QVBoxLayout()
        layout.addLayout(graph_layout)
        labels_layout = QVBoxLayout()
        layout1 = QHBoxLayout()
        layout1.addWidget(QLabel("SO2 [mmHg]"))
        # self.so2_text = QLineEdit(self)
        # self.so2_text.setText()
        # self.so2_text.setEnabled(False)
        layout1.addWidget(QLabel("{0}".format(so2_value)))
        labels_layout.addLayout(layout1)
        layout2 = QHBoxLayout()
        layout2.addWidget(QLabel("HR [BPM]"))
        # self.hr_text = QLineEdit(self)
        # self.hr_text.setText()
        # self.hr_text.setEnabled(False)
        layout2.addWidget(QLabel("{0}".format(hr_value)))
        labels_layout.addLayout(layout2)
        layout3 = QHBoxLayout()
        layout3.addWidget(QLabel("CO [L/min]"))
        # self.co_text = QLineEdit(self)
        # self.co_text.setText("{0}".format(co_value))
        # self.co_text.setEnabled(False)
        layout3.addWidget(QLabel("{0}".format(co_value)))
        labels_layout.addLayout(layout3)
        layout.addLayout(labels_layout)
        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication.instance()
    if app is None:
        app = QApplication(['Lux Visualization'])
    locale.setlocale(locale.LC_NUMERIC, "C")
    widget = AngelaApp(None)

    # widget.render_view()
    widget.resize(1300, 900)
    widget.show()
    sys.exit(app.exec_())
