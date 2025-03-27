import numpy as np
import pyscf

from pyscf import dft

def run_pyscf_dft(atoms, params):

    mol_hf = build_dft_mol(
            atoms,
            params['basis'],
            params['ecp'],
            params['symmetry'],
            params['charge'],
            params['spin'],
            )

    mf = dft.RKS(mol_hf)
    mf.xc = params['xc']
    mf.verbose = 0
    mf = mf.newton()
    mf.kernel()
    return mf


def build_dft_mol(atoms, basis, ecp, symmetry, charge, spin):

    atom_list = []
    for atom in atoms:
        atom_list.append("{} {:11.7f} {:11.7f} {:11.7f}".format(atom.symbol, *atom.position))
    molecule_str = "; ".join(atom_list)

    mol = pyscf.gto.Mole()
    mol.atom = molecule_str
    mol.basis = basis
    calc_ecp = {}
    for k, v in ecp.items():
        if v is not None:
            calc_ecp[k] = v
    if len(calc_ecp) > 0:
        mol.ecp = calc_ecp
    mol.charge = charge
    mol.spin = spin

    mol.symmetry = symmetry
    return mol


def format_output(mf, time_data):
    out = ''

    out += '{:^80}\n'.format("Molvis Ab Initio - PySCF")
    out += '{:^80}\n\n'.format("------------------------")

    mol = mf.mol

    out += 'Molecule\n'
    out += '--------\n'

    for i in range(mol.natm):
        out += 'Atom {} {} {:11.7f} {:11.7f} {:11.7f}\n'.format(
            i+1, mol.atom_symbol(i), *mol.atom_coord(i))

    
    out += '\n'
    out += 'Number of electrons: {}\n'.format(mol.nelectron)
    out += 'Charge: {}\n'.format(mol.charge)
    out += 'Spin: {}\n'.format(mol.spin)
    out += 'Symmetry: {}\n\n'.format(mol.symmetry)

    out += 'Total Energy: {:11.7f} Hartree\n'.format(mf.e_tot)
    out += 'Molecular Orbital Energies\n'
    out += '--------------------------\n'
    out += 'Orbital  Energy (Hartree)\n'
    out += '-------  ----------------\n'
    orb_energies = mf.mo_energy
    for i, en in enumerate(orb_energies):
        out += '{:7d}  {:11.7f}\n'.format(i, en)

    out += '\n'

    out += 'Molecular Orbital Coefficients\n'
    out += '-----------------------------\n'
    out += 'Orbital  Atom  Coefficient\n'
    out += '-------  ----  -----------\n'
    orb_coeffs = mf.mo_coeff
    for i in range(orb_coeffs.shape[1]):
        for j in range(orb_coeffs.shape[0]):
            out += '{:7d}  {:4d}  {:11.7f}\n'.format(j, i, orb_coeffs[j, i])

    orb_occ = mf.mo_occ

    out += '\n'

    out += 'Molecular Orbital Occupancies\n'
    out += '-----------------------------\n'
    out += 'Orbital  Occupancy\n'
    out += '-------  ---------\n'
    for i, occ in enumerate(orb_occ):
        out += '{:7d}  {:11.7f}\n'.format(i, occ)

    out += '\n'

    out += 'DFT Grid\n'
    out += '--------\n'
    out += 'Number of Grid Points: {}\n'.format(mf.grids.coords.shape[0])
    out += 'Grid Symmetry: {}\n'.format(mf.grids.symmetry)
    out += '\n'

    out += '\n'

    mulliken_pop = mf.mulliken_pop(verbose=0)
    out += 'Mulliken Population Analysis\n'
    out += '----------------------------\n'

    populations, charges = mulliken_pop

    out += '-- Mulliken Population --\n'
    chg = np.zeros(mol.natm)
    for i, s in enumerate(mol.ao_labels(fmt=None)):
        out += '{:5} {:4} {:4} {:11.7f}\n'.format(s[0], s[1], "".join(s[2:]),  populations[i])
    out += '\n'
    out += '-- Mulliken Charges --\n'
    for idx, chg in enumerate(charges):
        sym = mol.atom_symbol(idx)
        out += '{:3} {:11.7f}\n'.format(sym, chg)

    out += '\n'

    dip_moment = mf.dip_moment()

    out += 'Dipole Moment (Debye)\n'
    out += '---------------------\n'
    out += '{:11.7f} {:11.7f} {:11.7f}\n'.format(*dip_moment)

    out += '\n'

    quadrupole_moment = mf.quad_moment()

    out += 'Quadrupole Moment (Debye Ang)\n'
    out += '------------------------------\n'

    for i in range(3):
        out += '{:11.7f} {:11.7f} {:11.7f}\n'.format(*quadrupole_moment[i])

    out += '\n'

    out += 'Timing Information\n'
    out += '------------------\n'
    out += 'Total Time: {:11.7f} s\n'.format(time_data)

    out += '\n'
    out += 'End of Molvis Ab Initio Output\n'
    out += '------------------------------\n'
    out += '\n'

    return out

