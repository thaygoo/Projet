import blessed, math, os, time
term = blessed.Terminal()
# https://www.fileformat.info/info/unicode/block/box_drawing/images.htm
# Alpha : \u29BB
# Omega : \u25C9
# Normal : \u29BF
# Apple : 
# Berry : 
# Mice : 
# Rabbit : 
# Dear : 

def board(width, height, color): # REGLER LE SOUCIS DU Y
    # background + cursor + clear + hide cursor + term.on_darkslategray4
    print(term.home + term.clear + term.on_dimgrey)

    #centered manualy
    center = int(term.width/2) - int(((4 * width)+1)/2)

    #header
    print(term.move_xy(center, 0) + color + '╔' + 3 * '═' + (int(width) - 1) * ('╦' + 3 * '═') + '╗', end='')
    print(term.move_xy(center, 1) + color + '║' + width * (3 * ' ' + '║'), end='')

    #body
    y = 2
    for i in range(height - 1):
        print(term.move_xy(center, i + y) + color + '╠' + (int(width) - 1) * (3 * '═' + '╬') + 3 * '═' + '╣', end='')
        y += 1
        print(term.move_xy(center, i + y) + color + '║' + width * (3 * ' ' + '║'), end='')
        
    #foot
    print(term.move_xy(center, height*2) + color + '╚' + 3 * '═' + (int(width) - 1) * ('╩' + 3 * '═') + '╝', end='')

    #placing objects
    #Placing Alphas :
    for i in ['alpha', "α"], ['omega', "Ω"]:
        for j in [1, term.bold_red], [2, term.bold_green]:
            # display alpha and omega
            print(term.move_xy(*coordinate(*config('map.ano')[j[0]][i[0]][:2])) + j[1] + i[1])
            # display energy
            print(term.move_xy((coordinate(*config('map.ano')[j[0]][i[0]][:2])[0])-1, (coordinate(*config('map.ano')[j[0]][i[0]][:2])[1])+1) + j[1] + '%d' % (config('map.ano')[j[0]][i[0]][2]))

    # Placing normal wolves:
    for j in [1, "\u29BF", term.bold_red], [2, "\u29BF", term.bold_green]:
        for i in config('map.ano')[j[0]]['normal']:
            # display normal wolves
            print(term.move_xy(*coordinate(*i[:2])) + j[2] + j[1])
            # display energy of them
            print(term.move_xy((coordinate(*i[:2])[0])-1, (coordinate(*i[:2])[1])+1) + j[2] + '%d' % (i[2]))

    #place foods
    for j in ['berries', '\N{CHERRIES}'], ['apples', '\N{RED APPLE}'], ['mice', '\N{RAT}'], ['rabbits', '\N{RABBIT FACE}'], ['deers', '\N{OX}']: 
        for i in config('map.ano')['food'][j[0]]:
            # Display foods
            print(term.move_xy(*coordinate(*i[:2])) + j[1])
            # Display energy of foods
            print(term.move_xy((coordinate(*i[:2])[0])-1, (coordinate(*i[:2])[1])+1) + term.turquoise + '%d' % (i[2]))
    
    display()
    

def coordinate(x, y):
    home = int(term.width/2) - int(((4 * 20)+1)/2)
    x = home+(2+(4*(x-1)))
    y = (y*2)-1
    return x, y

def display():
    print(term.normal + term.move_xy(int((4 * 20)+1), int((2 * 20)+1)) + ' ')

def config(file):
    config = {
        1:{'alpha': '', 'omega': '', 'normal': []}, 
        2:{'alpha': '', 'omega': '', 'normal': []}, 
        "food":{'berries': [], 'apples': [], 'mice': [], 'rabbits': [], 'deers': []}, 
        'map':()
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
                        config[int(line[0])][line.split(' ')[3].rstrip("\n")] = [int(line.split(' ')[1]), int(line.split(' ')[2]), int(100)]
                    else:
                        config[int(line[0])]['normal'].append([int(line.split(' ')[1]), int(line.split(' ')[2]), int(100)])
                    line = fp.readline()

            elif 'berries' in line or 'apples' in line or 'mice' in line or 'rabbits' in line or 'deers' in line:
                config['food'][line.split(' ')[2]].append([int(line.split(' ')[0]), int(line.split(' ')[1]), int(line.split(' ')[3])])
               
            line = fp.readline()
    return config

#dic = config('map.ano')

#print(dic)

board(20,20,term.gold)

#x, y = coordinate(2,1)
#print(term.move_xy(x, y) + term.on_normal + term.black + '\u29BB')

""" for i in range(2000): 
    print(term.red + term.move_xy(10, 20) + "%d" % i)
    time.sleep(0.01) """