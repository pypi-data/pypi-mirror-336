import argparse
import sys
from .core import Lain

def save_report(out, args, atoms):
    save_file = args.save
    with open(f'{save_file}.csv', 'w+') as text:
        text.write(f'# file: {args.filename}\n')
        text.write(f'# task: {args.task}\n')
        text.write(f'# formula: {atoms.symbols}\n')
        text.write(f'# mobile_ion: {args.mobile_ion}\n')
        text.write(f'# resolution: {args.resolution}\n')
        if args.task == 'void':
            text.write(f'r1d,r2d,r3d\n')
        else:
            text.write(f'e1d,e2d,e3d\n')
        string = ','
        string = string.join(format(out[key], "0.3f") for key in out.keys())
        string += '\n'
        text.write(string)


def calculate(args):

    calc = Lain(verbose =args.verbose)
    atoms = calc.read_file(args.filename, oxi_check=args.oxi_check)

    if args.verbose:
        print(atoms)

    if args.task == 'bvse': 
        _ = calc.bvse_distribution(mobile_ion=args.mobile_ion,
                                   resolution=args.resolution)
        out = calc.percolation_barriers(encut = 20.0)
        print(out)
        if args.save:
            save_report(out, args, atoms)

    elif args.task =='void':
        _ = calc.void_distribution(mobile_ion=args.mobile_ion,
                                   resolution=args.resolution)
        out = calc.percolation_radii()
        print(out)
        if args.save:
            save_report(out, args, atoms)

    if args.task == 'grd': 
        _ = calc.bvse_distribution(mobile_ion=args.mobile_ion,
                                   resolution=args.resolution)
        if args.save_grd:
            path_grd = args.save_grd
        else: 
            path_grd = args.filename
        calc.write_grd(path_grd, task = args.task)

    if args.task == 'cube': 
        _ = calc.bvse_distribution(mobile_ion=args.mobile_ion,
                                   resolution=args.resolution)
        if args.save_grd:
            path_grd = args.save_grd
        else: 
            path_grd = args.filename
        calc.write_cube(path_grd, task = args.task)



def main():

    parser = argparse.ArgumentParser(description='Bond valence site energy calculator')

    parser.add_argument('task', choices=['bvse', 'void', 'grd', 'cube'],
                        help='task to perform, can be "bvse", "void", "grd", "cube')

    parser.add_argument('filename', type=str,
                        help='path to file (.cif, POSCAR, etc.)')
   
    parser.add_argument('mobile_ion', type=str,
                        help='mobile ion of interest')

    parser.add_argument('-o', '--oxi-check', default=True, type = bool,
                        help='assign oxidation states'
                                                    '(default: True)')
    parser.add_argument('-r', '--resolution', default=0.25, type=float,
                        help='grid resolution in angstrom')

    parser.add_argument('-v', '--verbose', choices=[0, 1], default=0, type=int,
                        help='print additional info')
    
    parser.add_argument('-s', '--save', type=str,
                        help='path to save calculation results', default = None)    

    parser.add_argument('-grd', '--save-grd', type=str,
                        help='path to save the .grd file', default = None)

    args = parser.parse_args(sys.argv[1:])
    calculate(args)



if __name__ == '__main__':
    main()
