#!/usr/bin/python
""" Testing basic functionality of Logic class. """

# Allow direct execution
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))




def logic_test():
    """ Main testing function. """
    from pylogic import Logic

    logic_str = 'Make == Subaru and Model != Impreza,'
    logic_str += 'Color ~= Blue or Color == Red, '
    logic_str += 'MPG > 30 or MPG == 24'

    print(f'Initial Logic String: {logic_str}')

    addtl_evals = {'~=': '{1} in {0}'}

    log = Logic(logic_str, evaluators=addtl_evals)

    print(log, end='\n\n')


if __name__ == '__main__':
    logic_test()
