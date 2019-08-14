""" The vulcan-logic core. """

import ast
import copy

class Logic:
    """ A logic string container. """

    def __init__(self, logic_str=None, weight=None, evaluators=None):
        """ Logic class initialization. """

        self.__evaluators = {'==': '{0} == {1}',
                             '!=': '{0} != {1}',
                             '>=': '{0} >= {1}',
                             '<=': '{0} <= {1}',
                             '>': '{0} > {1}',
                             '<': '{0} < {1}'}

        self.__logic_str = logic_str
        self.__logic_matrix = None
        self.__weight = None
        self.__evaluators.update(evaluators)

        self.logic = logic_str
        self.weight = weight



    def __repr__(self):
        eval_string = ""
        for row in self.__logic_matrix:
            tmp = self.__evaluators[row['eval']]
            tmp = tmp.replace('{0}', row['left'])
            tmp = tmp.replace('{1}', row['right'])

            eval_string += tmp + ' and '
        return None if eval_string == "" else eval_string[:-5]



    def __str__(self):
        """ Prints the __logic_matrix in a readable format. """
        print_str = ''
        for row in self.__logic_matrix:
            print_str += row['left'] + ' '
            print_str += row['eval'] + ' '
            print_str += row['right'] + '\n'
        return print_str[:-1] # Trim final newline



    def _set_weight(self, weight=None):
        """ Calculates the weight of the Logic string.

        By default, Logic weight is calculated as the number of equations
        within the logic string. Future versions should allow field names
        to contribute varying weights.
        """

        for row in self.__logic_matrix:
            try:
                row['weight']
            except KeyError:
                row['weight'] = 1

        if weight is None:
            self.__weight = sum(row['weight'] for row in self.__logic_matrix)
        else:
            self.__weight = weight



    @property # weight(self)
    def weight(self):
        """ Gets or sets the weight of the Logic String. """
        return self.__weight



    @weight.setter
    def weight(self, weight):
        return self._set_weight(weight)



    @property # logic(self)
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



    @staticmethod # astype(var, conv_type)
    def astype(var, conv_type):
        """ Converts a variable to a given type. """

        # If variable is already of conv_type, return immediately
        if isinstance(var, conv_type):
            return var

        # Check that conv_type is actually a type.
        if isinstance(conv_type, type):
            try:
                return ast.literal_eval(str(conv_type(var)))
            except (ValueError, TypeError) as err:
                print(err)

        return None



    def eval(self, dictionary=None):
        """ Evaluates logic equations.

        Accepts a dictionary as an argument. If no dictionary is
        provided, logic equations are evaluated without any
        replacement.
        """

        if dictionary is not None:
            logic = self.replace_variables(dictionary)
        else:
            logic = self.__logic_matrix

        for row in logic:
            eval_string = self.to_eval_string(row)
            row['validity'] = eval(eval_string) #pylint: disable=eval-used

        for row in logic:
            if not row['validity'] or row['validity'] is None:
                return False

        return True



    def replace_variables(self, dictionary):
        """ Replaces variables within an equation with values from a dict. """

        logic = copy.deepcopy(self.__logic_matrix)
        for row in logic:
            for key, value in dictionary.items():
                if row['left'] == key:
                    row['left'] = value

                if row['right'] == key:
                    row['right'] = value

        return logic



    def rebase_weight(self, dictionary=None):
        """ Base weights on a dictionary of values. """

        if dictionary is not None:
            for row in self.__logic_matrix:
                for match_str, adj_weight in dictionary.items():
                    if match_str in row.values():
                        row['weight'] = adj_weight

            self.weight = sum(row['weight'] for row in self.__logic_matrix)



    def split_equation(self, equation):
        """ Splits an equation into a dict of its parts. """

        eq_dict = {'eval': None, 'left': None, 'right': None}

        # Evaluators must be sorted so that longer strings match first.
        for evaluator in sorted(self.__evaluators, key=len, reverse=True):
            if evaluator in equation:
                left_end = equation.find(evaluator)
                right_start = left_end + len(evaluator)
                eq_dict['eval'] = evaluator
                eq_dict['left'] = equation[:left_end].strip()
                eq_dict['right'] = equation[right_start:].strip()
                break

        return eq_dict



    def to_eval_string(self, eq_dict):
        """ Takes an equation dictionary and returns a string for eval(). """

        # Match right type to left type
        right = self.astype(eq_dict['right'], type(eq_dict['left']))

        # Change left/right sides of equation into typed strings for eval().
        left = type_parser(right) + '("' + str(eq_dict['left']) + '")'
        right = type_parser(right) + '("' + str(right) + '")'

        eval_string = self.__evaluators[eq_dict['eval']]
        eval_string = eval_string.replace('{0}', left)
        eval_string = eval_string.replace('{1}', right)

        return eval_string


def type_parser(var):
    """ Returns string representation of variable type.

    If passed a variable with class: 'type', this function will return a
    shortened string. Otherwise, it finds the type of the variable, and
    returns the shortened string of that type.
    """

    if isinstance(var, type):
        return str(var)[8:-2]
    return str(type(var))[8:-2]
