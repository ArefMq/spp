#!/usr/bin/env python2
import argparse
from interpreter import Interpreter, UnknownInstruction
from compiler import Compiler


def main(filename, input_list, verbose):
    interpreter = None
    try:
        if filename.endswith('.s'):
            interpreter = Interpreter(filename, verbose)
            interpreter.run(input_list)
        elif filename.endswith('.spp'):
            interpreter = Compiler(filename, verbose)
            interpreter.save('%s.s' % filename[:-4])
            interpreter.save('%s.express.s' % filename[:-4], True)
            interpreter.run(input_list)
    except UnknownInstruction as exp:
        print('Instruction Syntax Error:\n%s' % exp)
    except KeyboardInterrupt:
        print('User Interruption')
    finally:
        result = '[result= %d]' % interpreter.memory_map.get('y', 0) if interpreter else ''
        print('HALT %s' % result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="<Required> File to run (either 's' or 'spp' format)")
    parser.add_argument("-i", "--input", nargs='+', help="Input variables", type=int)
    parser.add_argument("-v", "--verbose", action='store_true')

    args = parser.parse_args()
    filename = args.filename.strip()
    input_list = args.input

    if not filename.endswith('.s') and not filename.endswith('.spp'):
        print('File type not recognized.')
    else:
        main(filename, input_list, args.verbose)
