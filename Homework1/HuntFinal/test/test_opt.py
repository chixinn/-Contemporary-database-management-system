import random
from flask.testing import FlaskClient
from pymongo import MongoClient
from action import opt
from action.init_db import init_db




# 将数据库markets数据清除，避免测试出现前后不一致——暴力debug
def db_zero(ls=['markets']):
    db = client['game']      # 这里要用方括号索引数据库和文档集才能删除文档集
    for col in db.collection_names():
        if col in ls:
            mongo_col = db[col]
            mongo_col.drop()


client = MongoClient("localhost", 27017)
# 测试伊始，将players也一并删除，同上——暴力debug
db_zero(ls=['players', 'markets','treasures','history'])
players = client.game.treasures
treasures = client.game.treasures
markets = client.game.markets
history=client.game.history
init_db(treasures) # 这里还是初始化一下宝物信息库

# 以下三个列表用于生成测试案例
treasure_names = []
for trea in treasures.find():
    treasure_names.append(trea['name'])
usernames = ['cxn', 'sqy', 'zyq']
operations = ["login", "market",  "sell",'unwear','history','homepage','register']
prices = [40, 50, 60, 70, 100, 200, 1000]
passwd=['123456','123456','123456']
seller=['cxn', 'sqy', 'zyq']#


def verify_json(json, username: str, operation: str, treasure: 'str' = 'test', price: 'int' = 0,seller:'str'='testseller',passwd:'str'='testpasswd'):
    if operation == "login":
        result = opt.login(username,passwd)
    elif operation == "market":
        result = opt.look_market(username)
    elif operation == "sell":
        result = opt.sell(username, treasure, price)
    elif operation =='history':
        result=opt.look_history(username)
    elif operation == 'homepage':
        result=opt.homepage(username)
    elif operation == 'register':
        result =opt.user_register(username,passwd)
    elif operation == 'buy':
        result=opt.buy(username,treasure,seller)
    else:
        result = None
    assert json == result


def test_opt_get(client: FlaskClient):
    # 嵌套for循环生成不同的测试案例
    for username in usernames:
        for operation in operations:
            if operation in ['register','login']:
                for item in passwd:
                    response = client.get("/%s/%s/%s" % (username, operation,item))
            if operation in ['box', 'market','homepage','history']:
                response = client.get("/%s/%s" % (username, operation))
                json = response.data.decode('utf-8')
                db_zero()
                verify_json(json, username, operation)
            else:
                if operation == 'sell':
                    for treasure in treasure_names:
                        for price in prices:
                            response = client.get("/%s/%s/%s/%d" % (username, operation,treasure,price))
                            json = response.data.decode('utf-8')
                            db_zero()
                            verify_json(json, username, operation, treasure, price)
              
              