#!/usr/bin/env python

"""
The players Module:
    Contains the player class for producing player objects.
"""

from board import GameBoard


class Player(GameBoard):
    """Contains methods for setting and getting player names and
    player scores. Inherits methods from the players Gameboard class.
    """

    plyer_num = 1

    def __init__(self):
        super(Player, self).__init__()
        self.player_name = self.set_player_name()
        self.score = 0

    def set_player_name(self):
        """Propmt for player name and set to variable"""
        name_prmpt = "Enter Name for Player_{}: ".format(self.get_plyr_num())
        while True:
            name = input(name_prmpt).strip().lower()
            if not name.isalnum():
                print("valid name should consist numbers and letters only")
                continue
            else:
                self.set_plyr_num()
                break
        return name.title()

    def __str__(self):
        """string reprsentation of player. returns player name
        and player score"""
        return "{}: {} points".format(self.player_name,
                                      self.score)

    @classmethod
    def get_plyr_num(cls):
        """class method to set player number. eg. player number 1
        or player number 2"""
        return cls.plyer_num

    @classmethod
    def set_plyr_num(cls):
        """class method to get player number. eg. player number 1
        or player number 2"""
        cls.plyer_num += 1
