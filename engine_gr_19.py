import blessed, time
from random import *

from urllib3 import Retry
term = blessed.Terminal()

# other functions
def config(file):
    """Get the data from the config file and create a dictionnary with it.

    Parameters
    ----------
    file (str) : name of the config file 

    Version
    -------
    specification: Hugo (v3 28/02/22)
    """
    config = {
        1:{'alpha': '', 'omega': '', 'normal': []}, 
        2:{'alpha': '', 'omega': '', 'normal': []}, 
        "food":{'berries': [], 'apples': [], 'mice': [], 'rabbits': [], 'deers': []}, 
        'map':(),
        'pacify': [],
        'wolfplayed': [],
        'saved_energy': {},
        'rounds': [0, False, 0] 
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
                        config[int(line[0])][line.split(' ')[3].rstrip("\n")] = [int(line.split(' ')[1]), int(line.split(' ')[2]), int(100), 0]
                    else:
                        config[int(line[0])]['normal'].append([int(line.split(' ')[1]), int(line.split(' ')[2]), int(100), 0])
                    line = fp.readline()

            elif 'berries' in line or 'apples' in line or 'mice' in line or 'rabbits' in line or 'deers' in line:
                config['food'][line.split(' ')[2]].append([int(line.split(' ')[0]), int(line.split(' ')[1]), int(line.split(' ')[3])])
               
            line = fp.readline()
    return config

def coordinate(x, y):
    """Transfer simple coordinates into real coordinate of the plate.

    Parameters
    ----------
    x, y (int): x, y simples coordinates (coordinates of the BOARD)

    Return
    ------
    x, y (int): x, y real coordinates (coordinates in CHARACTERS)

    Version
    -------
    specification: Mathis - Malo (v2 08/03/22)
    """
    home = int(term.width/2) - int(((4 * int(dictionnary['map'][1]))+1)/2)
    x = home+(2+(4*(int(x)-1)))
    y = (int(y)*2)-1
    return int(x), int(y) + 1 

def board(width, height, color):
    """Creation of the board, placing all the things on it.

    Parameters
    ----------
    width (int) : width of the board
    height (int) : height of the board
    color (str) : color of the board

    Version
    -------
    specification: Hugo - Malo (v3 28/02/22)
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
            if dictionnary[j[0]][i[0]][2] <= 0: # Human ?
                # display alpha and omega
                print(term.move_xy(*coordinate(*dictionnary[j[0]][i[0]][:2])) + j[1] + '᙭')
                # display energy
                print(term.move_xy((coordinate(*dictionnary[j[0]][i[0]][:2])[0])-1, (coordinate(*dictionnary[j[0]][i[0]][:2])[1])+1) + j[1] + '%d' % (dictionnary[j[0]][i[0]][2]))
            else:
                # display alpha and omega
                print(term.move_xy(*coordinate(*dictionnary[j[0]][i[0]][:2])) + j[1] + i[1])
                # display energy
                print(term.move_xy((coordinate(*dictionnary[j[0]][i[0]][:2])[0])-1, (coordinate(*dictionnary[j[0]][i[0]][:2])[1])+1) + j[1] + '%d' % (dictionnary[j[0]][i[0]][2]))

    # Placing normal wolves:
    for j in [1, term.bold_red], [2, term.bold_green]:
        for i in dictionnary[j[0]]['normal']:
            if i[2] <= 0:
                # display normal wolves
                print(term.move_xy(*coordinate(*i[:2])) + j[1] + "᙭")
                # display energy of them
                print(term.move_xy((coordinate(*i[:2])[0])-1, (coordinate(*i[:2])[1])+1) + j[1] + f'{i[2]}')
            else:
                # display normal wolves
                print(term.move_xy(*coordinate(*i[:2])) + j[1] + "⦿")
                # display energy of them
                print(term.move_xy((coordinate(*i[:2])[0])-1, (coordinate(*i[:2])[1])+1) + j[1] + f'{i[2]}')

    # Rounds
    print(term.normal + term.move_xy(coordinate(1, 0)[0], 2+(2*int(dictionnary['map'][1]))) + term.bold + color + "Rounds %d " % dictionnary['rounds'][0])

def get_human_orders(player):
    """Input asking for human orders using a specific format and associate orders with adequate function
    Input model :
    (Coordinates of the wolf receiving orders):(order)(coordinates of the target)
        @ = moving order
        < = eating order
        * = fighting order
        'pacify' = pacify order
        
    Parameters
    ----------
    player (int) : player 1 or 2

    Return
    ------
    orders (list) : Return the orders on a list

    Examples
    --------
    3-2:@4-2 1-1:*1-2 2-3:@2-4 3-3:<4-4 

    Version
    -------
    specification: Marius (v4 18/03/22)
    """
    orders = {
        'pacify' : [],
        'feed' : [],
        'fight' : [],
        'move' : []
    }
    p = input(term.normal + term.move_xy(coordinate(0, 0)[0], 5+(2*int(dictionnary['map'][1]))) + "Player %d : " % player)

    for i in range(len(p.rsplit(" "))):
        if 'pacify' in p.rsplit(" ")[i]:
            orders['pacify'].append(p.rsplit(" ")[i])
        elif '<' in p.rsplit(" ")[i]:
            orders['feed'].append(p.rsplit(" ")[i])
        elif '*' in p.rsplit(" ")[i]:
            orders['fight'].append(p.rsplit(" ")[i])
        elif '@' in p.rsplit(" ")[i]:
            orders['move'].append(p.rsplit(" ")[i])

    return orders

def nexturn():
    """Checks if Alpha Wolves have enough health to continue

    Return
    ------
    True or False according to Alphas' status 

    Version
    -------
    specification: Marius (v1 17/02/22)
    """
    if dictionnary[1]["alpha"][2] <= 0 and dictionnary[2]["alpha"][2] <=0: # both lose
        return "Equality ! Both of the alphas are dead."
    elif dictionnary[1]["alpha"][2] <=0: # player 1 lose
        return "Well play ! Player 2 win !"
    elif dictionnary[2]["alpha"][2] <=0: # player 2 lose
        return "Well play ! Player 1 win !"
    else:
        return 0 # no loser

def find(coos):
    """ Returns a list stats of a wolf according to its position

    Parameters
    ----------
    coos (List): coordinates of a wolf (ex : find([3-3]))

    Return
    ------
    (List): 
        [1] Player owning the wolf
        [2] Type of the wolf
        [3] Energy of the wolf
        [4] Bonus
        [5] (Only for normal wolves) : Position of the wolf in the dictionnary

    Version
    -------
    specification: Hugo (v2 17/03/22) """
    for i in ['alpha', 'omega']:
        for j in [1, 2]:
            if dictionnary[j][i][0] == int(coos[0]) and dictionnary[j][i][1] == int(coos[1]):
                return [j, i, dictionnary[j][i][2], dictionnary[j][i][3]]

    for j in [1, 2]:
        for i in range(len(dictionnary[j]['normal'])):
            if dictionnary[j]['normal'][i][0] == int(coos[0]) and dictionnary[j]['normal'][i][1] == int(coos[1]):
                return [j, 'normal', dictionnary[j]['normal'][i][2], dictionnary[j]['normal'][i][3], i]

def findattack(coos):
    """ Same as find() but in another dictionnary
    """
    for i in ['alpha', 'omega']:
        for j in [1, 2]:
            if dictionnary['saved_energy'][j][i][0] == int(coos[0]) and dictionnary['saved_energy'][j][i][1] == int(coos[1]):
                return [j, i, dictionnary['saved_energy'][j][i][2], dictionnary['saved_energy'][j][i][3]]

    for j in [1, 2]:
        for i in range(len(dictionnary['saved_energy'][j]['normal'])):
            if dictionnary['saved_energy'][j]['normal'][i][0] == int(coos[0]) and dictionnary['saved_energy'][j]['normal'][i][1] == int(coos[1]):
                return [j, 'normal', dictionnary['saved_energy'][j]['normal'][i][2], dictionnary['saved_energy'][j]['normal'][i][3], i]

def move(order, team): 
    """ Moves wolf to asked coordinates

    Parameters
    ----------
    order (list) : orders for the wolves.
    team (int) : Player 1 or player 2

    Return
    -------
    ValueError if 
        The wolf already had another order
        The wolf is trying to go too far
        The wolf is trying to get out of the map


    Version
    -------
    specification: Mathis (v2 17/03/22) """
    order=order.rsplit(':@')
    for i in range(2):
        order[i] = order[i].split('-')

    for i in range(0,2):
        for j in range(0,2):
            order[i][j] = int(order[i][j])
    
    if not find(order[1]):
        if find(order[0]):
            if order[0] not in dictionnary['wolfplayed'] :
                if int(order[0][1]) - int(order[1][1]) in [-1,0,1] and int(order[0][0]) - int(order[1][0]) in [-1,0,1]:
                    if 0 < int(order[1][0]) < int(dictionnary['map'][0]) + 1 and 0 < int(order[1][1]) < int(dictionnary['map'][1]) + 1:
                    #Checks if the final position isn't too far
                        index = find(order[0])
                        if index[0] == team:
                            if len(index) > 4:
                                dictionnary[index[0]][index[1]][index[4]][:2] = order[1]
                            else:
                                dictionnary[index[0]][index[1]][:2] = order[1]
                        else:
                            return "Error: Please be sure to use the good wolves."
                    else:
                        return "Error: Out of bounds."
                else:
                    return "Error: you cannot go there."
            else:
                    return "Error: This wolves already played."
        else:
            return "ValueError: This wolve does not exist"
    else:
        return "ValueError: Ther is already a wolf on this case."

    dictionnary['wolfplayed'].append(order[1])
    board(int(dictionnary['map'][0]), int(dictionnary['map'][1]), term.gold)

def pacify(order, team):
    """Pacification of the omega wolve

    Parameters
    ----------
    order (str) : order for the wolves.
    team (int) : Player 1 or player 2

    Return 
    -------
    ValueError if
        Not using your team's omega wolf


    Version
    -------
    specification: Malo (v2 17/03/22)
    """

    #split the order
    order = order.split(':')[0]
    order = order.split('-')
    
    if find(order):
        # check if its really an omega and good team
        if find(order)[1] == 'omega' and int(find(order)[0]) == team and int(find(order)[2]) >= 40 :
            #remove 40 energy to the omega
            dictionnary[team]['omega'][2] -= 40
            #loop for the tchebitchev distance
            for i in range (-6, 7):
                for j in range(-6, 7):
                    x = i+int(order[0])
                    y = j+int(order[1])
                    if 0 < x < int(dictionnary['map'][0])+1 and 0 < y < int(dictionnary['map'][1])+1:
                        if find([x, y]):
                            dictionnary["pacify"].append([x,y])
        else:
            return "ValueError : Please check that you are using an omega and/ or the good team"
    else:
        return "ValueError : Please check that you are using a real wolf."
    dictionnary['wolfplayed'].append([int(order[0]), int(order[1])])

def bonus():
    """Manages bonuses for Alpha(+30) and other wolves(+10) and resets it after every round

    Version
    -------
    specification: Hugo (v1 12/03/22)
    """

    # Reset bonuses
    for j in range(1, 3):
        for i in dictionnary[j]['normal']:
            i[3] = 0

        for i in 'alpha', 'omega':
            dictionnary[j][i][3] = 0
    
    # Bonuses for normal wolves
    for j in range(1, 3):
        for i in dictionnary[j]['normal']:
            for y in dictionnary[j]['normal']:
                if -3 < y[:2][0] - i[:2][0] < 3 and -3 < y[:2][1] - i[:2][1] < 3 and i[:2] != y[:2]:
                    i[3] += 10
            if -3 < dictionnary[j]['omega'][:2][0] - i[:2][0] < 3 and -3 < dictionnary[j]['omega'][:2][1] - i[:2][1] < 3 and dictionnary[j]['omega'][:2] != y[:2]:
                i[3] += 10
            if -5 < dictionnary[j]['alpha'][:2][0] - i[:2][0] < 5 and -5 < dictionnary[j]['alpha'][:2][1] - i[:2][1] < 5 and dictionnary[j]['alpha'][:2] != y[:2]:
                i[3] += 30

    # Bonuses for alpha and omega
    for j in range(1, 3):
        for i in 'alpha', 'omega':
            for y in dictionnary[j]['normal']:
                if -3 < y[:2][0] - dictionnary[j][i][:2][0] < 3 and -3 < y[:2][1] - dictionnary[j][i][:2][0] < 3 and dictionnary[j][i][:2] != y[:2]:
                    dictionnary[j][i][3] += 10
            if -3 < dictionnary[j]['omega'][:2][0] - dictionnary[j][i][:2][0] < 3 and -3 < dictionnary[j]['omega'][:2][1] - dictionnary[j][i][:2][1] < 3 and dictionnary[j][i][:2] != dictionnary[j]['omega'][:2]:
                    dictionnary[j][i][3] += 10
            if -5 < dictionnary[j]['alpha'][:2][0] - dictionnary[j][i][:2][0] < 5 and -5 < dictionnary[j]['alpha'][:2][1] - dictionnary[j][i][:2][1] < 5 and dictionnary[j][i][:2] != dictionnary[j]['alpha'][:2]:
                    dictionnary[j][i][3] += 30

def findfood(coos):
    """Returns stats of food according to its coordinates

    Parameters
    ----------
    coos(list) coordinates of the food (ex: [4-4])

    Returns
    -------
    List :
        [0] Emplacement of the fruit in its list
        [1] Type of fruit
        [2] Energy of the fruit

    Version
    -------
    specification: Mathis (v1 12/03/22)
    """

    for i in ['berries','apples','mice','rabbits','deers',]:
        for j in range(len(dictionnary['food'][i])):
            #trouver dans le dictionnaire ce qui correspond aux coordonées plateau
            if dictionnary['food'][i][j][0]==int(coos[0]) and dictionnary['food'][i][j][1]==int(coos[1]):
                #return le type de food et sa valeur nutritionelle
                return [j,i,dictionnary['food'][i][j][2]]

def feeding(order, team):
    """Make a specific wolf eat an designed consumable

    Parameters
    -----------
    order(str): order for the wolves
    team(int) Player 1 or player 2

    Return
    ------
    ValueError if
        The food is empty or doesn't exist
        The food is too far
        The wolf already has 100 energy

    Version
    -------
    specification: Hugo - Mathis (v3 22/03/22)
    """
    order=order.rsplit(':<')
    for i in range(2):
        order[i] = order[i].split('-')

    for i in range(0,2):
        for j in range(0,2):
            order[i][j] = int(order[i][j])

    if find(order[0]) and int(find(order[0])[0]) == team and int(find(order[0])[2]) < 100 : #check good team and not full life
        if int(order[0][1]) - int(order[1][1]) in [-1,0,1] and int(order[0][0]) - int(order[1][0]) in [-1,0,1]: # check distance
            if findfood(order[1]) and findfood(order[1])[2] > 0: # check that food exist
                index = find(order[0])
                foodindex = findfood(order[1])
                print(index)
                print(foodindex)
                if len(index) > 4: # check if normal wolves
                    if (dictionnary[team][index[1]][index[4]][2] + dictionnary['food'][foodindex[1]][foodindex[0]][2]) >= 100: # is food bigger than the energy required ?
                        #dictionnary['food'][foodindex[1]][foodindex[0]][2] = dictionnary['food'][foodindex[1]][foodindex[0]][2] - (dictionnary['food'][foodindex[1]][foodindex[0]][2] + dictionnary[team][index[1]][index[4]][2]) - 100
                        dictionnary[team][index[1]][index[4]][2] = 100
                    else: # food not enought to heal max energy
                        #dictionnary[team][index[1]][index[4]][2] += dictionnary['food'][foodindex[1]][foodindex[0]][2]
                        dictionnary['food'][foodindex[1]][foodindex[0]][2] = 0
                else: # alpha or omega
                    if (dictionnary[team][index[1]][2] + dictionnary['food'][foodindex[1]][foodindex[0]][2]) >= 100: # is food bigger than the energy required ?
                        #dictionnary['food'][foodindex[1]][foodindex[0]][2] = dictionnary['food'][foodindex[1]][foodindex[0]][2] - (dictionnary['food'][foodindex[1]][foodindex[0]][2] + dictionnary[team][index[1]][2]) - 100
                        dictionnary[team][index[1]][2] = 100
                    else: # food not enought to heal max energy
                        #dictionnary[team][index[1]][2] += dictionnary['food'][foodindex[1]][foodindex[0]][2]
                        dictionnary['food'][foodindex[1]][foodindex[0]] = 0

                board(int(dictionnary['map'][0]), int(dictionnary['map'][1]), term.gold)
                print('%d    ' % dictionnary['food'][foodindex[1]][foodindex[0]][2])
                #u = input('')
            else:
                return "ValueError : Please check that the food really exist or isn't empty."
        else:
            return "ValueError : Please check that you are at the good distance of the food."
    else:
        return "ValueError : Please check that you are using your wolf, and that he is not full life."

    dictionnary['wolfplayed'].append(order[0])
    board(int(dictionnary['map'][0]), int(dictionnary['map'][1]), term.gold)

def fighting(order): 
    """Manage fights and energy loss

    Parameters
    ----------
    order(str): order for the wolves

    Returns
    -------
    ValueError if   
        at least ne of the wolves is human
        the wolf attacking is pacified
        the target is too far
        at least one of the wolves doesn't exist


    Version
    -------
    specification: Hugo - Malo (v4 19/03/22)
    """
    order=order.rsplit(':*')
    for i in range(2):
        order[i] = order[i].split('-')

    for i in range(0,2):
        for j in range(0,2):
            order[i][j] = int(order[i][j])


    if find(order[0]) and find(order[1]): # are both of wolves exists ?
        if int(order[0][1]) - int(order[1][1]) in [-1,0,1] and int(order[0][0]) - int(order[1][0]) in [-1,0,1]: # check distance
            if order[0] not in dictionnary['pacify']: # 1st pacified ?
                if find(order[0])[2] > 0 and find(order[1])[2] > 0: # Are wolves humans ??
                    index = find(order[1])
                    if len(index) > 4: # normal
                        dictionnary[index[0]][index[1]][index[4]][2] -= int((find(order[0])[2] + find(order[0])[3]) /10)
                        if dictionnary[index[0]][index[1]][index[4]][2] < 0:
                            dictionnary[index[0]][index[1]][index[4]][2] = 0
                    else: # alpha omega
                        dictionnary[index[0]][index[1]][2] -= int((find(order[0])[2] + find(order[0])[3]) /10)
                        if dictionnary[index[0]][index[1]][2] < 0:
                            dictionnary[index[0]][index[1]][2] = 0
                else: 
                    return "ValueError: Please verify that wolves aren't humanized."
            else:
                return "ValueError: Please verify that your wolve isn't pacified ?"
        else:
            return 'ValueError: Please check that you are at enough distance to touch him.'    
    else: 
        return 'ValueError: Please check that both of the wolves exists.'
    dictionnary['rounds'][1] = True
    dictionnary['wolfplayed'].append(order[0])

def syntaxer(pos1, pos2, type):
    """Return nicely orders for ia

    Parameters
    ----------
    pos1(list): position of the first wolf
    pos2(list): position of the second wolf
    type (str): type of the action

    Returns
    -------
    Return the orders nicely in str

    Version
    -------
    specification: Hugo - Malo (v4 22/03/22)
    """
    if type == 'pacify':
        return ('%d-%d:pacify' % (pos1[0],pos1[1]))
    elif type == 'feed':
        return ('%d-%d:<%d-%d' % (pos1[0],pos1[1],pos2[0],pos2[1]))
    elif type == 'fight':
        return ('%d-%d:*%d-%d' % (pos1[0],pos1[1],pos2[0],pos2[1]))
    else:
        return ('%d-%d:@%d-%d' % (pos1[0],pos1[1],pos2[0],pos2[1]))

def generate_orders(team):
    """Our dumb ai

    Parameters
    ----------
    team(int): team of the player

    Returns
    -------
    Return a list of order for the play game.

    Version
    -------
    specification: Hugo - Malo (v4 24/03/22)
    """
    pos2 = [1, 1]
    orders = {
        'pacify' : [], # 1-1:pacify
        'feed' : [], # 3-3:<4-4
        'fight' : [], # 3-3:*3-2
        'move' : [] # 3-3:@3-4
    }

    if randint(0,20) == 10:
        orders['pacify'].append(syntaxer(dictionnary[team]['omega'][:2], 'pacify', 'pacify'))
    else:
        r = randint(0,4)
        for j in range(0,2):
            pos2[j] = (int(dictionnary[team]['omega'][j]) + randint(-1, 1))

        if r == 0: 
            orders['feed'].append(syntaxer(dictionnary[team]['omega'][:2], pos2, 'feed'))
        elif r == 1: #fight
            orders['fight'].append(syntaxer(dictionnary[team]['omega'][:2], pos2, 'fight'))
        else: #move
            orders['move'].append(syntaxer(dictionnary[team]['omega'][:2], pos2, 'move'))

    for i in dictionnary[team]['normal']:
        r = randint(0,4)
        for j in range(0,2):
            pos2[j] = (int(i[j]) + randint(-1, 1))

        if r == 0: 
            orders['feed'].append(syntaxer(i[:2], pos2, 'feed'))
        elif r == 1: #fight
            orders['fight'].append(syntaxer(i[:2], pos2, 'fight'))
        else: #move
            orders['move'].append(syntaxer(i[:2], pos2, 'move'))

    r = randint(0,4)
    for j in range(0,2):
        pos2[j] = (int(dictionnary[team]['alpha'][j]) + randint(-1, 1))

    if r == 0: 
        orders['feed'].append(syntaxer(dictionnary[team]['alpha'][:2], pos2, 'feed'))
    elif r == 1: #fight
        orders['fight'].append(syntaxer(dictionnary[team]['alpha'][:2], pos2, 'fight'))
    else: #move
        orders['move'].append(syntaxer(dictionnary[team]['alpha'][:2], pos2, 'move'))

    return orders

def play_game(group_1, type_1, group_2, type_2):
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

    while nexturn() == 0 and dictionnary['rounds'][2] <= 200:
        bonus()
        dictionnary['saved_energy'] = dictionnary.copy()
        dictionnary['rounds'][1] = False
        dictionnary['pacify'] = []
        dictionnary['wolfplayed'] = []
        orders= []

        board(int(dictionnary['map'][0]), int(dictionnary['map'][1]), term.gold)
        
        for i in [type_1, group_1], [type_2, group_2]:
            if i[0] == 'human':
                orders.append(get_human_orders(i[1]))
                print(term.home + term.clear)
                board(int(dictionnary['map'][0]), int(dictionnary['map'][1]), term.gold)

            elif i[0] == 'AI':
                orders.append(generate_orders(i[1]))
                
            elif i[0] == 'remote':
                print('ok')

            else:
                return 'ValueError: Wrong type of player.'

        for i in range(0,2):
            # First step : Pacify
            if orders[i]['pacify']:
                pacify(orders[i]['pacify'][0], (i+1))

            # Second step : Feed
            for j in orders[i]['feed']:
                feeding(j, (i+1))

            # Third step : Fight
            for j in orders[i]['fight']:
                fighting(j)

            # Fourth step : Move
            for j in orders[i]['move']:
                    move(j, (i +1))

        dictionnary['rounds'][0] += 1
        
        if not dictionnary['rounds'][1]:
            dictionnary['rounds'][2] += 1
        else:
            dictionnary['rounds'][2] = 0
        time.sleep(0.1)

    print(nexturn())
        
print(term.home + term.clear)
dictionnary = config('map10.ano')
play_game(1, 'AI', 2, 'AI')