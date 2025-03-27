import sys
import os
import pyvista as pv
import numpy as np
import mendeleev as md
import multiprocessing
from PyQt5 import QtWidgets, QtGui, QtCore
from pyvistaqt import MainWindow, QtInteractor
import xyz_py
from spin_phonon_suite.vibrations import BOHR2M, E0_TO_C, HARTREE2J
from gaussian_suite.extractor import make_extractor as make_gaussian_extractor
from ase.data import chemical_symbols
from time import perf_counter

from .atom import Atom
from .bond import Bond
from .molecule import Molecule
from .orbitals import Orbital
from .surface import Surface
from .crystal import Crystal
from .calc import MolcasInput
from .efield import electric_distort
from .bond_critical import BondCriticalPoints
from pymolvis.ab_initio.ab_init_gui import AbInitioGui
from pymolvis.ab_initio.ab_initio_driver import run_pyscf_dft, format_output
from .symmetry import analyze_symmetry, SymmetryWindow


class QtDisplay(MainWindow):

    def __init__(self, parent=None, show=True):

        QtWidgets.QMainWindow.__init__(self, parent)

        self.atoms = []
        self.bonds = []
        self.critical_points = None
        self.show_cp_labels = False
        self.overlay_atoms = []
        self.overlay_bonds = []
        self.overlay_opacity = 1.0
        self.molecules = []
        self.opacity = 1.0
        self.resolution = 15
        self.is_metallic = 0
        self.shininess = 1
        self.scaler = 1.12
        self.specular = 0.0
        self.specular_power = 0.5
        self.diffuse = 1.0
        self.shadows = False
        self.pbr = False
        self.show_orbitals = False
        self.surface = None
        self.picker = None
        self.axes_shown = False
        self.box_shown = False
        self.labels_shown = False
        self.output = ''
        self.display_atoms = True
        self.display_bonds = True
        self.atom_list = []
        self.atom_show_dict = self.make_atom_show_dict()
        self.bond_show_dict = self.make_bond_show_dict()
        self.axes = None
        self.style = 'surface'
        self.saved = False
        self.atom_scaler = 2.0
        self.bond_radius = 0.08
        self.show_measure = False
        self.move_enabled = False
        self.colored_bonds = False
        self.grid_points = 30
        self.selected_mo = 0
        self.calculation_instructions = None
        self.calculation_output = ''

        self.style_options = ['surface', 'wireframe', 'points', 'points_gaussian']

        self.list_widget_atoms = None
        self.atom_toggle_button = None
        self.list_widget_bonds = None
        self.bond_toggle_button = None

        self.setWindowTitle('MolVis - Molecule Viewer')
        self.frame = QtWidgets.QFrame()
        # add a second widget to the displacy

        self.layout = QtWidgets.QGridLayout()
        self.frame.setLayout(self.layout)
        self.setCentralWidget(self.frame)

        # side panel
        self.side_panel = QtWidgets.QFrame()
        self.side_panel_layout = QtWidgets.QVBoxLayout()
        self.side_panel_layout.setSpacing(0)
        self.side_panel_layout.setContentsMargins(0, 0, 0, 0)
        self.side_panel.setLayout(self.side_panel_layout)
        self.layout.addWidget(self.side_panel, 0, 0, 4, 1)

        # set the width of the side_panel
        self.side_panel.setMaximumWidth(300)
        self.side_panel.setMinimumWidth(200)

        # add a scroll panel to the side panel
        self.side_panel_scroll = QtWidgets.QScrollArea()
        self.side_panel_scroll.setWidgetResizable(True)
        self.side_panel_scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.side_panel_scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.side_panel_layout.addWidget(self.side_panel_scroll)

        # add a widget to the scroll panel

        self.textout = QtWidgets.QTextBrowser()
        self.layout.addWidget(self.textout, 3, 1)

        self.text_scroll = QtWidgets.QScrollArea()
        self.text_scroll.setWidget(self.textout)
        self.text_scroll.setWidgetResizable(True)
        self.text_scroll.setMaximumHeight(200)
        self.layout.addWidget(self.text_scroll, 3, 1)

        self.side_tabs = QtWidgets.QTabWidget()
        self.options_tab = QtWidgets.QWidget()
        self.side_tabs.addTab(self.options_tab, 'Options')
        self.structure_tab = QtWidgets.QWidget()
        self.side_tabs.addTab(self.structure_tab, 'Structure')
        self.ab_initio_tab = QtWidgets.QWidget()
        self.side_tabs.addTab(self.ab_initio_tab, 'Ab Initio')
        self.side_panel_scroll.setWidget(self.side_tabs)
        # self.side_panel_layout.addWidget(self.side_tabs)

        self.ab_initio_tab_layout = QtWidgets.QVBoxLayout()
        self.abinit_widget = QtWidgets.QWidget()
        self.abinit_widget.setMaximumWidth(280)
        self.abinit_widget_layout = QtWidgets.QVBoxLayout()

        self.ab_set_up_button = QtWidgets.QPushButton('Set Up')
        self.ab_set_up_button.clicked.connect(self.ab_initio_set_up)

        self.ab_run_button = QtWidgets.QPushButton('Run')
        self.ab_run_button.clicked.connect(self.run_pyscf)

        self.abinit_widget_layout.addWidget(self.ab_set_up_button)
        self.abinit_widget_layout.addWidget(self.ab_run_button)
        self.abinit_widget.setLayout(self.abinit_widget_layout)
        
        self.ab_initio_tab_layout.addWidget(self.abinit_widget)
        self.ab_initio_tab.setLayout(self.ab_initio_tab_layout)


        self.options_tab_layout = QtWidgets.QVBoxLayout()
        self.structure_tab_layout = QtWidgets.QVBoxLayout()
        self.side_tabs.setMaximumWidth(280)
        self.side_tabs.setMinimumWidth(280)

        self.option_widget = QtWidgets.QWidget()
        self.option_widget.setMaximumWidth(280)
        self.option_widget.setMinimumWidth(280)
        self.option_widget_layout = QtWidgets.QVBoxLayout()
        self.option_scroll = QtWidgets.QScrollArea()
        self.option_scroll.setWidget(self.option_widget)
        self.option_scroll.setWidgetResizable(True)
        self.option_widget.setLayout(self.option_widget_layout)

        self.structure_group1 = QtWidgets.QGroupBox('Show')
        self.structure_group1.setMaximumHeight(100)
        self.structure_group1_layout = QtWidgets.QVBoxLayout()
        self.atoms_checkbox = QtWidgets.QCheckBox('Atoms')
        self.atoms_checkbox.setChecked(True)
        self.atoms_checkbox.stateChanged.connect(self.toggle_display_atoms)
        self.structure_group1_layout.addWidget(self.atoms_checkbox)

        self.bonds_checkbox = QtWidgets.QCheckBox('Bonds')
        self.bonds_checkbox.setChecked(True)
        self.bonds_checkbox.stateChanged.connect(self.toggle_display_bonds)
        self.structure_group1_layout.addWidget(self.bonds_checkbox)
        self.structure_group1.setLayout(self.structure_group1_layout)

        self.structure_group5 = QtWidgets.QGroupBox('Symmetry')
        self.structure_group5.setMaximumHeight(150)
        self.structure_group5_layout = QtWidgets.QVBoxLayout()
        self.symm_anal_button = QtWidgets.QPushButton("Symmetry Analysis")
        self.symm_anal_button.clicked.connect(self.symm_analysis)
        self.structure_group5_layout.addWidget(self.symm_anal_button)
        self.structure_group5.setLayout(self.structure_group5_layout)

        self.structure_group4 = QtWidgets.QGroupBox('Style')
        self.structure_group4.setMaximumHeight(150)
        self.structure_group4_layout = QtWidgets.QVBoxLayout()
        self.surface_show_button = QtWidgets.QPushButton('Surface')
        self.surface_show_button.clicked.connect(lambda: self.change_style('surface'))
        self.structure_group4_layout.addWidget(self.surface_show_button)
        self.wireframe_show_button = QtWidgets.QPushButton('Wireframe')
        self.wireframe_show_button.clicked.connect(lambda: self.change_style('wireframe'))
        self.structure_group4_layout.addWidget(self.wireframe_show_button)
        self.colored_bonds_button = QtWidgets.QCheckBox('Colored Bonds')
        self.colored_bonds_button.stateChanged.connect(self.toggle_colored_bonds)
        self.structure_group4_layout.addWidget(self.colored_bonds_button)
        self.structure_group4.setLayout(self.structure_group4_layout)

        self.structure_group2 = QtWidgets.QGroupBox('Atoms')
        self.structure_group2.setMaximumHeight(200)
        self.structure_group2_layout = QtWidgets.QVBoxLayout()
        self.add_atoms_to_widget()

        self.structure_group3 = QtWidgets.QGroupBox('Bonds')
        self.structure_group3.setMaximumHeight(200)
        self.structure_group3_layout = QtWidgets.QVBoxLayout()
        self.add_bonds_to_widget()

        self.structure_tab_layout.addWidget(self.structure_group1)
        self.structure_tab_layout.addWidget(self.structure_group4)
        self.structure_tab_layout.addWidget(self.structure_group2)
        self.structure_tab_layout.addWidget(self.structure_group3)
        self.structure_tab_layout.addWidget(self.structure_group5)
        self.structure_tab.setLayout(self.structure_tab_layout)

        # display
        side_panel_group1 = QtWidgets.QGroupBox('Display Settings')
        side_panel_group1_layout = QtWidgets.QVBoxLayout()
        side_panel_group1.setLayout(side_panel_group1_layout)
        side_panel_group1.setMaximumHeight(100)
        side_panel_group1.setMinimumHeight(100)

        side_g1_axes = QtWidgets.QCheckBox('Show Axes')
        side_g1_axes.setChecked(False)
        side_g1_axes.stateChanged.connect(self.add_axes)
        side_panel_group1_layout.addWidget(side_g1_axes)

        self.side_g1_bounding_box = QtWidgets.QCheckBox('Show Bounding Box')
        self.side_g1_bounding_box.setChecked(False)
        self.side_g1_bounding_box.stateChanged.connect(self.add_bounding_box)
        side_panel_group1_layout.addWidget(self.side_g1_bounding_box)

        side_g1_show_labels = QtWidgets.QCheckBox('Show Atom Labels')
        side_g1_show_labels.setChecked(False)
        side_g1_show_labels.stateChanged.connect(self.add_labels)
        side_panel_group1_layout.addWidget(side_g1_show_labels)

        # render
        side_panel_group2 = QtWidgets.QGroupBox('Rendering Settings')
        side_panel_group2_layout = QtWidgets.QVBoxLayout()
        side_panel_group2.setLayout(side_panel_group2_layout)
        side_panel_group2.setMaximumHeight(200)
        side_panel_group2.setMinimumHeight(200)

        side_g2_anti_aliasing = QtWidgets.QCheckBox('Anti Aliasing')
        side_g2_anti_aliasing.setChecked(False)
        side_g2_anti_aliasing.stateChanged.connect(self.anti_aliasing)

        side_g2_shadows = QtWidgets.QCheckBox('Shadows')
        side_g2_shadows.setChecked(False)
        side_g2_shadows.stateChanged.connect(self.toggle_shadows)

        side_g2_pbr = QtWidgets.QCheckBox('PBR Rendering')
        side_g2_pbr.setChecked(False)
        side_g2_pbr.stateChanged.connect(self.pbr_rendering)

        # add a button to the widget group for metallic
        side_g2_metallic = QtWidgets.QPushButton('Metallic')
        side_g2_metallic.clicked.connect(self.metallic)

        side_g2_roughness = QtWidgets.QPushButton('Roughness')
        side_g2_roughness.clicked.connect(self.shiny)

        side_g2_diffuse = QtWidgets.QPushButton('Diffuse')
        side_g2_diffuse.clicked.connect(self.set_diffuse)

        side_panel_group2_layout.addWidget(side_g2_shadows)
        side_panel_group2_layout.addWidget(side_g2_anti_aliasing)
        side_panel_group2_layout.addWidget(side_g2_pbr)
        side_panel_group2_layout.addWidget(side_g2_metallic)
        side_panel_group2_layout.addWidget(side_g2_roughness)
        side_panel_group2_layout.addWidget(side_g2_diffuse)

        side_panel_group3 = QtWidgets.QGroupBox('Surfaces')
        side_panel_group3_layout = QtWidgets.QVBoxLayout()
        side_panel_group3.setLayout(side_panel_group3_layout)
        side_panel_group3.setMaximumHeight(150)
        side_panel_group3.setMinimumHeight(150)

        side_g3_surface = QtWidgets.QPushButton('Add Surface')
        side_g3_surface.clicked.connect(self.add_surface)
        side_panel_group3_layout.addWidget(side_g3_surface)

        side_g3_atom_surface = QtWidgets.QPushButton('Add Atom Surface')
        side_g3_atom_surface.clicked.connect(self.add_atom_surface)
        side_panel_group3_layout.addWidget(side_g3_atom_surface)

        side_g3_cuboid = QtWidgets.QPushButton('Add Cuboid')
        side_g3_cuboid.clicked.connect(self.add_cuboid)
        side_panel_group3_layout.addWidget(side_g3_cuboid)

        side_panel_group4 = QtWidgets.QGroupBox('Lights')
        side_panel_group4_layout = QtWidgets.QVBoxLayout()
        side_panel_group4.setLayout(side_panel_group4_layout)
        side_panel_group4.setMaximumHeight(100)
        side_panel_group4.setMinimumHeight(100)

        side_g4_light = QtWidgets.QPushButton('Add Light')
        side_g4_light.clicked.connect(self.lighting)
        side_panel_group4_layout.addWidget(side_g4_light)

        side_g4_remove_light = QtWidgets.QPushButton('Remove Light')
        side_g4_remove_light.clicked.connect(self.remove_lighting)
        side_panel_group4_layout.addWidget(side_g4_remove_light)

        side_panel_group5 = QtWidgets.QGroupBox('Colour')
        side_panel_group5_layout = QtWidgets.QVBoxLayout()
        side_panel_group5.setLayout(side_panel_group5_layout)
        side_panel_group5.setMaximumHeight(100)
        side_panel_group5.setMinimumHeight(100)

        side_g5_colour = QtWidgets.QPushButton('Atom Colour')
        side_g5_colour.clicked.connect(self.atom_color)
        side_panel_group5_layout.addWidget(side_g5_colour)

        side_g5_surf_colour = QtWidgets.QPushButton('Atom Surface Colour')
        side_g5_surf_colour.clicked.connect(self.atom_surface_color)
        side_panel_group5_layout.addWidget(side_g5_surf_colour)

        self.option_widget_layout.addWidget(side_panel_group1)
        self.option_widget_layout.addWidget(side_panel_group2)
        self.option_widget_layout.addWidget(side_panel_group3)
        self.option_widget_layout.addWidget(side_panel_group4)
        self.option_widget_layout.addWidget(side_panel_group5)
        self.options_tab_layout.addWidget(self.option_widget)
        self.options_tab.setLayout(self.options_tab_layout)

        # set the tow frames next to each other
        self.plotter = QtInteractor(self.frame)
        self.layout.addWidget(self.plotter.interactor, 0, 1)

        # make main_menu > self.main_menu for efield func
        self.main_menu = self.menuBar()
        self.main_menu.setNativeMenuBar(False)

        exit_button = QtWidgets.QAction('Exit', self)
        exit_button.setShortcut('Ctrl+Q')
        exit_button.triggered.connect(self.close_app)

        critical_points_button = QtWidgets.QAction('Load Critical Points', self)
        critical_points_button.triggered.connect(self.display_critical_points)

        open_button = QtWidgets.QAction('Open', self)
        open_button.setShortcut('Ctrl+O')
        open_button.triggered.connect(self.open_file)

        toggle_background = QtWidgets.QAction('Toggle Background', self)
        toggle_background.setShortcut('Ctrl+B')
        toggle_background.triggered.connect(self.toggle_background)

        add_atom_button = QtWidgets.QAction('Add Atom', self)
        add_atom_button.triggered.connect(self.new_atom)
        add_atom_button.setShortcut('Ctrl+A')

        ref_frame_button = QtWidgets.QAction('Change Reference Frame', self)
        ref_frame_button.triggered.connect(self.change_ref_frame)

        bond_button = QtWidgets.QAction('Find Bonds', self)
        bond_button.triggered.connect(self.find_bonds)
        bond_button.setShortcut('Ctrl+F')

        export_button = QtWidgets.QAction('Export', self)
        export_button.triggered.connect(self.export)
        export_button.setShortcut('Ctrl+s')

        figure_button = QtWidgets.QAction('Save Figure', self)
        figure_button.triggered.connect(self.save_figure)
        figure_button.setShortcut('Ctrl+Shift+S')

        cuboid_button = QtWidgets.QAction('Add Cuboid', self)
        cuboid_button.triggered.connect(self.add_cuboid)

        add_axes_button = QtWidgets.QAction('Add Axes', self)
        add_axes_button.triggered.connect(self.add_axes)

        vector_button = QtWidgets.QAction('Add Vector', self)
        vector_button.triggered.connect(self.add_vector)
        vector_button.setShortcut('Ctrl+V')

        light_source = QtWidgets.QAction('Move Light Source', self)
        light_source.triggered.connect(self.move_light_source)

        clear_button = QtWidgets.QAction('Clear', self)
        clear_button.triggered.connect(self.clear_all)
        clear_button.setShortcut('Ctrl+C')

        resultion_button = QtWidgets.QAction('Resolution', self)
        resultion_button.triggered.connect(self.change_resolution)

        opacity_button = QtWidgets.QAction('Opacity', self)
        opacity_button.triggered.connect(self.change_opacity)

        metalic_button = QtWidgets.QAction('Metallic', self)
        metalic_button.triggered.connect(self.metallic)

        shiny_button = QtWidgets.QAction('Roughness', self)
        shiny_button.triggered.connect(self.shiny)

        diffuse_button = QtWidgets.QAction('Diffuse', self)
        diffuse_button.triggered.connect(self.set_diffuse)

        labels_button = QtWidgets.QAction('Add Labels', self)
        labels_button.triggered.connect(self.add_labels)

        load_orbitals = QtWidgets.QAction('Load Orbitals', self)
        load_orbitals.triggered.connect(self.load_orbitals)

        align_button = QtWidgets.QAction('Align Molecule', self)
        align_button.triggered.connect(self.align)

        show_credits = QtWidgets.QAction('Credits', self)
        show_credits.triggered.connect(self.show_credit)

        surface_button = QtWidgets.QAction('Add Surface', self)
        surface_button.triggered.connect(self.add_surface)

        shadow_button = QtWidgets.QAction('Toggle Shadows', self)
        shadow_button.triggered.connect(self.toggle_shadows)

        pick_bg = QtWidgets.QAction('Background Colour', self)
        pick_bg.triggered.connect(self.pick_background)

        light_button = QtWidgets.QAction('Add Lighting', self)
        light_button.triggered.connect(self.lighting)

        remove_light = QtWidgets.QAction('Remove Lighting', self)
        remove_light.triggered.connect(self.remove_lighting)

        anti_alias = QtWidgets.QAction('Anti-Aliasing', self)
        anti_alias.triggered.connect(self.anti_aliasing)

        pbr_button = QtWidgets.QAction('Physically Based Rendering', self)
        pbr_button.triggered.connect(self.pbr_rendering)

        svg_button = QtWidgets.QAction('Export SVG', self)
        svg_button.triggered.connect(self.export_svg)

        atom_surface = QtWidgets.QAction('Add Atom Surface', self)
        atom_surface.triggered.connect(self.add_atom_surface)

        clear_surface = QtWidgets.QAction('Clear Surface', self)
        clear_surface.triggered.connect(self.clear_surface)

        plane_button = QtWidgets.QAction('Miller Index Plane', self)
        plane_button.triggered.connect(self.add_plane)

        atom_color_button = QtWidgets.QAction('Atom Color', self)
        atom_color_button.triggered.connect(self.atom_color)

        molcas_input_button = QtWidgets.QAction('Molcas Input', self)
        molcas_input_button.triggered.connect(self.molcas_input)

        save_log = QtWidgets.QAction('Save Log', self)
        save_log.triggered.connect(self.save_log)

        specular_button = QtWidgets.QAction('Specular', self)
        specular_button.triggered.connect(self.set_specular)

        specular_power_button = QtWidgets.QAction('Specular Power', self)
        specular_power_button.triggered.connect(self.set_specular_power)

        atom_radius_scale_button = QtWidgets.QAction('Atom Radius Scaling', self)
        atom_radius_scale_button.triggered.connect(self.set_atom_radius)

        export_obj_file = QtWidgets.QAction('Export as .obj', self)
        export_obj_file.triggered.connect(self.export_obj)

        export_vrml_file = QtWidgets.QAction('Export VRML', self)
        export_vrml_file.triggered.connect(self.export_vrml)

        bond_radius_scaling_button = QtWidgets.QAction('Bond Radius Scaling', self)
        bond_radius_scaling_button.triggered.connect(self.set_bond_radius)

        clear_molecule_button = QtWidgets.QAction('Clear Molecule', self)
        clear_molecule_button.triggered.connect(self.clear_molecule)

        file_menu = self.main_menu.addMenu('File')
        file_menu.addAction(open_button)
        file_menu.addAction(load_orbitals)
        file_menu.addAction(critical_points_button)
        file_menu.addSeparator()
        file_menu.addAction(export_button)
        file_menu.addAction(figure_button)
        file_menu.addAction(export_obj_file)
        # file_menu.addAction(export_vrml_file)
        file_menu.addAction(svg_button)
        file_menu.addAction(save_log)
        file_menu.addSeparator()
        file_menu.addAction(clear_molecule_button)
        # file_menu.addAction(clear_button)
        file_menu.addAction(show_credits)
        file_menu.addAction(exit_button)

        object_menu = self.main_menu.addMenu('Object')
        object_menu.addAction(add_atom_button)
        object_menu.addAction(bond_button)
        object_menu.addSeparator()
        object_menu.addAction(add_axes_button)
        object_menu.addAction(vector_button)
        object_menu.addAction(plane_button)
        object_menu.addAction(labels_button)
        object_menu.addAction(align_button)
        object_menu.addAction(ref_frame_button)

        shape_menu = self.main_menu.addMenu('Surfaces')
        shape_menu.addAction(cuboid_button)
        shape_menu.addAction(surface_button)
        shape_menu.addAction(atom_surface)
        shape_menu.addAction(clear_surface)

        render_menu = self.main_menu.addMenu('Render')
        render_menu.addAction(resultion_button)
        render_menu.addAction(opacity_button)
        render_menu.addSeparator()
        render_menu.addAction(pbr_button)
        render_menu.addAction(metalic_button)
        render_menu.addAction(shiny_button)
        render_menu.addAction(diffuse_button)
        render_menu.addAction(specular_button)
        render_menu.addAction(specular_power_button)
        render_menu.addSeparator()
        render_menu.addAction(shadow_button)
        render_menu.addAction(anti_alias)
        render_menu.addSeparator()
        render_menu.addAction(light_button)
        render_menu.addAction(remove_light)
        render_menu.addSeparator()
        render_menu.addAction(atom_color_button)
        render_menu.addAction(pick_bg)
        render_menu.addAction(atom_radius_scale_button)
        render_menu.addAction(bond_radius_scaling_button)

        calc_menu = self.main_menu.addMenu('Calculations')
        calc_menu.addAction(molcas_input_button)

        # icon toolbar
        # degree setter will be a box on the toolbar where you can set the degree of the rotation
        toolbar = self.addToolBar('Toolbar')

        degree_label = QtWidgets.QLabel('Step (°)')

        picking = QtWidgets.QAction('Toggel Picker', self)
        picking.triggered.connect(self.enable_picker)

        bond_length_calc = QtWidgets.QAction('Bond Length Calculator', self)
        bond_length_calc.triggered.connect(self.bond_length_calculator)

        self.degree = QtWidgets.QLineEdit()
        self.degree.setPlaceholderText('0')
        self.degree.setFixedWidth(30)

        rot_right_path = os.path.join(os.path.dirname(__file__), 'assets', 'arrow.uturn.right.png')
        rot_left_path = os.path.join(os.path.dirname(__file__), 'assets', 'arrow.uturn.left.png')
        rot_up_path = os.path.join(os.path.dirname(__file__), 'assets', 'arrow.uturn.up.png')

        move_right_path = os.path.join(os.path.dirname(__file__), 'assets', 'arrow.right.png')
        move_left_path = os.path.join(os.path.dirname(__file__), 'assets', 'arrow.left.png')
        move_up_path = os.path.join(os.path.dirname(__file__), 'assets', 'arrow.up.png')
        move_down_path = os.path.join(os.path.dirname(__file__), 'assets', 'arrow.down.png')

        rot_right_icon = QtGui.QIcon(rot_right_path)
        rot_left_icon = QtGui.QIcon(rot_left_path)
        rot_up_icon = QtGui.QIcon(rot_up_path)

        move_right_icon = QtGui.QIcon(move_right_path)
        move_left_icon = QtGui.QIcon(move_left_path)
        move_up_icon = QtGui.QIcon(move_up_path)
        move_down_icon = QtGui.QIcon(move_down_path)

        # use the icos to make buttons for the toolbar displaying the icons

        rot_right = QtWidgets.QPushButton(rot_right_icon, 'X')
        rot_right.clicked.connect(self.rotate_x)
        rot_right.setToolTip('Rotate x-axis')
        rot_right.setFixedWidth(50)

        rot_left = QtWidgets.QPushButton(rot_left_icon, 'Y')
        rot_left.clicked.connect(self.rotate_y)
        rot_left.setToolTip('Rotate y-axis')
        rot_left.setFixedWidth(50)

        rot_up = QtWidgets.QPushButton(rot_up_icon, 'Z')
        rot_up.clicked.connect(self.rotate_z)
        rot_up.setToolTip('Rotate z-axis')
        rot_up.setFixedWidth(50)

        move_right = QtWidgets.QPushButton(move_right_icon, '')
        move_right.clicked.connect(self.move_right)
        move_right.setToolTip('Move right')
        move_right.setFixedWidth(50)

        move_left = QtWidgets.QPushButton(move_left_icon, '')
        move_left.clicked.connect(self.move_left)
        move_left.setToolTip('Move left')
        move_left.setFixedWidth(50)

        move_up = QtWidgets.QPushButton(move_up_icon, '')
        move_up.clicked.connect(self.move_up)
        move_up.setToolTip('Move up')
        move_up.setFixedWidth(50)

        move_down = QtWidgets.QPushButton(move_down_icon, '')
        move_down.clicked.connect(self.move_down)
        move_down.setToolTip('Move down')
        move_down.setFixedWidth(50)

        x_align_button = QtWidgets.QPushButton('X')
        x_align_button.clicked.connect(self.set_camera_x)
        x_align_button.setFixedWidth(50)
        
        y_align_button = QtWidgets.QPushButton('Y')
        y_align_button.clicked.connect(self.set_camera_y)
        y_align_button.setFixedWidth(50)

        z_align_button = QtWidgets.QPushButton('Z')
        z_align_button.clicked.connect(self.set_camera_z)
        z_align_button.setFixedWidth(50)

        distance = QtWidgets.QPushButton('Measure Distance')
        distance.clicked.connect(self.measure_distance)
        distance.setFixedWidth(200)

        move_joystick = QtWidgets.QPushButton('Move Atoms')
        move_joystick.clicked.connect(self.move_atoms)
        move_joystick.setFixedWidth(200)

        move_label = QtWidgets.QLabel('Step (px)')
        self.px_step = QtWidgets.QLineEdit()
        self.px_step.setPlaceholderText('0')
        self.px_step.setFixedWidth(50)

        toolbar.addWidget(x_align_button)
        toolbar.addWidget(y_align_button)
        toolbar.addWidget(z_align_button)
        toolbar.addWidget(degree_label)
        toolbar.addWidget(self.degree)
        toolbar.addWidget(rot_right)
        toolbar.addWidget(rot_left)
        toolbar.addWidget(rot_up)
        toolbar.addWidget(move_label)
        toolbar.addWidget(self.px_step)
        toolbar.addWidget(move_right)
        toolbar.addWidget(move_left)
        toolbar.addWidget(move_up)
        toolbar.addWidget(move_down)
        # toolbar.addAction(picking)
        toolbar.addWidget(distance)
        # toolbar.addWidget(move_joystick)
        # toolbar.addAction(bond_length_calc)

        self.update_output(f"Molvis - Molecule Viewer\nVersion: 1.0.0\nAuthor: William T. Morrillo\n")
        self.update_output("-" * 80 + "\n\n")

        if show:
            self.show()


    def clear_molecule(self):
        self.atoms = []
        self.bonds = []
        self.critical_points = None
        self.show_cp_labels = False
        self.overlay_atoms = []
        self.overlay_bonds = []
        self.overlay_opacity = 1.0
        self.molecules = []
        self.opacity = 1.0
        self.resolution = 15
        self.is_metallic = 0
        self.shininess = 1
        self.specular = 0.0
        self.specular_power = 0.5
        self.diffuse = 1.0
        self.shadows = False
        self.pbr = False
        self.show_orbitals = False
        self.surface = None
        self.picker = None
        self.axes_shown = False
        self.box_shown = False
        self.labels_shown = False
        self.output = ''
        self.display_atoms = True
        self.display_bonds = True
        self.atom_list = []
        self.atom_show_dict = self.make_atom_show_dict()
        self.bond_show_dict = self.make_bond_show_dict()
        self.axes = None
        self.style = 'surface'
        self.saved = False
        self.atom_scaler = 2.0
        self.bond_radius = 0.08
        self.show_measure = False
        self.move_enabled = False
        self.colored_bonds = False
        self.grid_points = 30
        self.selected_mo = 0
        self.calculation_instructions = None
        self.calculation_output = ''
        self.clear_render()
        self.add_atoms_to_widget()
        self.add_bonds_to_widget()
        return

    def close_app(self):
        if not self.saved:
            warn = ExitSave()
            if warn.exec_() == QtWidgets.QDialog.Accepted:
                self.save_log()
                self.close()
            else:
                self.close()
        else:
            self.close()


    def symm_analysis(self):
        if len(self.atoms) == 0:
            return
        symm_window = SymmetryWindow()
        if symm_window.exec_() == QtWidgets.QDialog.Accepted:
            tol, predict, refine, max_iter, conv_tol = symm_window.get_values()
            output = analyze_symmetry(self.atoms, tol=tol, predict=predict, refine=refine, max_iter=max_iter, convergence_tol=conv_tol)
            self.update_output(output)
        else:
            return


    def change_ref_frame(self):
        # get the ordering
        if len(self.atoms) == 0:
            return 
        if len(self.molecules) == 0:
            return

        ref_window = RefFrameWindow()
        if ref_window.exec_() == QtWidgets.QDialog.Accepted:
            matrix = ref_window.get_rotation()
        else:
            return

        self.atoms = []
        self.bonds = []

        for molecule in self.molecules:
            molecule.rotate(matrix)
            for atom in molecule.atoms:
                self.atoms.append(atom)
            for bond in molecule.bonds:
                self.bonds.append(bond)

            self.update_output("\n" + "-" * 80)
            self.update_output("Changing Molecule Reference Frame")
            self.update_output("\n" + "Rotated Coordinates:")
            self.update_output("{}\n\n".format(len(molecule.atoms)))
            for atom in molecule.atoms:
                self.update_output("{:5}    {:11.7f} {:11.7f} {:11.7f}".format(atom.symbol, *atom.position))
            self.update_output("-" * 80 + "\n\n")

        self.clear_render()
        self.render_structure()


    def display_critical_points(self):
        filename, ok =  QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', '', 'Critical Point Files (*.txt *.out *.log *.dat)')
        if not ok:
            return
        self.cp = BondCriticalPoints(filename, resolution=self.resolution)
        self.cp_labels = self.cp.indices
        self.cp_densities = self.cp.densities
        self.critical_points = self.cp.critcal_points
        self.cp_positions = list(map(lambda x: x.coordinate + x.radius, self.critical_points))
        self.cp_colors = self.cp.dict_colours
        self.critical_point_menu()
        self.render_critical_points()


    def render_critical_points(self):
        if self.critical_points is None:
            return
        for cp in self.critical_points:
            if self.cp_show_dict[cp._type]:
                pv.threaded(self.plotter.add_mesh(cp.mesh, color=cp.color, lighting=True, smooth_shading=True,
                                                  metallic=self.is_metallic, roughness=self.shininess, pbr=self.pbr, diffuse=self.diffuse,
                                                  style=self.style, specular=self.specular, specular_power=self.specular_power)
                            )
        if self.show_cp_labels:
            self.plotter.add_point_labels(self.cp_positions, self.cp_labels)

        # render a legend of the colors to types to the screen
        # the keys of self.cp_colors are the types and
        # the values are the colors
        labels = []
        labels.append(["Critical Point Type", "black"])
        for k,v in self.cp_colors.items():
            labels.append([k,v])
        self.plotter.add_legend(labels, loc='lower right')


    def critical_point_menu(self):
        self.cp_tab = QtWidgets.QWidget()
        self.side_tabs.addTab(self.cp_tab, 'Critical Points')
        self.cp_tab_layout = QtWidgets.QVBoxLayout()

        self.cp_type_list = QtWidgets.QListWidget()
        self.cp_type_list.setMaximumWidth(200)
        self.cp_show_dict = {}
        for _type in self.cp_colors.keys():
            self.cp_show_dict[_type] = True
            self.cp_type_list.addItem(_type)

        self.cp_toggle_button = QtWidgets.QPushButton("Toggle")
        self.cp_toggle_button.clicked.connect(self.cp_toggle)

        self.cp_tab_layout.addWidget(self.cp_type_list)
        self.cp_tab_layout.addWidget(self.cp_toggle_button)
        self.cp_tab.setLayout(self.cp_tab_layout)

    def cp_toggle(self):
        _type = self.cp_type_list.currentItem().text()
        self.cp_show_dict[_type] = not self.cp_show_dict[_type]
        self.clear_render()
        self.render_structure()

    def toggle_colored_bonds(self):
        self.colored_bonds = not self.colored_bonds
        self.clear_render()
        self.render_structure()

    def run_pyscf(self):
        if self.calculation_instructions is None:
            return

        if self.calculation_instructions['calc'] =='DFT':
            start = perf_counter()
            self.DFT_kernal = run_pyscf_dft(self.atoms, self.calculation_instructions)
            end = perf_counter()

            output = format_output(self.DFT_kernal, (end-start))

            self.update_output(output)

        else:
            return


    def ab_initio_set_up(self):
        if len(self.atoms) == 0:
            return
        atom_list = np.unique(list(map(lambda x: x.symbol, self.atoms)))
        ab_setup = AbInitioGui(atom_list)
        if ab_setup.exec_() == QtWidgets.QDialog.Accepted:
            self.calculation_instructions = ab_setup.parse_calculation()
            print(self.calculation_instructions)
        else:
            return

    def set_bond_radius(self):
        bond_window = BondRadiusSelector()
        if bond_window.exec_() == QtWidgets.QDialog.Accepted:
            radius = bond_window.get_scaler()
        else:
            return

        self.bond_radius = radius

        bonds = []
        atoms = self.atoms
        for bond in self.bonds:
            bond.radius = self.bond_radius
            bonds.append(bond)
        self.clear_render()
        self.clear_atoms_bonds()
        self.bonds = bonds
        self.atoms = atoms
        self.render_structure()

    def export_vrml(self):
        file_name, ok = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', '', 'VRML (*.vrml)')
        if not ok:
            return
        self.plotter.export_vrml(file_name)
        return

    def export_obj(self):
        file_name, ok = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', '', 'obj (*.obj)')
        if not ok:
            return
        self.plotter.export_obj(file_name)
        return

    def set_atom_radius(self):
        radius_window = AtomRadiusSelector()
        if radius_window.exec_() == QtWidgets.QDialog.Accepted:
            scaler = radius_window.get_scaler()
        else:
            return

        self.atom_scaler = scaler

        atoms = []
        bonds = self.bonds
        for atom in self.atoms:
            atom.radius_scale = self.atom_scaler
            atoms.append(atom)
        self.clear_render()
        self.clear_atoms_bonds()
        self.atoms = atoms
        self.bonds = bonds
        self.render_structure()

    def change_style(self, option):
        self.style = option
        self.clear_render()
        self.render_structure()

    def set_specular(self):
        specular, ok = QtWidgets.QInputDialog.getDouble(self, 'Set Specular', 'Enter specular value:', 0.0, 0.0, 1.0, 2)
        if not ok:
            self.popup("Error setting specular")
            return

        if specular < 0 or specular > 1:
            self.popup("Invalid input")
            return

        self.specular = specular
        self.clear_render()
        self.render_structure()

    def set_specular_power(self):
        spec_power, ok = QtWidgets.QInputDialog.getInt(self, 'Set Specular Power', 'Enter specular power value:', 0, 0, 128, 2)
        if not ok:
            self.popup("Error setting specular power")
            return

        if spec_power < 0 or spec_power > 128:
            self.popup("Invalid value")
            return

        self.specular_power = spec_power
        self.clear_render()
        self.render_structure()

    def set_camera_x(self):
        self.plotter.view_yz()

    def set_camera_y(self):
        self.plotter.view_xz()

    def set_camera_z(self):
        self.plotter.view_xy()

    def save_log(self):
        file_name, ok = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', '', 'txt (*.txt)')
        self.update_output("Saving log to {}".format(file_name))
        if ok:
            with open(file_name, 'w') as f:
                f.write(self.output)
            self.saved = True
        else:
            self.popup('Invalid filename')
            return

    def toggle_atom(self, symbol):
        self.update_output("Visualising {} atoms: {}".format(symbol, not self.atom_show_dict[symbol]))
        self.atom_show_dict[symbol] = not self.atom_show_dict[symbol]
        self.clear_render()
        self.render_structure()

    def toggle_bond(self, symbol):
        self.update_output("Visualising {} bonds: {}".format(symbol, not self.bond_show_dict[symbol]))
        self.bond_show_dict[symbol] = not self.bond_show_dict[symbol]
        self.clear_render()
        self.render_structure()

    def add_bonds_to_widget(self):

        if self.list_widget_bonds is not None:
            self.list_widget_bonds.clear()
        else:
            self.list_widget_bonds = QtWidgets.QListWidget()
            self.list_widget_bonds.setFixedWidth(200)
            self.bond_toggle_button = QtWidgets.QPushButton('Toggle')
            self.bond_toggle_button.clicked.connect(lambda: self.toggle_bond(self.list_widget_bonds.currentItem().text()))
            self.bond_toggle_button.setFixedWidth(200)
            self.structure_group3_layout.addWidget(self.list_widget_bonds)
            self.structure_group3_layout.addWidget(self.bond_toggle_button)
            self.structure_group3.setLayout(self.structure_group3_layout)

        if len(self.bonds) > 0:
            for bond, _ in self.bond_show_dict.items():
                self.list_widget_bonds.addItem(bond)

        return


    def add_atoms_to_widget(self):

        if self.list_widget_atoms is not None:
            self.list_widget_atoms.clear()
        else:
            self.list_widget_atoms = QtWidgets.QListWidget()
            self.list_widget_atoms.setFixedWidth(200)
            self.atom_toggle_button = QtWidgets.QPushButton('Toggle')
            self.atom_toggle_button.clicked.connect(lambda: self.toggle_atom(self.list_widget_atoms.currentItem().text()))
            self.atom_toggle_button.setFixedWidth(200)
            self.structure_group2_layout.addWidget(self.list_widget_atoms)
            self.structure_group2_layout.addWidget(self.atom_toggle_button)
            self.structure_group2.setLayout(self.structure_group2_layout)

        if len(self.atom_list) > 0:
            for atom in self.atom_list:
                self.list_widget_atoms.addItem(atom)

        return

    def unique_atoms(self):
        if len(self.atoms) == 0:
            return []
        symbols = list(map(lambda x: x.symbol, self.atoms))
        return np.unique(symbols)

    def make_atom_show_dict(self):
        if len(self.atom_list) == 0:
            return {}
        return {symbol: True for symbol in self.atom_list}

    def make_bond_show_dict(self):
        if len(self.bonds) == 0:
            return {}

        bond_dict = {}

        for bond in self.bonds:
            symbol1 = bond.atom1.symbol
            symbol2 = bond.atom2.symbol

            key = [symbol1, symbol2]
            key = np.argsort(key)
            key = f"{symbol1} - {symbol2}"
            key_2 = f"{symbol2} - {symbol1}"
            if key not in bond_dict and key_2 not in bond_dict:
                bond_dict[key] = True

        return bond_dict

    def toggle_display_atoms(self):
        self.display_atoms = not self.display_atoms
        self.clear_render()
        self.render_structure()

    def toggle_display_bonds(self):
        self.display_bonds = not self.display_bonds
        self.clear_render()
        self.render_structure()

    def molcas_input(self):
        molcas = MolcasInput(self.atoms)
        if molcas.exec_() == QtWidgets.QDialog.Accepted:
            molcas.generate()
            self.update_output("Molcas input file generated successfully")
        else:
            return

    def move_up(self):
        # move the camera_position upwards by self.px_step
        try:
            step = float(self.px_step.text())
        except ValueError:
            return
        self.plotter.camera.position = self.plotter.camera.position + np.array([0, step, 0])
        self.update_output('camera moved up')

    def move_down(self):
        try:
            step = float(self.px_step.text())
        except ValueError:
            return
        self.plotter.camera.position = self.plotter.camera.position - np.array([0, step, 0])
        self.update_output('camera moved down')

    def move_left(self):
        try:
            step = float(self.px_step.text())
        except ValueError:
            return
        self.plotter.camera.position = self.plotter.camera.position - np.array([step, 0, 0])
        self.update_output('camera moved left')

    def move_right(self):
        try:
            step = float(self.px_step.text())
        except ValueError:
            return
        self.plotter.camera.position = self.plotter.camera.position + np.array([step, 0, 0])
        self.update_output('camera moved right')

    def atom_surface_color(self):
        if self.surface is None:
            return

        surface = self.surface
        color = QtWidgets.QColorDialog.getColor()
        color = color.getRgbF()
        try:
            surface.color = color
        except AttributeError:
            self.popup("Must be an atom surface")
            return
        self.add_surface_mesh()

    def atom_color(self):
        if len(self.atoms) == 0:
            return

        atoms = np.unique(list(map(lambda x: x.symbol, self.atoms)))

        color_selector = ColorSelector(atoms)
        if color_selector.exec_() == QtWidgets.QDialog.Accepted:
            color_dict = color_selector.get_colors()
            if color_dict is None:
                self.popup("No atoms changed")

            atoms = self.atoms
            bonds = self.bonds
            for key, color in color_dict.items():
                color = color.getRgbF()
                for atom in atoms:
                    if atom.symbol == key:
                        atom.color = color
                for bond in bonds:
                    if bond.atom1.symbol == key:
                        bond.atom1.color = color
                    if bond.atom2.symbol == key:
                        bond.atom2.color = color
            self.atoms = atoms
            self.bonds = bonds
            if len(self.overlay_atoms) > 0:
                overlay_atoms = self.overlay_atoms
                for key, color in color_dict.items():
                    color = color.getRgbF()
                    for atom in overlay_atoms:
                        if atom.symbol == key:
                            atom.color = color
                self.overlay_atoms = overlay_atoms
            bonds = self.bonds
            self.clear_render()
            self.render_structure()
        else:
            self.popup("No atoms changed")

    def bond_length_calculator(self):
        if self.picker is None:
            self.popup('Please enable picker first')
            return

        if len(self.picker.mesh) < 2:
            return

        mesh1, mesh2 = self.picker.mesh[:2]

    def enable_picker(self):

        class Picker:
            def __init__(self):
                self.mesh = []

            def __call__(self, picked, *args):
                self.mesh.append(picked)

        if self.picker is None:
            self.picker = Picker()
            self.plotter.enable_point_picking(self.picker, left_clicking=True, font_size=12)
        elif self.picker is not None:
            self.picker = None
            self.plotter.disable_point_picking()

    def clear_surface(self):
        self.surface = None
        self.clear_render()
        self.render_structure()

    def add_bounding_box(self):
        if not self.box_shown:
            self.plotter.add_bounding_box()
            self.box_shown = True
            self.update_output("Displaying boudning box")
        else:
            self.plotter.remove_bounding_box()
            self.box_shown = False
            self.update_output("Removing bounding box")

    def add_plane(self):
        if len(self.molecules) == 0:
            self.popup('No Molecule Loaded')
            return

        min, max = self.molecules[0].bounding_box
        mix_x, mix_y, mix_z = min
        max_x, max_y, max_z = max
        self.plotter.add_bounding_box()

        plane, ok = QtWidgets.QInputDialog.getText(self, 'Miller Index Plane', 'Enter Miller Index Plane (h k l):')
        if not ok:
            self.popup('Invalid Plane')

        if plane == '':
            self.popup('Invalid Plane')
            return

        try:
            h, k, l = map(int, plane.split())
        except ValueError:
            self.popup('Invalid Plane')
            return

        if h == 0 and k == 0 and l == 0:
            self.popup('Invalid Plane')
            return

        if h < 0 or k < 0 or l < 0:
            self.popup('Invalid Plane')
            return

        if h > 10 or k > 10 or l > 10:
            self.popup('Invalid Plane')
            return

        color = QtWidgets.QColorDialog.getColor()

        mesh = self.add_miller_plane(h, k, l, mix_x, mix_y, mix_z, max_x, max_y, max_z)
        self.plotter.add_mesh(mesh, color=color.getRgbF(), opacity=0.5)

        return

    def add_miller_plane(self, h, k, l, min_x, max_x, min_y, max_y, min_z, max_z):

        if h != 0:
            x_intercept = min_x + (1/h) * (max_x - min_x)
        else:
            x_intercept = min_x

        if k != 0:
            y_intercept = min_y + (1/k) * (max_y - min_y)
        else:
            y_intercept = min_y

        if l != 0:
            z_intercept = min_z + (1/l) * (max_z - min_z)
        else:
            z_intercept = min_z

        center = [min_x + (max_x - min_x) / 2, min_y + (max_y - min_y) / 2, min_z + (max_z - min_z) / 2]

        v = np.array([x_intercept, y_intercept, z_intercept])

        # find the vector perpendicular to v
        perp_v = np.array([1, 1, 1])
        perp_v = perp_v - np.dot(perp_v, v) * v
        perp_v = perp_v / np.linalg.norm(perp_v)

        mesh = pv.Plane(center=center, direction=v, i_size=10, j_size=10)
        return mesh

    def add_atom_surface(self):

        surface_generator = AtomSurface()
        if surface_generator.exec_() == QtWidgets.QDialog.Accepted:
            symbol, center, width, length, z_level = surface_generator.get_atom_surface()
            if symbol is None:
                self.popup("Invalid Input")
                return
            packing = 'fcc'
            self.surface = Surface(symbol, center, width, length, z_level, packing, self.resolution)
            self.surface.create_surface()
            self.add_surface_mesh()
            self.update_output("\n" + "-" * 80)
            self.update_output("Atom Surface")
            self.update_output("Element: {}".format(symbol))
            self.update_output("Center: {}".format(center))
            self.update_output("Width: {}".format(width))
            self.update_output("Length: {}".format(length))
            self.update_output("Z Level: {}".format(z_level))
            self.update_output("-" * 80 + "\n\n")
        else:
            self.popup("Invalid Input")
            return

    def add_surface_mesh(self):
        self.plotter.add_mesh(self.surface.surface, color=self.surface.color,
                              opacity=self.opacity, lighting=True,
                              smooth_shading=True, metallic=self.is_metallic,
                              roughness=self.shininess, pbr=self.pbr, diffuse=self.diffuse)

    def export_svg(self):
        file_name, ok = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', '', 'SVG (*.svg)')
        if ok:
            self.plotter.save_graphic(file_name)
            self.update_output(f"Saved SVG to {file_name}")
        else:
            self.popup("Could not save a svg file")

    def pbr_rendering(self):
        self.pbr = not self.pbr
        self.clear_render()
        self.render_structure()
        self.update_output(f"PBR Rendering: {self.pbr}")

    def anti_aliasing(self):
        self.plotter.enable_anti_aliasing()

    def remove_lighting(self):
        self.plotter.remove_all_lights()

    def lighting(self):
        light_selector = LightSelector()
        if light_selector.exec_() == QtWidgets.QDialog.Accepted:
            position, cone_angle, intensity = light_selector.get_light()
            if position is None:
                self.popup("Invalid light")
                return
            light_source = pv.Light(position=position, focal_point=(0, 0, 0), color='white')
            light_source.positional = True
            light_source.shadow_attenuation = 0.1
            light_source.cone_angle = cone_angle
            light_source.intensity = intensity
            light_source.exponent = 10
            self.plotter.add_light(light_source)
            self.update_output("\n" + "-" * 80)
            self.update_output("Light Source")
            self.update_output("Position: {}".format(position))
            self.update_output("Cone Angle: {}".format(cone_angle))
            self.update_output("Intensity: {}".format(intensity))
            self.update_output("-" * 80 + "\n\n")
        else:
            self.popup('Internal Lighting Error')
            return

    def toggle_shadows(self):
        if not self.shadows:
            self.shadows = True
            self.plotter.enable_shadows()
            self.update_output("Shadows enabled")
        else:
            self.shadows = False
            self.plotter.disable_shadows()
            self.update_output("Shadows disabled")

    def add_surface(self):
        color = QtWidgets.QColorDialog.getColor()
        self.plotter.add_floor('-z', color=color.getRgbF(), opacity=1.0, lighting=True, pad=30, i_resolution=self.resolution*5, j_resolution=self.resolution*5, offset=0.04)

    def rotate_x(self):
        try:
            degree = float(self.degree.text())
        except ValueError:
            return
        self.do_rotation('x', degree)

    def rotate_y(self):
        try:
            degree = float(self.degree.text())
        except ValueError:
            return
        self.do_rotation('y', degree)

    def rotate_z(self):
        try:
            degree = float(self.degree.text())
        except ValueError:
            return
        self.do_rotation('z', degree)

    def do_rotation(self, axis, degree):
        current_pos = self.plotter.camera_position
        current_pos = np.array([
            [current_pos[0][0], current_pos[0][1], current_pos[0][2]],
            [current_pos[1][0], current_pos[1][1], current_pos[1][2]],
            [current_pos[2][0], current_pos[2][1], current_pos[2][2]]
            ])
        new_pos = current_pos @ self.rotation_matrix(axis, degree)
        new_pos = new_pos.flatten()
        new_pos = [(new_pos[0], new_pos[1], new_pos[2]), (new_pos[3], new_pos[4], new_pos[5]), (new_pos[6], new_pos[7], new_pos[8])]
        self.plotter.camera_position = new_pos

    def rotation_matrix(self, axis, degree):
        rads = np.radians(degree)
        if axis == 'x':
            return np.array([[1, 0, 0],
                             [0, np.cos(rads), -np.sin(rads)],
                             [0, np.sin(rads), np.cos(rads)]])
        elif axis == 'y':
            return np.array([[np.cos(rads), 0, np.sin(rads)],
                             [0, 1, 0],
                             [-np.sin(rads), 0, np.cos(rads)]])
        elif axis == 'z':
            return np.array([[np.cos(rads), -np.sin(rads), 0],
                             [np.sin(rads), np.cos(rads), 0],
                             [0, 0, 1]])


    def show_credit(self):
        QtWidgets.QMessageBox.about(self, 'Credits', 'MolVis - Molecule Viewer\n\n'
                                                     'Developed by:\n'
                                                     'William T. Morrillo\n'
                                                     'The Univeristy of Manchester')

    def load_orbitals(self):
        # get the molden file path
        file_path = QtWidgets.QFileDialog.getOpenFileName(self, 'Open h5 File', '', 'Molcas File (*.h5)')[0]
        if not file_path:
            self.popup('No file selected')
            return

        # self.popup("Under implementation (WIP)")
        self.orbitals = Orbital(file_path)
        coords, symbols = self.orbitals.structure
        molecule = Molecule(symbols, coords, self.resolution, self.atom_scaler, self.bond_radius, radius_scaler=self.radius_scaler)
        self.molecules.append(molecule)
        self.update_output("{}\n\n".format(len(molecule.atoms)))
        for atom in molecule.atoms:
            self.update_output("{:5}    {:11.7f} {:11.7f} {:11.7f}".format(atom.symbol, *atom.position))
            self.atoms.append(atom)
            if atom.symbol not in self.atom_show_dict.keys():
                self.atom_show_dict[atom.symbol] = True
        self.atom_list = self.unique_atoms()
        for bond in molecule.bonds:
            self.bonds.append(bond)
            symbol1 = bond.atom1.symbol
            symbol2 = bond.atom2.symbol
            key = [symbol1, symbol2]
            key = np.argsort(key)
            key = f"{symbol1} - {symbol2}"
            key_2 = f"{symbol2} - {symbol1}"
            if key not in self.bond_show_dict.keys() and key_2 not in self.bond_show_dict.keys():
                self.bond_show_dict[key] = True
        self.add_atoms_to_widget()
        self.add_bonds_to_widget()
        self.render_structure()
        self.orbitals.compute_mos(self.grid_points)
        self.orbital_menu()
        # self.display_orbital()
        self.show_orbitals = True
        return

    def display_orbital(self):
        self.selected_mo = int(self.mo_select.currentText().split(" ")[0])
        mesh = self.orbitals.mo_mesh(self.selected_mo)
        contours = mesh.contour(isosurfaces=[0.05, -0.05], scalars='orbital')
        pv.threaded(self.plotter.add_mesh(contours, cmap='coolwarm', opacity=0.9, lighting=True, smooth_shading=True,
                                          pbr=self.pbr, style=self.style, metallic=self.is_metallic, roughness=self.shininess,
                                          diffuse=self.diffuse, specular=self.specular, specular_power=self.specular_power))

    def orbital_menu(self):
        self.orbital_tab = QtWidgets.QWidget()
        self.side_tabs.addTab(self.orbital_tab, 'Orbitals')
        self.orbital_tab_layout = QtWidgets.QVBoxLayout()

        self.mo_label = QtWidgets.QLabel('Select Molecular Orbital')
        self.mo_select = QtWidgets.QComboBox()
        orb_labels = list(map(lambda x: str(x), range(len(self.orbitals.MOs))))
        types = self.orbitals.types
        orb_labels = list(map(lambda x, y: x + "  " + str(y), orb_labels, types))
        self.mo_select.addItems(orb_labels)
        self.mo_select_button = QtWidgets.QPushButton('Display')
        self.mo_select_button.clicked.connect(self.display_orbital)

        self.orbital_tab_layout.addWidget(self.mo_label)
        self.orbital_tab_layout.addWidget(self.mo_select)
        self.orbital_tab_layout.addWidget(self.mo_select_button)

        self.orbital_tab.setLayout(self.orbital_tab_layout)



    def align(self):
        if self.show_orbitals:
            self.popup('Cannot align molecule whilst displaying orbitals')
            return

        if len(self.molecules) == 0:
            return

        self.atoms = []
        self.bonds = []

        for molecule in self.molecules:
            molecule.align
            for atom in molecule.atoms:
                self.atoms.append(atom)
            for bond in molecule.bonds:
                self.bonds.append(bond)

            self.update_output("\n" + "-" * 80)
            self.update_output("Align Molecule")
            self.update_output("Eigenvector of the inertia tensor")
            _, vecs = molecule.Axes
            for vec in vecs:
                self.update_output("\t{:11.7f} {:11.7f} {:11.7f}".format(*vec))
            self.update_output("\n" + "Rotated Coordinates:")
            self.update_output("{}\n\n".format(len(molecule.atoms)))
            for atom in molecule.atoms:
                self.update_output("{:5}    {:11.7f} {:11.7f} {:11.7f}".format(atom.symbol, *atom.position))
            self.update_output("-" * 80 + "\n\n")

        self.clear_render()
        self.render_structure()

    def add_labels(self):
        if self.labels_shown:
            self.plotter.remove_actor(self.point_labels)
            self.labels_shown = False
        else:
            labels = list(map(lambda atom: atom.symbol, self.atoms))
            positions = list(map(lambda atom: np.array(atom.position) + atom.plotting_radius, self.atoms))
            if len(labels) > 0:
                self.point_labels = self.plotter.add_point_labels(positions, labels)
                self.labels_shown = True
            else:
                return

    def set_diffuse(self):
        dif, ok = QtWidgets.QInputDialog.getInt(self, 'Diffuse', 'Enter the diffuse value')
        if not ok:
            self.popup("lighting failed")
            return
        if dif < 0 or dif > 100:
            self.popup("enter a valid diffuse value")
            return

        dif = dif / 100
        self.diffuse = dif
        self.clear_render()
        self.render_structure()

    def metallic(self):
        met, ok = QtWidgets.QInputDialog.getInt(self, 'Metallic', 'Enter the metallic value: (0-100)', value=int(self.is_metallic))
        if not ok:
            return

        if met < 0 or met > 100:
            return

        met = met / 100
        self.is_metallic = met
        self.clear_render()
        self.render_structure()

    def shiny(self):
        shininess, ok = QtWidgets.QInputDialog.getInt(self, 'Shininess', 'Enter The Roughness: (0-100)', value=int(self.shininess * 100))
        if not ok:
            return

        if shininess < 0 or shininess > 100:
            return

        self.shininess = shininess / 100
        self.clear_render()
        self.render_structure()

    def change_opacity(self):
        opacity, ok = QtWidgets.QInputDialog.getInt(self, 'Opacity', 'Enter the opacity: (0-100)', value=int(self.opacity * 100))
        if not ok:
            return

        if opacity < 0 or opacity > 100:
            return

        self.opacity = opacity / 100
        self.clear_render()
        self.render_structure()

    def change_resolution(self):
        # pop up box with a slider to change the resolution
        resolution, ok = QtWidgets.QInputDialog.getInt(self, 'Resolution', 'Enter the resolution:', value=self.resolution)
        if not ok:
            return

        self.resolution = resolution
        atoms = []
        bonds = []
        for atom in self.atoms:
            atom.resolution = resolution
            atoms.append(atom)
        for bond in self.bonds:
            bond.resolution = resolution
            bonds.append(bond)
        if self.critical_points is not None:
            for cp in self.critical_points:
                cp.resolution = self.resolution
        self.clear_render()
        self.clear_atoms_bonds()
        self.atoms = atoms
        self.bonds = bonds
        self.render_structure()

    def clear_atoms_bonds(self):
        self.atoms = []
        self.bonds = []

    def clear_render(self):
        self.plotter.clear_actors()
        self.plotter.render()

    def clear_all(self):
        self.clear_render()
        self.clear_atoms_bonds()
        self.atom_show_dict = {}
        self.bond_show_dict = {}

    def move_light_source(self):
        light = self.plotter.renderer.lights

        position, ok = QtWidgets.QInputDialog.getText(self, 'Light Position', 'Enter the position (x y z):')
        if not ok:
            return
        if position == '':
            return

        try:
            position = np.array(position.split(), dtype=float)
        except ValueError:
            return

        self.plotter.render()

    def add_axes(self):
        if not self.axes_shown:
            # self.axes = self.plotter.add_axes()
            self.camera_oriatation = self.plotter.add_camera_orientation_widget()
            self.axes_shown = True
        else:
            # self.plotter.hide_axes()
            self.axes_shown = False
            self.plotter.clear_camera_widgets()

    def measure_distance(self):
        if not self.show_measure:
            self.measure = self.plotter.add_measurement_widget()
            self.show_measure = True
        else:
            self.plotter.clear_measure_widgets()
            self.show_measure = False

    def move_atoms(self):
        if not self.move_enabled:
            self.move = self.plotter.enable_joystick_actor_style()
            self.move_enabled = True
        else:
            self.plotter.remove(self.move)
            self.move_enbled = False

    def add_vector(self):
        # get the origin of the vector
        origin, ok = QtWidgets.QInputDialog.getText(self, 'Vector Origin', 'Enter the origin (x y z):')
        if not ok:
            return
        if origin == '':
            self.popup('Enter vector origin, cannot be empty')
            return

        try:
            origin = np.array(origin.split(), dtype=float)
        except ValueError:
            return

        # get the direction of the vector
        direction, ok = QtWidgets.QInputDialog.getText(self, 'Vector Direction', 'Enter the direction (x y z):')
        if not ok:
            return
        if direction == '':
            self.popup("Enter a direction (norm is the length)")
            return

        color = QtWidgets.QColorDialog.getColor()
        color = color.getRgbF()

        try:
            direction = np.array(direction.split(), dtype=float)
        except ValueError:
            return

        length = np.linalg.norm(direction)

        # create the vector
        vector = pv.Arrow(start=origin, direction=direction, scale=length, tip_radius=0.1, tip_length=0.3, shaft_radius=0.05)
        self.plotter.add_mesh(vector, color=color, lighting=True, smooth_shading=True)

    def add_cuboid(self):
        # get the dimensions of the cuboid
        dimensions, ok = QtWidgets.QInputDialog.getText(self, 'Cuboid Dimensions', 'Enter the dimensions (l w h):')
        if not ok:
            return
        if dimensions == '':
            self.popup('Invalid dimensions')
            return

        try:
            dimensions = np.array(dimensions.split(), dtype=float)
        except ValueError:
            return

        # get the position of the cuboid
        position, ok = QtWidgets.QInputDialog.getText(self, 'Cuboid Position', 'Enter the position (x y z):')
        if not ok:
            return
        if position == '':
            self.popup_error('Invalid input')
            return

        try:
            position = np.array(position.split(), dtype=float)
        except ValueError:
            return

        color = QtWidgets.QColorDialog.getColor()
        color = color.getRgbF()

        # create the cuboid
        cuboid = pv.Cube(center=position, x_length=dimensions[0], y_length=dimensions[1], z_length=dimensions[2])
        self.plotter.add_mesh(cuboid, color=color, smooth_shading=True, lighting=True)

    def save_figure(self):
        path = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', '', 'Image Files (*.png *.jpg *.jpeg *.bmp *.tiff)')[0]
        self.plotter.screenshot(path, transparent_background=True, scale=3)

    def popup(self, message):
        msg = QtWidgets.QMessageBox()
        msg.setText(message)
        msg.exec_()

    def new_atom(self):

        atom_selector = AtomSelector()
        if atom_selector.exec_() == QtWidgets.QDialog.Accepted:
            symbol, position = atom_selector.get_atom()
            if symbol is None:
                self.popup('Invalid atom')
                return
            atom = Atom(symbol, position, self.resolution, self.atom_scaler)
            self.update_output("\n" + "-" * 80)
            self.update_output("New Atom")
            self.update_output("Symbol = {}".format(symbol))
            self.update_output("Coordinates:")
            self.update_output("{:11.7f} {:11.7f} {:11.7f}".format(*position))
            self.update_output("-" * 80 + "\n\n")
            self.atoms.append(atom)
            self.atom_list = self.unique_atoms()
            if atom.symbol not in self.atom_show_dict.keys():
                self.atom_show_dict[atom.symbol] = True
            self.add_atoms_to_widget()
            self.render_structure()
        else:
            self.popup("Invalid Input")
            return

    def export(self):
        symbols = list(map(lambda x: x.symbol, self.atoms))
        coords = list(map(lambda x: x.position, self.atoms))
        # get the path 
        path = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', '', 'Molecule Files (*.xyz)')[0]
        xyz_py.save_xyz(path, symbols, coords)

    def find_bonds(self):
        scaler_window = BondFindScalerWindow()
        if scaler_window.exec_() == QtWidgets.QDialog.Accepted:
            self.scaler = scaler_window.get_scaler()
            print(self.scaler)
        coords = list(map(lambda x: x.position, self.atoms))
        symbols = list(map(lambda x: x.symbol, self.atoms))
        mol = Molecule(symbols, coords, self.resolution, self.atom_scaler, self.bond_radius, radius_scaler=self.scaler)
        self.molecules.append(mol)
        for bond in mol.bonds:
            self.bonds.append(bond)
            symbol1 = bond.atom1.symbol
            symbol2 = bond.atom2.symbol
            key = [symbol1, symbol2]
            key = np.argsort(key)
            key = f"{symbol1} - {symbol2}"
            key_2 = f"{symbol2} - {symbol1}"
            if key not in self.bond_show_dict.keys() and key_2 not in self.bond_show_dict.keys():
                self.bond_show_dict[key] = True
        self.add_bond(self.bonds)

    def toggle_background(self):
        if self.plotter.renderer.background_color == 'white':
            self.plotter.renderer.background_color = 'black'
        else:
            self.plotter.renderer.background_color = 'white'

    def pick_background(self):
        color = QtWidgets.QColorDialog.getColor()
        color = color.getRgbF()
        self.plotter.renderer.background_color = color

    def open_file(self):
        self.filename =  QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', '', 'Structure Files (*.xyz *.vasp *.cif POSCAR *.fchk)')[0]
        if self.filename == '':
            return
        if self.filename is None:
            return
        self.update_output(f"Loading {self.filename}\n\n")
        if self.filename.endswith('.xyz'):
            self.load_molecule()
        elif self.filename.endswith('.fchk'):
            self.load_fchk()
        else:
            self.load_crystal()

    def load_fchk(self):
        coords = make_gaussian_extractor(self.filename, ('fchk', 'coordinates'))[()]
        numbers = make_gaussian_extractor(self.filename, ('fchk', 'atomic_number'))[()]
        symbols = list(map(chemical_symbols.__getitem__, numbers))

        try:
            self.hess = make_gaussian_extractor(self.filename, ('fchk', 'hessian'))[()]
            self.grad_mu = make_gaussian_extractor(self.filename, ('fchk', 'dipole_derivatives'))[()]
            self.hess *= HARTREE2J / BOHR2M**2  # J/m^2 = N/m
            self.grad_mu *= E0_TO_C  # C
            self.add_efield_menu()
        except ValueError:
            self.allow_efield = False
            self.hess = None
            self.grad_mu = None

        coords *= BOHR2M * 1e10  # Angstrom

        molecule = Molecule(symbols, coords, self.resolution, self.atom_scaler, self.bond_radius, radius_scaler=self.scaler)
        self.molecules.append(molecule)
        self.update_output("{}\n\n".format(len(molecule.atoms)))
        for atom in molecule.atoms:
            self.update_output("{:5}    {:11.7f} {:11.7f} {:11.7f}".format(atom.symbol, *atom.position))
            self.atoms.append(atom)
            if atom.symbol not in self.atom_show_dict.keys():
                self.atom_show_dict[atom.symbol] = True
        self.atom_list = self.unique_atoms()
        for bond in molecule.bonds:
            self.bonds.append(bond)
            symbol1 = bond.atom1.symbol
            symbol2 = bond.atom2.symbol
            key = [symbol1, symbol2]
            key = np.argsort(key)
            key = f"{symbol1} - {symbol2}"
            key_2 = f"{symbol2} - {symbol1}"
            if key not in self.bond_show_dict.keys() and key_2 not in self.bond_show_dict.keys():
                self.bond_show_dict[key] = True
        self.add_atoms_to_widget()
        self.add_bonds_to_widget()
        self.render_structure()
        self.update_output("\n" + "-"*80 + "\n\n")
        if self.hess is not None:
            self.update_output("Hessian (N m^-1)\n\n")
            hess_shape = self.hess.shape
            print_str = "{:11.4f} " * hess_shape[0]
            for row in self.hess:
                self.update_output(print_str.format(*row))
            self.update_output("\n" + "-"*80 + "\n\n")
        if self.grad_mu is not None:
            grad_mu_shape = self.grad_mu.shape
            self.update_output("Dipole Derivatives (C)\n\n")
            print_str = "{:11.7e} " * grad_mu_shape[1]
            for row in self.grad_mu:
                self.update_output(print_str.format(*row))
            self.update_output("\n" + "-"*80 + "\n\n")

    def add_efield_menu(self):
        efield_menu = self.main_menu.addMenu("Electric Field")
        distort_button = QtWidgets.QAction('Distort', self)
        distort_button.triggered.connect(self.efield_distort)
        distort_overlay = QtWidgets.QAction('Overlay Distortion', self)
        distort_overlay.triggered.connect(self.efield_distort_overlay)

        efield_menu.addAction(distort_button)
        efield_menu.addAction(distort_overlay)
        return

    def efield_distort(self):
        vec_win = Efield()
        if vec_win.exec_() == QtWidgets.QDialog.Accepted:
            efield_vector, add_vec = vec_win.get_vector()
            if efield_vector is None:
                self.popup("Error parsing input")
                return
            dist_mol = electric_distort(self.atoms, self.hess, self.grad_mu, efield_vector, self.resolution, 1.0, self.atom_scaler, self.bond_radius)
            self.update_output("-" * 80 + "\n\n")
            self.update_output("Electric Field Distort\n\n")
            self.update_output("Computing the electric field distortion via \n >> H . r = grad_r mu . E\n\n")
            self.update_output("Electric field (V m^-1): {:11.7e} {:11.7e} {:11.7e}\n\n".format(*efield_vector))
            self.update_output("Distorted Coordinates")
            self.update_output("len(dist_mol.atoms)\n\n")
            for atom in dist_mol.atoms:
                self.update_output("{:5}    {:11.7f} {:11.7f} {:11.7f}".format(atom.symbol, *atom.position))
            self.update_output("-" * 80 + "\n\n")
            self.clear_render()
            self.clear_atoms_bonds()
            self.atoms.append(dist_mol.atoms)
            self.bonds.append(dist_mol.bonds)
            self.render_structure()
            if add_vec:
                norm_vec = efield_vector / np.linalg.norm(efield_vector)
                vec_start = -10 * norm_vec
                vec = pv.Arrow(vec_start, norm_vec, scale=4)
                self.add_object(vec)
        else:
            self.popup("Cancelled")
            return

    def efield_distort_overlay(self):
        vec_win = Efield()
        if vec_win.exec_() == QtWidgets.QDialog.Accepted:
            efield_vector, add_vec = vec_win.get_vector()
            if efield_vector is None:
                self.popup("Error parsing input")
                return
            dist_mol = electric_distort(self.atoms, self.hess, self.grad_mu, efield_vector, self.resolution, 0.4, self.atom_scaler, self.bond_radius)

            self.update_output("-" * 80 + "\n\n")
            self.update_output("Electric Field Distort\n\n")
            self.update_output("Computing the electric field distortion via \n >> H . r = grad_r mu . E\n\n")
            self.update_output("Electric field (V m^-1): {:11.7e} {:11.7e} {:11.7e}\n\n".format(*efield_vector))
            self.update_output("Distorted Coordinates")
            self.update_output("len(dist_mol.atoms)\n\n")
            for atom in dist_mol.atoms:
                self.update_output("{:5}    {:11.7f} {:11.7f} {:11.7f}".format(atom.symbol, *atom.position))
            self.update_output("-" * 80 + "\n\n")

            atoms = dist_mol.atoms
            bonds = dist_mol.bonds
            opacity = dist_mol.opacity

            self.overlay_atoms = atoms
            self.overlay_bonds = bonds
            self.overlay_opacity = opacity

            for atom in atoms:
                show = self.atom_show_dict.get(atom.symbol)
                if show:
                    pv.threaded(self.plotter.add_mesh(atom.mesh, color=atom.color, lighting=True, smooth_shading=True, opacity=opacity,
                                                      metallic=self.is_metallic, roughness=self.shininess, pbr=self.pbr, diffuse=self.diffuse,
                                                      style=self.style, specular=self.specular, specular_power=self.specular_power)
                                )
            for bond in bonds:
                symbol1 = bond.atom1.symbol
                symbol2 = bond.atom2.symbol
                key = f"{symbol1} - {symbol2}"
                key_2 = f"{symbol2} - {symbol1}"
                show = self.bond_show_dict.get(key)
                show_2 = self.bond_show_dict.get(key_2)
                if show or show_2:
                    pv.threaded(self.plotter.add_mesh(bond.mesh, color=bond.color, lighting=True, smooth_shading=True, opacity=opacity,
                                                      pbr=self.pbr, style=self.style, metallic=self.is_metallic, roughness=self.shininess, 
                                                      diffuse=self.diffuse, specular=self.specular, specular_power=self.specular_power)
                                )

            self.clear_render()
            self.render_structure()

            if add_vec:
                norm_vec = efield_vector / np.linalg.norm(efield_vector)
                vec_start = -10 * norm_vec
                vec = pv.Arrow(vec_start, norm_vec, scale=4)
                self.add_object(vec)

    def load_crystal(self):
        self.crystal = Crystal(self.filename, self.resolution, self.atom_scaler, self.bond_radius)
        self.update_output("{}\n\n".format(len(self.crystal.atoms)))
        for atom in self.crystal.atoms:
            self.update_output("{:5}    {:11.4f} {:11.4f} {:11.4f}".format(atom.symbol, *atom.position))
            self.atoms.append(atom)
            if atom.symbol not in self.atom_show_dict.keys():
                self.atom_show_dict[atom.symbol] = True
        self.atom_list = self.unique_atoms()
        self.bonds = self.crystal.bonds
        for bond in self.bonds:
            symbol1 = bond.atom1.symbol
            symbol2 = bond.atom2.symbol
            key = [symbol1, symbol2]
            key = np.argsort(key)
            key = f"{symbol1} - {symbol2}"
            key_2 = f"{symbol2} - {symbol1}"
            if key not in self.bond_show_dict.keys() and key_2 not in self.bond_show_dict.keys():
                self.bond_show_dict[key] = True
        self.add_atoms_to_widget()
        self.add_bonds_to_widget()
        self.render_structure()
        self.side_g1_bounding_box.setChecked(True)
        self.update_output("\n" + "-"*80 + "\n\n")

    def load_molecule(self):
        molecule = Molecule.from_xyz(self.filename, self.resolution, self.atom_scaler, self.bond_radius)
        self.molecules.append(molecule)
        self.update_output("{}\n\n".format(len(molecule.atoms)))
        for atom in molecule.atoms:
            self.update_output("{:5}    {:11.7f} {:11.7f} {:11.7f}".format(atom.symbol, *atom.position))
            self.atoms.append(atom)
            if atom.symbol not in self.atom_show_dict.keys():
                self.atom_show_dict[atom.symbol] = True
        self.atom_list = self.unique_atoms()
        for bond in molecule.bonds:
            self.bonds.append(bond)
            symbol1 = bond.atom1.symbol
            symbol2 = bond.atom2.symbol
            key = [symbol1, symbol2]
            key = np.argsort(key)
            key = f"{symbol1} - {symbol2}"
            key_2 = f"{symbol2} - {symbol1}"
            if key not in self.bond_show_dict.keys() and key_2 not in self.bond_show_dict.keys():
                self.bond_show_dict[key] = True
        self.add_atoms_to_widget()
        self.add_bonds_to_widget()
        self.render_structure()
        self.update_output("\n" + "-"*80 + "\n\n")

    def render_structure(self):
        start = perf_counter()
        if self.display_atoms:
            self.add_atom(self.atoms)
        if self.display_bonds:
            self.add_bond(self.bonds)
        if self.surface is not None:
            self.add_surface_mesh()
        if len(self.overlay_atoms) > 0:
            if self.display_atoms:
                self.add_atom(self.overlay_atoms, opacity=self.overlay_opacity)
            if self.display_bonds:
                self.add_bond(self.overlay_bonds, opacity=self.overlay_opacity)
        self.render_critical_points()
        end = perf_counter()
        print("render time {:.3f} s".format(end - start))

    def add_atom(self, atom, opacity=None):
        if opacity is None:
            opacity = self.opacity
        if isinstance(atom, Atom):
            show = self.atom_show_dict.get(atom.symbol)
            if show:
                pv.threaded(self.plotter.add_mesh(atom.mesh, color=atom.color, lighting=True, smooth_shading=True, opacity=opacity,
                                                  metallic=self.is_metallic, roughness=self.shininess, pbr=self.pbr, diffuse=self.diffuse,
                                                  style=self.style, specular=self.specular, specular_power=self.specular_power)
                            )
        elif isinstance(atom, list):
            for a in atom:
                self.add_atom(a, opacity)
        else:
            raise ValueError('Input must be an Atom or a list of Atoms')

    def add_bond(self, bond, opacity=None):
        if opacity is None:
            opacity = self.opacity
        if isinstance(bond, Bond):
            symbol1 = bond.atom1.symbol
            symbol2 = bond.atom2.symbol
            key = f"{symbol1} - {symbol2}"
            key_2 = f"{symbol2} - {symbol1}"
            show = self.bond_show_dict.get(key)
            show_2 = self.bond_show_dict.get(key_2)
            if show or show_2:
                if not self.colored_bonds:
                    pv.threaded(self.plotter.add_mesh(bond.mesh, color=bond.color, lighting=True, smooth_shading=True, opacity=opacity,
                                                      pbr=self.pbr, style=self.style, metallic=self.is_metallic, roughness=self.shininess, 
                                                      diffuse=self.diffuse, specular=self.specular, specular_power=self.specular_power)
                            )
                else:
                    mesh_tuples = bond.colored_mesh
                    for mesh, color in mesh_tuples:
                        pv.threaded(self.plotter.add_mesh(mesh, color=color, lighting=True, smooth_shading=True, opacity=opacity,
                                                          pbr=self.pbr, style=self.style, metallic=self.is_metallic, roughness=self.shininess, 
                                                          diffuse=self.diffuse, specular=self.specular, specular_power=self.specular_power)
                                    )
        elif isinstance(bond, list):
            for b in bond:
                self.add_bond(b, opacity)
        else:
            raise ValueError('Input must be a Bond or a list of Bonds')

    def add_object(self, mesh):
        self.plotter.add_mesh(mesh, color='grey', lighting=True, smooth_shading=True)

    def update_output(self, message):
        # check if the message ends in a new line character
        if message == '':
            return
        if message[-1] != '\n':
            message += '\n'
        self.output += message
        self.textout.setText(self.output)


class AtomSelector(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Select Atom')
        self.setGeometry(100, 100, 300, 150)
        self.initUI()

    def initUI(self):
        layout = QtWidgets.QGridLayout()

        self.atom_label = QtWidgets.QLabel('Select Atom:')
        layout.addWidget(self.atom_label, 0, 0)

        self.symbol = QtWidgets.QLineEdit()
        self.symbol.setPlaceholderText('Atom Symbol')
        layout.addWidget(self.symbol, 0, 1)

        self.x_label = QtWidgets.QLabel('X:')
        layout.addWidget(self.x_label, 2, 0)
        self.x = QtWidgets.QLineEdit()
        self.x.setPlaceholderText('0.0')
        layout.addWidget(self.x, 2, 1)
        self.x.setValidator(QtGui.QDoubleValidator())

        self.y_label = QtWidgets.QLabel('Y:')
        layout.addWidget(self.y_label, 3, 0)
        self.y = QtWidgets.QLineEdit()
        self.y.setPlaceholderText('0.0')
        layout.addWidget(self.y, 3, 1)
        self.y.setValidator(QtGui.QDoubleValidator())

        self.z_label = QtWidgets.QLabel('Z:')
        layout.addWidget(self.z_label, 4, 0)
        self.z = QtWidgets.QLineEdit()
        self.z.setPlaceholderText('0.0')
        layout.addWidget(self.z, 4, 1)
        self.z.setValidator(QtGui.QDoubleValidator())

        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box, 5, 0, 1, 2)

        self.setLayout(layout)

    def get_atom(self):
        symbol = self.symbol.text()
        try:
            x = float(self.x.text())
            y = float(self.y.text())
            z = float(self.z.text())
        except ValueError:
            return None, None
        return symbol, np.array([x, y, z])


class LightSelector(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Add Lighting')
        self.setGeometry(100, 100, 300, 150)
        self.initUI()

    def initUI(self):

        layout = QtWidgets.QGridLayout()

        self.position_label = QtWidgets.QLabel('Source Position (x, y, z):')
        layout.addWidget(self.position_label, 0, 0)

        self.position_x = QtWidgets.QLineEdit()
        self.position_x.setValidator(QtGui.QDoubleValidator())
        self.position_x.setPlaceholderText('0.0')
        layout.addWidget(self.position_x, 0, 1)

        self.position_y = QtWidgets.QLineEdit()
        self.position_y.setValidator(QtGui.QDoubleValidator())
        self.position_y.setPlaceholderText('0.0')
        layout.addWidget(self.position_y, 0, 2)

        self.position_z = QtWidgets.QLineEdit()
        self.position_z.setValidator(QtGui.QDoubleValidator())
        self.position_z.setPlaceholderText('0.0')
        layout.addWidget(self.position_z, 0, 3)

        self.cone_label = QtWidgets.QLabel('Cone Angle (°)')
        layout.addWidget(self.cone_label, 1, 0)

        self.cone_angle = QtWidgets.QLineEdit()
        self.cone_angle.setValidator(QtGui.QDoubleValidator())
        self.cone_angle.setPlaceholderText('30.0')
        layout.addWidget(self.cone_angle, 1, 1, 1, 3)

        self.intensity_label = QtWidgets.QLabel('Intensity:')
        layout.addWidget(self.intensity_label, 2, 0)

        self.intensity = QtWidgets.QLineEdit()
        self.intensity.setValidator(QtGui.QDoubleValidator())
        self.intensity.setPlaceholderText('1.0')
        layout.addWidget(self.intensity, 2, 1, 1, 3)

        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box, 3, 0, 1, 4)

        self.setLayout(layout)

    def get_light(self):
        try:
            x = float(self.position_x.text())
            y = float(self.position_y.text())
            z = float(self.position_z.text())
            cone_angle = float(self.cone_angle.text())
            intensity = float(self.intensity.text())
        except ValueError:
            return None, None, None
        return np.array([x, y, z]), cone_angle, intensity


class ColorSelector(QtWidgets.QDialog):

    def __init__(self, atom_types):
        self.selected_colors = {}
        self.atom_types = atom_types
        super().__init__()
        self.setWindowTitle('Select Colors')
        self.setGeometry(100, 100, 300, 150)
        self.initUI()

    def initUI(self):
        layout = QtWidgets.QGridLayout()

        # make a list selection
        self.atom_list = QtWidgets.QListWidget()
        for atom in self.atom_types:
            self.atom_list.addItem(atom)
        layout.addWidget(self.atom_list, 0, 0)

        self.color_button = QtWidgets.QPushButton('Select Color')
        self.color_button.clicked.connect(self.select_color)
        layout.addWidget(self.color_button, 0, 1)

        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box, len(self.atom_types), 0, 1, 2)
        self.setLayout(layout)

    def select_color(self):
        color = QtWidgets.QColorDialog()
        symbol = self.atom_list.currentItem().text()
        self.selected_colors[symbol] = color.getColor()
        return

    def get_colors(self):
        return self.selected_colors


class AtomSurface(QtWidgets.QDialog):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Add Atom Surface')
        self.setGeometry(100, 100, 300, 300)
        self.initUI()

    def initUI(self):
        layout = QtWidgets.QGridLayout()

        self.symbol_label = QtWidgets.QLabel('Element:')
        layout.addWidget(self.symbol_label, 0, 0)

        self.symbol = QtWidgets.QLineEdit()
        self.symbol.setPlaceholderText('e.g. C')
        layout.addWidget(self.symbol, 0, 1)

        self.center_label = QtWidgets.QLabel('Surface Center (x, y):')
        layout.addWidget(self.center_label, 1, 0)
        self.center_x = QtWidgets.QLineEdit()
        self.center_x.setValidator(QtGui.QDoubleValidator())
        self.center_x.setPlaceholderText('0.0')
        layout.addWidget(self.center_x, 1, 1)
        self.center_y = QtWidgets.QLineEdit()
        self.center_y.setValidator(QtGui.QDoubleValidator())
        self.center_y.setPlaceholderText('0.0')
        layout.addWidget(self.center_y, 1, 2)

        self.width_label = QtWidgets.QLabel('Width (x, y):')
        layout.addWidget(self.width_label, 2, 0)
        self.width_x = QtWidgets.QLineEdit()
        self.width_x.setValidator(QtGui.QDoubleValidator())
        self.width_x.setPlaceholderText('0.0')
        layout.addWidget(self.width_x, 2, 1)
        self.width_y = QtWidgets.QLineEdit()
        self.width_y.setValidator(QtGui.QDoubleValidator())
        self.width_y.setPlaceholderText('0.0')
        layout.addWidget(self.width_y, 2, 2)

        self.z_label = QtWidgets.QLabel('Z level:')
        layout.addWidget(self.z_label, 3, 0)
        self.z = QtWidgets.QLineEdit()
        self.z.setValidator(QtGui.QDoubleValidator())
        self.z.setPlaceholderText('0.0')
        layout.addWidget(self.z, 3, 1)

        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box, 4, 0, 1, 3)

        self.setLayout(layout)

    def get_atom_surface(self):
        try:
            symbol = self.symbol.text()
            center_x = float(self.center_x.text())
            center_y = float(self.center_y.text())
            center = np.array([center_x, center_y, 0])
            width = float(self.width_x.text())
            length = float(self.width_y.text())
            z = float(self.z.text())

            return symbol, center, width, length, z
        except ValueError:
            return None, None, None, None, None


class Efield(QtWidgets.QDialog):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Electric Field')
        self.setGeometry(100, 100, 300, 300)
        self.initUI()

    def initUI(self):
        layout = QtWidgets.QGridLayout()

        field_label = QtWidgets.QLabel('Electric Field Vector')
        layout.addWidget(field_label, 0, 0, 1, 3)

        x_label = QtWidgets.QLabel('X')
        layout.addWidget(x_label, 1, 0, 1, 1)
        y_label = QtWidgets.QLabel('Y')
        layout.addWidget(y_label, 1, 1, 1, 1)
        z_label = QtWidgets.QLabel('Z')
        layout.addWidget(z_label, 1, 2, 1, 1)

        self.x = QtWidgets.QLineEdit()
        self.x.setValidator(QtGui.QDoubleValidator())
        self.x.setPlaceholderText('0.0')
        layout.addWidget(self.x, 2, 0, 1, 1)

        self.y = QtWidgets.QLineEdit()
        self.y.setValidator(QtGui.QDoubleValidator())
        self.y.setPlaceholderText('0.0')
        layout.addWidget(self.y, 2, 1, 1, 1)

        self.z = QtWidgets.QLineEdit()
        self.z.setValidator(QtGui.QDoubleValidator())
        self.z.setPlaceholderText('0.0')
        layout.addWidget(self.z, 2, 2, 1, 1)

        self.vec_checkbox = QtWidgets.QCheckBox('Display Vector')
        layout.addWidget(self.vec_checkbox, 3, 0, 1, 3)

        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box, 4, 0, 1, 3)

        self.setLayout(layout)

    def get_vector(self):
        try:
            x = float(self.x.text())
            y = float(self.y.text())
            z = float(self.z.text())
            add_vec = self.vec_checkbox.isChecked()
            return np.array([x, y, z]), add_vec
        except ValueError:
            return None, None

class BondRadiusSelector(QtWidgets.QDialog):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Set Bond Radius')
        self.setGeometry(100, 100, 300, 100)
        self.initUI()

    def initUI(self):
        layout = QtWidgets.QVBoxLayout()
        label = QtWidgets.QLabel("Set the Bond Radius (default = 0.08)")
        layout.addWidget(label)

        self.scaler_input = QtWidgets.QLineEdit()
        self.scaler_input.setValidator(QtGui.QDoubleValidator())
        self.scaler_input.setPlaceholderText('1.5')
        layout.addWidget(self.scaler_input)

        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

        self.setLayout(layout)

    def get_scaler(self):
        try:
            scaler = float(self.scaler_input.text())
            return scaler
        except ValueError:
            return 1.5

class BondFindScalerWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Set Bond Scaler Radius')
        self.setGeometry(100, 100, 300, 100)
        self.initUI()

    def initUI(self):
        layout = QtWidgets.QVBoxLayout()
        label = QtWidgets.QLabel("Set the Scaler to the Bond Finder (default = 1.12)")
        layout.addWidget(label)

        self.scaler_input = QtWidgets.QLineEdit()
        self.scaler_input.setValidator(QtGui.QDoubleValidator())
        self.scaler_input.setPlaceholderText('1.12')
        layout.addWidget(self.scaler_input)

        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

        self.setLayout(layout)

    def get_scaler(self):
        try:
            scaler = float(self.scaler_input.text())
            return scaler
        except ValueError:
            return 1.12


class AtomRadiusSelector(QtWidgets.QDialog):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Set Atom Radius Scaler')
        self.setGeometry(100, 100, 300, 100)
        self.initUI()

    def initUI(self):
        layout = QtWidgets.QVBoxLayout()
        label = QtWidgets.QLabel("Set the Atom Radius Scaler (default = 1.5)")
        layout.addWidget(label)

        self.scaler_input = QtWidgets.QLineEdit()
        self.scaler_input.setValidator(QtGui.QDoubleValidator())
        self.scaler_input.setPlaceholderText('1.5')
        layout.addWidget(self.scaler_input)

        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

        self.setLayout(layout)

    def get_scaler(self):
        try:
            scaler = float(self.scaler_input.text())
            return scaler
        except ValueError:
            return 1.5


class RefFrameWindow(QtWidgets.QDialog):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Change Reference Frame')
        self.setGeometry(100, 100, 300, 100)
        self.initUI()

    def initUI(self):

        layout = QtWidgets.QGridLayout()

        label = QtWidgets.QLabel("New Reference Frame")

        self.x_combo = QtWidgets.QComboBox()
        self.x_combo.addItems(["x", "y", "z"])
        self.y_combo = QtWidgets.QComboBox()
        self.y_combo.addItems(["x", "y", "z"])
        self.z_combo = QtWidgets.QComboBox()
        self.z_combo.addItems(["x", "y", "z"])

        layout.addWidget(label, 0, 1)
        layout.addWidget(self.x_combo, 1, 0)
        layout.addWidget(self.y_combo, 1, 1)
        layout.addWidget(self.z_combo, 1, 2)

        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Yes | QtWidgets.QDialogButtonBox.No)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box, 2, 1)

        self.setLayout(layout)

    def get_rotation(self):

        x = self.x_combo.currentText()
        y = self.y_combo.currentText()
        z = self.z_combo.currentText()

        rot_set = set([x, y, z])
        if len(rot_set) != 3:
            return np.eye(3)


        def get_vec(axis):
            ref = np.eye(3)
            match axis:
                case 'x':
                    return ref[:, 0]
                case 'y': 
                    return ref[:, 1]
                case _:
                    return ref[:, 2]

        x = get_vec(x)
        y = get_vec(y)
        z = get_vec(z)

        return np.hstack((x.reshape(-1, 1),
                          y.reshape(-1, 1),
                          z.reshape(-1, 1)))



class ExitSave(QtWidgets.QDialog):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Save Log')
        self.setGeometry(100, 100, 300, 100)
        self.initUI()

    def initUI(self):
        layout = QtWidgets.QVBoxLayout()

        label = QtWidgets.QLabel("Do you want to save the MolVis output before exiting?")
        layout.addWidget(label)

        # yes no buttonbox
        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Yes | QtWidgets.QDialogButtonBox.No)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

        self.setLayout(layout)


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(os.path.join(os.path.dirname(__file__), 'assets/icon.png')))
    app.setApplicationName('MolVis')
    app.setOrganizationName('MolVis')
    app.setDesktopFileName('MolVis')
    window = QtDisplay()
    if len(sys.argv) > 1:
        if os.path.exists(sys.argv[1]):
            window.filename = sys.argv[1]
            if window.filename.endswith(".xyz"):
                window.load_molecule()
            else:
                window.load_crystal()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
