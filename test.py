import blessed, math, os, time
term = blessed.Terminal()
#https://www.fileformat.info/info/unicode/block/box_drawing/images.htm

def board(width, height, color):
    # background + cursor + clear + hide cursor
    print(term.on_darkslategray4 + term.home + term.clear + term.hide_cursor)

    #header
    print(term.center(color + '\u2554' + 3 * '\u2550' + (int(width) - 1) * ('\u2566' + 3 * '\u2550') + '\u2557'))
    print(term.center(color + '\u2551' + width * (3 * '\u0020' + '\u2551')))

    #body
    for i in range(height - 1):
        print(term.center(color + '\u2560' + (int(width) - 1) * (3 * '\u2550' + '\u256C') + 3 * '\u2550' + '\u2563'))
        print(term.center(color + '\u2551' + width * (3 * '\u0020' + '\u2551')))
        
    #foot
    print(term.center(color + '\u255A' + 3 * '\u2550' + (int(width) - 1) * ('\u2569' + 3 * '\u2550') + '\u255D'))

def config(file):
    config = {1:{}, 2:{}, "food":{}, 'map':()}
    with open(file) as fp:
        line = fp.readline()
        while line:
            if line.strip() == 'map:':
                line = fp.readline()
                print(line)
                config['map'] = line.rsplit(" ")
            line = fp.readline()
    return config

#print(config('map.ano'))
board(20,10,term.black)