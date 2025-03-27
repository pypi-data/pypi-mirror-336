import numpy as np
import mendeleev as md
from vasp_suite.structure import Structure
from vasp_suite.graphs import Node, MolGraph
import multiprocessing as mp
from time import perf_counter

from .atom import Atom
from .bond import Bond


class Crystal():

    def __init__(self, file, resolution, scaler, bond_radius):
        self.resolution = resolution
        self.scaler = scaler
        self.bond_radius = bond_radius
        if file.endswith('.cif'):
            self.structure = Structure.from_cif(file)
        else:
            try:
                self.structure = Structure.from_poscar(file)
            except NotImplementedError:
                raise ValueError('Invalid file format')

    @property
    def atoms(self):
        symbols = self.structure.atom_list
        coords = self.structure.cart_coords
        return list(map(Atom, symbols, coords, [self.resolution]*len(symbols), [self.scaler]*len(symbols)))

    @property
    def graph(self):
        graph = MolGraph()
        for idx, atom in enumerate(self.atoms):
            node = Node(atom.position, atom.symbol, atom.radius, idx, atom.mass, scaler=1.12)
            node.__setattr__('atom', atom)
            graph.add_node(node)
        graph.construct_graph
        return graph

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

