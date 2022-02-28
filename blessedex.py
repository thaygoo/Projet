import blessed, random, time
term = blessed.Terminal()

#https://www.fileformat.info/info/unicode/block/box_drawing/images.htm

color = term.red
lenght = 20
# clear screen and hide cursor
print(term.home + term.clear + term.hide_cursor)

#header
print(color + '\u2554'+3*'\u2550'+(int(lenght)-1)*('\u2566'+3*'\u2550')+'\u2557')
print(color + '\u2551'+lenght*(3*'\u0020'+'\u2551'))
#body
for i in range(lenght-1):
    print(color + '\u2560'+(int(lenght)-1)*(3*'\u2550'+'\u256C')+3*'\u2550'+'\u2563')
    print(color + '\u2551'+lenght*(3*'\u0020'+'\u2551'))
#foot
print(color + '\u255A'+3*'\u2550'+(int(lenght)-1)*('\u2569'+3*'\u2550')+'\u255D')



# move cursor + change color of symbol + change color of background + symbol + back to normal
#print(term.move_yx(row, col) + term.green + term.on_rosybrown2 + '●' + term.normal, end='', flush=True)

# move cursor + change color of symbol + change color of background + single space + back to normal
#print(term.move_yx(row, col) + term.on_skyblue + ' ' + term.normal, end='', flush=True)

# move cursor + change color of symbol + change color of background + symbol + back to normal
#print(term.move_yx(row, col) + term.red + term.on_rosybrown2 + '●' + term.normal, end='', flush=True)