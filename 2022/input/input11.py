from copy import copy


class Monkey:

    def __init__(self, initial_items, mod):
        self.initial_items = initial_items
        self.mod = mod

    def init(self):
        self.items = copy(self.initial_items)
        self.inspections = 0

    def compute(self, worry_level):
        raise Exception("Whoot?")

    def next_monkey(self, worry_level):
        raise Exception("Whoot?")


class Monkey0(Monkey):

    def __init__(self):
        super().__init__([92, 73, 86, 83, 65, 51, 55, 93], 11)

    def compute(self, worry_level):
        return worry_level * 5

    def next_monkey(self, worry_level):
        return 3 if worry_level % self.mod == 0 else 4


class Monkey1(Monkey):

    def __init__(self):
        super().__init__([99, 67, 62, 61, 59, 98], 2)

    def compute(self, worry_level):
        return worry_level * worry_level

    def next_monkey(self, worry_level):
        return 6 if worry_level % self.mod == 0 else 7


class Monkey2(Monkey):

    def __init__(self):
        super().__init__([81, 89, 56, 61, 99], 5)

    def compute(self, worry_level):
        return worry_level * 7

    def next_monkey(self, worry_level):
        return 1 if worry_level % self.mod == 0 else 5


class Monkey3(Monkey):

    def __init__(self):
        super().__init__([97, 74, 68], 17)

    def compute(self, worry_level):
        return worry_level + 1

    def next_monkey(self, worry_level):
        return 2 if worry_level % self.mod == 0 else 5


class Monkey4(Monkey):

    def __init__(self):
        super().__init__([78, 73], 19)

    def compute(self, worry_level):
        return worry_level + 3

    def next_monkey(self, worry_level):
        return 2 if worry_level % self.mod == 0 else 3


class Monkey5(Monkey):

    def __init__(self):
        super().__init__([50], 7)

    def compute(self, worry_level):
        return worry_level + 5

    def next_monkey(self, worry_level):
        return 1 if worry_level % self.mod == 0 else 6


class Monkey6(Monkey):

    def __init__(self):
        super().__init__([95, 88, 53, 75], 3)

    def compute(self, worry_level):
        return worry_level + 8

    def next_monkey(self, worry_level):
        return 0 if worry_level % self.mod == 0 else 7


class Monkey7(Monkey):

    def __init__(self):
        super().__init__([50, 77, 98, 85, 94, 56, 89], 13)

    def compute(self, worry_level):
        return worry_level + 2

    def next_monkey(self, worry_level):
        return 4 if worry_level % self.mod == 0 else 0


monkeys = [Monkey0(), Monkey1(), Monkey2(), Monkey3(), Monkey4(), Monkey5(), Monkey6(), Monkey7()]
