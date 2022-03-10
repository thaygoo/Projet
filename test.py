import blessed
term = blessed.Terminal()

def board(width, height, color): 
    # background + cursor + clear + hide cursor + term.on_darkslategray4
    print(term.home + term.clear)

    #centered manualy
    center = int(term.width/2) - int(((4 * width)+1)/2)

    #header
    for i in range(5, 21, 5):
        print(term.normal + term.move_xy(coordinate(i, 0)[0], 0) + color + '%d' % i)

    for i in range(5, 21, 5):
        print(term.move_xy(int(term.width/2) - int(((4 * 20)+1)/2)-3, (i*2)) + '%d' % i)

    print(term.on_gray25 + term.move_xy(center, 1) + color + '╔' + 3 * '═' + (int(width) - 1) * ('╦' + 3 * '═') + '╗', end='')
    print(term.move_xy(center, 2) + color + '║' + width * (3 * ' ' + '║'), end='')

    #body
    y = 3
    for i in range(height):
        print(term.move_xy(center, i + y) + color + '╠' + (int(width) - 1) * (3 * '═' + '╬') + 3 * '═' + '╣', end='')
        y += 1
        print(term.move_xy(center, i + y) + color + '║' + width * (3 * ' ' + '║'), end='')
        
    #foot
    print(term.move_xy(center, (height*2)+1) + color + '╚' + 3 * '═' + (int(width) - 1) * ('╩' + 3 * '═') + '╝', end='')

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

    print(term.normal + term.move_xy(int(term.width/2) - int(((4 * 20)+1)/2), coordinate(0, 21)[1]) + (' ' * ((4 * width)+1)))

    display()
    

def coordinate(x, y):
    home = int(term.width/2) - int(((4 * 20)+1)/2)
    x = home+(2+(4*(x-1)))
    y = (y*2)-1
    return x, y+1

def display():
    print(term.normal + term.move_xy(int((4 * 20)+4), int((2 * 20)+2)) + ' ')

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

def get_order(player, ):
    while not i[0] or not i[1] or not i[2]:
        i = input(term.move_xy(*coordinate(0, 22)) + "Entrez vos ordre : ")
        i = i.rsplit(' ')

    if player == 'human':
        print(i)

    return 

#dic = config('map.ano')

#print(dic) 


board(20,20,term.gold)

#x, y = coordinate(2,1)
#print(term.move_xy(x, y) + term.on_normal + term.black + '\u29BB')

""" for i in range(200): 
    print(term.turquoise + term.on_gray25 + term.move_xy(*coordinate(*config('map.ano')['food']['deers'][1][:2])) + '%d' % (config('map.ano')['food']['deers'][1][2] - i))
    time.sleep(0.01) """

""" i = 1
while i != 'stop':
    i = input(term.move_xy(*coordinate(0, 22)) + "Entrez vos ordre : ")
    i = i.rsplit(' ')
    print(term.move_xy(*coordinate(int(i[0]), int(i[1]))) + f'{i[2]}') """