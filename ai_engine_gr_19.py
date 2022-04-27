from random import *

def team_group(dictionnary, team):
    """
    check if wolve's team are grouped
    """

def assemble(dictionnary, team):
    """
    assemble wolves nicely
    """

def pacification(dictionnary, team):
    """
    check if it has a utility to pacify or not

    is alpha going to die after this turn ?
    """

def defense(dictionnary, team):
    """
    put stronger wolf on the front of the attack and put the rest behind 
    go eat to recover
    """

def finish(dictionnary, team):
    """
    check if it's possible to finish game and kill alpha
    """

def recovery(dictionnary, team):
    """
    heal the wolves
    """








def find(dictionnary, coos):
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
            if find(dictionnary, pos2):
                if find(dictionnary, pos2)[0] != team:
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
            if find(dictionnary, pos2):
                if find(dictionnary, pos2)[0] != team:
                    orders['fight'].append(syntaxer(i[:2], pos2, 'fight'))
        else: #move
            orders['move'].append(syntaxer(i[:2], pos2, 'move'))

    r = randint(0,4)
    for j in range(0,2):
        pos2[j] = (int(dictionnary[team]['alpha'][j]) + randint(-1, 1))

    if r == 0: 
        orders['feed'].append(syntaxer(dictionnary[team]['alpha'][:2], pos2, 'feed'))
    elif r == 1: #fight
        if find(dictionnary, pos2):
                if find(dictionnary, pos2)[0] != team:
                    orders['fight'].append(syntaxer(dictionnary[team]['alpha'][:2], pos2, 'fight'))
    else: #move
        orders['move'].append(syntaxer(dictionnary[team]['alpha'][:2], pos2, 'move'))

    return orders