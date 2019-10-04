""" The pylogic core. """

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

        self.__weight = None
        self.evaluators = evaluators

        self.logic = logic_str
        self.weight = weight



    def __repr__(self):
        eval_string = ""
        for row in self.__equation_dict:
            tmp = self.__evaluators[row['eval']]
            tmp = tmp.replace('{0}', row['left'])
            tmp = tmp.replace('{1}', row['right'])

            eval_string += tmp + ' and '
        return None if eval_string == "" else eval_string[:-5]



    def __str__(self):
        """ Prints the parsed logic string in a readable format. """
        print_str = self.logic
        for key, value in self.__equation_dict.items():
            equation = self.__evaluators[value['eval']]
            equation = equation.replace('{0}', value['left'])
            equation = equation.replace('{1}', value['right'])
            print_str = print_str.replace('{' + key + '}', equation)

        return print_str



    @property
    def logic(self):
        """ Getter method returns parsed logic string. """
        return self.__logic_str



    @logic.setter
    def logic(self, logic_str):
        """ Creates parsed logic string and equation dictionary. """
        self.__logic_str, equations = parse_logic_string(logic_str)
        for key, equation in equations.items():
            equations[key] = self.split_equation(equation)

        self.__equation_dict = equations



    @property
    def evaluators(self):
        """ Getter method for the evaluators variable. """
        return self.__evaluators



    @evaluators.setter
    def evaluators(self, evals):
        """ Setter method for the evaluators variable.

        Only adding to or modifiying evaluators in the base set is supported.
        """
        self.__evaluators.update(evals)



    def _set_weight(self, weight=None):
        """ Calculates the weight of the Logic string.

        By default, Logic weight is calculated as the number of equations
        within the logic string. Future versions should allow field names
        to contribute varying weights.
        """

        if weight is None:
            self.__weight = len(self.__equation_dict)
        else:
            self.__weight = weight



    @property
    def weight(self):
        """ Gets or sets the weight of the Logic String. """
        return self.__weight



    @weight.setter
    def weight(self, weight):
        return self._set_weight(weight)



    @staticmethod # astype(var, conv_type)
    def astype(var, conv_type):
        """ Converts a variable to a given type. """

        # If variable is already of conv_type, return immediately
        if isinstance(var, conv_type) or var is None:
            return var

        # Check that conv_type is actually a type.
        if isinstance(conv_type, type):
            try:
                return conv_type(var)
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
            equations = self.replace_variables(dictionary)
        else:
            equations = self.__equation_dict

        for _, equation in equations.items():
            eval_string = self.to_eval_string(equation)
            try:
                equation['validity'] = eval(eval_string) #pylint: disable=eval-used
            except NameError:
                equation['validity'] = eval_string

        validity_str = self.logic

        for key, equation in equations.items():
            key = '{' + key + '}'
            validity_str = validity_str.replace(key, str(equation['validity']))

        print(validity_str)
        try:
            return eval(validity_str) #pylint: disable=eval-used
        except NameError:
            return validity_str



    def replace_variables(self, dictionary):
        """ Replaces variables within an equation with values from a dict. """

        equations = copy.deepcopy(self.__equation_dict)
        for _, equation in equations.items():
            for key, value in dictionary.items():
                if equation['left'] == key:
                    equation['left'] = value

                if equation['right'] == key:
                    equation['right'] = value

        return equations



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

    if var in [None, type(None)]:
        return ''

    if isinstance(var, type):
        return str(var)[8:-2].replace('__main__.', '')
    return str(type(var))[8:-2].replace('__main__.', '')



def parse_logic_string(logic_str):
    """ Parses a logic string into equations and logic operators."""

    # Subsitute commas for "and" statements. (Backwards compatibility)
    logic_str = '(' + logic_str + ')'
    logic_str = logic_str.replace(', ', ') and (')
    logic_str = logic_str.replace(',', ') and (')

    # Loop over logic string, marking the positions of logical operators.
    i = 0
    logic_pos = []
    while i < len(logic_str):
        if logic_str[i] in ['(', ')']:
            logic_pos.append(i)
        elif logic_str[i - 1:i + 4] == ' and ':
            for k in range(5):
                logic_pos.append(i - 1 + k)
        elif logic_str[i - 1:i + 3] == ' or ':
            for k in range(4):
                logic_pos.append(i - 1 + k)
        i += 1

    # Build a dictionary of equations between logical operators.
    i = 0
    logic_counter = 0
    logic_dict = {}
    prev_pos = 0
    for pos in logic_pos:
        if pos - prev_pos > 1:
            logic_dict[str(logic_counter)] = logic_str[prev_pos + 1:pos]
            logic_counter += 1

        prev_pos = pos

    # Substitute equations for dictionary values.
    for key, value in logic_dict.items():
        logic_str = logic_str.replace(value, '{' + key + '}')

    return logic_str, logic_dict
