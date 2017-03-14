#!/usr/bin/env python

"""
The ship module.
Contains the ship class and other variables that describe the ship object.
"""


SHIP_INFO = [
    ("Aircraft Carrier", 5),
    ("Battleship", 4),
    ("Submarine", 3),
    ("Cruiser", 3),
    ("Patrol Boat", 2)
]

# ship markers to mark the state of ship on boards
VERTICAL_SHIP = '|'
HORIZONTAL_SHIP = '-'
EMPTY = 'O'
MISS = '.'
HIT = '*'
SUNK = '#'

MARKERS = [VERTICAL_SHIP, HORIZONTAL_SHIP, MISS, HIT, SUNK, EMPTY]


class Ship:
    """Contain methods for setting and getting various ship specifications.
    Before and when placed on the playing boards.
    """

    def __init__(self, name, location, size, orient):
        self.name = name
        self.size = size
        self.target_location = location
        self.orientation = orient
        self.cordinates = []
        self.screen_name = []
        self.marker = orient != 0 and VERTICAL_SHIP or HORIZONTAL_SHIP

    def set_ship_cordinates(self):
        """generates and set ship cordinates using user selected board
        locations, size and ship orientation.
        """
        # create a lookup dict, mapping alphabets to board indices, eg A:0
        loc_dict = {}
        for i in range(26):
            loc_dict[chr(ord('A') + i)] = i
        hx_1 = self.target_location[:1]
        hy_1 = self.target_location[1:]
        # a horizontal ship placement
        if self.orientation == 0:
            self.cordinates = [(int(hy_1) - 1, loc_dict[chr(c)]) for c in
                               range(ord(hx_1), ord(hx_1) + self.size)]
            self.screen_name = [''.join([chr(c), hy_1]) for c in
                                range(ord(hx_1), ord(hx_1) + self.size)]
        # a vertical ship placement
        else:
            self.cordinates = [(d - 1, loc_dict[hx_1]) for d in
                               range(int(hy_1), int(hy_1) + self.size)]
            self.screen_name = [''.join([hx_1, str(d)]) for d in
                                range(int(hy_1), int(hy_1) + self.size)]

    def __str__(self):
        """string representation of the ship object
        returns ship name and ship size"""
        return "The {}, with size of {} ".format(self.name, self.size)
