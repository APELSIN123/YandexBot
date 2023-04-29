from .deck import Deck
from .player import Player
from ..decks import *
import random


class Game:
    def __init__(self, n_players: int, deck: list):
        self.n_players = n_players
        self.players = []
        self.deck = Deck(deck.copy(), random.shuffle(deck.copy()))
        self.deck.set_trump()
        self.trump_color = self.deck.trump_color
        self.field = {}

    def add_player(self, telegram_id: int, index: int):
        hand = []
        for i in range(6):
            hand.append(self.deck.pop_card())
        self.players.append(Player(telegram_id, hand, index))

    def attack(self, card: Card, index: int):
        defender = self.players[(index + 1) % self.n_players]
        if len(self.field) < 6 and len(self.field) < len(defender.hand):
            attacker = self.players[index]
            attack_card = attacker.delete_card(card)
            if attack_card:
                self.field[attack_card] = None

    def beat(self, attack_card: Card, defend_card: Card):
        if not self.field[attack_card]:
            defender = self.players[(self.attacker_index + 1) % self.n_players]
            beat_options = defender.beat_check(self.field, self.trump_color)
            if defend_card in beat_options[attack_card]:
                self.field[attack_card] = defender.delete_card(defend_card)

    def append(self, append_card: Card, index: int, defender: Player):
        if len(self.field) < 6 and len(self.field) < len(defender.hand):
            appender = self.players[index]
            if append_card in appender.append_check(self.field):
                self.field[append_card] = None

    def check_endgame(self):
        if self.deck:
            return False
        return True