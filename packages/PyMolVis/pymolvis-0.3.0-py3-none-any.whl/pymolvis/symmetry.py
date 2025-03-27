import numpy as np
import datetime
from time import perf_counter
from .symm import *
from .symm_util import *
from .write_util import *
from .sa_cli import *

from PyQt5 import QtWidgets, QtCore, QtGui

"""
def analyse(symbols, coords, bond_dict, tol, f, quiet=False):
"""

class str_writer:
    def __init__(self):
        self.string = ''

    def write(self, s):
        self.string += s

def analyze_symmetry(atoms, tol=1e-3, predict=None, refine=False, max_iter=50, convergence_tol=1e-6):

    coordinates = list(map(lambda x: x.position, atoms))
    symbols = list(map(lambda x: x.symbol, atoms))

    f = str_writer()

    start = perf_counter()

    f.write("{:^80}\n".format('Symmetry Analysis'))
    f.write("{:^80}\n".format('-----------------'))
    f.write("{:^80}\n".format("Author: William T. Morrillo"))
    now = datetime.datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    f.write("{:^80}\n\n".format("Date: {}".format(dt_string)))

    f.write("{:^80}\n".format("symmetry_analysis is a programme to compute the point group symmetry"))
    f.write("{:^80}\n\n".format("of a given molecular structure."))

    # Read the xyz file and prepare the structure for symmetry analysis
    f.write("Tolerance : {:.3e} Å\n\n".format(tol))
    f.write('\n')
    write_coordinates(symbols, coordinates, f)
    f.write("{:^80}\n".format("Molecular Parameterisation"))
    f.write("{:^80}\n\n".format("--------------------------"))
    coordinates = prepare_structure(symbols, coordinates, f)
    f.write("Prepared Structure\n")
    f.write("------------------\n")
    write_coordinates(symbols, coordinates, f)
    f.write("\n")
    f.write("{:^80}\n".format("Molecular Graph"))
    f.write("{:^80}\n".format("---------------"))
    graph = make_graph(symbols, coordinates)
    write_bonding_environment(graph.edges, f)
    write_angles(graph.edges, f)
    end_prep = perf_counter()
    f.write("Molecule preparation took {:11.7f} s\n\n".format(end_prep-start))

    if predict is None:
        f.write("{:^80}\n".format("Finding Point Group"))
        f.write("{:^80}\n".format("-------------------"))
        point_group = analyse(symbols, coordinates, graph.edges, tol, f)
    else:
        # analyse the prediction
        # start lowering the tol based off of the analysis
        # write a function to compare the prediction to analysis
        f.write("{:^80}\n".format("Finding Predicted Point Group"))
        f.write("{:^80}\n".format("-----------------------------"))
        # tol = 1e-4
        converged = False
        iter = 1
        while not converged:
            f.write('Iteration {} -> Tolerance = {:11.7f} Å\n'.format(iter, tol))
            point_group = analyse(symbols, coordinates, graph.edges, tol, f)
            converged, tol = pg_compare(predict, point_group, tol)

            if iter == 50:
                converged = True

            if converged:
                f.write("\n")
                f.write("{:^80}\n".format(" Point group {} found ".format(point_group)))
                f.write("{:^80}\n".format(" Distance from perfect point group: {} Å ".format(tol)))
            else:
                f.write("\nPredicted point group: {} \t Point group found: {}\n".format(predict, point_group))
                f.write("Adjusting Tolerance to {:11.7f} Å\n".format(tol))
            iter +=1
            f.write("--" + '\n\n')

    end_analysis = perf_counter()

    f.write("\n")
    f.write("{:-^80}\n".format(" Analysis Complete "))

    f.write("Symmetry analysis took {:11.7f} s\n\n".format(end_analysis-end_prep))

    if refine:
        refine_start = perf_counter()
        f.write("{:^80}\n".format("Refining Distance To Point Group {}".format(point_group)))
        f.write("{:^80}\n\n".format("-------------------------------------"))

        if point_group is None:
            f.write("Point group was not found. Unable to refine distance\n")
            f.write("Unexpected termination of symmetry_analysis\n")
            f.write("symmetry analysis took {:11.7f} s".format(perf_counter() - start))
            exit(1)

        dtol = min(1e-3, tol / 20)
        prev_tol = 0
        tol -= dtol

        # finds the base case
        refining=True
        iter = 1
        while refining:

            step_start = perf_counter()
            pg = analyse(symbols, coordinates, graph.edges, tol, f, quiet=True)
            step_end = perf_counter()
            t = step_end - step_start
            f.write("Step: {:<3} point group: {} \t tol = {:11.9f} Å \t dtol = {:11.9f} Å \t time: {:7.4e} s\n".format(iter, pg, tol, dtol, t))

            if point_group == pg and abs(tol - prev_tol) < convergence_tol:
                refining = False

            elif iter > max_iter:
                refining = False
                f.write("Maximum number of iterations reached. Could not converge\n")
                f.write("Unexpected termination of symmetry analysis\n")
                f.write("symmetry analysis took {:11.7f} s".format(perf_counter() - start))
                exit(1)

            elif point_group == pg:
                prev_tol = tol
                tol -= dtol
                if tol < 0:
                    tol += dtol
                    dtol *= 0.7
                    tol -= dtol
                iter += 1
            else:
                tol += dtol
                prev_tol = tol
                dtol *= 0.7
                tol -= dtol
                if tol < 0:
                    tol += dtol
                    dtol *= 0.7
                    tol -= dtol
                iter += 1

        refine_end = perf_counter()
        f.write("dtol has been converged to {:11.9f} Å\n\n".format(abs(tol - prev_tol)))
        f.write("{:^80}\n\n".format("Distance to {} = {:11.9f} Å".format(point_group, tol)))
        f.write("{:-^80}\n".format(" Refine Complete "))
        f.write("Refine took {:11.7f} s\n\n".format(refine_end - refine_start))

    f.write("{:^80}\n\n".format("Point group: {}".format(point_group)))
    end = perf_counter()
    f.write("Normal termination of symmetry_analysis - programme took {:11.7f} s to complete\n".format(end-start))

    return f.string



class SymmetryWindow(QtWidgets.QDialog):


    def __init__(self):
        super().__init__()
        self.setWindowTitle("Symmetry Analysis")
        self.setGeometry(100, 100, 300, 300)
        self.initUI()


    def initUI(self):

        layout = QtWidgets.QVBoxLayout()

        self.tol_label = QtWidgets.QLabel("Tolerance (Å)")
        self.tol = QtWidgets.QLineEdit()
        self.tol.setValidator(QtGui.QDoubleValidator())
        self.tol.setPlaceholderText("1e-3")
        
        self.predict_label = QtWidgets.QLabel("Predicted Point Group")
        self.predict = QtWidgets.QLineEdit()
        self.predict.setPlaceholderText("C1")
        
        self.refine_check = QtWidgets.QCheckBox("Refine")

        self.refine_conv_tol = QtWidgets.QLabel("Convergence Tolerance (Å)")
        self.conv_tol = QtWidgets.QLineEdit()
        self.conv_tol.setValidator(QtGui.QDoubleValidator())
        self.conv_tol.setPlaceholderText("1e-6")

        self.max_iter_label = QtWidgets.QLabel("Max Iterations")
        self.max_iter = QtWidgets.QLineEdit()
        self.max_iter.setValidator(QtGui.QIntValidator())

        layout.addWidget(self.tol_label)
        layout.addWidget(self.tol)
        layout.addWidget(self.predict_label)
        layout.addWidget(self.predict)
        layout.addWidget(self.refine_check)
        layout.addWidget(self.refine_conv_tol)
        layout.addWidget(self.conv_tol)
        layout.addWidget(self.max_iter_label)
        layout.addWidget(self.max_iter)

        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.button_box.button(QtWidgets.QDialogButtonBox.Ok).setText("Run")

        layout.addWidget(self.button_box)
        
        self.setLayout(layout)

    def get_values(self):
        try:
            tol = float(self.tol.text())
        except:
            tol = 1e-3

        try:
            max_iter = int(self.max_iter.text())
        except:
            max_iter = 50

        try:
            conv_tol = float(self.conv_tol.text())
        except:
            conv_tol = 1e-6

        predict = self.predict.text()
        if predict == "":
            predict = None

        return tol, predict, self.refine_check.isChecked(), max_iter, conv_tol

