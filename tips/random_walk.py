import numpy as np



#print(walk)

upper = 2
lower = -1
upper_times = 0   # 先到达上界的次数
lower_times = 0   # 先到达下界的次数
run_times = range(99999)
for i in run_times:
    draws = np.random.randint(0,2,1000)
    steps = np.where(draws>0, 1, -1)
    walk = steps.cumsum()
    for n in walk:
        if n >= upper:
            upper_times += 1
            break
        if n <= lower:
            lower_times += 1
            break
print(upper_times, lower_times)



