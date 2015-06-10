

class Operator(object):

    pass


class GreaterThan(Operator):

    def __str__(self):

        return '>'

    def evaluate(self, first, second):

        return first > second


class GreaterThanOrEqual(Operator):

    def __str__(self):

        return '>='

    def evaluate(self, first, second):

        return first >= second


class LessThan(Operator):

    def __str__(self):

        return '<'

    def evaluate(self, first, second):

        return first < second


class LessThanOrEqual(Operator):

    def __str__(self):

        return '<='

    def evaluate(self, first, second):

        return first <= second


class NotEqual(Operator):

    def __str__(self):

        return '!='

    def evaluate(self, first, second):

        return first != second


class Equal(Operator):

    def __str__(self):

        return '=='

    def evaluate(self, first, second):

        return first == second

