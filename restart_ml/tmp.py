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

# 先用root安装git
[wzg@ workspace]$ su root
[root@ workspace]# yum install git

先到自己的github上建一个空repository，然后clone这个空的repository
[root@ workspace]# git clone https://github.com/wzgdavid/test.git
[root@ test]# vim a.py            //随便建一个文件
[root@ test]# git status
[root@ test]# git commit -m 'sdf'    //试一下提交，他会提示我需要干嘛
    git config --global user.name "Your Name"
    git config --global user.email you@example.com

设置完毕后，您可以用下面的命令来修正本次提交所使用的用户身份：

    git commit --amend --reset-author
用以上提示的三句命令，
[root@ test]# git push origin master  # 然后可以push了
