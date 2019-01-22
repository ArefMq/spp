#!/usr/bin/env python2
import argparse
from interpreter import Interpreter, UnknownInstruction
from compiler import Compiler
from godel import Godel


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="<Required> File to run (either 's' or 'spp' format)")
    parser.add_argument("-i", "--input", nargs='+', help="Input variables", type=int)
    parser.add_argument("-v", "--verbose", action='store_true')
    parser.add_argument("-c", "--compile", action='store_false', help="Only compile the input and does not run the "
                                                                      "interpreter.")
    parser.add_argument("-g", "--godel", action='store_false', help="Encode the output via Godel encoding.")
    args = parser.parse_args()
    filename = args.filename.strip()
    input_list = args.input
    if not filename.endswith('.s') and not filename.endswith('.spp') and not filename.endswith('.godel'):
        print('File type not recognized.')
    else:
        run(filename, input_list, args.verbose, args.compile, args.godel)


def run(filename, input_list, verbose, compile_only, godel):
    interpreter = None
    try:
        if filename.endswith('.s'):
            interpreter = run_s(filename, godel, input_list, verbose)

        elif filename.endswith('.spp'):
            interpreter = run_spp(compile_only, filename, godel, input_list, verbose)

        elif filename.endswith('.godel'):
            interpreter = run_godel(compile_only, filename, input_list, verbose)

    except UnknownInstruction as exp:
        print('Instruction Syntax Error:\n%s' % exp)
    except KeyboardInterrupt:
        print('User Interruption')
    finally:
        result = '[result= %d]' % interpreter.memory_map.get('y', 0) if interpreter else ''
        print('HALT %s' % result)


def run_godel(compile_only, filename, input_list, verbose):
    g = Godel(verbose)
    g.open(filename)
    interpreter = Compiler(verbosity=verbose)
    interpreter.code = g.code
    interpreter.compile()
    interpreter.save('%s.s' % filename[:-6])
    interpreter.save('%s.express.s' % filename[:-6], True)
    if not compile_only:
        interpreter.run(input_list)
    return interpreter


def run_spp(compile_only, filename, godel, input_list, verbose):
    interpreter = Compiler(filename, verbose)
    interpreter.save('%s.s' % filename[:-4])
    interpreter.save('%s.express.s' % filename[:-4], True)
    if not compile_only:
        interpreter.run(input_list)
    if godel:
        g = Godel(verbose)
        g.save('%s.godel' % filename[:-4], interpreter.code)
    return interpreter


def run_s(filename, godel, input_list, verbose):
    interpreter = Interpreter(filename, verbose)
    interpreter.run(input_list)
    if godel:
        g = Godel(verbose)
        g.save('%s.godel' % filename[:-2], interpreter.code)
    return interpreter


if __name__ == "__main__":
    main()
