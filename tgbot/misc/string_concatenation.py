
class StringConcatenationCls:
    def __init__(self):
        self.concatenator = ''

    def merger(self, dish_name):
        self.concatenator += dish_name + '|'
        return self.concatenator


string_concatenation = StringConcatenationCls()
