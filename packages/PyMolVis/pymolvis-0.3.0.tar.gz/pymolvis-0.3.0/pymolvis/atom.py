import pyvista as pv
import mendeleev as md


class Atom:

    def __init__(self, symbol, position, resolution, radius_scale=1.5):
        self.symbol = symbol
        self.position = position
        self.resolution = resolution
        self.radius_scale = radius_scale
        self.color = self.get_color()

    @property
    def element(self):
        return md.element(self.symbol)

    @property
    def radius(self):
        return self.element.covalent_radius * 1e-2

    @property
    def plotting_radius(self):
        return self.radius / self.radius_scale

    @property
    def mass(self):
        return self.element.atomic_weight

    def get_color(self):
        return self.element.cpk_color

    @property
    def mesh(self):
        return pv.Sphere(
                radius=self.plotting_radius,
                center=self.position,
                theta_resolution=self.resolution,
                phi_resolution=self.resolution,
                )
