#!/usr/bin/python
""" Testing basic functionality of Logic class. """

# Allow direct execution
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))




def logic_test():
    """ Main testing function. """
    from pylogic import Logic

    logic_str = 'Make == Subaru, Model != Impreza, Color ~= Blue, MPG > 30'
    addtl_evals = {'~=': '{1} in {0}'}
    example_cars = [{'Make': 'Ford',
                     'Model': 'Mustang',
                     'Color': 'Blue',
                     'MPG': 18.5},
                    {'Make': 'Subaru',
                     'Model': 'Impreza',
                     'Color': 'Desert Khaki',
                     'MPG': 38.0},
                    {'Make': 'Subaru',
                     'Model': 'Outback',
                     'Color': 'Crystal Black',
                     'MPG': 32.0},
                    {'Make': 'Subaru',
                     'Model': 'Crosstrek',
                     'Color': 'Hyper Blue',
                     'MPG': 34.0},
                    {'Make': 'Subaru',
                     'Model': 'Legacy',
                     'Color': 'Pacific Blue',
                     'MPG': 33.0},
                    {'Make': 'Subaru',
                     'Model': 'Ascent',
                     'Color': 'Red',
                     'MPG': 24.0}]

    log = Logic(logic_str, evaluators=addtl_evals)

    print(log, end='\n\n')

    for car in example_cars:
        for key, value in car.items():
            print(str(key) + ': ' + str(value))
        print('Matched: ', end='')
        print(log.eval(car))
        print()



if __name__ == '__main__':
    logic_test()
