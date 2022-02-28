import blessed, random, time
term = blessed.Terminal()

#https://www.fileformat.info/info/unicode/block/box_drawing/images.htm



color = term.rgb_to_xyz(233, 172, 10)
width = 5
height = 5
# clear screen and hide cursor
print(term.home + term.clear + term.hide_cursor)

#header
print(term.center(color + '\u2554'+3*'\u2550'+(int(width)-1)*('\u2566'+3*'\u2550')+'\u2557'))
print(term.center(color + '\u2551'+width*(3*'\u0020'+'\u2551')))
#body
for i in range(height-1):
    print(term.center(color + '\u2560'+(int(width)-1)*(3*'\u2550'+'\u256C')+3*'\u2550'+'\u2563'))
    print(term.center(color + '\u2551'+width*(3*'\u0020'+'\u2551')))
#foot
print(term.center(color + '\u255A'+3*'\u2550'+(int(width)-1)*('\u2569'+3*'\u2550')+'\u255D'))

# move cursor + change color of symbol + change color of background + symbol + back to normal
#print(term.move_yx(row, col) + term.green + term.on_rosybrown2 + '●' + term.normal, end='', flush=True)

# move cursor + change color of symbol + change color of background + single space + back to normal
#print(term.move_yx(row, col) + term.on_skyblue + ' ' + term.normal, end='', flush=True)

# move cursor + change color of symbol + change color of background + symbol + back to normal
#print(term.move_yx(row, col) + term.red + term.on_rosybrown2 + '●' + term.normal, end='', flush=True)