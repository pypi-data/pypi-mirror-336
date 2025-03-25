"""
Convergence testing for vasp calculations
"""
import os
import shutil
import csv
import numpy as np

from .structure import Structure
from .parser import ParseOUTCAR, ParseOSZICAR
from .core import generate_kpoints

import matplotlib.pyplot as plt


def make_dirs(combinations):
    """
    Make directories for each combination of parameters
    and copy the input files into them
    """
    cwd = os.getcwd()

    for c in combinations:
        dir = '{}{}{}_{}'.format(c[0][0], c[0][1], c[0][2], c[1])
        if not os.path.exists(dir):
            os.makedirs(dir)
        shutil.copy(os.path.join(cwd, 'INCAR'), os.path.join(cwd, dir))
        shutil.copy(os.path.join(cwd, 'POTCAR'), os.path.join(cwd, dir))
        shutil.copy(os.path.join(cwd, 'POSCAR'), os.path.join(cwd, dir))
        os.chdir(dir)
        generate_kpoints(c[0])
        with open('INCAR', 'a') as f:
            f.write('ENCUT = {}\n'.format(c[1]))
        os.chdir(cwd)

    with open('convergence.txt', 'w') as f:
        for i in combinations:
            f.write('{}{}{}_{}\n'.format(i[0][0], i[0][1], i[0][2], i[1]))


def get_combinations(filename, max_encut, min_encut, kpoints=None):
    """
    Convergence test calculation set up
    """

    if os.path.splitext(filename)[1] == ".cif":
        filename = 'POSCAR'

    poscar = Structure.from_poscar(filename)

    # get the kpoint mesh and densities
    if kpoints:
        mesh, density = poscar.generate_mesh(kpoints)
    else:
        mesh, density = poscar.calculate_mesh()

    encut_values = poscar.calculate_encut(max_encut, min_encut)

    combinations = [[x, y, z] for x, z in zip(mesh[:5], density[:5])
                    for y in encut_values]

    return combinations


def extract_data(combinations):
    """
    extracting data from the calculations
    for post processing
    """

    with open('conv.csv', 'w') as output_writer:
        output_writer_csv = csv.writer(output_writer, delimiter=',')

        output_writer_csv.writerow(
                ["Cutoff [eV]", "nk_1", "nk_2", "nk_3", "nk,red",
                 r"\rho_k [A^-3]", "E_0 [eV]", "p_ext [kbar]", "#SCF", "t [s]"]
                )

    for c in combinations:
        dir = '{}{}{}_{}'.format(c[0][0], c[0][1], c[0][2], c[1])
        outcar = ParseOUTCAR(os.path.join(dir, 'OUTCAR'))
        oszicar = ParseOSZICAR(os.path.join(dir, 'OSZICAR'))

        energy = list(oszicar.energy)
        ext_pressure = list(outcar.external_pressure)
        num_scf = list(oszicar.electronic_steps)
        time = list(outcar.elapsed_time)
        n_k_red = np.prod(c[0])

        with open('conv.csv', 'a') as output_writer:
            output_writer_csv = csv.writer(output_writer, delimiter=',')
            output_writer_csv.writerow(
                    [c[1], c[0][0], c[0][1], c[0][2], str(n_k_red), c[2][0],
                     str(energy[0]), str(ext_pressure[0]),
                     str(num_scf[0]), str(time[0])]
                    )


def kpoint_plot(data, num_atoms, plot_gradient=False):
    unique_encut = np.unique(data[r"Cutoff [eV]"])
    height = int(np.ceil(len(unique_encut) / 2))
    width = 2

    fig, axs = plt.subplots(height, width, figsize=(10, height * 5))

    for i, encut in enumerate(unique_encut):
        encut_data = data[data[r"Cutoff [eV]"] == encut]
        energy_per_atom = encut_data["E_0 [eV]"] / num_atoms
        gradient = np.gradient(energy_per_atom, encut_data[r"\rho_k [A^-3]"])

        axs[int(i // width), int(i % width)].plot(
                encut_data[r"\rho_k [A^-3]"],
                energy_per_atom,
                "k",
                label=r"ENCUT = {}".format(encut),
                marker="s"
                )
        axs[int(i // width), int(i % width)].set_xlabel(r"$\rho_k$ (Å$^{-3}$)")
        axs[int(i // width), int(i % width)].set_ylabel("Energy per atom (eV)")
        axs[int(i // width), int(i % width)].set_title("ENCUT = {}".format(encut))

        if plot_gradient:
            grad_ax = axs[int(i // width), int(i % width)].twinx()
            grad_ax.plot(
                    encut_data[r"\rho_k [A^-3]"],
                    gradient,
                    "--r",
                    marker="s"
                    )
            grad_ax.set_ylabel("Gradient (eV/Å$^{-3}$)")
            grad_ax.yaxis.label.set_color("red")

    fig.tight_layout()
    fig.savefig("kpoint_convergence.pdf", dpi=300)


def cutoff_plot(data, num_atoms, plot_gradient=False):
    unique_rho = np.unique(data[r"\rho_k [A^-3]"])
    height = int(np.ceil(len(unique_rho) / 2))
    width = 2

    fig, axs = plt.subplots(height, width, figsize=(10, height * 5))

    for i, rho in enumerate(unique_rho):
        rho_data = data[data[r"\rho_k [A^-3]"] == rho]
        energy_per_atom = rho_data["E_0 [eV]"] / num_atoms
        gradient = np.gradient(energy_per_atom, rho_data[r"Cutoff [eV]"])
        double_gradient = np.gradient(gradient, rho_data[r"Cutoff [eV]"])

        axs[int(i // width), int(i % width)].plot(
                rho_data["Cutoff [eV]"],
                energy_per_atom,
                "k",
                label=r"$\rho_k$ = {}".format(rho),
                marker="s"
                )
        axs[int(i // width), int(i % width)].set_xlabel("ENCUT (eV)")
        axs[int(i // width), int(i % width)].set_ylabel("Energy per atom (eV)")
        axs[int(i // width), int(i % width)].set_title(r"$\rho_k$ = {}".format(rho))

        if plot_gradient:
            grad_ax = axs[int(i // width), int(i % width)].twinx()
            grad_ax.plot(
                    rho_data["Cutoff [eV]"],
                    gradient,
                    "--r",
                    label=r"Gradient",
                    marker="o"
                    )
            grad_ax.set_ylabel("Gradient")
            grad_ax.yaxis.label.set_color("red")

            double_grad_ax = axs[int(i // width), int(i % width)].twinx()
            double_grad_ax.plot(
                    rho_data["Cutoff [eV]"],
                    double_gradient,
                    "--b",
                    label=r"Double derivative",
                    marker="o"
                    )
            double_grad_ax.set_ylabel("Double derivative")


    fig.tight_layout()
    fig.savefig("encut_convergence.pdf", dpi=300)
