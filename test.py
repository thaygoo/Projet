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
    print(term.home + term.clear )

    #centered manualy
    center = int(term.width/2) - int(((4 * width)+1)/2)

    #header
    print(term.move_xy(center, 0) + color + '╔' + 3 * '═' + (int(width) - 1) * ('╦' + 3 * '═') + '╗')
    print(term.move_xy(center, 0) + color + '║' + width * (3 * ' ' + '║'))

    #body
    for i in range(height - 1):
        print(term.move_xy(center, 0) + color + '╠' + (int(width) - 1) * (3 * '═' + '╬') + 3 * '═' + '╣')
        print(term.move_xy(center, 0) + color + '║' + width * (3 * ' ' + '║'))
        
    #foot
    print(term.move_xy(center, 0) + color + '╚' + 3 * '═' + (int(width) - 1) * ('╩' + 3 * '═') + '╝')

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
                while 'foods:' not in line:
                    if 'alpha' in line:
                        config[int(line[0])]['alpha'] = [int(line.split(' ').pop(1)), int(line.split(' ').pop(2)), int(100)]
                    elif 'omega' in line:
                        config[int(line[0])]['omega'] = [int(line.split(' ').pop(1)), int(line.split(' ').pop(2)), int(100)]
                    else:
                        config[int(line[0])]['normal'].append([int(line.split(' ').pop(1)), int(line.split(' ').pop(2)), int(100)])
                    line = fp.readline()

            print(line)
            #elif 'foods:' in line:
            #    print(line)
            line = fp.readline()
    return config

#dic = config('map.ano')
#print('\n', dic[1], '\n\n', dic[2], '\n\n', dic['food'])
board(8,8,term.gold)

print(term.red + term.move_xy(10, 6) + '\u29BB')