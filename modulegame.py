import blessed, distancemodule, time
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
        'pacify': [],
        'wolfplayed': []
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

# def display():
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
    3-2:@4-2 1-1:*1-2 2-3:@2-4 3-3:<4-4 
    """
    orders = {
        'pacify' : [],
        'feed' : [],
        'fight' : [],
        'move' : []
    }
    p = input(term.normal + term.move_xy(coordinate(0, 0)[0], 3+(2*int(dictionnary['map'][1]))) + "Player %d : " % player)

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
    """ Pacification of the omega wolve

    Parameters
    ----------
    order (list) : order for the wolves.

    Version
    -------
    specification: Hugo (v2 17/03/22) """
    if 0 < int(coos[0]) < int(dictionnary['map'][0])+1 and 0 < int(coos[1]) < int(dictionnary['map'][1])+1:
        for i in ['alpha', 'omega']:
            for j in [1, 2]:
                if dictionnary[j][i][0] == int(coos[0]) and dictionnary[j][i][1] == int(coos[1]):
                    return [j, i, dictionnary[j][i][2], dictionnary[j][i][3]]

        for j in [1, 2]:
            for i in range(len(dictionnary[j]['normal'])):
                if dictionnary[j]['normal'][i][0] == int(coos[0]) and dictionnary[j]['normal'][i][1] == int(coos[1]):
                    return [j, 'normal', dictionnary[j]['normal'][i][2], dictionnary[j]['normal'][i][3], i]
    else:
        return "ValueError: Not in the bounds"

def findattack(coos):
    """ Pacification of the omega wolve

    Parameters
    ----------
    order (list) : order for the wolves.

    Version
    -------
    specification: Hugo (v2 17/03/22) """
    if 0 < int(coos[0]) < int(dictionnary['map'][0]) and 0 < int(coos[1]) < int(dictionnary['map'][1]):
        for i in ['alpha', 'omega']:
            for j in [1, 2]:
                if attackdic[j][i][0] == int(coos[0]) and attackdic[j][i][1] == int(coos[1]):
                    return [j, i, attackdic[j][i][2], attackdic[j][i][3]]

        for j in [1, 2]:
            for i in range(len(attackdic[j]['normal'])):
                if attackdic[j]['normal'][i][0] == int(coos[0]) and attackdic[j]['normal'][i][1] == int(coos[1]):
                    return [j, 'normal', attackdic[j]['normal'][i][2], attackdic[j]['normal'][i][3], i]
    else:
        return "ValueError: Not in the bounds"

def move(order, team): #3-3:@4-3  NE PAS ALLER SUR UNE CASE OCCUPée
    order=order.rsplit(':@')
    for i in range(2):
        order[i] = order[i].split('-')

    for i in range(0,2):
        for j in range(0,2):
            order[i][j] = int(order[i][j])
    
    if order[0] not in dictionnary['wolfplayed']:
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
                    return ("Error: Please be sure to use the good wolves.")
            else:
                return ("Error: Out of bounds.")
        else:
            return ("Error: you cannot go there.") 
    else:
            return ("Error: This wolves already played.") 

    dictionnary['wolfplayed'].append(order[1])
    board(int(dictionnary['map'][0]), int(dictionnary['map'][1]), term.gold)

def pacify(order, team): # pacify(1-1:pacify, 1)
    """Pacification of the omega wolve

    Parameters
    ----------
    order (str) : order for the wolves.

    Version
    -------
    specification: Hugo (v2 17/03/22)
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
    """Manage bonuses

    Parameters
    ----------
    team (int) : team number
    wolves (list) : coos

    Version
    -------
    specification: Mathis (v1 17/02/22)

    1(r1, c1) 2(r2, c2)   (r2 - r1) , (c2 - c1)
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
    """Manage bonuses

    Version
    -------
    specification: Mathis (v1 17/02/22)
    """

    for i in ['berries','apples','mice','rabbits','deers',]:
        for j in range(len(dictionnary['food'][i])):
            #trouver dans le dictionnaire ce qui correspond aux coordonées plateau
            if dictionnary['food'][i][j][0]==int(coos[0]) and dictionnary['food'][i][j][1]==int(coos[1]):
                #return le type de food et sa valeur nutritionelle
                return [j,i,dictionnary['food'][i][j][2]]

def feeding(order, team): #3-3:<4-3
    """Manage bonuses

    Version
    -------
    specification: Mathis (v1 17/02/22)
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
                if len(index) > 4: # check if normal wolves
                    if (dictionnary[team][index[1]][index[4]][2] + foodindex[0]) <= 100: # is food bigger than the energy required ?
                        dictionnary['food'][foodindex[1]][foodindex[0]][2] = (dictionnary[team][index[1]][index[4]][2] + dictionnary['food'][foodindex[1]][foodindex[0]][2]) - 100
                        dictionnary[team][index[1]][index[4]][2] = 100
                    else: # food not enought to heal max energy
                        dictionnary[team][index[1]][index[4]][2] += dictionnary['food'][foodindex[1]][foodindex[0]][2]
                        dictionnary['food'][foodindex[1]][foodindex[0]][2] = 0
                else: # alpha or omega
                    if (dictionnary[team][index[1]][index[2]] + foodindex[0]) <= 100: # is food bigger than the energy required ?
                        dictionnary['food'][foodindex[1]][foodindex[0]][2] = (dictionnary[team][index[1]][index[2]] + dictionnary['food'][foodindex[1]][foodindex[0]][2]) - 100
                        dictionnary[team][index[1]][index[2]] = 100
                    else: # food not enought to heal max energy
                        dictionnary[team][index[1]][index[2]] += dictionnary['food'][foodindex[1]][foodindex[0]][2]
                        dictionnary['food'][foodindex[1]][foodindex[0]] = 0
            else:
                return "ValueError : Please check that the food really exist or isn't empty."
        else:
            return "ValueError : Please check that you are at the good distance of the food."
    else:
        return "ValueError : Please check that you are using your wolf, and that he is not full life."
    dictionnary['wolfplayed'].append(order[0])
    board(int(dictionnary['map'][0]), int(dictionnary['map'][1]), term.gold)

def fighting(order): #3-3:*4-3
    """Manage bonuses

    Version
    -------
    specification: Mathis (v1 17/02/22)
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
                        dictionnary[index[0]][index[1]][index[4]][2] -= int((findattack(order[0])[2] + findattack(order[0])[3]) /10)
                        if dictionnary[index[0]][index[1]][index[4]][2] < 0:
                            dictionnary[index[0]][index[1]][index[4]][2] = 0
                    else: # alpha omega
                        dictionnary[index[0]][index[1]] -= int((findattack(order[0])[2] + findattack(order[0])[3]) /10)
                        if dictionnary[index[0]][index[1]] < 0:
                            dictionnary[index[0]][index[1]] = 0
                else: 
                    return "ValueError: Please verify that wolves aren't humanized."
            else:
                return "ValueError: Please verify that your wolve isn't pacified ?"
        else:
            return 'ValueError: Please check that you are at enough distance to touch him.'    
    else: 
        return 'ValueError: Please check that both of the wolves exists.' 
    dictionnary['wolfplayed'].append(order[0])

#   ---------------------------------------------------------------------------------------------------------------------------------
# TASKS :
# ARE WOLF HAVE PLAYED THIS ROUND YET ? 
# Je pense le mettre avant d'apliquer les ordres pour qu'il soit extérieur aux fonctions
# COUNT OF ROUND important ça
# histoire des 200 tours consécutifs tied
# Verifier que les deux alphas ne meurent pas au même tour
# Spécifications
# vidéo
# rapport

dictionnary = config('map10.ano')
attackdic = []

# main function
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
    3-2:@4-2 1-1:*1-2 2-3:@2-4 3-3:<4-4
    8-9:@7-9 9-9:*9-10 9-8:@9-7 8-8:<7-7
    """

    while nexturn():
        print(term.home + term.clear)
        bonus()
        attackdic = dictionnary.copy() # per round
        dictionnary['pacify'] = [] # per round
        dictionnary['wolfplayed'] = []
        orders= []

        board(int(dictionnary['map'][0]), int(dictionnary['map'][1]), term.gold)
        
        for i in [type_1, group_1], [type_2, group_2]:
            if i[0] == 'human':
                orders.append(get_human_orders(i[1]))
                print(term.home + term.clear)
                board(int(dictionnary['map'][0]), int(dictionnary['map'][1]), term.gold)

        for i in range(0,2):
            """ # First step : Pacify
            if orders[i]['pacify']:
                pacify(orders[i]['pacify'][0], (i+1))

            # Second step : Feed
            for j in orders[i]['feed']:
                feeding(j, (i+1))

            # Third step : Fight
            for j in orders[i]['fight']:
                fighting(j) """

            # Fourth step : Move
            for j in orders[i]['move']:
                    move(j, (i +1))
        print(dictionnary['wolfplayed'])
        time.sleep(5)


play_game(1, 'human', 2, 'human')