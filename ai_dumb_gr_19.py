from random import *

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

def generate_orders(dictionnary, team):
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