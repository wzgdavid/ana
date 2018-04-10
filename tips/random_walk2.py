'''
n手同时设定止盈止损，随机达到止损止盈的预期
'''
import numpy as np
from copy import copy,deepcopy


#print(walk)
atr = 4
borders = [
            (-0.5*atr, 0.5*atr),
            (-1*atr, 1  *atr),
            (-1.5  *atr, 1.5*atr),
            (-2  *atr, 2  *atr)
         ]


# 一次
draws = np.random.randint(0,2,1000)
steps = np.where(draws>0, 1, -1)
walk = steps.cumsum()
#print(walk)
one = 0
for n in walk:
    the_borders = borders
    index = []
    for i, border in enumerate(the_borders):
        print(the_borders)
        if n >= border[1]:
            one += border[1]
            index.append(i)
        elif n <=border[0]:
            one += border[0]
            index.append(i)
    for i in reversed(index):
        the_borders.pop(i)
print(one)

# n次
#sum_ = 0
#for n in range(3):
#    draws = np.random.randint(0,2,1000)
#    steps = np.where(draws>0, 1, -1)
#    walk = steps.cumsum()
#    #print(walk)
#    one = 0
#    for n in walk:
#        the_borders = copy(borders)
#        
#        index = []
#        for i, border in enumerate(the_borders):
#            if n >= border[1]:
#                one += border[1]
#                
#                index.append(i)
#            elif n <=border[0]:
#                one += border[0]
#                print(border[0],one)
#                index.append(i)
#        for i in reversed(index):
#            the_borders.pop(i)
#    #print(one)
#print(sum)