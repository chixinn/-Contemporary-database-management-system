import random
from flask import Flask, Blueprint, jsonify,make_response

from action.init_db import base

from flask import Flask, request, flash, url_for, redirect, render_template
from flask import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, create_engine, MetaData, Table, func, select
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, and_



engine = create_engine('postgresql+psycopg2://chixinning:123456@localhost/hunt',encoding='utf-8',echo=True)
conn = engine.connect()
meta = MetaData(engine)
MAXSTROAGE=20
DBSession = sessionmaker(bind=engine)
 
session = DBSession()

players = Table("players", meta, autoload=True)
treasures = Table("treasures", meta, autoload=True)
takeaway = Table("takeaway", meta, autoload=True)
markets = Table("markets", meta, autoload=True)
box = Table("box", meta, autoload=True)


# 不使用前缀url，进入打印欢迎词
#定义路由与蓝图
bp = Blueprint("operation", __name__)
@bp.route("/", methods=['GET'])
def hello():
    return "<h1>Welcome to the game</h1>"

# 直接复制上次文档数据库的代码部分，因为操作都是一样的。
@bp.route("/<string:username>/<string:operation>/<string:treasure>/<int:price>", methods=['GET'])
@bp.route("/<string:username>/<string:operation>/<string:treasure>/<string:seller>", methods=['GET'])
@bp.route("/<string:username>/<string:operation>/<string:treasure>/", methods=['GET'])
@bp.route("/<string:username>/<string:operation>", methods=['GET'])
@bp.route("/<string:username>/<string:operation>/<string:passwd>", methods=['GET'])

def inputs(username, operation, treasure='test_treasure', price=0,seller='testseller',passwd='testpasswd'):
    if operation == 'login':#玩家登陆,done
        return login(username,passwd)
    elif operation == 'market':#玩家查看市场,done
        return look_market(username)
    elif operation == 'wear':#玩家佩戴，注意佩戴的物品不在存储箱中，即存储箱是仓库的概念，done
        return wear(username, treasure)
    elif operation == 'buy':#玩家购买,done
        return buy(username, treasure,seller)
    elif operation == 'withdraw':#玩家不卖了,done 注意可卖的东西宝物是在箱子里不在身上
        return withdraw(username,treasure)                           
    elif operation == 'sell':#挂牌出售，功能支持玩家改价，卖的东西一定不能在身上，否则对于mongoDB来说会显示两条玩家信息,sql可以支持直接改价吗？可以
        return sell(username, treasure, price)
    elif operation == 'unwear':#满足符合先从身上脱下来以后才能穿的逻辑,done
        return unwear(username,treasure)
    elif operation =='box':#查看存储箱中有什么,done
        return look_box(username)
    elif operation =='homepage':#玩家登陆主页，玩家自行查看玩家个人信息,done
        return homepage(username)
    elif operation =='mysale':#查看我的出售
        return look_mysale(username)#玩家查看自己在卖什么
    elif operation == 'register':
        return user_register(username,passwd)#玩家注册逻辑补充
    elif operation == 'forgetPasswd':
        return forget_passwd(username)#忘记密码了嘛
    elif operation == 'takeaway':#但看我的出售
        return look_mytakeaway(username)
    # elif operation =='debug':#我编程测试用的
        # return debug_test(username)
    else:
        return "<h1>输入错误</h1><h2>支持输入的格式如下</h2><p>四个参数：\
        /<string:username>/<string:operation>/<string:treasure>/<int:price></p><p>\
        三个参数：/<string:username>/<string:operation>/<string:treasure></p><p>\
        两个参数：/<string:username>/<string:operation></p>\
        <h2>支持的Operation有：</h2>\
        <ul>\
        <li>售卖：sell/不卖：withdraw/改价：sell重新输入价格</li>\
        <li>查看市场:market/查看用户自己的主页：index/查看自己存储箱里有啥：box</li>\
        <li>穿wear/脱unwear/\
        </ul>"
#用户主页

# 要全部增加边界防bug
#用户注册
def user_register(username,passwd):

    try:
        conn.execute(players.insert().values(pname=username,passwd=passwd, money=1000, fortune=10, working=10))
        player=conn.execute(select([players]).where(players.c.pname == username)).fetchone()
        # 相应的takeaway也要insert()
        conn.execute(takeaway.insert().values(pid=player['pid'],tname='rope',tlevel=5,ttype='working',tid=83))
        conn.execute(takeaway.insert().values(pid=player['pid'],tname='diya',tlevel=5,ttype='fortune',tid=82))
        conn.execute(takeaway.insert().values(pid=player['pid'],tname='diamond',tlevel=5,ttype='fortune',tid=81))


        return make_response(jsonify({"state": "Success", "name": username, "money": 1000, "fortune": 10, "workability": 10}))
    except Exception:
        return '404 ： 都注册过了还整啥啊,'
    # return render_template('index.html',users=username)
    return jsonify({"state": "Success", "name": username, "money": 1000, "fortune": 10, "workability": 10})



# 进入游戏
def login(username,passwd):
    if conn.execute(select([players]).where(players.c.pname == username)).fetchone()==None:
        return '404: No Such User Error'
    userRealpasswd = conn.execute(select([players]).where(players.c.pname == username)).fetchone()[2]
    if passwd!=userRealpasswd:
        return '<h1>密码错了 爬！</h1>'+str(userRealpasswd)
    return make_response(jsonify({"state": "Login Success", "name": username, "money": 1000,"passwd":passwd, "fortune": 10, "workability": 10}))
    # return '4-4'
# 忘记密码

def forget_passwd(username):
    player=conn.execute(select([players]).where(players.c.pname == username)).fetchone()
    if player==None:
        return '404: No Such User Error'
    # return '4-4'
    return make_response(jsonify({"state": "Forget Query Success", "name": username, "money": player['money'],"passwd":player['passwd'], "fortune": player['fortune'], "workability": player['working']}))

# 查看用户主页

def homepage(username):
    
    player=conn.execute(select([players]).where(players.c.pname == username)).fetchone()
    if player==None:
        return '404: No Such User Error'
    # return '4-4'
    return make_response(jsonify({"state": "No Front End ANY MORE", "name": username, "money": player['money'],"passwd":player['passwd'], "fortune": player['fortune'], "workability": player['working']}))

    #return render_template('index.html',users=users)

#浏览储物箱
# #浏览存储箱
def look_box(username):
    player=conn.execute(select([players]).where(players.c.pname == username)).fetchone()
    if player==None:
        return '404: No Such User Error'
    player_pid=player['pid']
    # return jsonify({"user_id":player_pid})
    user_box = conn.execute(select([box]).where(box.c.pid == player_pid)).fetchall()
    tid_list=[]
    for i in user_box:
        tid_list.append(i[2])
    treasure_list=[]
    for i in tid_list:
        user_treasure=conn.execute(select([treasures]).where(treasures.c.tid==i)).fetchall()
        treasure_list.append(user_treasure)
    # return '4-4'
    return make_response(jsonify({"user_box":str(user_box),"State":"Look Box Query Success","name": username,"Treasure_list":str(treasure_list)}))
   
# 浏览我当前穿了什么
def look_mytakeaway(username):
    player=conn.execute(select([players]).where(players.c.pname == username)).fetchone()
    if player==None:
        return '404: No Such User Error'
    player_pid=player['pid']
    # return jsonify({"user_id":player_pid})
    user_takeaway = conn.execute(select([takeaway]).where(takeaway.c.pid == player_pid)).fetchall()
    treasure_li=[]
    for i in user_takeaway:
        treasure_li.append([i[2],i[4],i[5]])
    # return '4-4'
    return make_response(jsonify({"user_takeaway":str(treasure_li),"State":"QuerySuccess","name": username}))

# 浏览我在卖些个傻子
def look_mysale(username):
    player=conn.execute(select([players]).where(players.c.pname == username)).fetchone()
    if player==None:
        return '404: No Such User Error'
    mysale=conn.execute(select([markets]).where(markets.c.sid==player['pid'])).fetchall()
    mysale_list=[]
    for i in mysale:
        mysale_list.append(i[-2:-1])
    # return '4-4'
    return make_response(jsonify({"user_sell":str(mysale),"State":"QuerySuccess","name": username}))

def debug_test(username):
    #有唯一项的都要fetchone 而不是fetch_all
    player=conn.execute(select([players]).where(players.c.pname == username)).fetchone()
    if player==None:
        return '404: No Such User Error'
    # player=conn.execute(select([players]).where(players.c.pname == username)).fetchall()
    player_pid=player['pid']
    # trea_level = session.query(treasures).filter(treasures.c.tid == 1).all()# 这个可以把treasures.c改成功了
    # res=session.query(box).filter(and_(box.c.tid == 1)).all()# 成功了
    # session.query(box).filter(box.c.tid==1).delete()#外key的原因?
    # session.commit()
    # 用bid来删除，因为符合条件的不止一个，但bid是唯一的
    # drop_bid = conn.execute(select([box]).where(box.c.tid == 1 and box.c.pid == 1)).fetchone()[0]
    # conn.execute(box.delete().where(box.c.bid == drop_bid))#终于多重条件删掉了5555
    # res=session.query(box).filter(and_(box.c.tid == 1)).count()
    recovery_treasure(player_pid)
    # session.query(box).filter(and_(box.c.pid == 1,box.c.tid == 1)).delete()
    return '4-4'
    return 'jjj'
    

#跟TakeawayTable有关的SQL
# 佩戴宝物
#佩戴宝物(待测试)
# unwear的逻辑和wear差不多。
# !!!注意我这里wear/sqy/adfa/一定要加后面这个反斜线
def wear(username, treasure):
    player=conn.execute(select([players]).where(players.c.pname == username)).fetchone()
    if player==None:
        return '404: No Such User Error'
    treasure_towear=conn.execute(select([treasures]).where(treasures.c.tname == treasure)).fetchone()
    if treasure_towear == None:
        return make_response(jsonify({"State":"Treasure found in treasures Error"}))
    pid=player["pid"]  
    
    player_box=conn.execute(select([box]).where(box.c.pid == pid)).fetchall()
    #获取该玩家的随身携带 
    current_takeaway=conn.execute(select([takeaway]).where(takeaway.c.pid == pid)).fetchall()
    #再获取要佩戴的宝物类型和id
    treasure_towear_type=treasure_towear["type"]
    treasure_towear_id=treasure_towear["tid"]
    # return str(treasure_towear_id.dtype())
    # return str(treasure_towear_id)
    treasure_towear_level=treasure_towear["level"]
    itemlist=conn.execute(select([markets]).where(markets.c.sid == pid and markets.c.tid == treasure_towear_id)).fetchall()#获得我的出售列表：
    for item in itemlist:
        if (item["tid"]==treasure_towear_id):
            return make_response(jsonify({"State":"UnSale Before Wearing"}))
    # 最后要从存储箱中找到对应的宝物，还要再预先检查箱子里有没有这玩意 
    player_box_list=[]
    for i in player_box:
        player_box_list.append(i[2])
    if treasure_towear_id not in player_box_list:
        return make_response(jsonify({"State":"Not in the Box"}))
    count=0
    for i in current_takeaway:
        if(i[5]=='working' and treasure_towear_type == 'working' ):
            return make_response(jsonify({"State":"Unwear Working Before Wearing"}))
        if(i[5]=='fortune'and treasure_towear_type == 'fortune'):
            count=count+1
    if(count==2):#这里即可灵活的调整fortune的大小，添加working也是如此
        return make_response(jsonify({"State":"Unwear Fortune Before Wearing"}))
   #incaseNone
    current_fortune_level=player['fortune']#直接通过player也可以索引到这个
    if treasure_towear_type=="working":#不同情况的更新
        # return jsonify({"State":"aaaaaa"})
        #盒子和佩戴不能共存:但盒子会因为寻宝寻到同名宝物啊
        # 用bid来删除，因为符合条件的不止一个，但bid是唯一的
        # drop_bid = conn.execute(select([box]).where(box.c.tid == treasure_towear_id and box.c.pid == pid)).fetchone()[0]
        drop_bid=session.query(box).filter(and_(box.c.tid == treasure_towear_id,box.c.pid == pid)).one()[0]
        conn.execute(box.delete().where(box.c.bid == drop_bid))#终于多重条件删掉了5555
        conn.execute(players.update().where(players.c.pid == pid).values(working=treasure_towear_level))
        conn.execute(takeaway.insert().values(pid=pid,tname=treasure,tid=treasure_towear_id,tlevel=treasure_towear_level,ttype='working'))
        player=conn.execute(select([players]).where(players.c.pname == username)).fetchone()
        # return '4-4'
        return make_response(jsonify({"State":"Wear Success!","name": username, "money": player['money'],"passwd":player['passwd'], "fortune": player['fortune'], "workability": player['working']}))
    if treasure_towear_type=='fortune':
        new_fortune_level=treasure_towear_level+current_fortune_level
        drop_bid=session.query(box).filter(and_(box.c.tid == treasure_towear_id,box.c.pid == pid)).one()[0]

        # drop_bid = conn.execute(select([box]).where(box.c.tid == treasure_towear_id and box.c.pid == pid)).fetchone()[0]
        conn.execute(box.delete().where(box.c.bid == drop_bid))#终于多重条件删掉了5555
        conn.execute(players.update().where(players.c.pid == pid).values(fortune=new_fortune_level))
        conn.execute(takeaway.insert().values(pid=pid,tname=treasure,tid=treasure_towear_id,tlevel=treasure_towear_level,ttype='fortune'))

        # conn.execute(takeaway.insert().values(pid==pid,tname=treasure,tid=treasure_towear_id,tlevel=treasure_towear_level,ttype='fortune'))
        player=conn.execute(select([players]).where(players.c.pname == username)).fetchone()
        # return '4-4'
        return make_response(jsonify({"State":"Wear Success!","name": username, "money": player['money'],"passwd":player['passwd'], "fortune": player['fortune'], "workability": player['working']}))
    
#脱下
def unwear(username,treasure):
    # 首先判断宝物库没有该宝物
    player=conn.execute(select([players]).where(players.c.pname == username)).fetchone()
    if player==None:
        return '404: No Such User Error'
    treasure_tounwear=conn.execute(select([treasures]).where(treasures.c.tname == treasure)).fetchone()
    if treasure_tounwear == None:
        return make_response(jsonify({"State":"Treasure found in treasures Error"}))
    # return str(treasure_tounwear)
    #获取要佩戴宝物的玩家
    pid=player["pid"]   
    # return str(pid) 
    #获取该玩家的随身携带 
    current_takeaway=conn.execute(select([takeaway]).where(takeaway.c.pid == pid)).fetchall()
    #再获取要脱下的宝物类型和id
    treasure_tounwear_type=treasure_tounwear["type"]
    treasure_tounwear_id=treasure_tounwear["tid"]
    treasure_tounwear_level=treasure_tounwear["level"]
    #遍历current_takeaway 判断是不是真的在戴：
    current_list=[]
    for i in current_takeaway:
        current_list.append(i[2])
    # return str(current_list)
    if treasure not in current_list:
         return make_response(jsonify({"State":"Treasure found in takeawway Error"}))
    # 然后就可以脱了 脱了要更新回box,
    # 且current takeaway,
    # 然后相应的人物属性也要更新:
    # 脱了就是删了Orz:D
    if treasure_tounwear_type=='working':
        # 为了防止有重复的 还是要设置删除功能 这里要继续debug
        # conn.execute(takeaway.delete().where(takeaway.c.pid==pid and takeaway.c.tname==treasure))
        #注意这个bug！！！
        drop_aid=session.query(takeaway).filter(and_(takeaway.c.tid == treasure_tounwear_id,takeaway.c.pid == pid)).one()[0]
        # drop_aid = conn.execute(select([takeaway]).where(takeaway.c.tid == treasure_tounwear_id and takeaway.c.pid == pid)).fetchone()[0]
        # return str(drop_aid)+'************'+str(pid)+'*********'+str(treasure_tounwear_id )
        conn.execute(takeaway.delete().where(takeaway.c.aid == drop_aid))#终于多重条件删掉了5555
        #box UPdate前要检查size
        size=session.query(box).filter(and_(box.c.pid == pid)).count()
        if size > MAXSTROAGE:
            recovery_treasure(pid)
        conn.execute(box.insert().values(pid=pid,tid=treasure_tounwear_id))#与bid无瓜
        conn.execute(players.update().where(players.c.pid==pid).values(working=10))#不能为0
        player=conn.execute(select([players]).where(players.c.pname == username)).fetchone()
        current_takeaway=conn.execute(select([takeaway]).where(takeaway.c.pid == pid)).fetchone()
        # return '4-4'
        return make_response(jsonify({"State":"UnWear Success!","name": username,"fortune": player['fortune'], "workability": player['working'],"takeaway":str(current_takeaway)}))

    if (treasure_tounwear_type=='fortune'):
        # conn.execute(takeaway.delete().where(takeaway.c.pid==pid and takeaway.c.tname==treasure))
        drop_aid=session.query(takeaway).filter(and_(takeaway.c.tid == treasure_tounwear_id,takeaway.c.pid == pid)).one()[0]

        # drop_aid = conn.execute(select([takeaway]).where(takeaway.c.tid == treasure_tounwear_id and takeaway.c.pid == pid)).fetchone()[0]
        conn.execute(takeaway.delete().where(takeaway.c.aid == drop_aid))#终于多重条件删掉了5555
        size=session.query(box).filter(and_(box.c.pid == pid)).count()
        if size > MAXSTROAGE:
            recovery_treasure(pid)
        conn.execute(box.insert().values(pid=pid,tid=treasure_tounwear_id))#与bid无瓜
        current_fortune_level=player['fortune']
        conn.execute(players.update().where(players.c.pid==pid).values(fortune=current_fortune_level-treasure_tounwear_level))
        player=conn.execute(select([players]).where(players.c.pname == username)).fetchone()
        current_takeaway=conn.execute(select([takeaway]).where(takeaway.c.pid == pid)).fetchone()
        # return '4-4'
        return make_response(jsonify({"State":"UnWear Success!","name": username,"fortune": player['fortune'], "workability": player['working'],"takeaway":str(current_takeaway)}))
        

# 查看市场

def look_market(username):
    market=conn.execute(select([markets])).fetchall()
    sell_info_list=[]
    for i in market:
        treasure_on_sell_seller='seller_id: '+str(i[0])
        treasure_on_sell_name='item_id: '+str(i[1])
        treasure_on_sell_price='price:'+str(i[2])
        sell_info_list.append([treasure_on_sell_name,treasure_on_sell_seller,treasure_on_sell_price])
    return make_response(jsonify({"State":"Success!","sell_list":str(sell_info_list)}))

    


def sell(username, treasure, price=0):
    if price==0:
        return "<h1>你没输入价格</h1> 爬"
    player=conn.execute(select([players]).where(players.c.pname == username)).fetchone()
    if player==None:
        return make_response(jsonify({"State":"Player Not found ERR"}))
    pid=player['pid']
    treasure_to_sell=conn.execute(select([treasures]).where(treasures.c.tname == treasure)).fetchone()
    if treasure_to_sell==None:
        return make_response(jsonify({"State":"Trea Not found in treasures ERR"}))
    treasure_to_sell_id=treasure_to_sell['tid']
    # conn.execute(markets.insert().values(sid=pid, tid=treasure_to_sell_id, price=price))
    res=session.query(markets).filter(and_(markets.c.sid == pid , markets.c.tid==treasure_to_sell_id)).all()
    #卖的东西只能是在玩家箱子里的东西:
    res2=session.query(box).filter(and_(box.c.pid==pid,box.c.tid==treasure_to_sell_id)).one()

    if res2==[]:
        # return '4-4'
        return jsonify({"State":"Trea Not found in Box ERR"})

    if res==[]:#注意这里不是None!!!!!啊啊啊啊啊啊啊
        conn.execute(markets.insert().values(sid=pid, tid=treasure_to_sell_id, price=price))
        # return '4-4'
        return jsonify({"State":"On Sale Success"})
    else:
        conn.execute(markets.update().where(markets.c.sid == pid and markets.c.tid==treasure_to_sell_id ).values(price=price))
        # return '4-4'
        return jsonify({"State":"Update Price Success"})
        
  
    

# 回收
def withdraw(username, treasure):
    # session = sessionmaker(engine)()
    player=conn.execute(select([players]).where(players.c.pname == username)).fetchone()
    if player==None:
        return make_response(jsonify({"State":"Player Not found ERR"}))
    pid=player['pid']
    #在库里
    treasure_to_sell=conn.execute(select([treasures]).where(treasures.c.tname == treasure)).fetchone()
    if treasure_to_sell==None:
        return make_response(jsonify({"State":"Trea Not found ERR"}))
    treasure_to_sell_id=treasure_to_sell['tid']
    #在市场上
    drop_mid=session.query(markets).filter(and_(markets.c.tid == treasure_to_sell_id,markets.c.sid == pid)).one()[0]
    # drop_mid = conn.execute(select([markets]).where(markets.c.tid == treasure_to_sell_id and markets.c.sid == pid)).fetchone()[0]
    if drop_mid==None:
        return '<h1>没这个东西</h1>爬'
    conn.execute(markets.delete().where(markets.c.mid == drop_mid))#终于多重条件删掉了5555
    # 市场上回收没有放回箱子这一步
   
    # res=conn.execute(markets.delete().where(markets.c.seller==pid and markets.c.tid==treasure_to_sell_id))
    return make_response(jsonify({"State":"WithDraw Item Success"}))
        


# 购买
def buy(username, treasure,seller):
    #边界检查
    buyer=conn.execute(select([players]).where(players.c.pname == username)).fetchone()
    seller=conn.execute(select([players]).where(players.c.pname == seller)).fetchone()
    if buyer==None:
        return jsonify({"State":"Buyer Not found ERR"})
    seller_id=seller['pid']
    if seller==None:
        return jsonify({"State":"Seller Not found ERR"})
    buyer_id=buyer['pid']
    treasure_to_buy=conn.execute(select([treasures]).where(treasures.c.tname == treasure)).fetchone()
    if treasure_to_buy==None:
        return jsonify({"State":"Trea Not found ERR"})
    treasure_to_buy_tid=treasure_to_buy['tid']
    #市场检查
    # treasure_to_buy=conn.execute(select([markets]).where(markets.c.tid == treasure_to_buy_tid and markets.c.sid==seller_id )).fetchone()
    # drop_mid=session.query(markets).filter(and_(markets.c.tid == treasure_to_sell_id,markets.c.sid == pid)).one()[0]

    treasure_to_buy=session.query(markets).filter(and_(markets.c.tid == treasure_to_buy_tid ,markets.c.sid==seller_id)).one()
    drop_mid=treasure_to_buy[0]
    if treasure_to_buy ==None:
        return jsonify({"State":"Trea Not in market found ERR"})
    seller_box_id=conn.execute(select([box]).where(box.c.pid == seller_id and box.c.tid==treasure_to_buy_tid)).fetchone()[0]
    treasure_to_buy_price=treasure_to_buy[3]
    seller_money=seller['money']+treasure_to_buy_price
    buyer_money=buyer['money']-treasure_to_buy_price
    # buyer_box=conn.execute(select([box]).where(box.c.pid == buyer_id )).fetchall()
    if buyer_money<0:
        return '<h1>你买不起</h1>爬'
    # buyer箱子检查
    try:
        session.query(box).filter(and_(box.c.pid==buyer_id,box.c.tid==treasure_to_buy_tid)).one()
        session.query(takeaway).filter(and_(takeaway.c.pid==buyer_id,takeaway.c.tid==treasure_to_buy_tid))
        # return str(res)
        return jsonify({"State":"Transaction Failure! due to Already Have One"})
    except:
    #删seller箱子
        conn.execute(box.delete().where(box.c.bid == seller_box_id))
    #增buyer箱子(recovery_treasure)
    #更新双方的账户
        size=session.query(box).filter(and_(box.c.pid == buyer_id)).count()
        if size > MAXSTROAGE:
            recovery_treasure(buyer_id)
        try:
        # conn.execute(box.insert().values(pid=pid,tid=treasure_tounwear_id))#与bid无瓜

            conn.execute(box.insert().values(pid=buyer_id,tid=treasure_to_buy[2]))
            conn.execute(players.update().where(players.c.pid==buyer_id).values(money=buyer_money))
            conn.execute(players.update().where(players.c.pid==seller_id).values(money=seller_money))
        # 该市场记录还需要删除
            conn.execute(markets.delete().where(markets.c.mid== drop_mid))
        
            return jsonify({"State":"Transaction Success!"})
        except:
            return jsonify({"State":"Transaction Failure!"})
    





#工具人function
# 宝箱充满系统回收最low宝物
def recovery_treasure(pid):
   # 成功了
    user_box = conn.execute(select([box]).where(box.c.pid == pid)).fetchall()
    print(" current storage size,"+str(len(user_box)))
    drop_treasure_level=99999#因为没有mongoDB的嵌套所以只能手动初始化了
    drop_tid=0#不是循环里的局部变量是要先初始化的
    for trea in user_box:
        tmp_level = conn.execute(select([treasures]).where(treasures.c.tid == trea[2])).fetchone()[3]
        if tmp_level < drop_treasure_level:
            drop_treasure_level = tmp_level
            drop_tid = trea[2]#注意sqlalchmey和mongoDB的不同
    # 删除该宝物
    # 用bid来删除，因为符合条件的不止一个，但bid是唯一的
    drop_bid = conn.execute(select([box]).where(box.c.tid == drop_tid and box.c.pid == pid)).fetchone()[0]
    conn.execute(box.delete().where(box.c.bid == drop_bid))
    # box_new=conn.execute(select([box]).where(box.c.pid == pid)).fetchall()

    print("系统回收成功")
    return 0


