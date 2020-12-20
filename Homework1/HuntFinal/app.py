import os
import random
import sys

from pymongo import MongoClient
from flask import Flask
from flask_apscheduler import APScheduler

from action.config import Config
from action.init_db import init_db
from action.opt import bp
from action.opt import recovery_treasure
from time import time


file_dir = os.path.dirname(__file__)    #
sys.path.append(file_dir)   #

client = MongoClient('localhost', 27017)
players = client.game.players
markets = client.game.markets
treasures = client.game.treasures
history=client.game.history#历史,回滚使用。


# 自动寻宝
def hunt():
    # 遍历每个玩家
    for player in players.find():
        name = player["name"]
        # 宝箱充满
        if len(player['box']) >= 20:#maxBoxVolumn=20
            print("存储箱已满,将自动回收一件低端宝物~")
            recovery_treasure(name)
        # 将玩家佩戴饰品的级别作为寻到宝物的依据
        treasure_takeaway=player['takeaway']
        print(treasure_takeaway)
        print(treasure_takeaway[0]['type'])
        box = players.find_one({"name": name})['box']
        #level是训到宝物的一句
        fortune_level=10
        for treasure in treasure_takeaway:
            if(treasure['type']=="fortune"):
                fortune_level=fortune_level+treasure['level']#玩家是否需要写入attribute属性
        print(fortune_level)
        prob_treasure_list=[]
        # 运气性，将运气上下五个级别的宝物作为寻宝的范围
        #注意这个地方要写数据库
        #如果单纯的这样写会return cursor
        for col in treasures.find({"level": {"$lte": fortune_level+3, "$gte": fortune_level-3}}):
            prob_treasure_list.append(col)
        print(len(prob_treasure_list))
        # 随机寻宝
        x = random.randint(0, len(prob_treasure_list)-1)
        box.append(prob_treasure_list[x])
        # 更新宝物
        players.update_one({"name": name}, {"$set": {"box": box}})
        history.insert_one({"name":name,"opt_time":time(),"opt_type":"hunt","detail":"hunt"+" "+str(x)})
        print("玩家 %-4s 获得宝物 %s" % (name,prob_treasure_list[x]['name'] ))


# 自动劳动(debug done)
def labour():
    # 遍历每个玩家
    for player in players.find():
        treasure_takeaway=player['takeaway']
        #print(treasure_takeaway)
        #print("得到takeaway")
        working_level=10
        #print(treasure_takeaway[0]["type"])
        #print("#")
        for treasure in treasure_takeaway:
            if(treasure["type"]=="working"):
                working_level=treasure['level']
                break
        money_get = random.randint((working_level-1)*100, (working_level+1)*100)
        # 打入账户
        money = player['money'] + money_get
        name = player["name"]
        # 更新账户
        players.update_one({"name": name}, {"$set": {"money": money}})
        history.insert_one({"name":name,"opt_time":time(),"opt_type":"labour","detail":"labour"+" "+"money"+str(money)})

        print("玩家 %-4s 到账 %d" % (name, money_get))



if __name__ == "__main__":
    # 初始化宝物信息库
    init_db(treasures)

    app = Flask(__name__)
    app.config.from_object(Config())  

    scheduler = APScheduler()#APS定期巡航
    scheduler.init_app(app)
    scheduler.start()

    app.register_blueprint(bp)
    app.run()
    
