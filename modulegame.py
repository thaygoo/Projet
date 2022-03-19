import blessed
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
        'map':(),
        'pacify': []
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
    home = int(term.width/2) - int(((4 * int(dictionnary['map'][1]))+1)/2)
    x = home+(2+(4*(int(x)-1)))
    y = (int(y)*2)-1
    return int(x), int(y) + 1 

def display():
    """Deals a problem encounter while displaying the final board.

    Version
    -------
    specification: Hugo (v1 08/03/22)
    """
    print(term.normal + term.move_xy(int((4 * 20)+1), int((2 * 20)+2)) + ' ')

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
    print(term.home)

    #centered manualy
    center = int(term.width/2) - int(((4 * width)+1)/2)

    #coordinate numbers
    for i in range(0, int(dictionnary['map'][0])+1, 5): # X 
        print(term.normal + term.bold + term.move_xy(coordinate(i, 0)[0], 0) + color + f'{i}')

    for i in range(0, int(dictionnary['map'][1])+1, 5): # Y
        print(term.move_xy(int(term.width/2) - int(((4 * int(dictionnary['map'][0]))+1)/2)-2, (i*2)) + f'{i}')

    #header
    print(term.on_gray25 + term.move_xy(center, 1) + color + '╔' + 3 * '═' + (int(width) - 1) * ('╦' + 3 * '═') + '╗', end='')
    print(term.move_xy(center, 2) + color + '║' + width * (3 * ' ' + '║'), end='')

    #body
    y = 3
    for i in range(height-1):
        print(term.move_xy(center, i + y) + color + '╠' + (int(width) - 1) * (3 * '═' + '╬') + 3 * '═' + '╣', end='')
        y += 1
        print(term.move_xy(center, i + y) + color + '║' + width * (3 * ' ' + '║'), end='')
        
    #foot
    print(term.move_xy(center, (height*2)+1) + color + '╚' + 3 * '═' + (int(width) - 1) * ('╩' + 3 * '═') + '╝', end='')

    #placing objects
    #place foods
    for j in ['berries', '\N{CHERRIES}'], ['apples', '\N{RED APPLE}'], ['mice', '\N{RAT}'], ['rabbits', '\N{RABBIT FACE}'], ['deers', '\N{OX}']: 
        for i in dictionnary['food'][j[0]]:
            # Display foods
            print(term.move_xy(*coordinate(*i[:2])) + j[1])
            # Display energy of foods
            print(term.move_xy((coordinate(*i[:2])[0])-1, (coordinate(*i[:2])[1])+1) + term.turquoise + f'{i[2]}')

    #Placing Alphas :
    for i in ['alpha', "α"], ['omega', "Ω"]:
        for j in [1, term.bold_red], [2, term.bold_green]:
            # display alpha and omega
            print(term.move_xy(*coordinate(*dictionnary[j[0]][i[0]][:2])) + j[1] + i[1])
            # display energy
            print(term.move_xy((coordinate(*dictionnary[j[0]][i[0]][:2])[0])-1, (coordinate(*dictionnary[j[0]][i[0]][:2])[1])+1) + j[1] + '%d' % (dictionnary[j[0]][i[0]][2]))

    # Placing normal wolves:
    for j in [1, term.bold_red], [2, term.bold_green]:
        for i in dictionnary[j[0]]['normal']:
            # display normal wolves
            print(term.move_xy(*coordinate(*i[:2])) + j[1] + "⦿")
            # display energy of them
            print(term.move_xy((coordinate(*i[:2])[0])-1, (coordinate(*i[:2])[1])+1) + j[1] + f'{i[2]}')
    
    display()

def get_human_orders(player):
    """Creation of the board, place all the things on it.

    Parameters
    ----------
    player (int) : player 1 or 2

    Version
    -------
    specification: Hugo (v1 10/03/22)

    Return
    ------
    orders (list) : Return the orders on a list

    Examples
    --------
    12-12:@12-13 12-14:*12-13 10-10:pacify
    """
    orders = []
    p = input(term.move_xy(*coordinate(0, 22)) + "Joueur %d, entrez vos ordres: " % player)

    for i in range(len(p.rsplit(" "))):
        orders.append(p.rsplit(" ")[i])

    return orders

def nexturn():
    """Check if Alpha Wolves have enough health to continue

    Return
    ------

    Version
    -------
    specification: Marius (v1 17/02/22)
    """
    if dictionnary[1]["alpha"][2] <= 0 or dictionnary[2]["alpha"][2] <=0:
        return False
    else:
        return True

def find(coos):
    for y in [0, 1]: 
        for i in ['alpha', 'omega']:
            for j in [1, 2]:
                if dictionnary[j][i][0] == int(coos[0]) and dictionnary[j][i][1] == int(coos[1]):
                    return [j, i]

        for j in [1, 2]:
            for i in range(len(dictionnary[j]['normal'])):
                if dictionnary[j]['normal'][i][0] == int(coos[0]) and dictionnary[j]['normal'][i][1] == int(coos[1]):
                    return [j, 'normal', i]

def move(orders, team): #3-3:@4-3
    for order in orders:
        if '@' in order:
        #Filters moving orders
            order=order.rsplit(':@')
            for i in range(2):
                order[i] = order[i].split('-')
            
            if int(order[0][1])-int(order[1][1]) in [-1,0,1] and int(order[0][0])-int(order[1][0]) in [-1,0,1]:
                if 0<int(order[1][0])<21 and 0<int(order[1][1])<21:
                #Checks if the final position isn't too far
                    
                    index = find(order[0])
                    if index[0] == team:
                        if len(index) > 2:
                            dictionnary[index[0]][index[1]][index[2]][:2] = order[1]
                        else:
                            dictionnary[index[0]][index[1]][:2] = order[1]
                    else:
                        print ("Error: Please be sure to use the good wolves")
                #Moving to new coordinates
                else:
                    print ("Error: Out of bounds")
            else:
                print ("Error: you cannot go there")
    board(int(dictionnary['map'][0]), int(dictionnary['map'][1]), term.gold)

def distance(pos1, pos2): # UNDER DEVELOPPEMENT
    """Calculate the distance between two different object.

    Parameters
    ----------
    pos1, pos2 (list) : Positions of the objects

    Version
    -------
    specification: Mathis (v1 17/02/22)

    1(r1, c1) 2(r2, c2)   (r2 - r1) , (c2 - c1)

    """

    pos1 = pos1.split('-')

    return [(pos2[0] - pos1[0]), (pos2[1] - pos1[1])]

def pacify(order):
    """Pacification of the omega wolve

    Parameters
    ----------


    Version
    -------
    specification: Hugo (v2 28/02/22)
    """
    #Tous les loups du plateau à condition qu'ils se trouvent à 6 cases de distance, cout de la chose, 40 énergy pour pacifier un tour.



    return

def bonus():
    """Manage bonuses

    Version
    -------
    specification: Mathis (v1 17/02/22)
    """
    
    return

def feeding():
    """Manage bonuses

    Version
    -------
    specification: Mathis (v1 17/02/22)
    """
    
    return

def fighting():
    """Manage bonuses

    Version
    -------
    specification: Mathis (v1 17/02/22)
    """

    return

#---------------------------------------------------------------------------------------------------------------------------------

print(term.home + term.clear)

dictionnary = config('map.ano')

#board(int(dictionnary['map'][0]), int(dictionnary['map'][1]), term.gold)

print(distance([5, 5], [2, 2]))

""" 
orders = get_human_orders(1)
move(orders, 1) """



# main function
def play_game(group_1, type_1, group_2, type_2, configfile):
    """Play a game.
    
    Parameters
    ----------
    configfile: path of the config file.
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