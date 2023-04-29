class Card:
    def __init__(self, number: str, color: str):
        """
        :param number: значение
        :param color: масть
        """
        self.number = number
        self.color = color

    def __call__(self) -> tuple:
        return (self.number, self.color)

    def __repr__(self):
        return f'{self.number}{self.color}'

    def __gt__(self, other) -> bool:
        """
        :return: Результат равнения по значению
        """
        number1 = self.number
        number2 = other.number

        if number1 == "J": number1 = 11
        elif number1 == "Q": number1 = 12
        elif number1 == "K": number1 = 13
        elif number1 == "T": number1 = 14
        else: number1 = int(number1)

        if number2 == "J": number2 = 11
        elif number2 == "Q": number2 = 12
        elif number2 == "K": number2 = 13
        elif number2 == "T": number2 = 14
        else: number2 = int(number2)

        return number1 > number2

    def __eq__(self, other) -> bool:
        """
        :return: Результат равнения по значению
        """
        number1 = self.number
        number2 = other.number

        if number1 == "J": number1 = 11
        elif number1 == "Q": number1 = 12
        elif number1 == "K": number1 = 13
        elif number1 == "T": number1 = 14
        else: number1 = int(number1)

        if number2 == "J": number2 = 11
        elif number2 == "Q": number2 = 12
        elif number2 == "K": number2 = 13
        elif number2 == "T": number2 = 14
        else: number2 = int(number2)

        return number1 == number2