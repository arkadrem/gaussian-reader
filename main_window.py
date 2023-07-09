import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial import distance
import numpy as np

import input_functions
import output_functions
from canvas import MplCanvas
from info import uiInfo
from plot_functions import input_plot_coordinates


class uiMainWindow(object):
    def analyze_button_clicked(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = uiInfo()
        self.ui.setup_ui(self.window)
        self.window.show()

        input_file = self.input_edit.text()
        output_file = self.output_edit.text()

        self.ui.memory_text.setText(input_functions.memory(input_file))
        self.ui.checkpoint_text.setText(input_functions.checkpoint(input_file))
        self.ui.options_text.setText(input_functions.options(input_file))
        self.ui.comment_text.setText(input_functions.comment(input_file))
        self.ui.charge_text.setText(input_functions.charge(input_file))
        self.ui.multiplicity_text.setText(input_functions.multiplicity(input_file))
        self.ui.coordinates_text.setText(input_functions.coordinates(input_file))

        self.ui.energy_text.setText(output_functions.molecule_energy(output_file))
        self.ui.thermochemistry_text.setText(output_functions.thermochemistry(output_file))
        self.ui.frequencies_text.setText(output_functions.frequencies(output_file))
        self.ui.opt_text.setText(output_functions.latest_coordinates(output_file))
        self.ui.quote_text.setText(output_functions.joke(output_file))

    def original_button_clicked(self):
        input_file = self.input_edit.text()
        atoms, x, y, z = input_plot_coordinates(input_file)

        self.plot_window = originalPlot()
        self.plot_window.set_data(atoms, x, y, z)
        self.plot_window.show_plot()
        self.plot_window.show()

    def optimized_button_clicked(self):
        input_file = self.input_edit.text()
        output_file = self.output_edit.text()

        atoms = input_plot_coordinates(input_file)
        atoms = atoms[0]

        coordinates_list = output_functions.optimized_coordinates(output_file)
        coordinates = coordinates_list[-1]

        x = coordinates[0]
        y = coordinates[1]
        z = coordinates[2]

        self.plot_window = originalPlot()
        self.plot_window.set_data(atoms, x, y, z)
        self.plot_window.show_plot()
        self.plot_window.show()

    def energy_button_clicked(self):
        output_file = self.output_edit.text()

        scf_list = output_functions.scf(output_file)
        indices = range(len(scf_list))

        self.plot_window = energyPlot()
        self.plot_window.set_data(indices, scf_list)
        self.plot_window.show_plot()
        self.plot_window.show()

    def setup_ui(self, main_window):
        main_window.setObjectName("MainWindow")
        main_window.resize(325, 500)
        self.centralwidget = QtWidgets.QWidget(main_window)
        self.centralwidget.setObjectName("centralwidget")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(60, 30, 291, 381))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        self.title = QtWidgets.QLabel(self.layoutWidget)
        self.title.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(20)
        self.title.setFont(font)
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setObjectName("title")
        self.gridLayout.addWidget(self.title, 0, 0, 1, 1)

        self.input_label = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(12)
        self.input_label.setFont(font)
        self.input_label.setObjectName("input_label")
        self.gridLayout.addWidget(self.input_label, 2, 0, 1, 1)

        self.input_edit = QtWidgets.QLineEdit(self.layoutWidget)
        self.input_edit.setObjectName("input_edit")
        self.gridLayout.addWidget(self.input_edit, 3, 0, 1, 1)

        self.energy_button = QtWidgets.QPushButton(self.layoutWidget, clicked=lambda: self.energy_button_clicked())
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(16)
        self.energy_button.setFont(font)
        self.energy_button.setObjectName("energy_button")
        self.gridLayout.addWidget(self.energy_button, 9, 0, 1, 1)

        spacerItem = QtWidgets.QSpacerItem(20, 50, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)

        self.output_label = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(12)
        self.output_label.setFont(font)
        self.output_label.setObjectName("output_label")
        self.gridLayout.addWidget(self.output_label, 4, 0, 1, 1)

        self.output_edit = QtWidgets.QLineEdit(self.layoutWidget)
        self.output_edit.setObjectName("output_edit")
        self.gridLayout.addWidget(self.output_edit, 5, 0, 1, 1)

        self.analyze_button = QtWidgets.QPushButton(self.layoutWidget, clicked=lambda: self.analyze_button_clicked())
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(16)
        self.analyze_button.setFont(font)
        self.analyze_button.setObjectName("analyze_button")
        self.gridLayout.addWidget(self.analyze_button, 6, 0, 1, 1)

        spacerItem1 = QtWidgets.QSpacerItem(20, 50, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 11, 0, 1, 1)

        self.original_molecule_button = QtWidgets.QPushButton(self.layoutWidget,
                                                              clicked=lambda: self.original_button_clicked())
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(16)
        self.original_molecule_button.setFont(font)
        self.original_molecule_button.setObjectName("original_molecule_button")
        self.gridLayout.addWidget(self.original_molecule_button, 7, 0, 1, 1)

        self.optimized_molecule_button = QtWidgets.QPushButton(self.layoutWidget,
                                                               clicked=lambda: self.optimized_button_clicked())
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(16)
        self.optimized_molecule_button.setFont(font)
        self.optimized_molecule_button.setObjectName("optimized_molecule_button")
        self.gridLayout.addWidget(self.optimized_molecule_button, 8, 0, 1, 1)

        main_window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(main_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 410, 21))
        self.menubar.setObjectName("menubar")
        main_window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(main_window)
        self.statusbar.setObjectName("statusbar")
        main_window.setStatusBar(self.statusbar)

        self.translate_ui(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def translate_ui(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.title.setText(_translate("MainWindow", "Welcome to Gauss"))
        self.input_label.setText(_translate("MainWindow", "Input file"))
        self.energy_button.setText(_translate("MainWindow", "Energy Plot"))
        self.output_label.setText(_translate("MainWindow", "Output file"))
        self.analyze_button.setText(_translate("MainWindow", "Analyze"))
        self.original_molecule_button.setText(_translate("MainWindow", "Original Molecule"))
        self.optimized_molecule_button.setText(_translate("MainWindow", "Optimized Molecule"))


class originalPlot(QtWidgets.QMainWindow):
    def __init__(self):
        super(originalPlot, self).__init__()

        sc = MplCanvas(self, width=25, height=20, dpi=100)
        self.setCentralWidget(sc)

        self.ax = sc.figure.add_subplot(111, projection='3d')

        self.ax.set_title('Molecule')
        self.ax.set_xlabel('x [Å]')
        self.ax.set_ylabel('y [Å]')
        self.ax.set_zlabel('z [Å]')

        self.atoms = None
        self.x = None
        self.y = None
        self.z = None

    def set_data(self, atoms, x, y, z):
        self.atoms = atoms
        self.x = x
        self.y = y
        self.z = z

    def show_plot(self):
        self.ax.clear()
        self.ax.scatter(self.x, self.y, self.z)

        coordinates = np.column_stack((self.x, self.y, self.z))
        dist_matrix = distance.cdist(coordinates, coordinates)

        num_points = len(self.x)
        for i in range(num_points):
            closest_point_index = np.argsort(dist_matrix[i])[1]  # Exclude the point itself
            self.ax.plot([self.x[i], self.x[closest_point_index]], [self.y[i], self.y[closest_point_index]],
                         [self.z[i], self.z[closest_point_index]], 'k-', linewidth=0.5)

        for xi, yi, zi, label in zip(self.x, self.y, self.z, self.atoms):
            self.ax.text(xi, yi, zi, label, color='red')

        self.ax.set_title('Molecule')
        self.ax.set_xlabel('x [Å]')
        self.ax.set_ylabel('y [Å]')
        self.ax.set_zlabel('z [Å]')
        self.ax.figure.canvas.draw()


class optimizedPlot(QtWidgets.QMainWindow):
    def __init__(self):
        super(optimizedPlot, self).__init__()

        sc = MplCanvas(self, width=25, height=20, dpi=100)
        self.setCentralWidget(sc)

        self.ax = sc.ax
        self.ax.axis('on')  # Display only the plot axis

        self.ax.set_title('Molecule')
        self.ax.set_xlabel('x [Å]')
        self.ax.set_ylabel('y [Å]')
        self.ax.set_zlabel('z [Å]')

        self.atoms = None
        self.x = None
        self.y = None
        self.z = None

    def set_data(self, atoms, x, y, z):
        self.atoms = atoms
        self.x = x
        self.y = y
        self.z = z

    def show_plot(self):
        self.ax.clear()
        self.ax.scatter(self.x, self.y, self.z)

        coordinates = np.column_stack((self.x, self.y, self.z))
        dist_matrix = distance.cdist(coordinates, coordinates)

        num_points = len(self.x)
        for i in range(num_points):
            closest_point_index = np.argsort(dist_matrix[i])[1]  # Exclude the point itself
            self.ax.plot([self.x[i], self.x[closest_point_index]], [self.y[i], self.y[closest_point_index]],
                         [self.z[i], self.z[closest_point_index]], 'k-', linewidth=0.5)

        for xi, yi, zi, label in zip(self.x, self.y, self.z, self.atoms):
            self.ax.text(xi, yi, zi, label, color='red')

        self.ax.set_title('Molecule')
        self.ax.set_xlabel('x [Å]')
        self.ax.set_ylabel('y [Å]')
        self.ax.set_zlabel('z [Å]')
        self.ax.figure.canvas.draw()


class energyPlot(QtWidgets.QMainWindow):
    def __init__(self):
        super(energyPlot, self).__init__()

        sc = MplCanvas(self, width=25, height=20, dpi=100)
        self.setCentralWidget(sc)

        self.ax = sc.ax
        self.ax.axis('on')

        self.ax.set_xlabel('Step')
        self.ax.set_ylabel('Energy [a. u.]')
        self.ax.set_title('Energy of molecule')

        self.x = None
        self.y = None

    def set_data(self, x, y):
        self.x = x
        self.y = y

    def show_plot(self):
        self.ax.clear()
        self.ax.plot(self.x, self.y)
        self.ax.set_xlabel('Step')
        self.ax.set_ylabel('Energy [a. u.]')
        self.ax.set_title('Energy of molecule')
        self.ax.figure.canvas.draw()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = uiMainWindow()
    ui.setup_ui(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
