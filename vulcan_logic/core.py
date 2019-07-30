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
        return self.to_eval_string()



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

        self.__weight = len(self.__logic_matrix) if weight is None else weight



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
            if not isinstance(row['right'], type(row['left'])):
                row['right'] = self.astype(row['right'], type(row['left']))

            left = str(type(row['left'])) + '(' + str(row['left']) + ')'
            right = str(type(row['right'])) + '(' + str(row['right']) + ')'

            row['validity'] = None

            eval_string = self.__evaluators[row['eval']]
            eval_string = eval_string.replace('{0}', left)
            eval_string = eval_string.replace('{1}', right)
            row['validity'] = ast.literal_eval(repr(eval_string))


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



    def split_equation(self, equation):
        """ Splits an equation into a dict of its parts. """

        eq_dict = {'eval': None, 'left': None, 'right': None}

        max_eval_length = 0
        for evaluator in self.__evaluators:
            max_eval_length = max(len(evaluator), max_eval_length)

        for i in range(max_eval_length, 0, -1):
            for evaluator in self.__evaluators:
                if len(evaluator) != i:
                    continue

                if evaluator in equation:
                    left_end = equation.find(evaluator)
                    right_start = left_end + len(evaluator)
                    eq_dict['eval'] = evaluator
                    eq_dict['left'] = equation[:left_end].strip()
                    eq_dict['right'] = equation[right_start:].strip()
                    break

            if eq_dict['eval'] is not None:
                break


        return eq_dict



    def to_eval_string(self):
        """ Converts the logic matrix into a string for eval(). """

        eval_string = None if not self.__logic_matrix else ''

        for i, row in enumerate(self.__logic_matrix):
            if i > 0:
                eval_string += ' and '

            substring = self.__evaluators[row['eval']]
            substring = substring.replace('{0}', row['left'])
            substring = substring.replace('{1}', row['right'])

            eval_string += substring

        return eval_string
