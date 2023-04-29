from .card import Card


class Deck:
    def __init__(self, deck: list, shuffled_deck: list):
        """
        :param deck: Колода
        :param shuffled_deck: Перетасованная колода
        :param trump_color: Козырь
        """
        self.deck = deck
        self.shuffled_deck = shuffled_deck

    def __call__(self) -> list:
        return self.shuffled_deck

    def __getitem__(self, item: int) -> Card:
        return self.shuffled_deck[item]

    def pop_card(self) -> Card:
        """
        Достаёт карту из колоды, карта удаляется из списка
        :return: Карта из колоды
        """
        self.shuffled_deck.pop(0)
        return self.shuffled_deck[0]

    def set_trump(self):
        print(self.shuffled_deck[-1])
        self.trump_color = self.shuffled_deck[-1].color

