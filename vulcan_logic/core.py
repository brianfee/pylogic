""" The vulcan-logic core. """

class Logic:
    """ A logic string container. """

    def __init__(self, logic=None):
        """ Logic class initialization. """
        self.logic_matrix = self.set_logic_matrix(logic)



    def __str__(self):
        """ Prints the logic_matrix in a readable format. """
        print_str = ''
        for row in self.logic_matrix:
            print_str += row['left'] + ' '
            print_str += row['eval'] + ' '
            print_str += row['right'] + '\n'
        return print_str



    def set_logic_matrix(self, logic):
        """ Takes a logic string and expands it into an n x 3 matrix. """

        equations = [equation.strip() for equation in logic.split(',')]
        equations_matrix = []
        for equation in equations:
            equations_matrix.append(self.split_equation(equation))

        return equations_matrix



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

        eval_string = None if not self.logic_matrix else ''

        for i, row in enumerate(self.logic_matrix):
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
