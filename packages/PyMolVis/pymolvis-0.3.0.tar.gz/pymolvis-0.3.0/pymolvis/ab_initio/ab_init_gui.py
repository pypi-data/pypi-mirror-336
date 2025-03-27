import numpy as np
from PyQt5 import QtWidgets, QtGui, QtCore

# build the gui window that pops up
# add an panel to the side panel of the main window to host the Ab initio calculations

# the gui section returns effecitively a dictionary of the inputs to run

# create a seperate class to perform, store and report the results of the ab initio calculations

class AbInitioGui(QtWidgets.QDialog):

    def __init__(self, atom_list):
        super().__init__()
        self.setWindowTitle("MolVis Ab Initio")
        self.setGeometry(100, 100, 600, 600)
        self.set_basis_sets = {}
        self.set_ecp = {}
        self.atom_list=atom_list

        for atom in self.atom_list:
            self.set_basis_sets[atom] = 'sto-3g'
            self.set_ecp[atom] = None


        self.initUI()


    def initUI(self):
        layout = QtWidgets.QVBoxLayout()

        self.tabs = QtWidgets.QTabWidget()
        self.tabs_layout = QtWidgets.QGridLayout()
        self.tabs.setLayout(self.tabs_layout)

        self.dft_tab = QtWidgets.QWidget()
        self.scf_tab = QtWidgets.QWidget()
        self.mcscf_tab = QtWidgets.QWidget()

        # DFT tab design
        # basis sets
        # ecp
        # xc functional
        # calculations type (single point, geomopt, freq)
        # RHF, URHF, ...
        # d3bf - vdw
        self.dft_tab_layout = QtWidgets.QGridLayout()

        self.dft_tabs = QtWidgets.QTabWidget()
        self.dft_tabs_layout = QtWidgets.QVBoxLayout()
        self.dft_tabs.setLayout(self.dft_tabs_layout)

        self.basis_set_tab = QtWidgets.QWidget()

        self.basis_set_tab_layout = QtWidgets.QVBoxLayout()

        self.bs_list_widget = QtWidgets.QListWidget()
        for atom in self.atom_list:
            self.bs_list_widget.addItem(atom)
        self.basis_set_tab_layout.addWidget(self.bs_list_widget)

        self.bs_selector_label = QtWidgets.QLabel('Basis Set')
        self.bs_selector = QtWidgets.QComboBox()
        self.bs_selector.addItem('aug-cc-PVDZ')
        self.ecp_selector_label = QtWidgets.QLabel('Effective Core Potential')
        self.ecp_selector = QtWidgets.QComboBox()
        self.ecp_selector.addItem('None')

        self.bs_set_button = QtWidgets.QPushButton('Set')
        self.bs_set_button.clicked.connect(self.set_basis)

        self.basis_set_tab_layout.addWidget(self.bs_selector_label)
        self.basis_set_tab_layout.addWidget(self.bs_selector)
        self.basis_set_tab_layout.addWidget(self.ecp_selector_label)
        self.basis_set_tab_layout.addWidget(self.ecp_selector)
        self.basis_set_tab_layout.addWidget(self.bs_set_button)

        self.basis_set_tab.setLayout(self.basis_set_tab_layout)

        self.calc_params_tab = QtWidgets.QWidget()

        self.calc_params_tab_layout = QtWidgets.QVBoxLayout()

        # functional
        # charge
        # spin
        # symmetry
        self.func_label = QtWidgets.QLabel('xc Functional')
        self.func_selector = QtWidgets.QComboBox()
        self.func_selector.addItem('pbe')

        self.charge_label = QtWidgets.QLabel('Charge')
        self.charge_input = QtWidgets.QLineEdit()
        self.charge_input.setValidator(QtGui.QIntValidator())
        self.charge_input.setPlaceholderText('0')

        self.spin_label = QtWidgets.QLabel('Spin')
        self.spin_input = QtWidgets.QLineEdit()
        self.spin_input.setValidator(QtGui.QDoubleValidator())
        self.spin_input.setPlaceholderText('0.0')

        self.symmetry_check_box = QtWidgets.QCheckBox('Symmetry')

        self.calc_params_tab_layout.addWidget(self.func_label)
        self.calc_params_tab_layout.addWidget(self.func_selector)
        self.calc_params_tab_layout.addWidget(self.charge_label)
        self.calc_params_tab_layout.addWidget(self.charge_input)
        self.calc_params_tab_layout.addWidget(self.spin_label)
        self.calc_params_tab_layout.addWidget(self.spin_input)
        self.calc_params_tab_layout.addWidget(self.symmetry_check_box)

        self.calc_params_tab.setLayout(self.calc_params_tab_layout)

        self.dft_tabs.addTab(self.calc_params_tab, 'Calculation Parameters')
        self.dft_tabs.addTab(self.basis_set_tab, 'Basis Sets')

        self.dft_tab_layout.addWidget(self.dft_tabs)
        self.dft_tab.setLayout(self.dft_tab_layout)

        # scf tab design
        # self.scf_tab_layout = QtWidgets.QGridLayout()

        self.tabs.addTab(self.dft_tab, 'DFT')
        self.tabs.addTab(self.scf_tab, 'HF')
        self.tabs.addTab(self.mcscf_tab, 'MCSCF')

        layout.addWidget(self.tabs)

        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

        self.setLayout(layout)


    def parse_calculation(self):
        calculation_instructions = {}
        current_tab = self.tabs.currentIndex() # 0 is Dft, 1 is SCF, 2 is MCSCF
        if current_tab == 0:

            calculation_instructions['calc'] = 'DFT'
            calculation_instructions['basis'] = self.set_basis_sets
            calculation_instructions['ecp'] = self.set_ecp
            xc = self.func_selector.currentText()
            try:
                charge = float(self.charge_input.text())
            except:
                charge = 0
            try:
                spin = float(self.spin_input.text())
            except:
                spin = 0.0
            symm = self.symmetry_check_box.isChecked()

            calculation_instructions['xc'] = xc
            calculation_instructions['charge'] = charge
            calculation_instructions['spin'] = spin
            calculation_instructions['symmetry'] = symm

            return calculation_instructions


        else:
            return None

    def set_basis(self):
        if self.bs_list_widget.currentItem() is not None:
            atom = self.bs_list_widget.currentItem().text()
            self.set_basis_sets[atom] = self.bs_selector.currentText()
            self.set_ecp[atom] = self.ecp_selector.currentText()
            print(self.set_basis_sets)
            print(self.set_ecp)
        else:
            return
