from PyQt5 import QtWidgets, QtCore, QtGui
import numpy as np
import molcas_suite as molcas
import xyz_py
import os


class MolcasInput(QtWidgets.QDialog):

    def __init__(self, atoms):
        self.atoms = atoms
        super().__init__()
        self.setWindowTitle('Molcas Input')
        self.setGeometry(100, 100, 300, 300)
        self.initUI()

    def initUI(self):
        layout = QtWidgets.QGridLayout()
        tab_widget = QtWidgets.QTabWidget()
        std = QtWidgets.QWidget()
        tab_widget.addTab(std, 'Required Input')
        extra = QtWidgets.QWidget()
        tab_widget.addTab(extra, 'Extra Input')
        layout.addWidget(tab_widget, 0, 0)

        std_layout = QtWidgets.QGridLayout()
        central_atom_label = QtWidgets.QLabel('Central Atom')
        std_layout.addWidget(central_atom_label, 0, 0)
        self.central_atom = QtWidgets.QLineEdit()
        self.central_atom.setPlaceholderText('e.g. Dy1')
        std_layout.addWidget(self.central_atom, 0, 1)

        charge_label = QtWidgets.QLabel('Charge')
        std_layout.addWidget(charge_label, 1, 0)
        self.charge = QtWidgets.QLineEdit()
        self.charge.setPlaceholderText('0')
        self.charge.setValidator(QtGui.QIntValidator())
        std_layout.addWidget(self.charge, 1, 1)

        act_elect_label = QtWidgets.QLabel('Active Electrons')
        std_layout.addWidget(act_elect_label, 2, 0)
        self.n_active_elec = QtWidgets.QLineEdit()
        self.n_active_elec.setPlaceholderText('0')
        self.n_active_elec.setValidator(QtGui.QIntValidator())
        std_layout.addWidget(self.n_active_elec, 2, 1)

        act_orb_label = QtWidgets.QLabel('Active Orbitals')
        std_layout.addWidget(act_orb_label, 3, 0)
        self.n_active_orb = QtWidgets.QLineEdit()
        self.n_active_orb.setPlaceholderText('0')
        self.n_active_orb.setValidator(QtGui.QIntValidator())
        std_layout.addWidget(self.n_active_orb, 3, 1)

        coord_atoms = QtWidgets.QLabel('Coordinated Atoms')
        std_layout.addWidget(coord_atoms, 4, 0)
        self.coord_atoms = QtWidgets.QLineEdit()
        self.coord_atoms.setPlaceholderText('2')
        self.coord_atoms.setValidator(QtGui.QIntValidator())
        std_layout.addWidget(self.coord_atoms, 4, 1)

        std.setLayout(std_layout)

        extra_layout = QtWidgets.QGridLayout()

        decomp_label = QtWidgets.QLabel('Decomposition')
        self.decomp = QtWidgets.QComboBox()
        self.decomp.addItems(['High Cholesky', 'RICD_acCD'])
        extra_layout.addWidget(decomp_label, 0, 0)
        extra_layout.addWidget(self.decomp, 0, 1)

        high_spin_label = QtWidgets.QLabel('High Spin Only')
        self.high_spin = QtWidgets.QCheckBox()
        extra_layout.addWidget(high_spin_label, 1, 0)
        extra_layout.addWidget(self.high_spin, 1, 1)

        casspt2_label = QtWidgets.QLabel('CASSPT2')
        self.casspt2 = QtWidgets.QCheckBox()
        extra_layout.addWidget(casspt2_label, 2, 0)
        extra_layout.addWidget(self.casspt2, 2, 1)

        extra.setLayout(extra_layout)

        self.buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        layout.addWidget(self.buttonBox, 1, 0)

        self.setLayout(layout)

    def make_xyz(self):
        if not os.path.exists('molcas'):
            os.makedirs('molcas')

        curr_dir = os.getcwd()
        os.chdir('molcas')
        self.symbols = list(map(lambda x: x.symbol, self.atoms))
        formula = np.unique(self.symbols, return_counts=True)
        self.formula = ''.join([f'{f[0]}{f[1]}' for f in zip(formula[0], formula[1])])
        self.coords = list(map(lambda x: x.position, self.atoms))
        xyz_py.save_xyz(f'{self.formula}.xyz', self.symbols, self.coords)
        self.filename = f'{self.formula}.xyz'
        os.chdir(curr_dir)

    def generate(self):
        self.make_xyz()
        try:
            central_atom = self.central_atom.text()
            charge = int(self.charge.text())
            n_active_elec = int(self.n_active_elec.text())
            n_active_orb = int(self.n_active_orb.text())
            n_coord_atoms = int(self.coord_atoms.text())
            decomp = self.decomp.currentText()
            high_spin = self.high_spin.isChecked()
            casspt2 = self.casspt2.isChecked()
        except ValueError:
            return

        curr_dir = os.getcwd()
        os.chdir('molcas')

        molcas.generate_input.generate_input(
                self.symbols,
                self.coords,
                central_atom,
                charge,
                n_active_elec,
                n_active_orb,
                n_coord_atoms,
                "{}.input".format(self.formula),
                xfield=None,
                kirkwood=None,
                decomp=decomp,
                gateway_extra=((), {}),
                basis_set_central="ANO-RCC-VTZP",
                basis_set_coord="ANO-RCC-VDZP",
                basis_set_remaining="ANO-RCC-VDZ",
                rasscf_extra=((), {}),
                high_S_only=high_spin,
                initial_orb=None,
                max_orb=None,
                caspt2=casspt2,
                caspt2_extra=((), {}),
                rassi=True,
                rassi_extra=((), {}),
                single_aniso=True,
                single_aniso_extra=((), {}),
                quax=None,
                skip_magneto=False,
        )
        os.chdir(curr_dir)
        return

"""
    generate_input.generate_input(
        labels,
        coords,
        args.central_atom,
        args.charge,
        args.n_active_elec,
        args.n_active_orb,
        args.n_coord_atoms,
        name,
        xfield=xfield,
        kirkwood=args.kirkwood,
        decomp=args.decomp,
        gateway_extra=args.gateway_extra,
        basis_set_central=args.basis_set_central,
        basis_set_coord=args.basis_set_coord,
        basis_set_remaining=args.basis_set_remaining,
        rasscf_extra=args.rasscf_extra,
        high_S_only=args.high_S_only,
        initial_orb=args.initial_orb,
        max_orb=args.max_orb,
        caspt2=args.caspt2,
        caspt2_extra=args.caspt2_extra,
        rassi=args.rassi,
        rassi_extra=args.rassi_extra,
        single_aniso=args.single_aniso,
        single_aniso_extra=args.single_aniso_extra,
        quax=args.quax,
        skip_magneto=args.skip_magneto
    )
"""

