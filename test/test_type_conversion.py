#!/usr/bin/python
""" Testing basic functionality of Logic class. """

# Allow direct execution
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))




def logic_test():
    """ Main testing function. """
    from pylogic import Logic

    logic_str = 'Make == Subaru, Model != Impreza, Date > 01/01/2017'
    addtl_evals = {'~=': '{1} in {0}'}
    example_cars = [{'Make': 'Ford',
                     'Model': 'Mustang',
                     'Color': 'Blue',
                     'MPG': 18.5,
                     'Date': Parsed_Date('01/01/2019')},
                    {'Make': 'Subaru',
                     'Model': 'Impreza',
                     'Color': 'Desert Khaki',
                     'MPG': 38.0,
                     'Date': Parsed_Date('01/01/2016')},
                    {'Make': 'Subaru',
                     'Model': 'Outback',
                     'Color': 'Crystal Black',
                     'MPG': 32.0,
                     'Date': Parsed_Date('01/01/2018')},
                    {'Make': 'Subaru',
                     'Model': 'Crosstrek',
                     'Color': 'Hyper Blue',
                     'MPG': 34.0,
                     'Date': Parsed_Date('01/01/2017')},
                    {'Make': 'Subaru',
                     'Model': 'Legacy',
                     'Color': 'Pacific Blue',
                     'MPG': 33.0,
                     'Date': Parsed_Date('01/01/2016')},
                    {'Make': 'Subaru',
                     'Model': 'Ascent',
                     'Color': 'Red',
                     'MPG': 24.0,
                     'Date': Parsed_Date('01/01/2017')}]

    log = Logic(logic_str, evaluators=addtl_evals)

    print(log, end='\n\n')

    for car in example_cars:
        for key, value in car.items():
            print(str(key) + ': ' + str(value))
        print('Matched: ', end='')
        try:
            x = log.eval(car)
        except NameError as err:
            x = eval(str(err))

        print('X =', eval(str(x)))
        print()


import datetime
class Parsed_Date(datetime.date):
    def __new__(cls, datestring, *args, **kwargs):
        date = Parsed_Date.date_converter(datestring)
        return super().__new__(cls, date.year, date.month, date.day)
    
    @staticmethod
    def date_converter(date_val):
        if isinstance(date_val, datetime.date):
            return date_val

        if date_val is None:
            return date_val

        if '-' in date_val:
            parts = date_val.split('-')
        elif '/' in date_val:
            parts = date_val.split('/')
        else: # Assume yyyymmdd or non-parseable date string
            return date_val

        if len(parts[0]) == 4: # Assume yyyy-(m)m-(d)d
            year = int(parts[0])
            month = int(parts[1])
            day = int(parts[2])
        else: # Assume (m)m-(d)d-(yy)yy
            month = int(parts[0])
            day = int(parts[1])
            if len(parts[2]) == 2:
                year = int('20' + str(parts[2]))
            else:
                year = int(parts[2])

        try:
            converted = datetime.date(year, month, day)
        except (TypeError, ValueError) as error:
            print(f'Date Conversion Failed: {date_val} : {error}')

        return converted



if __name__ == '__main__':
    logic_test()
