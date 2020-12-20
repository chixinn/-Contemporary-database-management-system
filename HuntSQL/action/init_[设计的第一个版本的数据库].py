from flask_sqlalchemy import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String #区分大小写
from sqlalchemy import create_engine, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
# 创建表中的字段(列)
from sqlalchemy import Column
# 表中字段的属性
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy import UniqueConstraint, Index
from sqlalchemy.orm import sessionmaker, relationship

#生成 orm 基类
engine = create_engine('postgresql+psycopg2://chixinning:123456@localhost/test',encoding='utf-8',echo=True)


base=declarative_base()

# 创建表

# 不太确定是否要保留此，防止做过多的join从而保留一部分的冗余?
# 那这样也太逆范式化了吧。。。Orz
# 更改current_takeaway也像box一样select进去 这样更新就快乐很多!这样也可以支持多个takeaway的扩展了！
class Players(base):
    __tablename__ = 'players'
    pid = Column('pid',Integer, primary_key=True,nullable=False,autoincrement=True)# 设定主键
    pname = Column('pname',String(64), nullable=False, unique=True) # 用户名和密码都不可为空，且用户名是唯一索引
    passwd = Column('passwd',String(64),nullable=False) # 用户名和密码都不可为空
    money = Column('money',Integer, CheckConstraint("money > 0"))
    fortune = Column('fortune',Integer)
    working = Column('working',Integer)
base.metadata.create_all(engine)

class Treasures(base):
    __tablename__ = 'treasures'
    tid = Column(Integer, primary_key=True, autoincrement=True)
    tname = Column(String(64), unique=True)
    type = Column(String(32))
    level = Column(Integer)
base.metadata.create_all(engine)



class Markets(base):
    __tablename__ = 'markets'
    sid = Column('seller',Integer, primary_key=True, autoincrement=True, unique=True)
    tid = Column('treasure',Integer, ForeignKey('treasures.tid'))
    price = Column('PriceTag',Integer)
base.metadata.create_all(engine)
class Box(base):
    __tablename__ = 'box'
    bid = Column(Integer, primary_key=True)
    pid = Column(Integer, ForeignKey('players.pid'))
    tid = Column(Integer, ForeignKey('treasures.tid'))
base.metadata.create_all(engine)
class Takeaway(base):
    __tablename__ = 'takeaway'
    sid = Column('sid',Integer, primary_key=True, autoincrement=True, unique=True)
    pid=Column('pid',Integer, ForeignKey('players.pid'))
    twname=Column(String(10), ForeignKey('treasures.tname'),nullable=True)
    tf1name=Column(String(10), ForeignKey('treasures.tname'),nullable=True)
    tf2name=Column(String(10), ForeignKey('treasures.tname'),nullable=True)
    twlevel=Column('twlevel',Integer,nullable=True)
    tf1level=Column('tf1level',Integer,nullable=True)
    tf2level=Column('tf2level',Integer,nullable=True)
base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine)
    # 创建session 对象
session = DBSession()

def init_treasure(engine): #我自己不手动生成tid,它会帮我自动生成自增的tid,我需要做的只是insert进去就ok了
   
    session.add_all([
        Treasures(tname='pwklt',type='working',level=39),
Treasures(tname='baznw',type='working',level=45),
Treasures(tname='zmdul',type='working',level=29),
Treasures(tname='dmkve',type='working',level=27),
Treasures(tname='xnlts',type='working',level=7),
Treasures(tname='lahqy',type='working',level=11),
Treasures(tname='ftsch',type='working',level=29),
Treasures(tname='qtjvw',type='working',level=16),
Treasures(tname='fvesh',type='working',level=6),
Treasures(tname='jcmzv',type='working',level=16),
Treasures(tname='lugta',type='working',level=46),
Treasures(tname='hitkp',type='working',level=11),
Treasures(tname='nobst',type='working',level=46),
Treasures(tname='aezox',type='working',level=45),
Treasures(tname='qekng',type='working',level=40),
Treasures(tname='xmjup',type='working',level=30),
Treasures(tname='txiwn',type='working',level=29),
Treasures(tname='wcoqv',type='working',level=19),
Treasures(tname='catyf',type='working',level=47),
Treasures(tname='okheb',type='working',level=4),
Treasures(tname='fgnij',type='working',level=40),
Treasures(tname='awkfn',type='working',level=35),
Treasures(tname='pyejq',type='working',level=3),
Treasures(tname='ytcod',type='working',level=24),
Treasures(tname='arqgk',type='working',level=13),
Treasures(tname='ucleq',type='working',level=11),
Treasures(tname='oqgzk',type='working',level=17),
Treasures(tname='vosuf',type='working',level=44),
Treasures(tname='ocqdi',type='working',level=26),
Treasures(tname='yiugm',type='working',level=9),
Treasures(tname='zpoqs',type='working',level=9),
Treasures(tname='rakem',type='working',level=15),
Treasures(tname='acuby',type='working',level=19),
Treasures(tname='gwlxf',type='working',level=26),
Treasures(tname='gktax',type='working',level=6),
Treasures(tname='eztol',type='working',level=29),
Treasures(tname='qczaw',type='working',level=30),
Treasures(tname='euqov',type='working',level=16),
Treasures(tname='qlkji',type='working',level=35),
Treasures(tname='bgkre',type='working',level=15),
Treasures(tname='zyemw',type='fortune',level=18),
Treasures(tname='qlkec',type='fortune',level=46),
Treasures(tname='ocyrh',type='fortune',level=28),
Treasures(tname='dsjpz',type='fortune',level=36),
Treasures(tname='rkjnb',type='fortune',level=18),
Treasures(tname='tfuwn',type='fortune',level=48),
Treasures(tname='anvhi',type='fortune',level=7),
Treasures(tname='zgfne',type='fortune',level=26),
Treasures(tname='elphc',type='fortune',level=24),
Treasures(tname='dtqzu',type='fortune',level=2),
Treasures(tname='dspto',type='fortune',level=24),
Treasures(tname='zldnq',type='fortune',level=1),
Treasures(tname='wvyba',type='fortune',level=49),
Treasures(tname='ycsbt',type='fortune',level=22),
Treasures(tname='flenc',type='fortune',level=8),
Treasures(tname='ksymq',type='fortune',level=26),
Treasures(tname='ehwuk',type='fortune',level=44),
Treasures(tname='fcjth',type='fortune',level=35),
Treasures(tname='tzmbg',type='fortune',level=34),
Treasures(tname='oqwks',type='fortune',level=37),
Treasures(tname='dgkxt',type='fortune',level=28),
Treasures(tname='ocqsb',type='fortune',level=18),
Treasures(tname='zeoil',type='fortune',level=7),
Treasures(tname='ogirz',type='fortune',level=30),
Treasures(tname='sphmb',type='fortune',level=13),
Treasures(tname='vhuip',type='fortune',level=21),
Treasures(tname='uxbpf',type='fortune',level=18),
Treasures(tname='iylkq',type='fortune',level=22),
Treasures(tname='xmksh',type='fortune',level=36),
Treasures(tname='atwek',type='fortune',level=20),
Treasures(tname='xqhda',type='fortune',level=25),
Treasures(tname='iswug',type='fortune',level=27),
Treasures(tname='frcdh',type='fortune',level=33),
Treasures(tname='hpngv',type='fortune',level=28),
Treasures(tname='kfprw',type='fortune',level=39),
Treasures(tname='qmxsc',type='fortune',level=6),
Treasures(tname='epxgo',type='fortune',level=30),
Treasures(tname='rcyiz',type='fortune',level=35),
Treasures(tname='upqvt',type='fortune',level=24),
Treasures(tname='vdskm',type='fortune',level=38),
Treasures(tname='diamond',type='fortune',level=10),
Treasures(tname='diya',type='fortune',level=5),
Treasures(tname='rope',type='working',level=5)

    ])
    session.commit() 
def init_testplayer(engine):
    player_obj1=Players(pname='cxn',passwd='123456',money=1000,fortune=10,working=10)
    player_obj2=Players(pname='sqy',passwd='123456',money=10000,fortune=10,working=10)
    player_obj3=Players(pname='zyq',passwd='123456',money=1000,fortune=10,working=10)
    session.add_all([player_obj3,player_obj2,player_obj1])  
    session.commit() # 你个憨憨 不加session.commit根本无法commit      
def init_test_box(engine):
    session.add_all([Box(pid=1,tid=1),Box(pid=1,tid=2),Box(pid=1,tid=3),Box(pid=1,tid=4),
    Box(pid=2,tid=2),Box(pid=2,tid=5),Box(pid=2,tid=6),Box(pid=2,tid=66),Box(pid=2,tid=77),
    Box(pid=3,tid=3)])
    session.commit() 
def init_user_takeaway(engine):
    session.add_all(
        [Takeaway(pid=1,twname='rope',tf1name='diya',tf2name='diamond',twlevel=5,tf1level=5,tf2level=10),
        Takeaway(pid=2,twname='rope',tf1name='diya',tf2name='diamond',twlevel=5,tf1level=5,tf2level=10),
        Takeaway(pid=3,twname='rope',tf1name='diya',tf2name='diamond',twlevel=5,tf1level=5,tf2level=10)
        ]
    )
    session.commit() 




def drop_db(engine):
    base.metadata.drop_all(engine)

def init_db(engine):
    #放置重复建立报错，先dropdb再createdb 
    base.metadata.create_all(engine)
    init_treasure(engine)
    init_testplayer(engine)#
    init_test_box(engine)
    init_user_takeaway(engine)
if __name__ == '__main__':
    init_db(engine)
