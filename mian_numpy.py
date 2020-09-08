#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  5 18:06:02 2020

@author: llnilschwein
"""

import itertools as its
import numpy as np
import random 
import math
import pandas as pd
import matplotlib.pyplot as plt

colors = ['blue','green','white','yellow','orange']

# initialize play board as np array of size n_fields x n_camels
n_fields = 16

board = np.zeros((len(colors),n_fields))

# put camels onto the first three fields of the board
random.seed(7)

for k in range(len(colors)):
    field = random.randint(0,2)
    stackpos = board[:,field].max()+1
    board[k,field] = stackpos
    
def get_positions(board):
    # returns positions of different colors as np.array. winner is colors[positions[0]]
    L1 = board !=0
    
    M_mult = np.tile(np.arange(n_fields)*n_fields,(5,1))
    
    scores = M_mult*L1+board
    scores_lin = scores.sum(axis = 1)
    positions = (-scores_lin).argsort()
    return positions
    
def move_camel(board,color,number):
    L1 = board[color,:] !=0
    stackpos = board[color,L1]
    target_stacksize = max(board[:,np.roll(L1,number)])
    for k in range(len(board)):
        if board[k,L1] >=stackpos:
            board[k,L1] += target_stacksize - stackpos+1
            board[k,:] = np.roll(board[k,:],number)

#move_camel(board,3,3)  


  
# make generators for possible permutations
numbers = [1,2,3]
number_permutations = its.product(numbers,repeat = len(colors))              
color_permutations = its.permutations(range(len(colors)))     

# calculate total number of combinations
n_number_permutations = len(numbers)**len(colors)
n_color_permutations = math.factorial(len(colors))
n_total_permutations = n_number_permutations*n_color_permutations


# initialize result dataframe

#data  = pd.DataFrame(columns = ['color_1','number_1','color_2','number_2','color_3','number_3','color_4','number_4','color_5','number_5','result_blue','result_green','result_orange','result_yellow','result_white'])
count = 0

data_dict ={}
categories = ['color','number','rank']
for k in range(len(colors)):
    for cat in categories:
        data_dict[cat +'_%i'%(k)] = np.zeros(n_total_permutations)


for col_perm in color_permutations:
    number_permutations = its.product(numbers,repeat = len(colors))     
    for num_perm in number_permutations:
        board_to_evaluate = board.copy()
        for k in range(len(num_perm)):
            move_camel(board_to_evaluate,col_perm[k],num_perm[k])
#            data.loc[count,'color_'+str(k+1)] = col_perm[k]
            data_dict['color_'+str(k)][count]= col_perm[k]
#            data.loc[count,'number_'+str(k+1)] = num_perm[k]
            data_dict['number_'+str(k)][count]=num_perm[k]
        pos = get_positions(board_to_evaluate)
        for rank,col in enumerate(pos):
#           data.loc[count,'result_'+col]= result
           data_dict['rank_'+str(rank)][count] = col
           
        count += 1
        if count % 1000 ==0:
            print(count)
#
            
data = pd.DataFrame(data =data_dict)            
#for color in colors:
#    plt.plot(data.loc[:,'result_'+color].value_counts()/len(data),label = color,marker = 'o',linestyle = 'none',color = 'black',markerfacecoloralt=color,fillstyle = 'left',markersize = 20)
#plt.legend()
#plt.xlabel('Position after this round')
#plt.ylabel('Probability')
#plt.xticks([1,2,3,4,5])

fig,ax = plt.subplots(nrows =1,ncols=2,sharey =True)

colors_2_plot_win =[]
p_win = data.rank_0.value_counts(normalize = True)

for k in range(len(p_win)):
    colors_2_plot_win.append(colors[int(p_win.keys()[k])])
    
ax[0].plot(colors_2_plot_win,p_win)    

colors_2_plot_ru = []

p_ru = data.rank_1.value_counts(normalize = True)

for k in range(len(p_ru)):
    colors_2_plot_ru.append(colors[int(p_ru.keys()[k])])
    
ax[1].plot(colors_2_plot_ru,p_ru)  

ax[0].set_ylabel('Probability')
ax[0].set_title('Winner')
ax[1].set_title('Runner-up')



