#-*- coding: utf-8 -*-
import blessed, time
term = blessed.Terminal()

# other functions
def config(file):
    """Get the data of the config file and create a dictionnary with it.

    Parameters
    ----------
    file (str) : name of the config file 

    Version
    -------
    specification: Hugo (v2 28/02/22)
    """
    config = {
        1:{'alpha': '', 'omega': '', 'normal': []}, 
        2:{'alpha': '', 'omega': '', 'normal': []}, 
        "food":{'berries': [], 'apples': [], 'mice': [], 'rabbits': [], 'deers': []}, 
        'map':()
    }

    with open(file) as fp:
        line = fp.readline()
        while line:
            if 'map:' in line:
                line = fp.readline()
                line = line.rsplit(" ")
                line[1] = line[1].rstrip("\n")
                config['map'] = line

            elif 'werewolves:' in line:
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

def coordinate(x, y):
    """Transfer simple coordinate into real coordinate of the plate.

    Parameters
    ----------
    x, y (int): x, y simples coordinates 

    Return
    ------
    x, y (int): x, y real coordinates

    Version
    -------
    specification: Hugo (v1 08/03/22)
    """
    home = int(term.width/2) - int(((4 * 20)+1)/2)
    x = home+(2+(4*(x-1)))
    y = (y*2)-1
    return x, y

def display():
    """Deals a problem encounter while displaying the final board.

    Version
    -------
    specification: Hugo (v1 08/03/22)
    """
    print(term.normal + term.move_xy(int((4 * 20)+1), int((2 * 20)+1)) + ' ')

def board(width, height, color):
    """Creation of the board, place all the things on it.

    Parameters
    ----------
    width (int) : width of the board
    height (int) : height of the board
    color (str) : color of the board

    Version
    -------
    specification: Hugo (v2 28/02/22)
    """

    # background + cursor + clear + hide cursor + term.on_darkslategray4
    print(term.home + term.clear + term.on_dimgrey)

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
    #Placing Alphas :
    for i in ['alpha', "α"], ['omega', "Ω"]:
        for j in [1, term.bold_red], [2, term.bold_green]:
            # display alpha and omega
            print(term.move_xy(*coordinate(*config('map.ano')[j[0]][i[0]][:2])) + j[1] + i[1])
            # display energy
            print(term.move_xy((coordinate(*config('map.ano')[j[0]][i[0]][:2])[0])-1, (coordinate(*config('map.ano')[j[0]][i[0]][:2])[1])+1) + j[1] + '%d' % (config('map.ano')[j[0]][i[0]][2]))

    # Placing normal wolves:
    for j in [1, "\u29BF", term.bold_red], [2, "\u29BF", term.bold_green]:
        for i in config('map.ano')[j[0]]['normal']:
            # display normal wolves
            print(term.move_xy(*coordinate(*i[:2])) + j[2] + j[1])
            # display energy of them
            print(term.move_xy((coordinate(*i[:2])[0])-1, (coordinate(*i[:2])[1])+1) + j[2] + '%d' % (i[2]))

    #place foods
    for j in ['berries', '\N{CHERRIES}'], ['apples', '\N{RED APPLE}'], ['mice', '\N{RAT}'], ['rabbits', '\N{RABBIT FACE}'], ['deers', '\N{OX}']: 
        for i in config('map.ano')['food'][j[0]]:
            # Display foods
            print(term.move_xy(*coordinate(*i[:2])) + j[1])
            # Display energy of foods
            print(term.move_xy((coordinate(*i[:2])[0])-1, (coordinate(*i[:2])[1])+1) + term.turquoise + '%d' % (i[2]))
    
    display()



#------------------------------------------------------------------------------------------------------------------------------------------------------------------------


board(20, 20, term.gold)

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