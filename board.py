#!/usr/bin/env python

"""
The board module.
    Contains a board class and other variables describing
    board specifications.
"""

import copy
import random
from ship import MARKERS

BOARD_SIZE = 10


class GameBoard:
    """ A class containing metods and properties of the
    board on which the game is played"""

    def __init__(self):
        self.boardsize = BOARD_SIZE
        self.board = [[MARKERS[5] for x in range(self.boardsize)]
                      for y in range(self.boardsize)]
        self.occupied_cords = set()
        self.attacked_board = copy.deepcopy(self.board)
        self.all_board_ships = {}
        self.already_shot_cords = set()
        self.sunk_ships = []

    def print_board_heading(self):
        """prints the board header"""
        print("   " + " ".join([chr(c) for c in range(ord('A'),
                                ord('A') + self.boardsize)]))

    def print_board(self, which):
        """prints a selected board to screen. which is a number (1 or 2)
        representating which board is t be printed"""
        bod = which == 1 and self.board or self.attacked_board
        self.print_board_heading()
        row_num = 1
        for row in bod:
            print(str(row_num).rjust(2) + " " + (" ".join(row)))
            row_num += 1

    def get_valid_ship_loci(self):
        """get valid locations a ship can occupy for a given boardsize"""
        x_loc = range(ord('A'), ord('A') + self.boardsize)
        y_loc = range(1, self.boardsize + 1)
        valid_shiploci = [''.join([chr(c), str(i)])
                          for c in x_loc for i in y_loc]
        return valid_shiploci

    def invalid_loc_msg(self):
        """set message to display when invalid board location is selected"""
        # set seed to be consistent with error message
        random.seed(100)
        vld = self.get_valid_ship_loci()
        err = "select between {} - {}. E,g: {}".format(vld[0], vld[-1],
                                                       random.sample(vld, 4))
        return err

    def validate_ship_placement(self, shipobj):
        """return true if user entry is a valid board location.
        Vertical ships are set from target location downwards on board.
        Horizontal ships are set from target location rightwards.
        """
        resp = set(shipobj.screen_name).issubset(self.get_valid_ship_loci())
        return resp

    def update_board(self, shipobj):
        """update the board with cordinates generated from user selected
        locations and orientation for a given ship"""
        if not self.validate_and_add_ship_cords(shipobj):
            return False
        else:
            for y_cord, x_cord in shipobj.cordinates:
                self.board[y_cord][x_cord] = shipobj.marker
            return True

    def validate_and_add_ship_cords(self, shipobj):
        """verify that ships don’t overlap with any
        existing ships o board.
        """
        if set(shipobj.cordinates).isdisjoint(self.occupied_cords):
            self.occupied_cords.update(shipobj.cordinates)
            return True
        else:
            return False

    def track_allships_on_board(self, shipobj):
        """keep track of all ships placed on the board. ship are stored
        as dictionary with ship name as keys.
        """
        shiptrack = [shipobj.cordinates, shipobj.size]
        shipname = shipobj.name.replace(" ", "_")
        self.all_board_ships[shipname] = shiptrack

    def is_ship_sunk(self, shot_cords):
        """accepts an array of cordinates and ship size. check if an
        entire ship is sunk, if yes update board with the right marker"""
        is_sunk = False
        for key in self.all_board_ships.keys():
            if shot_cords in self.all_board_ships.get(key)[0]:
                # for any positive hit, decrement the size marker by 1
                self.all_board_ships[key][-1] -= 1
                # a zero size marker means all ship cordinates have been shot
                if self.all_board_ships[key][-1] == 0:
                    self.sunk_ships.append(self.all_board_ships.get(key)[0])
                    del self.all_board_ships[key]
                    is_sunk = True
                    break
        return is_sunk

    def mark_ship_as_sunk(self):
        """set sunk ship maker if a shot sinks an entire ship"""
        for y_cords, x_cords in self.sunk_ships[-1]:
            self.board[y_cords][x_cords] = MARKERS[4]
            self.attacked_board[y_cords][x_cords] = MARKERS[4]

    def process_hit_shots(self, shot_cords):
        """checks if an opponents shot is valid and sets the ship marker of
        both the primary and secondary boards to indicate a positive hit"""
        self.occupied_cords.remove(shot_cords)
        self.already_shot_cords.add(shot_cords)
        y_cord, x_cord = shot_cords
        self.board[y_cord][x_cord] = MARKERS[3]
        self.attacked_board[y_cord][x_cord] = MARKERS[3]

    def process_missed_shot(self, shot_cords):
        """checks that a shot is a valid shot and marks a
        location as missed shot location for every missed shot"""
        self.already_shot_cords.add(shot_cords)
        y_cord, x_cord = shot_cords
        self.board[y_cord][x_cord] = MARKERS[2]
        self.attacked_board[y_cord][x_cord] = MARKERS[2]
