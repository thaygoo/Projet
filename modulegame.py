#-*- coding: utf-8 -*-
import blessed, math, os, time
term = blessed.Terminal()

# other functions
def config(file):
    config = {
        1:{'alpha': '', 'omega': '', 'normal': []}, 
        2:{'alpha': '', 'omega': '', 'normal': []}, 
        "food":{'berries': [], 'apples': [], 'mice': [], 'rabbits': [], 'deers': []}, 
        'map':()
    } # Dictionnary of the configuration file

    with open(file) as fp: # Open the file
        line = fp.readline()
        while line:
            if 'map:' in line: # Is map in the line ? 
                line = fp.readline() 
                line = line.rsplit(" ") # Split coo's
                line[1] = line[1].rstrip("\n") # Keep only the coo's
                config['map'] = line 

            elif 'werewolves:' in line: # is wolve in the line ?
                line = fp.readline()
                while 'foods:' not in line: # Is food in the line ?
                    if 'alpha' in line or 'omega' in line: 
                        config[int(line[0])][line.split(' ')[3].rstrip("\n")] = [int(line.split(' ')[1]), int(line.split(' ')[2]), int(100)]
                    else:
                        config[int(line[0])]['normal'].append([int(line.split(' ')[1]), int(line.split(' ')[2]), int(100)])
                    line = fp.readline()

            elif 'berries' in line or 'apples' in line or 'mice' in line or 'rabbits' in line or 'deers' in line:
                config['food'][line.split(' ')[2]].append([int(line.split(' ')[0]), int(line.split(' ')[1]), int(line.split(' ')[3])])
               
            line = fp.readline()
    return config

def coos(x, y):
    home = int(term.width/2) - int(((4 * 20)+1)/2)
    x = home+(2+(4*(x-1)))
    y = (y*2)-1
    return x, y

def board(color):
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
    width = int(config('map.ano')['map'][0])
    height = int(config('map.ano')['map'][1])

    # background + cursor + clear + hide cursor + term.on_darkslategray4
    print(term.home + term.clear + term.on_dimgrey)

    #Printing the board
    #centered manualy
    center = int(term.width/2) - int(((4 * width)+1)/2)

    #header
    print(term.move_xy(center, 0) + color + '╔' + 3 * '═' + (int(width) - 1) * ('╦' + 3 * '═') + '╗', end='')
    print(term.move_xy(center, 1) + color + '║' + width * (3 * ' ' + '║'), end='')

    #body
    y = 2
    for i in range(height - 1):
        print(term.move_xy(center, i + y) + color + '╠' + (int(width) - 1) * (3 * '═' + '╬') + 3 * '═' + '╣', end='')
        y += 1
        print(term.move_xy(center, i + y) + color + '║' + width * (3 * ' ' + '║'), end='')
        
    #foot
    print(term.move_xy(center, height*2) + color + '╚' + 3 * '═' + (int(width) - 1) * ('╩' + 3 * '═') + '╝', end='')

    #placing objects



#------------------------------------------------------------------------------------------------------------------------------------------------------------------------


board(term.gold)

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