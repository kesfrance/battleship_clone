#!/usr/bin/env python
from players import Player
from ship import Ship
from ship import SHIP_INFO


def shot_to_loci(shot):
    """converts user selection of locations to shoot
    into to a two value tuple representing a board location"""
    loc_dict = {}
    for i in range(26):
        loc_dict[chr(ord('A') + i)] = i
    sh_x = shot[:1]
    sh_y = int(shot[1:]) - 1
    return (sh_y, loc_dict[sh_x])


def clear_screen():
    """clears screen"""
    print("\033c", end="")


def get_ships(valid_ship_loci, track):
    """prompt user to select ship location, and orientation.
    validates user input and return ship details.
    """
    ship = []
    ship_prompt = "Set the location of the {} ({} spaces): ".format(
                            SHIP_INFO[track][0], SHIP_INFO[track][1])
    ship_loc = input(ship_prompt).strip().upper()
    if ship_loc in valid_ship_loci:
        ship = [SHIP_INFO[track][0], ship_loc, SHIP_INFO[track][1]]
        while True:
            orient = input("Is it horizontal? (Y/N):").strip().lower()
            if orient in ['y', 'n']:
                ship.append(orient != 'y' and 1 or 0)
                break
            else:
                print('input should be a letter "Y" or "N"')
                continue
    return ship


def place_ships_on_board(player):
    """prompts for target ship location and orientation from user,
    creates a ship object and stores all ships placed on the board"""
    xl_1 = player.get_valid_ship_loci()
    track = len(SHIP_INFO) - 1
    while True:
        if track < 0:
            break
        ship = get_ships(xl_1, track)
        if ship:
            name, location, size, orient = ship
            shipobj = Ship(name, location, size, orient)
            shipobj.set_ship_cordinates()
            if player.validate_ship_placement(shipobj):
                if player.update_board(shipobj):
                    player.track_allships_on_board(shipobj)
                    clear_screen()
                    player.print_board(1)
                    track -= 1
                else:
                    clear_screen()
                    print("Position already occupied; Try again")
                    player.print_board(1)
            else:
                clear_screen()
                player.print_board(1)
                print("The {} takes {} spaces. cant fit that location".format(
                                        shipobj.name, shipobj.size))
        else:
            clear_screen()
            player.print_board(1)
            print("That is not a valid location")
            print(player.invalid_loc_msg())
            continue
    clear_screen()
    player.print_board(1)


def game_loop(players):
    """clears screen and prompt for each players turn"""
    clear_screen()
    count = 0
    while True:
        clear_screen()
        print("#" * 20)
        print("{} your turn to start now".format(players[count].player_name))
        players[count].print_board(1)
        place_ships_on_board(players[count])
        if count > 0:
            break
        while True:
            clear_screen()
            inp = input("It's {} turn \n Press ENTER to continue".format(
                        format(players[count+1].player_name)))
            if not inp:
                clear_screen()
                count += 1
                break
            else:
                continue


def attack(players):
    killer = 0
    while True:
        opponent = killer != 1 and 1 or 0
        if players[0].occupied_cords and players[1].occupied_cords:
            clear_screen()
            players[killer].print_board(1)
            print("{} your board above".format(players[killer].player_name))
            print("\n")
            players[opponent].print_board(2)
            print("{} your turn to shoot now".format(
                                            players[killer].player_name))
            shot = input('Select location to shoot on the 2nd board below >')
            shot = shot.strip().upper()
            if shot in players[killer].get_valid_ship_loci():
                shot_cords = shot_to_loci(shot)
                print("boom!! shooting at {}'s ship".format(
                                            players[opponent].player_name))

                if shot_cords in players[opponent].occupied_cords:
                    print("Good shot!!. Thats a hit")
                    players[opponent].process_hit_shots(shot_cords)
                    players[killer].score += 5

                    if players[opponent].is_ship_sunk(shot_cords):
                        players[opponent].mark_ship_as_sunk()
                        print("You have sunk an entire ship. Great.!!!")

                elif shot_cords in players[opponent].already_shot_cords:
                    msg = input("already shot location. Try again. Hit ENTER")
                    if not msg or msg:
                        continue
                else:
                    players[opponent].process_missed_shot(shot_cords)
                    print("Noo!! that's a miss")

                # a prompt to let user press enter
                switch = input("Press ENTER for {} turn".format(
                                            players[opponent].player_name))
                if not switch:
                    pass
                killer += 1
                killer = (killer % 2)

            else:
                # a prompt to let user press enter
                prompt = input("Not a valid location. Hit ENTER to try again")
                if not prompt:
                    continue
        else:
            clear_screen()
            print("#" * 20)
            print("GAME OVER: FINAL SCORE BELOW")

            for ply in players:
                print(ply)
                print("{} Your board below".format(ply.player_name))
                ply.print_board(1)
                print("\n")

            if players[0].occupied_cords:
                print("Winner is {} Good job".format(players[0].player_name))
            else:
                print("Winner is {}. Great!!".format(players[1].player_name))
            break


if __name__ == "__main__":
    player_1 = Player()
    player_2 = Player()
    players = [player_1, player_2]
    game_loop(players)
    while True:
        clear_screen()
        prompt = input("All ships on board now. Hit ENTER to start attacking")
        if not prompt:
            break
        else:
            continue
    attack(players)
