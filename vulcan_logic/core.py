""" The vulcan-logic core. """

class Logic:
    """ A logic string container. """

    def __init__(self, logic=None):
        """ LogicFrame class initialization. """
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
