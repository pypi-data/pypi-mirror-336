import numpy as np
from spin_phonon_suite.vibrations import construct_atomic_basis
from .molecule import Molecule


def electric_distort(atoms, hess, grad_mu, field_vector, resolution, opacity, scaler, bond_radius):
    coords = list(map(lambda x: x.position, atoms))
    symbols = list(map(lambda x: x.symbol, atoms))

    U = construct_atomic_basis(int(grad_mu.shape[0]/3), gaussian_fchk=True,
                               coords=coords)  # units in angstrom
    hess = U.T @ hess @ U

    E = np.array(field_vector)
    grad_mu_E = grad_mu @ E
    r = np.linalg.solve(-1 * hess, U.T @ grad_mu_E)
    r = (U @ r) * 1e10

    coords = coords + r.reshape(-1, 3)

    molecule = Molecule(symbols, coords, resolution, scaler, bond_radius)
    molecule.__setattr__('opacity', opacity)

    return molecule
