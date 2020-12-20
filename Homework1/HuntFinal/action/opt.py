import sys
import pymongo
from time import time
from flask import Flask, jsonify, request, abort,url_for,render_template,redirect
from flask import Blueprint
from pymongo import MongoClient





client = MongoClient('localhost', 27017)
players = client.game.players
markets = client.game.markets
treasures = client.game.treasures
history=client.game.history

# 不使用前缀url，进入打印欢迎词
#定义路由与蓝图
bp = Blueprint("operation", __name__)
@bp.route("/", methods=['GET'])
def hello():
    return "<h1>Welcome to the game</h1>"

# 
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
    elif operation == 'withdraw':#玩家不卖了,done
        return withdraw(username,treasure)                           
    elif operation == 'sell':#挂牌出售，功能支持玩家改价，否则对于mongoDB来说会显示两条玩家信息
        return sell(username, treasure, price)
    elif operation == 'unwear':#满足符合先从身上脱下来以后才能穿的逻辑,done
        return unwear(username,treasure)
    elif operation =='box':#查看存储箱中有什么,done
        return look_box(username)
    elif operation =='homepage':#玩家登陆主页，玩家自行查看玩家个人信息,done
        return homepage(username)
    elif operation == 'history':#模拟日志记录回滚历史
        return look_history(username)
    elif operation =='mysale':
        return look_mysale(username)#玩家查看自己在卖什么
    elif operation == 'register':
        return user_register(username,passwd)#玩家注册逻辑补充
    elif operation == 'forgetPasswd':
        return forget_passwd(username)#忘记密码了嘛
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

#
def forget_passwd(username):
    player=players.find_one({"name":username})
    return "<h1>你的密码是"+player["passwd"]+"</h1>"


def user_register(username,passwd):
    if (players.find_one({"name":username})!=None):
        return "哎呀你已经注册过了嘛！输入用户名和密码就可以登陆啦！"
    players.create_index([("name", pymongo.ASCENDING)], unique=True)    # 给players建立unique索引，避免用户昵称重复
    players.insert_one({"name": username, "money": 1000,
                            "takeaway": [{"name":"rope","level":10,"type":"working"},{"name":"dice","level":9,"type":"fortune"},
                            {"name":"diya","level":9,"type":"fortune"}],
                            "box": [],"passwd":passwd}).inserted_id#初始化玩家信息库，注意因为takeaway中的东西不能出现在box中，所以初始化box为空
    users=players.find({"name":username})
    history.insert({"name":username,"time":time(),"opt_type":"register","detail":username+" regiter "})
    #return render_template('index.html',users=users)
    return '4-4'





def homepage(username):
    if(players.find({"name":username})==None):
        return " <h1>你又输错名字了</h1>"
    users=players.find({"name":username})
    return '404'
    #return render_template('index.html',users=users)
#玩家查看自己的交易记录，此操作较少
def look_history(username):
    historyList=history.find({"name":username})
    return '404'
    #return render_template('historyindex.html',history=historyList)

# 玩家查看自己当前在卖啥：

def look_mysale(username):
    player=players.find_one(username)
    itemlist=markets.find({"owner":username})
    return '404'
    #return render_template('market_index.html',markets=itemlist,user=player,info='欢迎查看我的售卖～')




# 进入游戏
def login(username,passwd):
    if(passwd=='testpasswd'):
        return "<h1>哎呀 你忘记输入密码啦</h1>"

    user=players.find({"$and":[{"name":username},{"passwd":passwd}]})
    if user==None:
        if(players.find_one({"name":username})):
            history.insert({"name":username,"time":time(),"opt_type":"login","detail":username+" try to login  failed because of passwd"})
            return "<h1>该用户名已经注册～,快康康你是不是密码输入错了</h1>"
        else:
            history.insert({"name":username,"time":time(),"opt_type":"login","detail":username+" try to login  failed because of no prehead registeration"})
            return "<h1>你还没注册！快去注册！</h1>"
    else:
        history.insert({"name":username,"time":time(),"opt_type":"login","detail":username+" login "})
        #return render_template('index.html',users=user)
        return '404'

   
   
    
    
#浏览存储箱
def look_box(username):
    if players.find_one({"name": username}) == None:
        return "<h1>请先注册用户</h1>"
    player=players.find_one({"name": username},{"_id":0})
    box=player['box']
    #return render_template('box_index.html',box=box,username=username)
    return '404'

#浏览市场
#这里可用前端进行渲染
def look_market(username):
    # 用户名不存在
    if players.find_one({"name": username}) == None:
        return "<h1>请先注册用户</h1>"
    # 将markets中的宝物通过字符串展现出来,这也可以写成前端用render_templates展示
    market=markets.find({})
    user=players.find_one({"name": username})
    #return render_template('market_index.html',markets=market,user=user,info='')
    return '404'
#将宝物从身上拿下，放入存储箱中


def unwear(username,treasure):
    #首先判断输入的宝物名称是否合法
    #return username+treasure
    if treasures.find_one({"name": treasure}) == None:
        return "<h1>宝物库中没有 %s 宝物</h1><p>请返回重新输入</p>"  % treasure + "<br><br>"
    player=players.find_one({"name": username})#获取当前玩家,注意不要搞混！这样会报错的:D:D
    current_takeaway=player['takeaway']
    #首先获取要脱下的的宝物
    treasure_tounwear=treasures.find_one({"name": treasure},{"_id":0})#用来后面替换时直接用,宝物库的姓名索引是唯一的
    #treasure_tounwear=treasure_tounwear
    print(treasure_tounwear)
    box=player['box']
    #遍历玩家takeaway 看是否在其中：
    for tre in current_takeaway:
        if(treasure_tounwear["name"]==tre["name"]):
            #return str(current_takeaway)#test
            current_takeaway.remove(treasure_tounwear)
            box.append(treasure_tounwear)
            if(len(player["box"])>10):
                recovery_treasure(username)
            box=player['box']#这个也要改 别忘了
            #更新玩家信息
            players.update_one({"name": username}, {"$set": {"box": box}})
            players.update_one({"name": username}, {"$set": {"takeaway": current_takeaway}})
            history.insert_one({"name":username,"opt_time":time(),"opt_type":"unwear","detail":"unwear"+treasure})#记录一下这个历史~
            return "<h1>从身上脱下成功%s 宝物</p>"  % treasure + "<br><br>" 
        
    return "<h1>玩家takeaway中没有 %s 宝物</h1><p>请返回重新输入</p>"  % treasure + "<br><br>" 


#佩戴宝物
def wear(username, treasure):
    # 宝物库没有该宝物
    #首先判断输入的宝物名称是否合法
    if treasures.find_one({"name": treasure}) == None:
        return "<h1>宝物库中没有 %s 宝物</h1><p>请返回重新输入</p>"  % treasure + "<br><br>" 
    player=players.find_one({"name": username})#获取当前玩家
    
    box=player["box"]#获取玩家的box
    current_takeaway=player["takeaway"]
    print(current_takeaway)
    #首先获取要佩戴的宝物
    treasure_towear=treasures.find_one({"name": treasure})
    treasure_towear_type=treasure_towear["type"]
    if len(current_takeaway)>3:
        return "<h1>不要太贪心，要先脱下来才能再穿的！</h1>"
    #先看该玩家身上还能不能佩戴
    count_fortune=0
    for item in current_takeaway:
        if(item["type"]=="working" and treasure_towear_type=="working" ):
            return "<h1>不要太贪心，要先脱下来working才能再穿的！</h1>"
        if(item["type"]=="fortune" and treasure_towear_type=="fortune" ):
            count_fortune=count_fortune+1
    if count_fortune==2:
        return "<h2>不要太贪心，要先脱下幸运宝物来才能再穿的！</h2>"
    # 如果是你出售的，就不能穿了哦！
    itemlist=markets.find({"owner":username})#获得我的出售列表：
    for item in itemlist:
        if (item["name"]==treasure):
            return "<h2>如果是你出售的，就不能穿了哦！</h2>"
    # 从存储箱中找到对应的宝物，flag标记宝箱中有没有该宝物
    flag = 0
    for item in box:
        if item["name"] == treasure_towear["name"]:
            box.remove(item)#从存储箱移出
            current_takeaway.append(item)#放入takeaway之中
            # 更新宝箱和佩戴的宝物
            players.update_one({"name": username}, {"$set": {"box": box}})
            players.update_one({"name": username}, {"$set": {"takeaway": current_takeaway}})
            flag = 1
            history.insert_one({"name":username,"opt_time":time(),"opt_type":"wear","detail":"wear"+treasure})#记录一下这个历史~

            return "<h1>佩戴 %s 宝物成功</h1>" % treasure + "<br><br>" 
    if flag == 0:
        return "<h1>存储箱没有 %s 宝物</h1><p>请确认后重新输入</p>" % treasure + "<br><br>"


# 购买宝物
def buy(username, treasure,seller):
    # 市场没有该宝物
    if markets.find_one({"name": treasure},{"owner":seller}) == None:
        return "<h1>市场暂无 %s 宝物</h1>" % treasure + "<br><br>"
    #获取宝物信息：
    treasure_to_buy=markets.find_one({"$and":[{"name": treasure},{"owner":seller}]})
    # 买家到位
    player = players.find_one({"name": username})
    if player ==None:
        return '用户名又输入错误了亲'
    # 买家宝物到位，充满则进行回收
    box1 = player['box']
    if len(box1) >= 10:
        recovery_treasure(username)
    
    box = player['box']     # 回收宝物后需要重新索引宝箱数据，这个很关键，我一开始没想到
    box.append({"name":treasure,"level":treasure_to_buy["level"],"type":treasure_to_buy["type"]})
    players.update_one({"name": username}, {"$set": {"box": box}})
    # 这个逻辑不对，购买怎么可能是系统决定呢
    treasure_money = treasure_to_buy["price"]
    # 找到最便宜的宝物
    money1 = player['money'] - treasure_money
    if money1 < 0:
        return "<h1>买不起</h1>"
    players.update_one({"name": username}, {"$set": {"money": money1}})
    # 卖家钱到位
    money2 = players.find_one({"name": seller})['money'] + treasure_money
    players.update_one({"name": seller}, {"$set": {"money": money2}})
    # 市场删除该宝物
    markets.delete_one({"$and":[{"name": treasure},{"owner":seller}]})
    history.insert_one({"name":username,"opt_time":time(),"opt_type":"buy","detail":"buy "+treasure+" money: "+str(treasure_money)})#记录一下这个历史~
    return "<h1>玩家 %-6s 支付宝到账 %d</h1>" % (seller, treasure_money)+"<br><br>"

# 收回挂牌宝物
def withdraw(username, treasure):
    # 市场没有该宝物
    treasure_to_withdraw=markets.find_one({"$and":[{"name": treasure},{"owner":username}]})#防止在市场上回收了别人的宝物
    if treasure_to_withdraw == None:
        return "<h1>市场暂无 %s 宝物</h1><p>请重新检查输入</p>" % treasure + "<br><br>"
    # 市场删除宝物
    markets.delete_one({"$and":[{"name": treasure},{"owner":username}]})#防止在市场上回收了别人的宝物
    # 玩家收回宝物，同理充满则进行系统回收
    box = players.find_one({"name": username})['box']
    if len(box) >= 20:
        recovery_treasure(username)#回收
    box = players.find_one({"name": username})['box'] #回收后重新更新box
    #treasure_to_append=treasures.find_one({"name":treasure})#不用再访问而是直接查询
    treasure_to_append_type=treasure_to_withdraw["type"]
    treasure_to_append_level=treasure_to_withdraw["level"]

    box.append({"name":treasure,"level":treasure_to_append_level,"type":treasure_to_append_type})
    players.update_one({"name": username}, {"$set": {"box": box}})
    history.insert_one({"name":username,"opt_time":time(),"opt_type":"withdraw","detail":"withdraw "+treasure})#记录一下这个历史~

    return "<h1>收回宝物 %s 成功</h1>" % treasure + "<br><br>" 


# 出卖宝物
#挂牌出售，功能支持玩家改价，否则对于mongoDB来说会显示两条玩家信息
def sell(username, treasure, price=0):
    player = players.find_one({"name": username})
    treasure_to_sell=treasures.find_one({"name":treasure})
    if(price==0):
        return "<h1>啊哦你忘输入价格了啦</h1>"
    if(markets.find_one({"name":treasure},{"owner":username})):
        markets.update_one({"$and":[{"name":treasure},{"owner":username}]},{"$set":{"price":price}})
        history.insert_one({"name":username,"opt_time":time(),"opt_type":"resell","detail":"set the price of "+treasure+"to "+"money: "+str(price)})#记录一下这个历史~
        return "<h1>你还在卖着哦，改价成功！</h1>"
    # 卖家宝物到位
    if player ==None:
        return '用户名又输入错误了亲'
    box = player['box']
    flag=0#判断是否在盒子里
    for trea in box:
        if trea["name"] == treasure_to_sell["name"]:
            box.remove(trea)
            flag=1
            break
    if flag==0:
        return "<h1>咋搞的啊，又输入错宝物名字了,宝物不在存储库中是不能售卖的哦</h1>"
    
    players.update_one({"name": username}, {"$set": {"box": box}})
    # 市场宝物到位
    markets.insert_one({"name": treasure, "price": price, "owner": username,"type":treasure_to_sell["type"],"level":treasure_to_sell["level"]})
    info="挂牌成功" 
    marketList=markets.find({}) 
    history.insert_one({"name":username,"opt_time":time(),"opt_type":"sell","detail":"sell "+treasure+"money: "+str(price)})#记录一下这个历史~

    #return render_template("market_index.html",info=info,markets=marketList,user=player)
    return '404'

#工具人function
# 宝箱充满系统回收最low宝物
def recovery_treasure(name):
    # 获得玩家宝箱，初始化为box[0]为最low宝物
    box = players.find_one({"name": name})['box']
    drop_treasure_name=box[0]["name"]#获取被丢弃的低端宝物的名称
    level=box[0]["level"]#获取被抛弃的低端宝物的等级
    drop_treasure_type=box[0]["type"]#获取丢弃宝物的type
    for treasure in box[1:]:#trick:初始化1不用比
        temp = treasure["level"]
        if temp < level:
            level = temp
            drop_treasure_name=treasure["name"]
            drop_treasure_type=treasure["type"]
    #从宝箱中进行删除：注意这里宝物的名字都是不一样的以简化：
    for treasure in box:
        if (treasure["name"]==drop_treasure_name):
            box.remove(treasure)
            break
    #从箱子中删除中按道理是系统的回收：更新系统treasurelist
    #left to promote
    #更新玩家宝箱
    #print(box)
    players.update_one({'name': name}, {"$set": {"box": box}})

    history.insert_one({"name":name,"opt_time":time(),"opt_type":"Sysytem_recovery","detail":"系统回收了低端宝物： "+treasure['name']})#记录一下这个历史~

    print("玩家 %-6s 被系统回收宝物 %-6s" % (name, drop_treasure_name))




if __name__ == "__main__":
    print("welcome to the game")