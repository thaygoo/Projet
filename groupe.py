from random import choice


name = ["Malo", "Alex", "Jean-Mi", "Mathis", "Hugo"]
g1 = []
g2 = []
r = ""

def groupeprojet():
    for i in range(2):
        r = choice(name)
        g1.append(r)
        name.remove(r)
    for j in range(3):
        r = choice(name)
        g2.append(r)
        name.remove(r)
    return "Groupe 1:", g1, "Groupe 2:", g2

print(groupeprojet()) 
