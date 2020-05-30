import itertools as its

class Camel:
       def __init__(self, color, field, stackpos = 0):
           self.color = color
           self.field = field
           self.stackpos = stackpos

colors = ['blue','green','white','yellow','orange']

camels = {}

for color in colors:
    field = input(f'Enter field of {color} camel: ')
    stackpos = input(f'Enter number of camels below the {color} camel: ')
    camels[color] = Camel(color,field,stackpos)

