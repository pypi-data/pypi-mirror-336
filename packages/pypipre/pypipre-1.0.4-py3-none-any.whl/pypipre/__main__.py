import argparse
import os,sys,re
import pypipre as pipre

def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title='subcommands', dest='subcommand')
    help_parser = subparsers.add_parser('help', help='show help')
    info_parser = subparsers.add_parser('info', help='show info of the package')
    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    examples_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'examples'))
    mpi_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'bin/mpiexec.hydra'))
    if args.subcommand == 'help':
        print(f'''
  use 
    cp -r {examples_path} .
  to copy out a example, and use 
    python solver.py thermal1.mtx thermal1_b.mtx solver.json
  to run the example, use
    {mpi_path} -n 2 python solver.py thermal1.mtx thermal1_b.mtx solver.json
  to run the example with 2 processes.
    ''')


    if args.subcommand == 'info':
        print("Devices:")
        for it in pipre.getAllDevices():
          print(f"    {it}")
        print("Solvers:")
        for it in pipre.getSolverList():
          print(f"    {it}")
        print("Preconditioners:")
        for it in pipre.getPreconditionerList():
          print(f"    {it}")
        print("Smoothers:")
        for it in pipre.getSmootherList():
          print(f"    {it}")
        print("LevelTransfers:")
        for it in pipre.getLevelTransferList():
          print(f"    {it}")
        print("Aggregators:")
        for it in pipre.getAggregatorList():
          print(f"    {it}")
main()

