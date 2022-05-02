def config(file):
    """Get the data from the config file and create a dictionnary with it.

    Parameters
    ----------
    file (str) : name of the config file 

    Version
    -------
    specification: Marius (v3 28/02/22)
    """
    config = {
        1:{'alpha': '', 'omega': '', 'normal': []}, 
        2:{'alpha': '', 'omega': '', 'normal': []}, 
        "food":{'berries': [], 'apples': [], 'mice': [], 'rabbits': [], 'deers': []}, 
        'map':(),
        'pacify': (),
        'wolfplayed': [],
        'saved_energy': {},
        'stats': { 'healths': [0, 0]},
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



dictionnary = config('map.ano')