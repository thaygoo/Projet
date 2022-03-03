import blessed, math, os, time, random
from blessed import Terminal
from sqlalchemy import true
term = blessed.Terminal()
def search_data(file_path):
    """The function is going to take the information of a file.cpx.

    Parameter
    ---------
    file_path : path of the folder containing the file.cpx (str)

    Return
    ------
    dico_cpx: the dictonary containing all the file.cpx information (dict)

    Version
    -------
    specification: Gabriel Bogaerts (v. 1 19/02/21)
    implementation: Antoine De Coster, Gabriel Bogaerts (v. 2 25/02/21)

    """
    #open the file
    fh = open(file_path, 'r')

    #create dico
    dico_cpx = {}

    #list with one line for each part of the list
    text = fh.readlines()

    string = ''

    #clear text
    for line in text:
        string += line
    string = string.replace("\n", " ")
    string = string.replace(":", "")

    #Map
    string_before_anthills = string.split('anthills')[0]
    string_after_map = string_before_anthills.split('map ')[1]
    list_data_map = string_after_map.split(' ')
    #delete the two last element that are empty element due to the split
    del list_data_map[2:]
    #put list in dict
    dico_cpx['map'] = list_data_map

    #Anthills
    string_before_clods = string.split('clods')[0]
    string_after_anthills = string_before_clods.split('anthills ')[1]
    list_data_anthills = string_after_anthills.split(' ')
    #delete last element that is an empty element due to the split
    del list_data_anthills[-1]
    #put list in dict
    dico_cpx['anthills'] = list_data_anthills

    #Clods
    for index in range(len(text)):
        #stocking the infos about the clods
        if 'clods:' in text[index]:
            clods_infos = {}
            clods_number = 1
            while index < len(text) - 1:
                index += 1
                if text[index] != '':
                    current_clods = text[index].split(' ')
                    x = int(current_clods[0])
                    y = int(current_clods[1])
                    level = int(current_clods[2])
                    clods_infos['clod_' + str(clods_number)] = {}
                    clods_infos['clod_' + str(clods_number)]['coordinates'] = [x, y]
                    clods_infos['clod_' + str(clods_number)]['level'] = level
                    clods_number += 1
            dico_cpx['clods'] = clods_infos

    #close the file
    fh.close()

    return dico_cpx
def create_dico_rules():
    """Create the dictionary with the rules.

    Return
    ------
    dico_rules : dictionary with data about rules (dict)

    Version
    -------
    specification: Antoine De Coster (v. 1 19/02/21)
    implementation: Corentin Germeau (v. 2 15/03/21)

    """
    #dico rules
    dico_rules = {'team1': {'ant': {'level1': {'strength': 1, 'health_points': 3, 'scope': 3, 'color': '\x1b[38;2;139;129;76m%\x1b(B\x1b[m'}, #scope = portée
                                     'level2': {'strength': 2, 'health_points': 5, 'scope': 3, 'color': '\x1b[38;2;255;185;15m%\x1b(B\x1b[m'},
                                     'level3': {'strength': 3, 'health_points': 7, 'scope': 3, 'color': '\x1b[38;2;255;69;0m%\x1b(B\x1b[m'}}},

                  'team2': {'ant': {'level1': {'strength': 1, 'health_points': 3, 'scope': 3, 'color': '\x1b[38;2;85;26;139m%\x1b(B\x1b[m'}, 
                                     'level2': {'strength': 2, 'health_points': 5, 'scope': 3, 'color': '\x1b[38;2;221;160;221m%\x1b(B\x1b[m'},
                                     'level3': {'strength': 3, 'health_points': 7, 'scope': 3, 'color': '\x1b[38;2;238;0;238m%\x1b(B\x1b[m'}}}      
                    }
                                     
    return dico_rules

#3. Function informing the location of the elements
def create_ant(dico_ant_played, nb_turn, dico_rules, dico_gameboard, dico_level):
    """Save the position of the ants.

    Parameters
    ----------
    dico_ant_played: dictionary with data about ant played (dict)
    nb_turn: number of turns already played (int)
    dico_rules : dictionary with data about rules (dict)
    dico_gameboard: dictionary with data about the gameboard (dict)
    dico_level: the level that the ants will take (dict)

    Return
    ------
    dico_ant_played: dictionary with data about ant played (dict)

    Version
    -

    """
    
    if nb_turn != 1 and nb_turn%5 == 0:
        name = int((nb_turn/5)+1)
        
        for team_number in range(1, 3):
            dico_ant_played['team' + str(team_number)]['ant' + str(name)] = {}
            dico_ant_played['team' + str(team_number)]['ant' + str(name)]['position'] = [int(dico_gameboard['anthills'][team_number-1][0]),int(dico_gameboard['anthills'][team_number-1][1])]
            dico_ant_played['team' + str(team_number)]['ant' + str(name)]['current_level'] = dico_level['team' + str(team_number)]
            dico_ant_played['team' + str(team_number)]['ant' + str(name)]['health_points'] = dico_rules['team' + str(team_number)]['ant']['level' + str(dico_level['team' + str(team_number)])]['health_points']
            dico_ant_played['team' + str(team_number)]['ant' + str(name)]['strength'] = dico_rules['team' + str(team_number)]['ant']['level' + str(dico_level['team' + str(team_number)])]['strength']
            dico_ant_played['team' + str(team_number)]['ant' + str(name)]['clod_carry'] = False
            dico_ant_played['team' + str(team_number)]['ant' + str(name)]['block'] = False

    return dico_ant_played
#4. Detect if there are clods around anthills
def create_dico_gameboard(dico_cpx):
    """Create the gameboard dictionary.

    Parameter
    ---------
    dico_cpx: the dictonary containing all the file.cpx information (dict)

    Return
    ------
    dico_gameboard : dictionary with data about gameboard (dict)

    Version
    -------
    specification: Corentin Germeau (v. 1 19/02/21)
    implementation: Antoine De Coster (v. 1 21/02/21)

    """
    #creation of the gameboard dictionary 
    dico_gameboard = {}

    #recover and store anthills positions in the dico gameboard.
    nb = 0
    list_anthills = []
    nb_anthills = int(len(dico_cpx['anthills'])/2)
    
    for anthills in range(0,nb_anthills):
        list_anthills.append((int(dico_cpx['anthills'][nb]),int(dico_cpx['anthills'][nb+1])))
        nb += 2
    dico_gameboard['anthills'] = list_anthills

    ##recover and store clods positions in the dico gameboard.
    dico_gameboard['clods'] = dico_cpx['clods']

    ##recover and store map positions in the dico gameboard.
    #no loop needed because there could not be more infos about the map (for the game such as described)
    dico_gameboard['map']= {}
    dico_gameboard['map']['nb_column'] = int(dico_cpx['map'][0])
    dico_gameboard['map']['nb_row'] = int(dico_cpx['map'][1])
    
    return dico_gameboard

#4. Detect if there are clods around anthills

def nearby_anthills(dico_gameboard):
    """Count the number of clods adjacent to the anthill.
    
    Parameter
    ---------
    dico_gameboard: dictionary with data about gameboard (dict)

    Return
    ------
    around_anthill: clods around anthill (dict)

  
    """
    around_anthill = {}
    around_anthill['team1'] = {'left': False, 'right': False, 'high': False, 'low': False, 'high_left' : False, 'high_right': False, 'low_left': False, 'low_right': False}
    around_anthill['team2'] = {'left': False, 'right': False, 'high': False, 'low': False, 'high_left' : False, 'high_right': False, 'low_left': False, 'low_right': False}

    for team_number in range(1,3):
        for clod_number in range(1, len(dico_gameboard['clods'])+1):
            # Check if there is a clod around the anthill
            x_anthill_left = dico_gameboard['anthills'][team_number-1][0] - 1
            y_anthill_left = dico_gameboard['anthills'][team_number-1][1]
            if dico_gameboard['clods']['clod_' + str(clod_number)]['coordinates'][0] == x_anthill_left and dico_gameboard['clods']['clod_' + str(clod_number)]['coordinates'][1] == y_anthill_left:
                around_anthill['team' + str(team_number)]['left'] = True

            x_anthill_right = dico_gameboard['anthills'][team_number-1][0] + 1
            y_anthill_right = dico_gameboard['anthills'][team_number-1][1]
            if dico_gameboard['clods']['clod_' + str(clod_number)]['coordinates'][0] == x_anthill_right and dico_gameboard['clods']['clod_' + str(clod_number)]['coordinates'][1] == y_anthill_right:
                around_anthill['team' + str(team_number)]['right'] = True

            x_anthill_high = dico_gameboard['anthills'][team_number-1][0]
            y_anthill_high = dico_gameboard['anthills'][team_number-1][1] - 1
            if dico_gameboard['clods']['clod_' + str(clod_number)]['coordinates'][0] == x_anthill_high and dico_gameboard['clods']['clod_' + str(clod_number)]['coordinates'][1] == y_anthill_high:
                around_anthill['team' + str(team_number)]['high'] = True

            x_anthill_low = dico_gameboard['anthills'][team_number-1][0]
            y_anthill_low = dico_gameboard['anthills'][team_number-1][1] + 1
            if dico_gameboard['clods']['clod_' + str(clod_number)]['coordinates'][0] == x_anthill_low and dico_gameboard['clods']['clod_' + str(clod_number)]['coordinates'][1] == y_anthill_low:
                around_anthill['team' + str(team_number)]['low'] = True

            x_anthill_high_left = dico_gameboard['anthills'][team_number-1][0] - 1
            y_anthill_high_left = dico_gameboard['anthills'][team_number-1][1] - 1
            if dico_gameboard['clods']['clod_' + str(clod_number)]['coordinates'][0] == x_anthill_high_left and dico_gameboard['clods']['clod_' + str(clod_number)]['coordinates'][1] == y_anthill_high_left:
                around_anthill['team' + str(team_number)]['high_left'] = True

            x_anthill_high_right = dico_gameboard['anthills'][team_number-1][0] + 1
            y_anthill_high_right = dico_gameboard['anthills'][team_number-1][1] - 1
            if dico_gameboard['clods']['clod_' + str(clod_number)]['coordinates'][0] == x_anthill_high_right and dico_gameboard['clods']['clod_' + str(clod_number)]['coordinates'][1] == y_anthill_high_right:
                around_anthill['team' + str(team_number)]['high_right'] = True

            x_anthill_low_left = dico_gameboard['anthills'][team_number-1][0] - 1
            y_anthill_low_left = dico_gameboard['anthills'][team_number-1][1] + 1
            if dico_gameboard['clods']['clod_' + str(clod_number)]['coordinates'][0] == x_anthill_low_left and dico_gameboard['clods']['clod_' + str(clod_number)]['coordinates'][1] == y_anthill_low_left:
                around_anthill['team' + str(team_number)]['low_left'] = True

            x_anthill_low_right = dico_gameboard['anthills'][team_number-1][0] + 1
            y_anthill_low_right = dico_gameboard['anthills'][team_number-1][1] + 1
            if dico_gameboard['clods']['clod_' + str(clod_number)]['coordinates'][0] == x_anthill_low_right and dico_gameboard['clods']['clod_' + str(clod_number)]['coordinates'][1] == y_anthill_low_right:
                around_anthill['team' + str(team_number)]['low_right'] = True

    return around_anthill
def list_nearby_anthills(dico_gameboard):
    """Verify the level of the new ant.
    
    Parameter
    ---------
    dico_gameboard: dictionary with data about gameboard (dict)

    Return
    ------
    dico_level: the level that the new ants will take (dict)

    Version
    -------
    specification: Gabriel Bogaerts (v. 1 19/02/21)
    implementation: Gabriel Bogaerts (v. 1 23/03/21)
    
    """
    around_anthill = {}
    around_anthill['team1'] = {}
    around_anthill['team2'] = {}
    dico_level = {}

    for team_number in range(1,3):
        for clod_number in range(1, len(dico_gameboard['clods'])+1):
            # Check if there is a clod around the anthill
            x_anthill_left = dico_gameboard['anthills'][team_number-1][0] - 1
            y_anthill_left = dico_gameboard['anthills'][team_number-1][1]
            if dico_gameboard['clods']['clod_' + str(clod_number)]['coordinates'][0] == x_anthill_left and dico_gameboard['clods']['clod_' + str(clod_number)]['coordinates'][1] == y_anthill_left:
                around_anthill['team' + str(team_number)]['left'] = True

            x_anthill_right = dico_gameboard['anthills'][team_number-1][0] + 1
            y_anthill_right = dico_gameboard['anthills'][team_number-1][1]
            if dico_gameboard['clods']['clod_' + str(clod_number)]['coordinates'][0] == x_anthill_right and dico_gameboard['clods']['clod_' + str(clod_number)]['coordinates'][1] == y_anthill_right:
                around_anthill['team' + str(team_number)]['right'] = True

            x_anthill_high = dico_gameboard['anthills'][team_number-1][0]
            y_anthill_high = dico_gameboard['anthills'][team_number-1][1] - 1
            if dico_gameboard['clods']['clod_' + str(clod_number)]['coordinates'][0] == x_anthill_high and dico_gameboard['clods']['clod_' + str(clod_number)]['coordinates'][1] == y_anthill_high:
                around_anthill['team' + str(team_number)]['high'] = True

            x_anthill_low = dico_gameboard['anthills'][team_number-1][0]
            y_anthill_low = dico_gameboard['anthills'][team_number-1][1] + 1
            if dico_gameboard['clods']['clod_' + str(clod_number)]['coordinates'][0] == x_anthill_low and dico_gameboard['clods']['clod_' + str(clod_number)]['coordinates'][1] == y_anthill_low:
                around_anthill['team' + str(team_number)]['low'] = True

            x_anthill_high_left = dico_gameboard['anthills'][team_number-1][0] - 1
            y_anthill_high_left = dico_gameboard['anthills'][team_number-1][1] - 1
            if dico_gameboard['clods']['clod_' + str(clod_number)]['coordinates'][0] == x_anthill_high_left and dico_gameboard['clods']['clod_' + str(clod_number)]['coordinates'][1] == y_anthill_high_left:
                around_anthill['team' + str(team_number)]['high_left'] = True

            x_anthill_high_right = dico_gameboard['anthills'][team_number-1][0] + 1
            y_anthill_high_right = dico_gameboard['anthills'][team_number-1][1] - 1
            if dico_gameboard['clods']['clod_' + str(clod_number)]['coordinates'][0] == x_anthill_high_right and dico_gameboard['clods']['clod_' + str(clod_number)]['coordinates'][1] == y_anthill_high_right:
                around_anthill['team' + str(team_number)]['high_right'] = True

            x_anthill_low_left = dico_gameboard['anthills'][team_number-1][0] - 1
            y_anthill_low_left = dico_gameboard['anthills'][team_number-1][1] + 1
            if dico_gameboard['clods']['clod_' + str(clod_number)]['coordinates'][0] == x_anthill_low_left and dico_gameboard['clods']['clod_' + str(clod_number)]['coordinates'][1] == y_anthill_low_left:
                around_anthill['team' + str(team_number)]['low_left'] = True

            x_anthill_low_right = dico_gameboard['anthills'][team_number-1][0] + 1
            y_anthill_low_right = dico_gameboard['anthills'][team_number-1][1] + 1
            if dico_gameboard['clods']['clod_' + str(clod_number)]['coordinates'][0] == x_anthill_low_right and dico_gameboard['clods']['clod_' + str(clod_number)]['coordinates'][1] == y_anthill_low_right:
                around_anthill['team' + str(team_number)]['low_right'] = True

        if len(around_anthill['team' + str(team_number)]) <= 2:
            dico_level['team' + str(team_number)] = 1

        if len(around_anthill['team' + str(team_number)]) >= 3 and len(around_anthill['team' + str(team_number)]) <= 5:
            dico_level['team' + str(team_number)] = 2
    
        if len(around_anthill['team' + str(team_number)]) >= 6 and len(around_anthill['team' + str(team_number)]) < 8:
            dico_level['team' + str(team_number)] = 3
    
        if len(around_anthill['team' + str(team_number)]) == 8:
            return True

    return dico_level

#6. Function checks if the game can continue
def create_dico_ant_played(dico_rules, dico_gameboard, dico_level, nb_turn): # other parameters : ai_vs_player
    """Create the ant dictonary with the players choices

    Parameters
    ----------
    dico_rules : dictionary with data about rules (dict)
    dico_gameboard: dictionary with data about the gameboard (dict)
    dico_level: the level that the ants will take (dict)
    nb_turn: number of turns already played (int)

    Return
    ------
    dico_ant_played: dictionary with data about ant played (dict)

    Version
    -------
    specification: Corentin Germeau (v. 1 19/02/21)
    implemantation: Antoine De Coster, Corentin Germeau (v. 3 29/03/21)

    """
   #create dict
    dico_ant_played = {}

    for team_number in range(1,3):
        #position need to be in a list to be modified further
        #add infos in dico
        dico_ant_played['team' + str(team_number)] = {}
        
        x_spawn_position = int(dico_gameboard['anthills'][team_number-1][0])
        y_spawn_position = int(dico_gameboard['anthills'][team_number-1][1])
        
            
        dico_ant_played['team' + str(team_number)]['ant1'] = { 'current_level':{},'health_points':{},'strength':{},'position':{}}
        dico_ant_played['team' + str(team_number)]['ant1']['current_level'] = dico_level['team' + str(team_number)]
        dico_ant_played['team' + str(team_number)]['ant1']['health_points'] = dico_rules['team' + str(team_number)]['ant']['level' + str(dico_level['team' + str(team_number)])]['health_points']
        dico_ant_played['team' + str(team_number)]['ant1']['strength'] = dico_rules['team' + str(team_number)]['ant']['level' + str(dico_level['team' + str(team_number)])]['strength']
        dico_ant_played['team' + str(team_number)]['ant1']['position'] = [x_spawn_position, y_spawn_position]
        dico_ant_played['team' + str(team_number)]['ant1']['clod_carry'] = False
        dico_ant_played['team' + str(team_number)]['ant1']['block'] = False
   
    return dico_ant_played
def around_ant(dico_ant_played, dico_gameboard):
    """Detect objects around ant.

    Parameters
    ----------
    dico_ant_played: dictionary with data about ant played (dict)
    dico_gameboard: dictionary with data about the gameboard (dict)

    Return
    ------
    list_ant: objects around ant (dict)

    Version
    -------
    specification: Corentin Germeau, Gabriel Bogaerts (v. 1 23/04/21)
    implementation: Corentin Germeau, Gabriel Bogaerts (v. 1 23/04/21)

    """
    list_ant = {}
    list_ant['team1'] = {}
    list_ant['team2'] = {}
    anthill1 = dico_gameboard['anthills'][0]
    anthill2 = dico_gameboard['anthills'][1]

    for team_number in range(1,3):
        for ant_nb in dico_ant_played['team' + str(team_number)]:
            list_ant['team' + str(team_number)][ant_nb] = {'left': False, 'right': False, 'high': False, 'low': False}
            for clod_number in range(1, len(dico_gameboard['clods'])+1):
                x_left = dico_ant_played['team' + str(team_number)][ant_nb]['position'][0] - 1
                y_left = dico_ant_played['team' + str(team_number)][ant_nb]['position'][1]
                if (x_left == dico_gameboard['clods']['clod_' + str(clod_number)]['coordinates'][0] and y_left == dico_gameboard['clods']['clod_' + str(clod_number)]['coordinates'][1]) or (x_left == anthill1[0] and y_left == anthill1[1]) or (x_left == anthill2[0] and y_left == anthill2[1]):
                    list_ant['team' + str(team_number)][ant_nb]['left'] = True

                x_right = dico_ant_played['team' + str(team_number)][ant_nb]['position'][0] + 1
                y_right = dico_ant_played['team' + str(team_number)][ant_nb]['position'][1]
                if (x_right == dico_gameboard['clods']['clod_' + str(clod_number)]['coordinates'][0] and y_right == dico_gameboard['clods']['clod_' + str(clod_number)]['coordinates'][1]) or (x_right == anthill1[0] and y_right == anthill1[1]) or (x_right == anthill2[0] and y_right == anthill2[1]):
                    list_ant['team' + str(team_number)][ant_nb]['right'] = True
                    
                x_high = dico_ant_played['team' + str(team_number)][ant_nb]['position'][0] 
                y_high = dico_ant_played['team' + str(team_number)][ant_nb]['position'][1] - 1
                if (x_high == dico_gameboard['clods']['clod_' + str(clod_number)]['coordinates'][0] and y_high == dico_gameboard['clods']['clod_' + str(clod_number)]['coordinates'][1]) or (x_high == anthill1[0] and y_high == anthill1[1]) or (x_high == anthill2[0] and y_high == anthill2[1]):
                    list_ant['team' + str(team_number)][ant_nb]['high'] = True
                    
                x_low = dico_ant_played['team' + str(team_number)][ant_nb]['position'][0] 
                y_low = dico_ant_played['team' + str(team_number)][ant_nb]['position'][1] + 1
                if (x_low == dico_gameboard['clods']['clod_' + str(clod_number)]['coordinates'][0] and y_low == dico_gameboard['clods']['clod_' + str(clod_number)]['coordinates'][1]) or (x_low == anthill1[0] and y_low == anthill1[1]) or (x_low == anthill2[0] and y_low == anthill2[1]):
                   list_ant['team' + str(team_number)][ant_nb]['low'] = True

    return list_ant
def is_game_over(nb_turn, dico_gameboard):
    """Check if the game is over.

    Parameter
    ---------
    nb_turn: number of turns already played (int)
    dico_gameboard: dictionary with data about gameboard (dict)

    Return
    ------
    result: True if game is over, False otherwise (bool)

    specification: Gabriel Bogaerts (v. 1 19/02/21)
    implementation: Gabriel Bogaerts (v. 1 25/03/21)

    """
    #Check if there are more than 200 turns or if there 8 clods around the anthill
    if nb_turn > 200 or list_nearby_anthills(dico_gameboard) == True:
        return True

    #return False if the game should continue
    else:
        return False
def view_board(dico_ant_played, dico_gameboard, dico_rules, nb_turn, dico_level): 
    """Print the gameboard.

    Parameters
    ----------
    dico_ant_played: dictionary with data about ant played (dict)
    dico_gameboard: dictionary with data about the gameboard (dict)
    dico_rules : dictionary with data about rules (dict)
    nb_turn: number of turns already played (int)
    dico_level: the level that the ants will take (dict)

    Version
    -------
    specification: Corentin Germeau (v. 1 19/02/21)
    implementation: Antoine De Coster, Corentin Germeau, Gabriel Bogaerts (v. 5 29/03/21)

    """
    nb_row = int(dico_gameboard['map']['nb_row'])
    nb_col = int(dico_gameboard['map']['nb_column'])
    anthill1 = dico_gameboard['anthills'][0]
    anthill2 = dico_gameboard['anthills'][1]

    # /!\ Il nous manque 10 lignes qui ont disparues !
    #loop the number of row and column
    for row in range(1, nb_row+1):
        for col in range(1, nb_col+1):
            #Print "#" for an empty case
            print(term.move_xy(col,row) + term.white + '#' + term.normal, end = '', flush = True)

            #team number is 1 or 2 
            #spawn of anthills
            for team_number in range(1,3):
                if nb_turn != 1:
                    if row == dico_gameboard['anthills'][team_number-1][1] and col == dico_gameboard['anthills'][team_number-1][0]:
                        if team_number == 1:
                            # '\x1b[38;2;255;165;0mѪ\x1b(B\x1b[m' is the anthills('Ѫ') in orange
                            print(term.move_xy(col,row) + '\x1b[38;2;255;165;0mѪ\x1b(B\x1b[m', end = '', flush = True)
                        else:
                            # '\x1b[38;2;255;165;0mѪ\x1b(B\x1b[m' is the anthills('Ѫ') in yellow
                            print(term.move_xy(col,row) + '\x1b[33mѪ\x1b(B\x1b[m', end = '', flush = True)

                #spawn of ants
                for ant_nb in dico_ant_played['team' + str(team_number)]:  
                    if row == dico_ant_played['team' + str(team_number)][str(ant_nb)]['position'][1] and col == dico_ant_played['team' + str(team_number)][str(ant_nb)]['position'][0]:
                        # Vérifier le niveau des nouvelles fourmis qui vont spawner avec dico_level
                        if dico_ant_played['team' + str(team_number)][str(ant_nb)]['current_level'] == 1:
                            color = dico_rules['team' + str(team_number)]['ant']['level1']['color']

                        if dico_ant_played['team' + str(team_number)][str(ant_nb)]['current_level'] == 2:
                            color = dico_rules['team' + str(team_number)]['ant']['level2']['color']

                        if dico_ant_played['team' + str(team_number)][str(ant_nb)]['current_level'] == 3:
                            color = dico_rules['team' + str(team_number)]['ant']['level3']['color']
                        
                        print(term.move_xy(col,row) + color, end = '', flush = True)

                        if dico_ant_played['team' + str(team_number)][str(ant_nb)]['position'] != [anthill1[0], anthill1[1]]:
                            # '\x1b[38;2;255;165;0mѪ\x1b(B\x1b[m' is the anthills('Ѫ') in brown
                            print(term.move_xy(anthill1[0],anthill1[1]) + '\x1b[38;2;255;165;0mѪ\x1b(B\x1b[m', end = '', flush = True)
                            
                        if dico_ant_played['team' + str(team_number)][str(ant_nb)]['position'] != [anthill2[0], anthill2[1]]:
                            # '\x1b[38;2;255;165;0mѪ\x1b(B\x1b[m' is the anthills('Ѫ') in yellow
                            print(term.move_xy(anthill2[0],anthill2[1]) + '\x1b[33mѪ\x1b(B\x1b[m', end = '', flush = True)

            #spawn of clods
            for clod_number in range(1, len(dico_gameboard['clods'])+1):
                if row == dico_gameboard['clods']['clod_' + str(clod_number)]['coordinates'][1] and col == dico_gameboard['clods']['clod_' + str(clod_number)]['coordinates'][0]:
                    # '\x1b[32m$\x1b(B\x1b[m' is the clods ('$') in red  
                    print(term.move_xy(col,row) + '\x1b[32m$\x1b(B\x1b[m', end = '', flush = True)

#12. Movements, attacks, lifting and depositing clods

def play_game(group_1, type_1, group_2, type_2, file_path):
    """Play a Copixhe game.

   
    Notes
    -----
    Player type is either human, AI or remote.
    
    If there is an external referee, set group id to 0 for remote player.

    """

    nb_turn = 1

    dico_cpx = search_data(file_path)
    dico_gameboard = create_dico_gameboard(dico_cpx)
    dico_rules = create_dico_rules()
    dico_level = list_nearby_anthills(dico_gameboard)
    dico_ant_played = create_dico_ant_played(dico_rules, dico_gameboard, dico_level, nb_turn)
    around_anthill = nearby_anthills(dico_gameboard)
    around_ants = around_ant(dico_ant_played, dico_gameboard)
    if true :
        dico_ant_played = create_ant(dico_ant_played, nb_turn, dico_rules, dico_gameboard, dico_level)
        around_anthill = nearby_anthills(dico_gameboard)
        around_ants = around_ant(dico_ant_played, dico_gameboard)
        print(term.home + term.clear)
        print('Map :')
        time.sleep(0.5)
        print('\n')
        print(term.home + term.clear)
        view_board(dico_ant_played, dico_gameboard, dico_rules, nb_turn, dico_level)

        nb_turn += 1
        print('\n')
        print(dico_ant_played)
        print('\n')
        print('turn = ' + str(nb_turn))
        print('\n')

    print('GAME OVER')
    # close connection, if necessary 
play_game(1, 'player', 2, 'player', 'basic.cpx')