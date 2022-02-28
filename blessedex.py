import blessed, random, time
term = blessed.Terminal()
#https://www.fileformat.info/info/unicode/block/box_drawing/images.htm

color = term.black
width = 5
height = 5

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