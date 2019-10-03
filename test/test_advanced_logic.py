#!/usr/bin/python
""" Testing basic functionality of Logic class. """

# Allow direct execution
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))




def logic_test():
    """ Main testing function. """
    from pylogic import parse_logic_string

    logic_str = 'Make == Subaru and Model != Impreza,'
    logic_str += 'Color ~= Blue or Color == Red,'
    logic_str += 'MPG > 30 or MPG == 24'

    print(f'Logic String: {logic_str}\n')
    parsed_logic_str, parsed_logic_dict = parse_logic_string(logic_str)
    for key, value in parsed_logic_dict.items():
        print(key, value, sep=': ')

    print('\n', parsed_logic_str, sep='')



if __name__ == '__main__':
    logic_test()
