from random import *

orders = {
        'pacify' : [], # 1-1:pacify
        'feed' : [], # 3-3:<4-4
        'fight' : [], # 3-3:*3-2
        'move' : [] # 3-3:@3-4
    }

def human(dictionnary, team):
    """
    return false if no human

    if human automatically go to the nearest food, the best one (qui nourrit le mieux et le plus proche)
    """

def pacific(dictionnary, team):
    """
    check if it has a utility to pacify or not

    is alpha going to die after this turn ?
    """

def defense(dictionnary, team):
    """
    put stronger wolf on the front of the attack and put the rest behind 
    go eat to recover
    """

def attack(dictionnary, team):
    """
    if in attack mode, attack all the other wolves.
    wolves that are too low doesn't come with
    """

def recover(dictionnary, team):
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

def findfood(dictionnary, coos):
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
    """minds of our ai

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

    

    return orders