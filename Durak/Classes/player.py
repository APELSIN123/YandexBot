from ..decks import *


class Player:
    def __init__(self, telegram_id: int, hand: list, index: int):
        """
        :param telegram_id: id по телеграмму
        :param hand: колода у игрока
        :param index: индекс игрока (начинается с 0)
        """
        self.telegram_id = telegram_id
        self.hand = hand
        self.index = index

    def take_card(self, card: Card):
        """
        Добавляет карту в руку
        :param card: карта, которую нужно взять
        """
        self.hand.append(card)

    def delete_card(self, card: Card) -> Card or None:
        """
        Проверяет карты на наличие и удаляет
        :param card: карта, которую надо удалить
        :return: удалённую карту или ничего, если удалять было нечего
        """
        if card not in self.hand:
            return None

        del self.hand[self.hand.index(card)]
        return card

    def sort_hand(self, type_of_deck: str):
        """
        Сортирует карты относительно расположения в decks.py
        :param type_of_deck: тип колоды 24, 36 или 52
        """
        if type_of_deck == "24":
            self.hand.sort(key=lambda x: small_deck.index(x))
        if type_of_deck == "36":
            self.hand.sort(key=lambda x: basic_deck.index(x))
        if type_of_deck == "52":
            self.hand.sort(key=lambda x: poker_deck.index(x))

    def beat_check(self, field: dict, trump_color: str) -> dict:
        """
        Проверяет возможность побить карты
        :param field: игровое поле с картами
        :param trump_color: козырь
        :return: словарь атакующая карта - варианты побить
        """
        options = {}
        for attack in dict.keys():
            options[attack] = []
            for card in self.hand:
                if attack.color == card.color and card >= attack:
                    options[attack].append(card)
                elif card.color == trump_color and attack.color != trump_color:
                    options[attack].append(card)
        return options

    def append_check(self, field: dict) -> dict:
        """
        Проверяет возможность добавить карты на поле
        :param field: игровое поле с картами
        :return: карта с поля - возможные варианты подкидных карт
        """
        options = {}
        for i in field.items():
            for j in i:
                options[j] = []
                for card in self.hand:
                    if card == j:
                        options[j].append(card)
        return options


    def __getitem__(self, item: int) -> Card:
        return self.hand[item]
