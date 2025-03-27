import numpy as np
import pyvista as pv
from .atom import Atom


class Surface:

    def __init__(self, symbol, center, width, length, z_level, packing, resolution):
        self.symbol = symbol
        self.center = center
        self.width = width
        self.z_level = z_level
        self.length = length
        self.packing = packing
        self.resolution = resolution

        self.unit_position = np.array([-self.width/2, -self.length/2, self.z_level])
        self.unit = None

    available_packings = ['fcc', 'bcc']

    def check_packing(self):
        if self.packing not in self.available_packings:
            raise ValueError(f"Invalid packing: {self.packing}")

    @property
    def generate_unit(self):
        self.make_unit()

    def make_unit(self):
        # initial atom
        atom = Atom(self.symbol, self.unit_position, resolution=self.resolution)
        atom_2 = Atom(self.symbol, self.unit_position + np.array([(atom.radius * np.sqrt(2))/2, (atom.radius * np.sqrt(2))/2, (-atom.radius * np.sqrt(2))/2]), resolution=self.resolution)
        self.color = atom.color
        self.unit = atom.mesh.merge(atom_2.mesh)
        self.unit_width = atom.radius * np.sqrt(2)
        self.unit_length = atom.radius * np.sqrt(2)

    def create_surface(self):
        if self.unit is None:
            self.generate_unit

        units_in_width = int(self.width / self.unit_width)
        units_in_length = int(self.length / self.unit_length)

        print("adding {} units".format(units_in_width * units_in_length))

        # tile the width
        self.surface = self.unit
        for i in range(units_in_width):
            for j in range(units_in_length):
                # for atom in self.unit:
                    # position = atom.position + np.array([i * self.unit_width, j * self.unit_length, 0])
                    # self.surface.append(Atom(self.symbol, position, resolution=self.resolution))
                self.surface = self.surface.merge(self.unit.copy().translate([i * self.unit_width, j * self.unit_length, 0]))

        print(type(self.surface))

        print("surface created")
        self.surface
