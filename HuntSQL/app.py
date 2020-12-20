# from apscheduler.schedulers.blocking import BlockingScheduler
from flask_apscheduler import APScheduler
from flask import Flask
import os
import random
import sys
from action.config import Config
from action.init_db import Players, Takeaway, drop_db, init_db
from action.opt import bp
from action.opt import recovery_treasure

from sqlalchemy import create_engine, MetaData, Table,select
from sqlalchemy.orm import sessionmaker
from action.config import Config
from action.init_db import init_db
from time import time
MAXSTROAGE=20
import apscheduler.schedulers.blocking #本来想打最大数的 没用到

from action.init_db import init_db

file_dir = os.path.dirname(__file__)    #
sys.path.append(file_dir)   #
# app = Flask(__name__)
# @app.route('/')
# def index():
#     return "Hello, World!"
engine = create_engine('postgresql+psycopg2://chixinning:123456@localhost/hunt',encoding='utf-8',echo=True)

db_session_class = sessionmaker(bind=engine)    # db_session_class 仅仅是一个类
session = db_session_class() 
conn = engine.connect()
meta = MetaData(engine)

players = Table("players", meta, autoload=True)
treasures = Table("treasures", meta, autoload=True)
box = Table("box", meta, autoload=True)

# 自动寻宝
def labour():
    # 遍历每个玩家
    for player in conn.execute(select([players])):
        print('*************')
        # print(player['pname'])
        name=player['pname']
        # working_level=10#初始working_level的值，在sql里可以新建玩家的时候就初始化 (mongodb)
        working_level = player['working']
        money_get = random.randint((working_level-1)*100, (working_level+1)*100)
        # 打入账户
        money = player['money'] + money_get
        # 更新账户
        conn.execute(players.update().values(money=money))
        print('打工记录更新成功')
        # print("玩家 %-4s 到账 %d" % (name, money_get))
    return 0

# 自动打工
def hunt():
    # 遍历每个玩家
    session = sessionmaker(engine)()
    for player in conn.execute(select([players])):
        pid = player['pid']
        # pname=player['pname']
        # 若宝箱已满,根据id来count
        #这个地方不能改成直接在sql里count吗？
        player_box = conn.execute(select([box]).where(box.c.pid == pid)).fetchall()# 使用pid做joinKey
        size=session.query(box).filter(box.c.pid == pid).count()
        if size > MAXSTROAGE:
            recovery_treasure(pid)
        # 获取玩家当前的fortune值
        fortune_level=player['fortune']
        print(fortune_level)
        #level是寻到宝物的依据
        prob_treasure_list = session.query(treasures.c.tid).filter(treasures.c.level >= fortune_level - 3,treasures.c.level <= fortune_level + 3).all()
        if(len(prob_treasure_list)==0):#宝物库没有该level宝物怎么办？自动进入下次寻宝
            return 0
        # print(prob_treasure_list)
        x = random.randint(0, len(prob_treasure_list) - 1)
        # 更新该玩家的box库
        # 玩家宝物库里不能有同名宝物；
        for i in player_box:
            if prob_treasure_list[x][0]==i[2]:
                return 0
        # 因为tid只是外键不是unique
        conn.execute(box.insert().values(pid=pid, tid=prob_treasure_list[x][0]))
        # print("玩家 %-4s 获得宝物 %s" % (pname,prob_treasure_list[x]['name'] ))
        print("加油！寻宝人！")
    return 0

if __name__ == "__main__":
    drop_db(engine)
    init_db(engine)#进行初始化构建
    app = Flask(__name__)
   
    
    # take_obj=Takeaway(pid=1,twname='rope',tf1name='diamond',tf2nam2='diya')
    app.config.from_object(Config())
    scheduler = APScheduler()#APS定期巡航
    scheduler.init_app(app)
    scheduler.start()

    app.register_blueprint(bp)
    
    app.run()