import itertools as its
import numpy as np
import random 
import math
import pandas as pd
import copy
import matplotlib.pyplot as plt

colors = ['blue','green','white','yellow','orange']

# initialize play board as list of empty list
n_fields = 16

board = []

for k in range(n_fields):
    board.append([])

# put camels onto the first three fields of the board
random.seed(7)

camels = colors.copy()
random.shuffle(camels)

while len(camels)>0:        
    field = random.randint(0,2)
    board[field].append(camels.pop())


def get_positions(play_board):
    order = sum(play_board,[])
    order.reverse()
    positions = {}
    for k, color in enumerate(order):
        positions[color] = k+1
    
    return positions

def move_camel(play_board,color,number):
    caravan = []
    index = -1
    for field in play_board:
        index +=1
        if color in field:
            while color in field:
                caravan.append(field.pop())
            break
        else:
            pass
    caravan.reverse()
    play_board[index+number] = play_board[index+number]+caravan
  
# make generators for possible permutations
numbers = [1,2,3]
number_permutations = its.product(numbers,repeat = len(colors))              
color_permutations = its.permutations(colors)     

# calculate total number of combinations
n_number_permutations = len(numbers)**len(colors)
n_color_permutations = math.factorial(len(colors))
n_total_permutations = n_number_permutations*n_color_permutations


# initialize result dataframe

data  = pd.DataFrame(columns = ['color_1','number_1','color_2','number_2','color_3','number_3','color_4','number_4','color_5','number_5','result_blue','result_green','result_orange','result_yellow','result_white'])
count = 0
for col_perm in color_permutations:
    number_permutations = its.product(numbers,repeat = len(colors))     
    for num_perm in number_permutations:
        board_to_evaluate = copy.deepcopy(board)
        for k in range(len(num_perm)):
            move_camel(board_to_evaluate,col_perm[k],num_perm[k])
            data.loc[count,'color_'+str(k+1)] = col_perm[k]
            data.loc[count,'number_'+str(k+1)] = num_perm[k]
            
        pos = get_positions(board_to_evaluate)
        for col,result in pos.items():
            data.loc[count,'result_'+col]= result
        count += 1
        if count % 1000 ==0:
            print(count)

for color in colors:
    plt.plot(data.loc[:,'result_'+color].value_counts()/len(data),label = color,marker = 'o',linestyle = 'none',color = 'black',markerfacecoloralt=color,fillstyle = 'left',markersize = 20)
plt.legend()
plt.xlabel('Position after this round')
plt.ylabel('Probability')
plt.xticks([1,2,3,4,5])
       
    
