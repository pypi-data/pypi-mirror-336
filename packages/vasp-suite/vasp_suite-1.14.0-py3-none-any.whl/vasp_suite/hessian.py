import numpy as np

from .parser import ParseOUTCAR

THZ_TO_INV_CM = 33.35641


def parse_frequencies(outcar: ParseOUTCAR):
    freqs = np.array(list(outcar.hessian_eigenvalues))
    if len(freqs) == 0:
        raise ValueError("No eigenvalues found in OUTCAR \n \
                Run VASP with the following tags: \n \
                IBRION=5, NSW=1 \n\n \
                NSW=1 is important to calculate the normal modes in older versions of VASP \n \
                It is suggested to increase the convergence tolerance EDIFFG to 1E-6")
    return freqs * THZ_TO_INV_CM


def parse_displacements(outcar: ParseOUTCAR):
    displacements = np.array(list(outcar.hessian_eigenvectors))
    disp_norms = list(map(np.linalg.norm, displacements))
    if not all(np.isclose(1., disp_norms)):
        raise ValueError("Displacements are not normalized")
    return displacements
