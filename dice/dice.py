import random


class BaseDice:
    def __init__(self):
        self.dices = []

    @classmethod
    def roll(cls, *args, **kwargs):
        pass

    def value(self):
        pass


class Dice(BaseDice):
    def __init__(self):
        super().__init__()
        self.success = []

    def __str__(self):
        string = []
        for k, dice in enumerate(self.dices):
            if self.success[k]:
                string.append(str(dice))
            else:
                string.append(f"~~{dice}~~")

        return ', '.join(string)

    def value(self):
        total = 0
        for k, dice in enumerate(self.dices):
            if self.success[k]:
                total += dice

        return total

    @classmethod
    def roll(cls, number, sides):
        self = Dice()
        for _ in range(number):
            self.dices.append(random.randint(1, sides))
            self.success.append(True)

        return self

    def eq(self, number):
        # comparing if self.dice equals to number
        for key, dice in enumerate(self.dices):
            self.success[key] = dice == number

    def ge(self, number):
        # comparing if self.dice >= to number
        for key, dice in enumerate(self.dices):
            self.success[key] = dice >= number

    def gt(self, number):
        # comparing if self.dice > to number
        for key, dice in enumerate(self.dices):
            self.success[key] = dice > number

    def le(self, number):
        # comparing if self.dice <= to number
        for key, dice in enumerate(self.dices):
            self.success[key] = dice <= number

    def lt(self, number):
        # comparing if self.dice < to number
        for key, dice in enumerate(self.dices):
            self.success[key] = dice < number


class FateDice(BaseDice):
    # 1 - -1
    # 2 - -1
    # 3 - 0
    # 4 - 0
    # 5 - 1
    # 6 - 1

    def __str__(self):
        string = ""
        for dice in self.dices:
            if dice == -1:
                string += "-"

            elif dice == 0:
                string += "b"

            elif dice == 1:
                string += "+"

        return string

    def value(self):
        return sum(self.dices)

    @classmethod
    def roll(cls, number):
        self = FateDice()
        for _ in range(number):
            self.dices.append(random.randint(-1, 1))

        return self


# """ 6df """
# test = FateDice.roll(6)
# print(f"[6df  ]: {str(test)} = {test.value()}")
#
# """ 5d6 """
# test = Dice.roll(5, 6)
# print(f"[5d6  ]: {str(test)} = {test.value()}")
#
# """ 5d6=3 """
# test = Dice.roll(5, 6)
# test.eq(3)
# print(f"[5d6=3]: {str(test)} = {test.value()}")

