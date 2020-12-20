# 使用python随机生成字符串和随机数 保证宝物的名字不同, 自己受打实在太麻烦了Orz
import random
dbfile=open('db.txt','w+')
level=random.randint(1,80)
namelist=[]
levellist=[]
textstr='Treasures(tname=)'
'''treasure_obj=Treasures(tname='kwdro',type='working',level=31) 
    session.add(treasure_obj)'''

for i in range(40):
    name=random.sample('zyxwvutsrqponmlkjihgfedcba',5)
    name_=''
    textstr='Treasures(tname='
    for i in name:
        name_=name_+i
    level=random.randint(1,50)
    if name_ not in namelist:
        namelist.append(name)
        textstr=textstr+'\''+str(name_)+'\''+',type=\'working\',level='+str(level)+'),'
        print(textstr,file=dbfile)

for i in range(40):
    name=random.sample('zyxwvutsrqponmlkjihgfedcba',5)
    name_=''
    textstr='Treasures(tname='
    for i in name:
        name_=name_+i
    level=random.randint(1,50)
    if name_ not in namelist:
        namelist.append(name)
        textstr=textstr+'\''+str(name_)+'\''+',type=\'fortune\',level='+str(level)+'),'
        print(textstr,file=dbfile)
         




