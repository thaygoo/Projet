#-*- coding: utf-8 -*-
import blessed, math, os, time
term = blessed.Terminal()

# other functions
def config():

    return

def board(width, height, color):
    """Creation of the board, place all the things on it.

    Parameters
    ----------
    width (int) : width of the board
    height (int) : height of the board
    color (str) : color of the board

    Return
    ------
    plate (dic) : board
    dic (dic) : everything, like berry or wolves

    Version
    -------
    specification: Hugo (v2 28/02/22)
    """
    # background + cursor + clear + hide cursor
    print(term.on_darkslategray4 + term.home + term.clear + term.hide_cursor)

    #header
    print(term.center(color + '\u2554' + 3 * '\u2550' + (int(width) - 1) * ('\u2566' + 3 * '\u2550') + '\u2557'))
    print(term.center(color + '\u2551' + width * (3 * '\u0020' + '\u2551')))

    #body
    for i in range(height - 1):
        print(term.center(color + '\u2560' + (int(width) - 1) * (3 * '\u2550' + '\u256C') + 3 * '\u2550' + '\u2563'))
        print(term.center(color + '\u2551' + width * (3 * '\u0020' + '\u2551')))
        
    #foot
    print(term.center(color + '\u255A' + 3 * '\u2550' + (int(width) - 1) * ('\u2569' + 3 * '\u2550') + '\u255D'))


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------




# main function
def play_game(map_path, group_1, type_1, group_2, type_2):
    """Play a game.
    
    Parameters
    ----------
    map_path: path of map file (str)
    group_1: group of player 1 (int)
    type_1: type of player 1 (str)
    group_2: group of player 2 (int)
    type_2: type of player 2 (str)
    
    Notes
    -----
    Player type is either 'human', 'AI' or 'remote'.
    
    If there is an external referee, set group id to 0 for remote player.
    
    """
    
    #...
    #...
    #...

    # create connection, if necessary
    """ if type_1 == 'remote':
        connection = create_connection(group_2, group_1)
    elif type_2 == 'remote':
        connection = create_connection(group_1, group_2) """

    #...
    #...
    #...

    #while ...:
    
    #    ...
    #    ...
    #    ...

        # get orders of player 1 and notify them to player 2, if necessary
""" if type_1 == 'remote':
            orders = get_remote_orders(connection)
        else:
            orders = get_AI_orders(..., 1)
            if type_2 == 'remote':
                notify_remote_orders(connection, orders)
        
        # get orders of player 2 and notify them to player 1, if necessary
        if type_2 == 'remote':
            orders = get_remote_orders(connection)
        else:
            orders = get_AI_orders(..., 2)
            if type_1 == 'remote':
                notify_remote_orders(connection, orders) """
        
        #...
        #...
        #...

    # close connection, if necessary
""" if type_1 == 'remote' or type_2 == 'remote':
        close_connection(connection) """
        
    #...
    #...
    #...