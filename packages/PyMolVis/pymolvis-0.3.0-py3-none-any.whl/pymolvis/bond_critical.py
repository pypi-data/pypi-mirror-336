import numpy as np
import re
import pyvista as pv
import seaborn as sns

class Parser:

    headerREGEX = re.compile(r'^\s*-+\s*CP\s*(?P<index>\d+),\s*Type\s*(?P<type>\([+-]?\d+,[+-]?\d+\))\s*-+\s*$')
    coordREGEX = re.compile(r'^\s*Position\s*\(Angstrom\):\s*(?P<x>[+-]?\d+\.\d+)\s*(?P<y>[+-]?\d+\.\d+)\s*(?P<z>[+-]?\d+\.\d+)\s*$')
    densityREGEX = re.compile(r'^\s*Density\s*of\s*all\s*electrons:\s*(?P<density>[+-]?\d+\.\d+E[+-]?\d+)\s*$')

    def __init__(self, filename):
        self.filename = filename
        self.indices = np.array([])
        self.types = np.array([])
        self.coords = np.array([])
        self.densities = np.array([])
        self.parse_bond_critical_points
    
    @property
    def lines(self):
        with open(self.filename) as f:
            return f.readlines()


    @property
    def parse_bond_critical_points(self):

        for line in self.lines:
            header_match = self.headerREGEX.match(line)
            coord_match = self.coordREGEX.match(line)
            density_match = self.densityREGEX.match(line)

            if header_match:
                index = int(header_match.group('index'))
                type = str(header_match.group('type'))
                self.indices = np.append(self.indices, '{:.0f}'.format(index))
                self.types = np.append(self.types, type)

            if coord_match:
                x = float(coord_match.group('x'))
                y = float(coord_match.group('y'))
                z = float(coord_match.group('z'))
                coord = np.array([x, y, z]).reshape(1, 3)
                if len(self.coords) == 0:
                    self.coords = coord
                else:
                    self.coords = np.vstack((self.coords, coord))

            if density_match:
                density = float(density_match.group('density'))
                self.densities = np.append(self.densities, density)


class BondCriticalPoints(Parser):

    def __init__(self, filename, radius=0.15, resolution=20, color='type'):
        super().__init__(filename)
        self.color_types = {'type': self.get_colors_type, 'density': self.get_colors_density}
        self.color_type = color
        self.parse_bond_critical_points
        self.radius = radius
        self.resolution = resolution
        self.critcal_points = []
        self.get_colours
        self.make_critical_points

    @property
    def get_colours(self):
        self.color_types[self.color_type]()

    def get_colors_type(self):
        unique_types = np.unique(self.types)
        colours = sns.color_palette('hsv', len(unique_types))
        self.dict_colours = dict(zip(unique_types, colours))
        self.colors = list(map(lambda x: self.dict_colours[x], self.types))

    def get_colors_density(self):
        colours = sns.color_palette('viridis', as_cmap=True)
        self.colors = colours(self.densities)
        self.dict_colours = {':.2f'.format(density): color for density, color in zip(self.densities, self.colors)}


    @property
    def make_critical_points(self):
        for coord, color, _type in zip(self.coords, self.colors, self.types):
            cp = CriticalPoint(coord, color, _type, self.radius, self.resolution)
            self.critcal_points.append(cp)


class CriticalPoint:

    def __init__(self, coordinate, color, _type, radius, resolution):
        self.coordinate = coordinate
        self.radius = radius
        self.resolution = resolution
        self.color = color
        self._type = _type


    @property
    def mesh(self):
        return pv.Sphere(
        radius=self.radius,
        center=self.coordinate,
        theta_resolution=self.resolution,
        phi_resolution=self.resolution,
        )

