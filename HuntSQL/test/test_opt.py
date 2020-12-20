#测试逻辑跟MongoDB差不多
# 关于pytest ：与上次不同，因为没有前端，很多边界测试的返回值跟JSON assert难以匹配通过。
# report.txt中的是我只测试了很少一部分函数的report。
# 主要测试还是根据URL进行测试。
from flask.testing import FlaskClient
from sqlalchemy import create_engine, MetaData, Table, select
from sqlalchemy.ext.declarative import declarative_base

from action import opt
from action.init_db import init_testplayer,init_test_box,init_user_takeaway,init_treasure,init_db,drop_db

base = declarative_base()



# 加载数据库
engine = create_engine("postgresql://chixinning:123456@localhost:5432/hunt")
conn = engine.connect()
meta = MetaData(engine)

takeaway = Table("takeaway", meta, autoload=True)
players = Table("players", meta, autoload=True)
treasures = Table("treasures", meta, autoload=True)
markets = Table("markets", meta, autoload=True)
box = Table("box", meta, autoload=True)

# 定义一个清空数据库其它内容只有初始化的函数


drop_db(engine)  # 先清除原先的不然初始化有问题, 删除了表，而不是让表的内容为空
init_db(engine)
# 使用测试案例的前提是存在宝物库，和正常运行的前提一样，只有宝物库是初始化了的
# 测试案例列表
# 没有测试很多 所以opt.py的覆盖率就比较低，边界检查的情况都写在代码中了

init_testplayer(engine)

# hunt=# select * from players;
#  pname | pid | passwd | money | fortune | working
# -------+-----+--------+-------+---------+---------
#  zyq   |   1 | 123456 |  1000 |      10 |      10
#  sqy   |   2 | 123456 | 10000 |      10 |      10
#  cxn   |   3 | 123456 |  1000 |      10 |      10
# (3 rows)
init_test_box(engine)
# hunt=# select * from box;
#  bid | pid | tid
# -----+-----+-----
#    1 |   1 |   1
#    2 |   1 |   2
#    3 |   1 |   3
#    4 |   1 |   4
#    5 |   2 |   2
#    6 |   2 |   5
#    7 |   2 |   6
#    8 |   2 |  66
#    9 |   2 |  77
#   10 |   3 |   3
# (10 rows)
init_user_takeaway(engine)
# hunt=# select * from takeaway;
#  aid | pid |  tname  | tid | tlevel |  ttype
# -----+-----+---------+-----+--------+---------
#    1 |   1 | rope    |  83 |      5 | working
#    2 |   1 | diya    |  82 |      5 | fortune
#    3 |   1 | diamond |  81 |     10 | fortune
#    4 |   2 | rope    |  83 |      5 | working
#    5 |   2 | diya    |  82 |      5 | fortune
#    6 |   2 | diamond |  81 |     10 | fortune
#    7 |   3 | rope    |  83 |      5 | working
#    8 |   3 | diya    |  82 |      5 | fortune
#    9 |   3 | diamond |  81 |     10 | fortune
# (9 rows)



def verify_json(json, username: str, operation: str, treasure: 'str' = 'test', price: 'int' = 0,seller:'str'='testseller',passwd:'str'='testpasswd'):
    if operation == "login":
        result = opt.login(username,passwd)
    elif operation == "market":
        result = opt.look_market(username)
    elif operation == 'homepage':
        result=opt.homepage(username)
    elif operation == 'register':
        username='yzr'
        passwd='123456'
        result =opt.user_register(username,passwd)
    elif operation == 'buy':
        result=opt.buy(username,treasure,seller)
    elif operation =='sell':
        result=opt.sell(username,treasure,price)
    elif operation =='withdraw':
        result=opt.withdraw(username,treasure)
    elif operation =='wear':
        result=opt.wear(username,treasure)
    elif operation =='unwear':
        result=opt.unwear(username,treasure)
    else:
        result = None
    assert json == result

def test_opt_login(client:FlaskClient):
    operation='login'
    username='cxn'
    passwd="123456"
    response = client.get("/%s/%s/%s" % (username, operation,passwd))
    json=response.data.decode('utf-8')
    verify_json(json,username,operation)
# def test_opt_forgetPasswd(client:FlaskClient):
#     operation=''
def test_opt_homepage(client:FlaskClient):
    operation='homepage'
    username='zyq'
    response = client.get("/%s/%s" % (username, operation))
    json=response.data.decode('utf-8')
    verify_json(json,username,operation)

def test_opt_unwear(client:FlaskClient):
    operation='unwear'
    username='zyq'
    treasure='diamond'
    response = client.get("/%s/%s/%s/" % (username, operation,treasure))
    json=response.data.decode('utf-8')
    verify_json(json,username,operation)
def test_opt_unwear(client:FlaskClient):
    operation='unwear'
    username='zyq'
    treasure='rope'
    response = client.get("/%s/%s/%s/" % (username, operation,treasure))
    json=response.data.decode('utf-8')
    verify_json(json,username,operation)
def test_opt_unwear_noTrea(client:FlaskClient):
    operation='unwear'
    username='zyq'
    treasure='lalala'#no such treasure
    response = client.get("/%s/%s/%s/" % (username, operation,treasure))
    json=response.data.decode('utf-8')
    verify_json(json,username,operation)
def test_opt_unwear_noUser(client:FlaskClient):
    operation='unwear'
    username='hhh'
    treasure='lalala'#no such treasure
    response = client.get("/%s/%s/%s/" % (username, operation,treasure))
    json=response.data.decode('utf-8')
    verify_json(json,username,operation)
def test_opt_wear_noUser(client:FlaskClient):
    operation='wear'
    username='hhh'
    treasure='lalala'#no such treasure
    response = client.get("/%s/%s/%s/" % (username, operation,treasure))
    json=response.data.decode('utf-8')
    verify_json(json,username,operation)
def test_opt_unwear_noTrea(client:FlaskClient):
    operation='unwear'
    username='zyq'
    treasure='lalala'#no such treasure
    response = client.get("/%s/%s/%s/" % (username, operation,treasure))
    json=response.data.decode('utf-8')
    verify_json(json,username,operation)

def test_opt_sell(client:FlaskClient):
    operation='sell'
    username='zyq'
    treasure='diamond'
    price=123
    response = client.get("/%s/%s/%s/%s" % (username, operation,treasure,price))
    json=response.data.decode('utf-8')
    verify_json(json,username,operation)

def test_opt_wear_OnSale(client:FlaskClient):
    operation='wear'
    username='zyq'
    treasure='diamond'#no such treasure
    response = client.get("/%s/%s/%s/" % (username, operation,treasure))
    json=response.data.decode('utf-8')
    verify_json(json,username,operation)

def test_opt_wear_WrongTreaKind(client:FlaskClient):
    operation='wear'
    username='zyq'
    treasure='baznw'#no more working treasure
    response = client.get("/%s/%s/%s/" % (username, operation,treasure))
    json=response.data.decode('utf-8')
    verify_json(json,username,operation)

def test_opt_wear_working(client:FlaskClient):
    operation='wear'
    username='zyq'
    treasure='baznw'#no more working treasure
    response = client.get("/%s/%s/%s/" % (username, operation,treasure))
    json=response.data.decode('utf-8')
    verify_json(json,username,operation)

def test_opt_box(client:FlaskClient):
    operation='box'
    username='zyq'
    response = client.get("/%s/%s" % (username, operation))
    json=response.data.decode('utf-8')
    verify_json(json,username,operation)

def test_opt_market(client:FlaskClient):
    operation='market'
    username='zyq'
    response = client.get("/%s/%s" % (username,operation))
    json=response.data.decode('utf-8')
    verify_json(json,username,operation)

