import pyvista as pv
import numpy as np
from .atom import Atom
from time import perf_counter
import functools


class Bond:

    def __init__(self, atom1, atom2, radius, resolution=200):
        self.atom1 = atom1
        self.atom2 = atom2
        self.resolution = int(resolution / 2)
        self.radius = radius
        self.center
        self.centers
        self.direction
        self.height
        self.heights
        self.ratios

    @property
    def color(self):
        return 'grey'

    @functools.cached_property
    def center(self):
        return (self.atom1.position + self.atom2.position) / 2

    @functools.cached_property
    def direction(self):
        return self.atom2.position - self.atom1.position

    @functools.cached_property
    def height(self):
        return np.linalg.norm(self.direction)

    @functools.cached_property
    def ratios(self):
        ratio12 = self.atom1.radius / (self.atom1.radius + self.atom2.radius)
        ratio21 = self.atom2.radius / (self.atom1.radius + self.atom2.radius)
        return ratio12, ratio21

    @functools.cached_property
    def centers(self):
        # find the point that is (ratio12 / 2) away from atom1
        ratio12, ratio21 = self.ratios
        center1 = self.atom1.position + (ratio12 / 2) * self.direction
        center2 = self.atom2.position - (ratio21 / 2) * self.direction
        return center1, center2

    @functools.cached_property
    def heights(self):
        ratio12, ratio21 = self.ratios
        height1 = self.height * ratio12
        height2 = self.height * ratio21
        return height1, height2

    @property
    def colored_mesh(self):
        color1 = self.atom1.color
        color2 = self.atom2.color

        center1, center2 = self.centers
        height1, height2 = self.heights

        direction = self.direction

        mesh1 = pv.Capsule(
                center=center1,
                direction=direction,
                radius=self.radius,
                cylinder_length=height1,
                resolution=self.resolution,
                )
        mesh2 = pv.Capsule(
                center=center2,
                direction=direction,
                radius=self.radius,
                cylinder_length=height2,
                resolution=self.resolution,
                )
        return (mesh1, color1), (mesh2, color2)

    @functools.cached_property
    def mesh(self):
        """
        returns one cylinder mesh for the bond
        """
        bond =  pv.Capsule(
            center=self.center,
            direction=self.direction,
            radius=self.radius,
            cylinder_length=self.height,
            resolution=self.resolution
        )
        return bond

    def __eq__(self, other):
        return np.allclose(self.center, other.center)
