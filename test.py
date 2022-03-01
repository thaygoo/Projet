import blessed, math, os, time
term = blessed.Terminal()
#https://www.fileformat.info/info/unicode/block/box_drawing/images.htm

def board(width, height, color):
    # background + cursor + clear + hide cursor
    print(term.on_darkslategray4 + term.home + term.clear)

    #header
    print(term.center(color + '╔' + 3 * '═' + (int(width) - 1) * ('╦' + 3 * '═') + '╗'))
    print(term.center(color + '║' + width * (3 * ' ' + '║')))

    #body
    for i in range(height - 1):
        print(term.center(color + '╠' + (int(width) - 1) * (3 * '═' + '╬') + 3 * '═' + '╣'))
        print(term.center(color + '║' + width * (3 * ' ' + '║')))
        
    #foot
    print(term.center(color + '╚' + 3 * '═' + (int(width) - 1) * ('╩' + 3 * '═') + '╝'))

def config(file):
    config = {1:{'alpha': '', 'omega': '', 'normal': []}, 2:{'alpha': '', 'omega': '', 'normal': []}, "food":{}, 'map':()}

    with open(file) as fp:
        line = fp.readline()
        while line:
            if 'map:' in line.strip():
                line = fp.readline()
                line = line.rsplit(" ")
                line[1] = line[1].rstrip("\n")
                config['map'] = line

            elif 'werewolves:' in line.strip():
                line = fp.readline()
                while 'foods:' not in line.strip():
                    if 'alpha' in line.strip():
                        config[int(line.strip()[0])]['alpha'] = [int(line.strip().split(' ').pop(1)), int(line.strip().split(' ').pop(2)), int(100)]
                    elif 'omega' in line.strip():
                        config[int(line.strip()[0])]['omega'] = [int(line.strip().split(' ').pop(1)), int(line.strip().split(' ').pop(2)), int(100)]
                    else:
                        config[int(line.strip()[0])]['normal'].append([int(line.strip().split(' ').pop(1)), int(line.strip().split(' ').pop(2)), int(100)])
                    line = fp.readline()
            line = fp.readline()
    return config

dic = config('map.ano')
print('\n', dic[1], '\n\n', dic[2], '\n\n', dic['food'])
#board(8,8,term.black)