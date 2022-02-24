def config():
    """Read the config file and create a dictionnary with it.

    Return
    ------
    config (dic): dictionnary of configuration

    Version
    -------
    specification: Malo (v1 17/02/22)
    """

def board():
    """Creation of the board, place all the things on it.

    Return
    ------
    plate (dic) : board
    dic (dic) : everything, like berry or wolves

    Version
    -------
    specification: Hugo (v1 17/02/22)
    """

def nexturn():
    """Check if Alpha Wolves have enough health to continue

    Return
    ------
    next (bool) : next turn state

    Version
    -------
    specification: Marius (v1 17/02/22)
    """

def control():
    """Take commands of player

    Return
    ------
    controls (list) : controls on list

    Version
    -------
    specification: Hugo (v1 17/02/22)
    """

def ai_moves():
    """Take ai moves and send them as player control

    Return
    ------
    aicontrols (list) : ai's controls

    Version
    -------
    specification: Mathis (v1 17/02/22)
    """

def pacification():
    """Pacification of the omega wolve

    Version
    -------
    specification: Malo (v1 17/02/22)
    """

def bonus():
    """Manage bonus

    Version
    -------
    specification: Mathis (v1 17/02/22)
    """

def food():
    """Manage wolves foods

    Version
    -------
    specification: Hugo (v1 17/02/22)
    """

def attack():
    """Manage wolves attack's

    Version
    -------
    specification: Marius (v1 17/02/22)
    """

def movement():
    """Manage deplacement of the wolves

    Version
    -------
    specification: Hugo (v1 17/02/22)
    """

def end():
    """Manage the end of the game

    Return
    ------
    end (str) : return the stats of the game
    
    Version
    -------
    specification: Malo (v1 17/02/22)
    """

def between(obj1, obj2):
    """Give the distance between two thing on the plate
    
    Parameter
    ---------
    obj1 (string): name of the first obj
    obj2 (string): name of the second obj

    Version
    -------
    specification: Mathis (v1 17/02/22)
    """

def scoreboard():
    """Display the principal elements

    Version
    -------
    specification: Malo (v1 17/02/22)
    """

def energy(wolves, energy):
    """modify energy of a wolves

    Parameters
    ----------
    wolves (string): name of the wolve concern
    energy (int): energy that the wolve has to have

    Version
    -------
    specification: Mathis (v1 17/02/22)
    """