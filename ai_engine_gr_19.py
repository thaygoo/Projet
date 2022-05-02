from random import *

def team_group(dictionnary, team):
    """
    check if wolve's team are grouped
    return true or false
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

def attack(dictionnary, team):
    """
    if in attack mode, attack all the other wolves.
    wolves that are too low doesn't come with
    """

def finish(dictionnary, team):
    """
    check if it's possible to finish game and kill alpha
    """

def recovery(dictionnary, team):
    """
    heal the wolves
    """

def humans(dictionnary, team):
    """
    return false if no human

    if human automatically go to the nearest food, the best one (qui nourrit le mieux et le plus proche)
    """

def mode(dictionnary, team):
    """
    defensive or attack ?
    in relation with global health and local
    """

def isolate(dictionnary, team):
    """
    if a wolve is alone do maximum to move him in the meute
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

            
    for wolf in dictionnary[team]['normal']:
        played=0
        if wolf[2]<90:
            for k in (-1,0,1):
                for l in (-1,0,1):
                    z=int(wolf[0])+k
                    y=int(wolf[1])+l
                    if findfood([z,y])!= None:
                        if findfood([z,y])[2]>0:
                            orders['feed'].append(syntaxer(wolf[:2],[wolf[0]+k,wolf[1]+l],'feed'))
                            played=1
            if played==0: 
            #q et s représentent le chemin que doit emprunter le loup pour avancer vers la nouriture
            #fait avec beaucoup d'essais-erreurs parce que je suis pas très malin
                for k in (-2,-1,0,1,2):
                    for l in (-2,2):
                        if findfood([wolf[0]+l,wolf[1]+k])!=None:
                            if findfood([wolf[0]+l,wolf[1]+k])[2]>0:
                                if (wolf[0]+l)-wolf[0] >=1 : 
                                    q=1
                                elif (wolf[0]+l)-wolf[0]<=-1:
                                    q=-1
                                else:
                                    q=0

                                if (wolf[1]+k)-wolf[1] >=1:
                                    s=1
                                elif (wolf[1]+k)-wolf[1]<=-1:
                                    s=-1
                                else:
                                    s=0
                                orders['move'].append(syntaxer(wolf[:2],[int(wolf[0])+q,int(wolf[1])+s],'move'))
                                played=1
        
            if played==0: 
                for k in (-2,-1,0,1,2):
                    for l in (-2,2):
                        if findfood([wolf[0]+k,wolf[1]+l])!=None:
                            if findfood([wolf[0]+k,wolf[1]+l])[2]>0:

                                if (wolf[0]+k)-wolf[0]>=1 : 
                                    q=1
                                elif(wolf[0]+k)-wolf[0]<=-1:
                                    q=-1
                                else:
                                    q=0

                                if (wolf[1]+l)-wolf[1]>=1:
                                    s=1
                                elif (wolf[1]+l)-wolf[1]<=-1:
                                    s=-1
                                else:
                                    s=0
                                orders['move'].append(syntaxer(wolf[:2],[int(wolf[0])+s,int(wolf[1])+q],'move'))
                                played=1
        
        if played==0:
            alpha = dictionnary[team]['alpha']
            if alpha[0]-wolf[0]>=1:
                q=1
            elif alpha[0]-wolf[0]<=-1:
                q=-1
            else:
                q=0
            if alpha[1]-wolf[1]>=1:
                s=1
            elif alpha[1]-wolf[1]<=-1:
                s=-1
            else:
                s=0
            orders['move'].append(syntaxer(wolf[:2],[int(wolf[0])+q,int(wolf[1])+s],'move'))
            
            #accompagner l'alpha
                            


    omega = dictionnary[team]['omega']
    played=0
    if int(omega[2])<100:
        for k in (-1,0,1):
            for l in (-1,0,1):
                if played==0:
                    if findfood([omega[0]+k,int(omega[1])+l])!=None:
                        if findfood([omega[0]+k,omega[1]+l])[2]>0:
                            orders['feed'].append(syntaxer(omega[:2],[int(omega[0])+k,int(omega[1])+l],'feed'))
                            played=1
    
            if played==0: 
            #q et s représentent le chemin que doit emprunter le loup pour avancer vers la nouriture
            #fait avec beaucoup d'essais-erreurs parce que je suis pas très malin
                for k in (-2,-1,0,1,2):
                    for l in (-2,2):
                        if findfood([omega[0]+l,omega[1]+k])!=None:
                            if findfood([omega[0]+l,omega[1]+k])[2]>0:
                                if (omega[0]+l)-omega[0] >=1 : 
                                    q=1
                                elif (omega[0]+l)-omega[0]<=-1:
                                    q=-1
                                else:
                                    q=0

                                if (omega[1]+k)-omega[1] >=1:
                                    s=1
                                elif (omega[1]+k)-omega[1]<=-1:
                                    s=-1
                                else:
                                    s=0
                                orders['move'].append(syntaxer(omega[:2],[int(omega[0])+q,int(omega[1])+s],'move'))
                                played=1
        
            if played==0: 
                for k in (-2,-1,0,1,2):
                    for l in (-2,2):
                        if findfood([omega[0]+k,omega[1]+l])!=None:
                            if findfood([omega[0]+k,omega[1]+l])[2]>0:
                                if (omega[0]+k)-omega[0]>=1 : 
                                    q=1
                                elif(omega[0]+k)-omega[0]<=-1:
                                    q=-1
                                else:
                                    q=0

                                if (omega[1]+l)-omega[1]>=1:
                                    s=1
                                elif (omega[1]+l)-omega[1]<=-1:
                                    s=-1
                                else:
                                    s=0
                                orders['move'].append(syntaxer(omega[:2],[int(omega[0])+s,int(omega[1])+q],'move'))
                                played=1
    if played==0:
        alpha = dictionnary[team]['alpha']
        if alpha[0]-omega[0]>=1:
            q=1
        elif alpha[0]-omega[0]<=-1:
            q=-1
        else:
            q=0
        if alpha[1]-omega[1]>=1:
            s=1
        elif alpha[1]-omega[1]<=-1:
            s=-1
        else:
            s=0
        orders['move'].append(syntaxer(omega[:2],[int(omega[0])+q,int(omega[1])+s],'move'))
        #accompagner l'alpha
                            


    alpha = dictionnary[team]['alpha']
    played=0
    if alpha[2]<100:
        for k in ((-1),0,1):
            for l in ((-1),0,1):
                if played==0:
                    if findfood([alpha[0]+k,alpha[1]+l]) != None:
                        if findfood([alpha[0]+k,alpha[1]+l])[2]>0:
                            orders['feed'].append(syntaxer(alpha[:2],[alpha[0]+k,alpha[1]+l], 'feed'))
                            played=1
            if played==0: 
            #q et s représentent le chemin que doit emprunter le loup pour avancer vers la nouriture
            #fait avec beaucoup d'essais-erreurs parce que je suis pas très malin
                for k in (-2,-1,0,1,2):
                    for l in (-2,2):
                        if findfood([alpha[0]+l,alpha[1]+k])!=None:
                            if findfood([alpha[0]+l,alpha[1]+k])[2]>0:
                                if (alpha[0]+l)-alpha[0] >=1 : 
                                    q=1
                                elif (alpha[0]+l)-alpha[0]<=-1:
                                    q=-1
                                else:
                                    q=0

                                if (alpha[1]+k)-alpha[1] >=1:
                                    s=1
                                elif (alpha[1]+k)-alpha[1]<=-1:
                                    s=-1
                                else:
                                    s=0
                                orders['move'].append(syntaxer(alpha[:2],[int(alpha[0])+q,int(alpha[1])+s],'move'))
                                played=1
        
            if played==0: 
                for k in (-2,-1,0,1,2):
                    for l in (-2,2):
                        if findfood([alpha[0]+k,alpha[1]+l])!=None:
                            if findfood([alpha[0]+k,alpha[1]+l])[2]>0:

                                if (alpha[0]+k)-alpha[0]>=1 : 
                                    q=1
                                elif(alpha[0]+k)-alpha[0]<=-1:
                                    q=-1
                                else:
                                    q=0

                                if (alpha[1]+l)-alpha[1]>=1:
                                    s=1
                                elif (alpha[1]+l)-alpha[1]<=-1:
                                    s=-1
                                else:
                                    s=0
                                orders['move'].append(syntaxer(alpha[:2],[int(alpha[0])+s,int(alpha[1])+q],'move'))
                                played=1
    if played==0:
        orders['move'].append(syntaxer(alpha[:2],[alpha[0]+randint(-1,1),alpha[1]+randint(-1,1)], ''))
        played=1

    if played==0:
        orders['move'].append(syntaxer(alpha[:2],[alpha[0]+randint(-1,1),alpha[1]+randint(-1,1)], ''))
        played=1
                    
    return orders



"""    if randint(0,20) == 10:
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

    return orders"""