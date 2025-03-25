# Import argparse
import argparse
from textwrap import dedent
import numpy as np
import shutil
import os
import pandas as pd

# Import Modules
from . import core
from . import phonon
from . import conv
from . import input
from . structure import Molecule
# Create the wrapper funstions

THZ_TO_INV_CM = 33.35641
C0 = 299792458


def generate_input_func(args):
    '''
    Wrapper function for the generate_input function

    parameters
    ----------
    filename : str
    config_file : file

    Returns
    -------
    INCAR : file
    '''
    core.generate_input(
        filename=args.poscar,
        calculation=args.config_file,
            )

    with open('INCAR', 'a') as f:
        f.write('ENCUT = {}\n'.format(args.encut))

    if args.mesh is not None:
        core.generate_kpoints(mesh=args.mesh)
    elif args.kspacing is not None:
        with open('INCAR', 'a') as f:
            f.write('KSPACING = {}\n'.format(args.kspacing))
    else:
        raise NotImplementedError('No kpoint scheme specified')


def generate_supercell_func(args):
    '''
    Wrapper function for the generate_supercell function

    parameters
    ----------
    expansion : list
    poscar : str

    Returns
    -------
    POSCAR : file
    '''
    core.generate_supercell(
            expansion=np.array(args.dim, dtype=int),
            filename=args.poscar,
            )


def generate_job_func(args):
    '''
    Wrapper function for the generate_job function

    parameters
    ----------
    title : str
    cores : int
    vasp_type : str

    Returns
    -------
    job.sh : file
    '''
    core.generate_job(
            title=args.title,
            cores=args.cores,
            vasp_type=args.vasp_type,
            job_title=args.output,
            array=None,
            array_file=None,
            )


def start_up_func(args):
    '''
    Wrapper function for the start_up function

    parameters
    ----------
    None

    Returns
    -------
    configuration files : file
    '''
    core.create_input_configurations()


def dope_structure_func(args):
    '''
    Wrapper function for the dope_structure function

    parameters
    ----------
    filename : str
    dopant : str
    replace : str
    instances : int

    Returns
    -------
    POSCARs : file
    '''
    core.dope_structure_sym(
        filename=args.poscar,
        dopant=args.dopant,
        replace=args.replace,
        instances=args.instances,
        no_sym=args.no_symm,
        )


def generate_defect_func(args): 
    '''
    Wrapper function for the generate_defect function

    parameters
    ----------
    filename : str
    site : str
    instances : int

    Returns
    -------
    POSCAR : file
    '''
    core.generate_defect(
            filename=args.poscar,
            site=args.site,
            instances=args.instances,
            )


def find_molecule_func(args):
    '''
    Wrapper function for the asymmetric_unit function

    parameters
    ----------
    filename : str
    atom : str
    bond_max : float

    Returns
    -------
    POSCAR : file
    '''
    core.molecule(
            filename=args.poscar,
            atom=args.atom,
            scaler=args.scaler,
            )


def convert_cif_func(args):
    '''
    Wrapper function for the convert_cif function

    parameters
    ----------
    filename : str

    Returns
    -------
    POSCAR : file
    '''
    core.convert_cif(
            filename=args.filename,
            )

def phonon_calc(args):
    '''
    wrapper function for phonon calculation

    parameters
    ----------
    supercell : list
    mesh : list
    encut : int
    cores : int
    bec : bool

    Returns
    -------
    None
    '''
# Check if the config file exists
    if not phonon.check_config():
        raise ValueError('No config file found, please run the start_up command')

# Generate the input files
    core.generate_input('POSCAR', 'phonon')
    core.generate_kpoints(mesh=args.k_point_mesh)

    with open('INCAR', 'a') as f:
        f.write('ENCUT = {}\n'.format(str(args.encut)))

# write the phonon files to a phonopy_file
    phonon.store_disp_files()

# Generate the job file
    core.generate_job(
            title='phonon',
            cores=args.cores,
            vasp_type=args.vasp_type,
            job_title='phonopy',
            array='phonopy',
            array_file='phonon_files.txt',
    )

    if args.bec:
        os.mkdir('BEC')
        os.chdir('BEC')
        shutil.copy('../POSCAR', '.')
        core.generate_input('POSCAR', 'bec')
        core.generate_kpoints(mesh=args.bec_mesh)

        with open('INCAR', 'a') as f:
            f.write('ENCUT = {}\n'.format(str(args.encut)))
        core.generate_job('BEC', args.bec_cores, 'standard',
                          job_title='BORN', array=None, array_file=None)
        os.chdir('..')


def convergence_func(args):
    """
    Wrapper function for the convergence function

    parameters
    ----------
    poscar : str
        The structure file to be used, POSCAR or CIF
    cores : int
        The number of cores to be used
    """
    if not os.path.exists(args.poscar):
        raise FileNotFoundError('{} does not exist'.format(args.poscar))

    if args.gen:
        input_file = input.InputFileGenerator(filename=args.poscar, calculation=args.scf_type)
        input_file.generate_incar()
        input_file.generate_potcar()
        combinations = conv.get_combinations(filename=args.poscar, max_encut=args.max_encut + 50, min_encut=args.min_encut, kpoints=args.kpoints)
        conv.make_dirs(combinations)
        core.generate_job(title='CONV', cores=args.cores, vasp_type='standard', job_title='CONV', array='convergence', array_file='convergence.txt')
    elif args.parse:
        combinations = conv.get_combinations(filename=args.poscar, max_encut=args.max_encut + 50, min_encut=args.min_encut)
        conv.extract_data(combinations)
    elif args.plot:
        if not os.path.exists('conv.csv'):
            raise FileNotFoundError('conv.csv does not exist, please run the parse command first')
        data = pd.read_csv('conv.csv')
        if not os.path.exists(args.poscar):
            raise FileNotFoundError('{} does not exist'.format(args.poscar))
        struct = core.Structure.from_poscar(args.poscar)
        num_atoms = struct.N
        conv.kpoint_plot(data, num_atoms, args.gradient)
        conv.cutoff_plot(data, num_atoms, args.gradient)
    else:
        raise NotImplementedError('No action specified, please use the --gen, --parse or --plot flags')


def bridge_dimer_func(args):
    if not os.path.exists(args.poscar):
        raise FileNotFoundError('{} does not exist'.format(args.poscar))

    mol = Molecule(args.poscar, args.atom, args.scaler)
    mol.bridge_dimer()
    qm_graph = mol.qm_graph
    qm_graph.to_xyz("{}.xyz".format("".join(qm_graph.graph_formula)), mass_centered=True)


def coord_sphere_func(args):
    """
    Wrapper function for the coord_sphere function

    parameters
    ----------
    poscar : str
        The structure file to be used, POSCAR
    atom : str
        The atom to be used
    bond_max : float
        The maximum bond length
    coordination_number : int
        The number of coordination spheres to be found: (1, 2)
    """
    if not os.path.exists(args.poscar):
        raise FileNotFoundError('{} does not exist'.format(args.poscar))

    core.coord_sphere(
            filename=args.poscar,
            atom=args.atom,
            sphere_num=args.coordination_sphere_number,
            )

def reduce_func(args):
    """
    Wrapper function for the reduce function

    parameters
    ----------
    poscar : str
        The structure file to be used, POSCAR

    primitive : bool
        Whether to reduce to primitive cell or not

    niggli: bool
        Whether to reduce to niggli cell or not

    delaunay: bool
        Whether to reduce to delaunay cell or not

    refine: bool
        Whether to refine the cell or not
    """

    if not os.path.exists(args.poscar):
        raise FileNotFoundError('{} does not exist'.format(args.poscar))

    core.reduce(
            filename=args.poscar,
            primative=args.primitive,
            niggli=args.niggli,
            delaunay=args.delaunay,
            refine=args.refine,
            )

# phonopy interface
def phonopy_func(args):
    """
    function for interfacing with phonopy
    includes:
        - band structure input file generation
        - dos input file generation
    """
    if not os.path.exists(args.poscar):
        raise FileNotFoundError('{} does not exist'.format(args.poscar))

    if args.band and not args.mesh:
        if args.dim is None:
            raise ValueError('Please specify the dimensions of the supercell (--dim)')
        core.write_band(args.poscar, args.dim)

    if args.mesh and not args.band:
        if args.dim is None:
            raise ValueError('Please specify the dimensions of the supercell (--dim)')
        if args.mesh_points is None:
            raise ValueError('Please specify the mesh points (--mesh_points)')
        core.write_mesh(args.poscar, args.dim, args.mesh_points)

    if args.band and args.mesh:
        if args.dim is None:
            raise ValueError('Please specify the dimensions of the supercell (--dim)')
        if args.mesh_points is None:
            raise ValueError('Please specify the mesh points (--mesh_points)')
        core.write_band_dos(args.poscar, args.dim, args.mesh_points)


###########


def read_args(arg_list=None):
    '''Reads the command line arguments'''
    parser = argparse.ArgumentParser(
            prog='vasp_suite',
            description=dedent('''A suite of tools for VASP calculations'''),
            epilog=dedent('''To display options for a specific programme, use vasp_suite <programme> -h'''),
            formatter_class=argparse.RawDescriptionHelpFormatter
            )

    # Subparsers
    subparsers = parser.add_subparsers(dest='prog')

    gen_inp = subparsers.add_parser(
            'generate_input',
            description=dedent(
                '''
                Generation of INCAR and POTCAR files for VASP calculations.
                '''
                ),
            formatter_class=argparse.RawDescriptionHelpFormatter
            )

    gen_inp.set_defaults(func=generate_input_func)

    gen_inp.add_argument(
            '--config_file',
            required=True,
            help=dedent(
                """
                The configuration file for the input generation.

                Example:

                Inside ~/.vasp_suite_templates '.ini' configuration files are
                stored. To perform a relaxation caluclation using the relaxation.ini
                template, use the following command:

                "vasp_suite generate_input relaxation"
                """
                )
            )

    gen_inp.add_argument(
            '--poscar',
            required=True,
            help=dedent(
                '''
                The name of the structure file.
                '''
                ),
            )

    gen_inp.add_argument(
            '--encut',
            required=True,
            type=int,
            help=('The ENCUT value to be used in the calculation')
            )

    kp = gen_inp.add_mutually_exclusive_group(required=True)

    kp.add_argument(
            '--mesh',
            nargs=3,
            metavar=('Nx', 'Ny', 'Nz'),
            type=int,
            help='The kpoint mesh to be used in the calculation'
    )

    kp.add_argument(
        '--kspacing',
        type=float,
        help='The kpoint spacing to be used in the INCAR'
    )

    gen_job = subparsers.add_parser(
        'generate_job',
        formatter_class=argparse.RawDescriptionHelpFormatter
        )

    gen_job.set_defaults(func=generate_job_func)

    gen_job.add_argument(
        '--title',
        help='The title of the job'
        )

    gen_job.add_argument(
        '--cores',
        help='The number of cores to use',
        type=int,
        )

    gen_job.add_argument(
        '--vasp_type',
        help='The vasp program to use',
        choices=['standard', 'gamma'],
        required=True,
        )

    gen_job.add_argument(
            '--output',
            help='The output file name',
            required=False,
            default='submit'
            )

    gen_supercell = subparsers.add_parser(
        'supercell',
        formatter_class=argparse.RawDescriptionHelpFormatter
        )

    gen_supercell.set_defaults(func=generate_supercell_func)

    gen_supercell.add_argument(
        '--dim',
        nargs=3,
        metavar=('Nx', 'Ny', 'Nz'),
        help=dedent(
            '''
            The expansion vector for the supercell, a b c
            '''
            ),
        )

    gen_supercell.add_argument(
            '--poscar',
            help=dedent(
                '''
                The name of the structure file
                '''
                ),
            )

    start_up = subparsers.add_parser(
        'set_up',
        formatter_class=argparse.RawDescriptionHelpFormatter
        )

    start_up.set_defaults(func=start_up_func)

    dope_struct = subparsers.add_parser(
        'dope_structure',
        formatter_class=argparse.RawDescriptionHelpFormatter
        )

    dope_struct.set_defaults(func=dope_structure_func)

    dope_struct.add_argument(
        '--poscar',
        help='The name of the structure file',
        )

    dope_struct.add_argument(
            '--dopant',
            help='The element to dope the structure with',
            )

    dope_struct.add_argument(
            '--replace',
            help='The element to replace',
            )

    dope_struct.add_argument(
            '--instances',
            help='The number of instances of the dopant to add',
            type=int,
            )

    dope_struct.add_argument(
            '--no_symm',
            help='Do not remove symmetry equivelent structures',
            action='store_true',
            )

    gen_defect = subparsers.add_parser(
        'generate_defect',
        formatter_class=argparse.RawDescriptionHelpFormatter
        )

    gen_defect.set_defaults(func=generate_defect_func)

    gen_defect.add_argument(
            '--poscar',
            help='The name of the structure file',
            )

    gen_defect.add_argument(
            '--site',
            help='The name of the atom to remove',
            )

    gen_defect.add_argument(
            '--instances',
            help='The number of instances of defect',
            type=int,
            )

    asym = subparsers.add_parser(
        'find_molecule',
        formatter_class=argparse.RawDescriptionHelpFormatter
        )

    asym.set_defaults(func=find_molecule_func)

    asym.add_argument(
            '--poscar',
            help='The name of the structure file',
            required=True,
            )

    asym.add_argument(
            '--atom',
            help='The name of the spin centre in the molecular crystal',
            required=True,
            )

    asym.add_argument(
            '--scaler',
            help='The scaling factor when finding connectivity',
            type=float,
            default=1.12,
            )

    cif = subparsers.add_parser(
            'convert_cif',
            formatter_class=argparse.RawDescriptionHelpFormatter
            )

    cif.set_defaults(func=convert_cif_func)

    cif.add_argument(
            '--filename',
            help='The name of the .CIF file',
            required=True,
            )

    phonon = subparsers.add_parser(
            'phonopy_job',
            formatter_class=argparse.RawDescriptionHelpFormatter
            )

    phonon.set_defaults(func=phonon_calc)

    std = phonon.add_argument_group('Phonopy args')

    std.add_argument(
            '--k_point_mesh',
            help='The mesh to use for the phonon calculation',
            nargs=3,
            metavar=('Nx', 'Ny', 'Nz'),
            type=int,
            )

    std.add_argument(
            '--cores',
            help='The number of cores to use for the phonon calculation',
            type=int,
            required=True,
            )

    std.add_argument(
            '--encut',
            help='The energy cutoff for the phonon calculation',
            type=int,
            )

    std.add_argument(
            '--vasp_type',
            help='The vasp program to use',
            choices=['standard', 'gamma'],
            required=True,
            )

    bec = phonon.add_argument_group('Born effective charges')

    bec.add_argument(
            '--bec',
            help='Calculate the Born effective charges',
            action='store_true',
            )

    bec.add_argument(
            '--bec_mesh',
            help='The mesh to use for the Born effective charges',
            nargs=3,
            metavar=('Nx', 'Ny', 'Nz'),
            type=int,
            default=[1, 1, 1],
            )

    bec.add_argument(
            '--bec_cores',
            help='The number of cores to use for the BEC calculation',
            type=int,
            )

    conv = subparsers.add_parser(
            "convergence",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            )

    conv.set_defaults(func=convergence_func)

    prog_conv = conv.add_argument_group('Convergence programs')
    conv_prog = prog_conv.add_mutually_exclusive_group(required=True)

    conv_prog.add_argument(
            '--gen',
            help='Generate the convergence testing directories, input files and submission script',
            action='store_true',
            )

    conv_prog.add_argument(
            '--parse',
            help='Parse the convergence testing directories',
            action='store_true',
            )

    conv_prog.add_argument(
            '--plot',
            help='Plot the convergence testing results',
            action='store_true',
            )

    plot = conv.add_argument_group('Plotting options')
    plot.add_argument(
            '--gradient',
            help='Plot the gradient of the convergence testing results',
            action='store_true',
            )

    conv_std = conv.add_argument_group('Standard args')
    conv_std.add_argument(
            '--poscar',
            help='The name of the POSCAR file',
            required=True,
            )

    conv_std.add_argument(
            '--cores',
            help='The number of cores to use for the calculation',
            type=int,
            default=1,
            )

    conv_std.add_argument(
            '--max_encut',
            help='The maximum energy cutoff to test',
            type=int,
            default=1000,
            )

    conv_std.add_argument(
            '--min_encut',
            help='The minimum energy cutoff to test',
            type=int,
            default=200,
            )

    conv_std.add_argument(
            '--scf_type',
            help='The config file for the scf calculation. Default is scf with VDW',
            type=str,
            default='scf',
            required=False,
            )
    
    conv_std.add_argument(
            '--kpoints',
            help='A list of k-point meshes which overrides automatic k-mesh generation, e.g. --kpoints 111 211 222',
            nargs='+',
            type=int,
            default=None,
            required=False,
            )

    dimer = subparsers.add_parser(
            "bridge_dimer",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            )

    dimer.set_defaults(func=bridge_dimer_func)

    dimer.add_argument(
            "--poscar",
            help="The name of the POSCAR file",
            required=True,
            )

    dimer.add_argument(
            "--atom",
            help="The name of the first atom in the dimer e.g. Dy1",
            required=True,
            )

    dimer.add_argument(
            "--scaler",
            help="The scaling factor for the dimer",
            type=float,
            default=1.1,
    )

    cd_sphere = subparsers.add_parser(
            "coordination_sphere",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            )

    cd_sphere.set_defaults(func=coord_sphere_func)

    cd_sphere.add_argument(
            '--poscar',
            help='The name of the POSCAR file',
            )

    cd_sphere.add_argument(
            '--atom',
            help='The name of the atom to find the coordination sphere of, e.g. "Dy1"',
            )

    cd_sphere.add_argument(
            '--coordination_sphere_number',
            help='The coordination sphere number to find',
            type=int,
            )

    phon_int = subparsers.add_parser(
            "phonopy",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            )

    phon_int.set_defaults(func=phonopy_func)

    plot_args = phon_int.add_argument_group('Plotting options')
    plot_args.add_argument(
            '--band',
            help='Write the band.conf file?',
            action='store_true',
            )

    plot_args.add_argument(
            '--mesh',
            help='Write the mesh.conf file?',
            action='store_true',
            )

    phon_std = phon_int.add_argument_group('Standard args')
    phon_std.add_argument(
            '--poscar',
            help='The name of the POSCAR file',
            )

    phon_std.add_argument(
            '--dim',
            help='The supercell dimensions',
            metavar=('Nx', 'Ny', 'Nz'),
            nargs=3,
            type=int,
            )

    phon_std.add_argument(
            '--mesh_points',
            help='The mesh points',
            metavar=('Nx', 'Ny', 'Nz'),
            nargs=3,
            type=int,
            )

    red = subparsers.add_parser(
            "reduce",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            )

    red.set_defaults(func=reduce_func)

    red.add_argument(
            '--poscar',
            help='The name of the POSCAR file',
            )

    red_type = red.add_mutually_exclusive_group(required=True)

    red_type.add_argument(
            '--primitive',
            help='Reduce to the primitive cell',
            action='store_true',
            )

    red_type.add_argument(
            '--niggli',
            help='Reduce to the Niggli cell',
            action='store_true',
            )

    red_type.add_argument(
            '--delaunay',
            help='Reduce to the Delaunay cell',
            action='store_true',
            )

    red_type.add_argument(
            '--refine',
            help='Refine the cell',
            action='store_true',
            )

    # Parse the ArgumentParser
    parser.set_defaults(func=lambda args: parser.print_help())
    args = parser.parse_known_args(arg_list)

    # Select programme
    if args in ['generate_input', 'generate_job', 'supercell', 'set_up',
                'dope_structure', 'generate_defect', 'convert_cif',
                'phonopy_job', 'convergence', 'coordination_sphere',
                'phonopy', 'reduce', 'find_molecule']:
        args.func(args)
    else:
        args = parser.parse_args(arg_list)
        args.func(args)


def main():
    read_args()
