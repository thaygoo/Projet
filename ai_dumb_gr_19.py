orders = {
        'pacify' : [], # 1-1:pacify
        'feed' : [], # 3-3:<4-4
        'fight' : [], # 3-3:*3-2
        'move' : [] # 3-3:@3-4
    }

wolfplayed = []

def human(dictionnary, team):
    for wolf in dictionnary[team]['normal']:
        if wolf[2] <= 0:
            recover(wolf[:2], dictionnary, team)

    if dictionnary[team]['omega'][2] <= 0:
        recover(dictionnary[team]['omega'][:2], dictionnary, team)

def recover(wolf, dictionnary, team):
    if -2 < (wolf[:2][0] - bestfood(dictionnary, wolf[:2])[0]) < 2 and -2 < (wolf[:2][1] - bestfood(dictionnary, wolf[:2])[1]) < 2:
        orders['feed'].append(syntaxer(wolf[:2],bestfood(dictionnary, wolf[:2]),'feed'))
    else:
        coos = wolf[:2]
        for i in range(0,2):
            if bestfood(dictionnary, wolf[:2])[i] > wolf[:2][i]:
                coos[i] += 1
            elif bestfood(dictionnary, wolf[:2])[i] < wolf[:2][i]:
                coos[i] -= 1
        orders['move'].append(syntaxer(wolf[:2], coos,'move'))
        wolfplayed.append(wolf[:2])

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

def bestfood(dictionnary, coos):
  foods = []
  k = 1
  while len(foods) < 3:
    k += 1
    for i in range (-k, k+1):
      for j in range(-k, k+1):
        x = i+int(coos[0])
        y = j+int(coos[1])
        if 0 < x < int(dictionnary['map'][0])+1 and 0 < y < int(dictionnary['map'][1])+1:
          if findfood(dictionnary, [x, y]):
            foods.append([findfood(dictionnary, [x, y])[2], [x,y]])

  return max(foods)[1]

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
    if team == 1:
        enemyteam = 2
    else:
        enemyteam = 1

    human(dictionnary, team)
    if dictionnary[team]['alpha'][2] < 70:
        recover(dictionnary[team]['alpha'][:2], dictionnary, team)
        #reste de la meute attaque ou protège, omega pacifie
    else:
        for wolf in dictionnary[team]['normal']:
            if -2 < (wolf[:2][0] - dictionnary[enemyteam]['alpha'][:2][0]) < 2 and -2 < (wolf[:2][1] - dictionnary[enemyteam]['alpha'][:2][1]) < 2:
                orders['fight'].append(syntaxer(wolf[:2],dictionnary[enemyteam]['alpha'][:2],'fight'))
            else:
                coos = wolf[:2]
                for i in range(0,2):
                    if dictionnary[enemyteam]['alpha'][:2][i] > wolf[:2][i]:
                        coos[i] += 1
                    elif dictionnary[enemyteam]['alpha'][:2][i] < wolf[:2][i]:
                        coos[i] -= 1
                orders['move'].append(syntaxer(wolf[:2], coos,'move'))
                wolfplayed.append(wolf[:2])

        
        if -2 < (dictionnary[team]['omega'][:2][0] - dictionnary[enemyteam]['alpha'][:2][0]) < 2 and -2 < (dictionnary[team]['omega'][:2][1] - dictionnary[enemyteam]['alpha'][:2][1]) < 2:
            orders['fight'].append(syntaxer(dictionnary[team]['omega'][:2],dictionnary[enemyteam]['alpha'][:2],'fight'))
        else:
            coos = dictionnary[team]['omega'][:2]
            for i in range(0,2):
                if dictionnary[enemyteam]['alpha'][:2][i] > dictionnary[team]['omega'][:2][i]:
                    coos[i] += 1
                elif dictionnary[enemyteam]['alpha'][:2][i] < dictionnary[team]['omega'][:2][i]:
                    coos[i] -= 1
            orders['move'].append(syntaxer(dictionnary[team]['omega'][:2], coos,'move'))
            wolfplayed.append(dictionnary[team]['omega'][:2])

        if -2 < (dictionnary[team]['alpha'][:2][0] - dictionnary[enemyteam]['alpha'][:2][0]) < 2 and -2 < (dictionnary[team]['alpha'][:2][1] - dictionnary[enemyteam]['alpha'][:2][1]) < 2:
            orders['fight'].append(syntaxer(dictionnary[team]['alpha'][:2],dictionnary[enemyteam]['alpha'][:2],'fight'))
        else:
            coos = dictionnary[team]['alpha'][:2]
            for i in range(0,2):
                if dictionnary[enemyteam]['alpha'][:2][i] > dictionnary[team]['alpha'][:2][i]:
                    coos[i] += 1
                elif dictionnary[enemyteam]['alpha'][:2][i] < dictionnary[team]['alpha'][:2][i]:
                    coos[i] -= 1
            orders['move'].append(syntaxer(dictionnary[team]['alpha'][:2], coos,'move'))
            wolfplayed.append(dictionnary[team]['alpha'][:2])


    return orders