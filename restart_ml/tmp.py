def foo(lst):#引用传递
    lst.append(1234)
l = [5,5,5,5]

foo(l)

print(l)

def bar(a):# 值传递
    a+=1

aa = 4
bar(aa)
print(aa)
# 表面上不一样，一个引用传递，一个值传递
# 其实内在都是把引用指向的内存中的对象传给函数，
#只因为是可变和不可变的原因
# 