""" The vulcan-logic core. """

import copy

class Logic:
    """ A logic string container. """

    def __init__(self, logic_str=None, weight=None):
        """ Logic class initialization. """
        self.__logic_str = logic_str
        self.__logic_matrix = None
        self.__weight = None

        self.logic = logic_str
        self.weight = weight


    def __repr__(self):
        return self.to_eval_string()



    def __str__(self):
        """ Prints the __logic_matrix in a readable format. """
        print_str = ''
        for row in self.__logic_matrix:
            print_str += row['left'] + ' '
            print_str += row['eval'] + ' '
            print_str += row['right'] + '\n'
        return print_str[:-1] # Trim final newline



    @property
    def weight(self):
        """ Gets or sets the weight of the Logic String. """
        return self.__weight



    @weight.setter
    def weight(self, weight):
        return self._set_weight(weight)



    def _set_weight(self, weight=None):
        """ Calculates the weight of the Logic string.

        By default, Logic weight is calculated as the number of equations
        within the logic string. Future versions should allow field names
        to contribute varying weights.
        """

        self.__weight = len(self.__logic_matrix) if weight is None else weight



    @property
    def logic(self):
        """ Gets or sets the weight of the Logic String. """
        return self.__logic_matrix



    @logic.setter
    def logic(self, logic):
        """ Takes a logic string and expands it into an n x 3 matrix. """

        equations = [equation.strip() for equation in logic.split(',')]
        equations_matrix = []
        for equation in equations:
            equations_matrix.append(self.split_equation(equation))

        self.__logic_matrix = equations_matrix



    @staticmethod
    def split_equation(equation):
        """ Splits an equation into a dict of its parts. """

        eq_dict = {'eval': None, 'left': None, 'right': None}
        evaluators = ['==', '!=', '<>', '>=', '<=', '~=', '>', '<', '~', '=']

        for evaluator in evaluators:
            if evaluator in equation:
                left_end = equation.find(evaluator)
                right_start = left_end + len(evaluator)
                eq_dict['eval'] = evaluator
                eq_dict['left'] = equation[:left_end].strip()
                eq_dict['right'] = equation[right_start:].strip()
                break
        return eq_dict



    def to_eval_string(self):
        """ Converts the logic matrix into a string for eval(). """

        eval_string = None if not self.__logic_matrix else ''

        for i, row in enumerate(self.__logic_matrix):
            if i > 0:
                eval_string += ' and '

            if row['eval'] in ['==', '>=', '<=', '>', '<', '!=']:
                eval_string += (row['left'] + ' ' +
                                row['eval'] + ' ' +
                                row['right'])

            elif row['eval'] == '=':
                eval_string += (row['left'] + ' == ' +
                                row['right'])

            elif row['eval'] in ['~', '~=']:
                eval_string += ("'" + row['right'] + "'" + ' in ' +
                                "'" + row['left'] + "'")

            elif row['eval'] in '<>':
                eval_string += (row['left'] + ' != ' +
                                row['right'])


        return eval_string



    def replace_variables(self, dictionary):
        logic = copy.deepcopy(self.__logic_matrix)
        for row in logic:
            for k, v in dictionary.items():
                if(row['left'] == k):
                    row['left'] = v

        return logic
