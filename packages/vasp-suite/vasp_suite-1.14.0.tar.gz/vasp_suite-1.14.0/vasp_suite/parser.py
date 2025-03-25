"""
A module for parsing vasp output files.
"""

import os
import re

from .structure import Structure


class Parser(Structure):
    """
    Parent class for all parsers
    """

    def __init__(self, output_file, poscar_file='POSCAR'):
        """
        Initializes the parser object.
        """
        # Initialize the structure object
        if not os.path.exists(output_file):
            raise ValueError("File not found: {}".format(output_file))
        if not (os.path.exists(poscar_file)):
            raise IOError("File not found: {}".format(poscar_file))
        poscar = Structure.from_poscar(poscar_file)
        for atrr in poscar.__dict__:
            setattr(self, atrr, getattr(poscar, atrr))
        self.output_file = output_file
        self.poscar_file = poscar_file

    @property
    def read_lines(self):
        """
        Reads the lines from the output file
        """
        with open(self.output_file, 'r') as f:
            return f.readlines()


class ParseOUTCAR(Parser):
    """
    Parses the OUTCAR file
    """

    # Patterns

    external_pressureREGEX = re.compile(
            r'^\s+external\s+pressure\s+=\s+(?P<pressure>[+-]?\d+\.\d+)\s+'
            )

    elapsed_timeREGEX = re.compile(
            r'^\s+Elapsed\s+time\s+\(sec\)\:\s+(?P<time>\d+\.\d+)\s+'
            )

    eigenval_hessianREGEX = re.compile(
            r'^\s+\d+\s*f\s*=\s*(?P<eigenval>\d+\.\d+)\s+THz\s+'
            )

    eigenval_hessianREGEX2 = re.compile(
            r'^\s+\d+\s*f/i\s*=\s*(?P<eigenval>\d+\.\d+)\s+THz\s+'
            )

    def __init__(self, output_file='OUTCAR', poscar_file='POSCAR'):
        """
        Initializes the OUTCAR parser object.
        """
        super().__init__(output_file, poscar_file)

    @property
    def external_pressure(self):
        """
        Returns the external pressure
        """
        # UNITS: kB
        for line in self.read_lines:
            match = self.external_pressureREGEX.match(line)

            if match:
                yield float(match.group('pressure'))

    @property
    def elapsed_time(self):
        for line in self.read_lines:
            match = self.elapsed_timeREGEX.match(line)

            if match:
                yield float(match.group('time'))

    @property
    def hessian_eigenvalues(self):
        """
        Returns the hessian eigenvalues
        """
        for line in self.read_lines:
            match = self.eigenval_hessianREGEX.match(line)
            match2 = self.eigenval_hessianREGEX2.match(line)

            if match:
                yield float(match.group('eigenval'))

            if match2:
                yield float(match2.group('eigenval'))

    @property
    def hessian_eigenvectors(self):
        """
        Returns the hessian eigenvectors
        """
        for idx, line in enumerate(self.read_lines):
            match = self.eigenval_hessianREGEX.match(line)
            match2 = self.eigenval_hessianREGEX2.match(line)

            if match:
                eigvecs = self.read_lines[idx+2:idx+2+self.N]
                eigvecs = list(map(lambda x: x.strip().split(), eigvecs))
                eigvecs = list(map(lambda x: list(map(lambda y: float(y), x[3:])), eigvecs))
                yield eigvecs

            if match2:
                eigvecs = self.read_lines[idx+2:idx+2+self.N]
                eigvecs = list(map(lambda x: x.strip().split(), eigvecs))
                eigvecs = list(map(lambda x: list(map(lambda y: float(y), x[3:])), eigvecs))
                yield eigvecs


class ParseOSZICAR(Parser):
    """
    Parses the OSZICAR file
    """

    energyRegex = re.compile(
            r"^\s+\d+\s+F=\s+[+-]?(\d*)?\.\d*[eE]?[+-]?\d*\s+E0=\s+(?P<e_0>[+-]?(\d*)?\.\d*[eE]?[+-]?\d*)\s+"
            )

    stepREGEX = re.compile(
            r'[A-Z]{3}:\s+(?P<step>\d+)\s+'
            )

    def __init__(self, ouput_file='OSZICAR', poscar_file='POSCAR'):
        """
        Initializes the OSZICAR parser object.
        """
        super().__init__(ouput_file, poscar_file)

    @property
    def energy(self):
        """
        returns the energy per atom
        """
        for line in self.read_lines:
            match = self.energyRegex.match(line)

            if match:
                yield float(match.group('e_0'))

    @property
    def electronic_steps(self):
        """
        returns the number of electronic steps per
        ionic step
        """
        steps = []
        for line in self.read_lines:
            match = self.stepREGEX.match(line)

            if match:
                steps.append(int(match.group('step')))
        electronic_steps = []
        prev = 0
        for idx, step in enumerate(steps):
            if step == 1:
                electronic_steps.append(steps[prev:idx])
                prev = idx
        electronic_steps.append(steps[prev:])
        for list in electronic_steps:
            if len(list) < 1:
                electronic_steps.remove(list)
        return [max(x) for x in electronic_steps]
