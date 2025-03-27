import numpy as np
import pyvista as pv
from .atom import Atom
from .bond import Bond
from vasp_suite.graphs import Node, MolGraph
import xyz_py
import multiprocessing as mp

class Molecule:

    def __init__(self, symbols, coords, resolution, scaler, bond_radius, radius_scaler=1.12):
        self.symbols = symbols
        self.coords = coords
        self.resolution = resolution
        self.scaler = scaler
        self.atoms = list(map(Atom, self.symbols, self.coords, [self.resolution] * len(self.symbols), [self.scaler] * len(self.symbols)))
        self.radius_scaler = radius_scaler

        self.bond_radius = bond_radius

    @classmethod
    def from_xyz(cls, filename, resolution, scaler, bond_radius):
        symbols, coords = xyz_py.load_xyz(filename)
        return cls(symbols, coords, resolution, scaler, bond_radius)

    @property
    def graph(self):
        graph = MolGraph(scaler=self.radius_scaler)
        for idx, atom in enumerate(self.atoms):
            node = Node(atom.position, atom.symbol, atom.radius, idx, atom.mass, scaler=self.radius_scaler)
            node.__setattr__('atom', atom)
            graph.add_node(node)
        graph.construct_graph
        return graph

    @property
    def Axes(self):
        coords = np.array(self.coords)
        masses = list(map(lambda x: x.mass, self.atoms))
        inertia_tensor = coords.T @ np.diag(masses) @ coords
        eigvals, eigvecs = np.linalg.eig(inertia_tensor)
        return eigvals, eigvecs

    @property
    def axes_mesh(self):
        origin = [-10, -10, -10]
        axes = self.Axes[1]
        return pv.Arrow(start=origin, direction=axes[:, 0], tip_length=0.1, tip_radius=0.05) + \
                pv.Arrow(start=origin, direction=axes[:, 1], tip_length=0.1, tip_radius=0.05) + \
                pv.Arrow(start=origin, direction=axes[:, 2], tip_length=0.1, tip_radius=0.05)

    @property
    def align(self):
        eigvals, eigvecs = self.Axes
        idx = np.argsort(eigvals)
        self.coords = self.coords @ eigvecs[:, idx]
        for idx, atom in enumerate(self.atoms):
            atom.position = self.coords[idx]

    def rotate(self, R):
        self.coords = self.coords @ R
        for idx, atom in enumerate(self.atoms):
            atom.position = self.coords[idx]

    def filter_bonds(self, bonds):
        """
        Fileter out repeated bonds
        """
        seen = []
        for bond in bonds:
            if bond not in seen:
                seen.append(bond)
                yield bond

    @property
    def bonds(self):
        graph = self.graph
        edges = graph.edges

        bonds = self.create_bonds(edges)
        bonds = list(self.filter_bonds(bonds))
        return bonds

    def process_edge(self, args):
        key, values = args
        bonds = []
        if len(values) == 0:
            return bonds
        elif len(values) == 1:
            atom1 = key.atom
            atom2 = values[0].atom
            bonds.append(Bond(atom1, atom2, self.bond_radius, resolution=self.resolution))
        else:
            for value in values:
                atom1 = key.atom
                atom2 = value.atom
                bonds.append(Bond(atom1, atom2, self.bond_radius, resolution=self.resolution))
        return bonds

    def create_bonds(self, edges):
        with mp.Pool() as pool:
            args = [(key, values) for key, values in edges.items()]
            results = pool.map(self.process_edge, args)
        # Flatten the list of lists
        bonds = [bond for bond_list in results for bond in bond_list]
        return bonds

    @property
    def bounding_box(self):
        coords = np.array(self.coords)
        min_coords = np.min(coords, axis=0) * 1.2
        max_coords = np.max(coords, axis=0) * 1.2
        return min_coords, max_coords
