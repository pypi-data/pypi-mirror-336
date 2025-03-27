import numpy as np
import h5py as h5
import pyvista as pv
from ase.data import chemical_symbols
import scipy.constants as constants
from time import perf_counter

BOHR2METER = constants.physical_constants['Bohr radius'][0]
BOHR2ANGSTROM = BOHR2METER * 1e10

class Orbital():

    def __init__(self, filename):
        self.filename = filename
        if not self.filename.endswith('rasscf.h5'):
            raise ValueError('File must be a RASSCF output file')
        self.exctract
        self.MOs = {}

    @property
    def exctract(self):
        with h5.File('TmNSiiPr_cextr.rasscf.h5', 'r') as f:
            self.primitives = f['/PRIMITIVES'][:]
            self.primitive_ids = f['/PRIMITIVE_IDS'][:]
            self.basis_ids = f['/BASIS_FUNCTION_IDS'][:]
            self.center_coords = f['/CENTER_COORDINATES'][:]
            self.center_atnums = f['/CENTER_ATNUMS'][:]
            self.mo_vectors = f['/MO_VECTORS'][:]
            self.mo_energies = f['/MO_ENERGIES'][:]
            self.types = f['/MO_TYPEINDICES'][:]
            print(f.keys())

        self.mo_vectors = self.mo_vectors.reshape(self.mo_energies.shape[0], -1)


    @staticmethod
    def gaussian_primitive(x, y, z, alpha, center, l, m, n):
        """Evaluate a Gaussian primitive on a grid."""
        x_term = (x - center[0])**l if l > 0 else 1.0
        y_term = (y - center[1])**m if m > 0 else 1.0
        z_term = (z - center[2])**n if n > 0 else 1.0
        r2 = (x - center[0])**2 + (y - center[1])**2 + (z - center[2])**2
        return x_term * y_term * z_term * np.exp(-alpha * r2)
    
    def grid(self, grid_points):
        max_x, min_x = 50, -50
        max_y, min_y = 50, -50
        max_z, min_z = 50, -50
        x = np.linspace(min_x, max_x, grid_points)
        y = np.linspace(min_y, max_y, grid_points)
        z = np.linspace(min_z, max_z, grid_points)
        X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
        return X, Y, Z


    def compute_mos(self, grid_points):
        self.grid_points = grid_points
        X, Y, Z = self.grid(grid_points)
        start = perf_counter()
        for j in range(len(self.mo_vectors)):
            mo_coeffs = self.mo_vectors[:, j]
            orbital = np.zeros_like(X)
            for i, (center_idx, l, m, n) in enumerate(self.basis_ids):
                center = self.center_coords[center_idx - 1]
                alpha, coeff = self.primitives[i]
                orbital += mo_coeffs[i] * coeff * self.gaussian_primitive(X, Y, Z, alpha, center, l, m, n)

            orbital /= np.max(np.abs(orbital))
            self.MOs[j] = {'X': X,
                           'Y': Y,
                           'Z': Z,
                           'energy': self.mo_energies[j],
                           'type': self.types[j],
                           'orbital': orbital}
            # print('orbital {} of {} computed'.format(j, len(self.mo_vectors)))
        end = perf_counter()
        print('Computation of molecular orbitals took {:.2f} s'.format(end - start))

    def mo_mesh(self, mo_idx):
        X = self.MOs[mo_idx]['X']
        Y = self.MOs[mo_idx]['Y']
        Z = self.MOs[mo_idx]['Z']
        orbital = self.MOs[mo_idx]['orbital']

        X_flat = X.ravel(order='F') * BOHR2ANGSTROM
        Y_flat = Y.ravel(order='F') * BOHR2ANGSTROM
        Z_flat = Z.ravel(order='F') * BOHR2ANGSTROM

        # normalise
        X_flat /= np.max(np.abs(X_flat))
        Y_flat /= np.max(np.abs(Y_flat))
        Z_flat /= np.max(np.abs(Z_flat))
        X_flat *= 5
        Y_flat *= 5
        Z_flat *= 5

        mesh = pv.StructuredGrid()
        mesh.points = np.c_[X_flat, Y_flat, Z_flat]
        mesh.dimensions = [self.grid_points, self.grid_points, self.grid_points]

        mesh.point_data['orbital'] = orbital.ravel(order='F')

        return mesh

    @property
    def structure(self):
        symbols = list(map(lambda x: chemical_symbols[x], self.center_atnums))
        center_coords = self.center_coords * BOHR2ANGSTROM
        return center_coords, symbols
