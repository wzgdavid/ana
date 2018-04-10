'''
n手同时设定止盈止损，随机达到止损止盈的预期
'''
import numpy as np
from copy import copy,deepcopy


# n次
sum_ = 0
for n in range(99999):
    atr = 4
    #borders = [                              # 1 397690
    #        (-0.5*atr, 2*atr),
    #        (-1*atr,   1.5  *atr),
    #        (-1.5*atr, 1*atr),
    #        (-2  *atr, 0.5  *atr)
    #     ]
    #borders = [                     # 止损 5
    #        (-0.5*atr, 0.5*atr),    # 2  结果 569368
    #        (-1*atr,   1  *atr),
    #        (-1.5*atr, 1.5*atr),
    #        (-2  *atr, 2  *atr)
    #     ]
    #borders = [                      #止损3        # 3   结果 299916
    #        (-0.5*atr, 2*atr),
    #        (-0.5*atr, 1.5  *atr),
    #        (-1*atr,   1*atr),
    #        (-1*atr,   0.5  *atr)
    #     ]
    #borders = [                     #止损3   # 4   结果  380686
    #        (-0.5*atr, 0.5*atr),
    #        (-0.5*atr, 1  *atr),
    #        (-1*atr,   1.5*atr),
    #        (-1*atr,   2  *atr)
    #     ]
    #borders = [                    #止损4      # 5   结果  424954
    #        (-1*atr,   0.5*atr),
    #        (-1*atr,   1  *atr),
    #        (-1*atr,   1.5*atr),
    #        (-1*atr,   2  *atr)
    #     ]
    #borders = [                    #止损4      # 5   结果  463066
    #        (-0.5*atr,   1*atr),
    #        (-0.5*atr,   1.2*atr),
    #        (-1*atr,   1.4  *atr),
    #        (-1*atr,   1.6*atr),
    #        (-1*atr,   2  *atr)
    #     ]
    #borders = [                        # 止损3      # 7   结果 391024
    #        (-1*atr,   1  *atr),
    #        (-1*atr,   1.5*atr),
    #        (-1*atr,   2  *atr)
    #     ]
    #borders = [                        # 止损3      # 7   结果 368588
    #        (-1*atr,   1  *atr),
    #        (-2*atr,   2  *atr)
    #     ]
    borders = [                        # 止损2      # 7   结果 259292
            (-1*atr,   1  *atr),
            (-1*atr,   2  *atr)
         ]
    #borders = [                     # 止损 4.5
    #                               # 2  结果 548582
    #        (-1*atr,   1  *atr),
    #        (-1.5*atr, 1.5*atr),
    #        (-2  *atr, 2  *atr)
    #     ]
    #borders = [                     # 止损 3.5
    #                               # 2  结果 393206
    #        (-0.5*atr,   0.5  *atr),
    #        (-1*atr, 1*atr),
    #        (-1  *atr, 2  *atr)
    #     ]
    draws = np.random.randint(0,2,1000)
    steps = np.where(draws>0, 1, -1)
    walk = steps.cumsum()
    #print(walk)
    one = 0
    for n in walk:
        the_borders = borders
        
        index = []
        for i, border in enumerate(the_borders):
            if n >= border[1]:
                one += border[1]
                
                index.append(i)
            elif n <=border[0]:
                one += border[0]
                
                index.append(i)
        for i in reversed(index):
            the_borders.pop(i)
    #print(one)
    sum_+=one
print(sum_)