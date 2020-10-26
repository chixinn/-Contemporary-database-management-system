# File Name: recommand.py

from random import choice
from itertools import chain
import MySQLdb


def recommand(user_id):
    # 创建连接数据库的对象
    db = MySQLdb.connect("localhost", "root", "", "recommand")
    # 获取处理数据的游标
    cursor = db.cursor()

    # 获取已经看过的最喜爱的番剧 ID 的 SQL 查询语句
    sql = 'SELECT anime_id FROM user_anime WHERE user_id = {}'.format(user_id)
    # 执行 SQL 查询语句
    cursor.execute(sql)
    # 最喜爱的番剧的 ID 列表
    # chain 方法的作用如其名，接收任意数量的可迭代对象作为参数
    # 将全部参数中的元素取出后变成一串数据存放到迭代器中返回
    love_anime_id_list = list(chain(*cursor.fetchall()))

    # 该语句用于查询前三个最喜欢的番剧类型及其数量的元组
    sql = '''SELECT style_id, COUNT(style_id) FROM (
          SELECT style_id FROM anime_style WHERE anime_id IN (
          SELECT anime_id FROM user_anime WHERE user_id = 1
          )) AS a GROUP BY 1 ORDER BY 2 DESC LIMIT 3;
          '''.format(user_id)
    cursor.execute(sql)
    # 前三个最喜欢的番剧类型及其数量的元组
    love_style = cursor.fetchall()
    # 该字典用于存储最喜欢的番剧类型 ID 及其对应的番剧 ID 列表
    anime_dict = {}
    # 将番剧类型及其对应番剧 ID 存入字典
    for (style_id, _) in love_style:
        sql = sql = 'SELECT anime_id FROM anime_style WHERE style_id = {}' \
                .format(style_id)
        cursor.execute(sql)
        anime_dict[str(style_id)] = [i[0] for i in cursor.fetchall()]
    # 喜欢的全部番剧的 ID 集合
    whole_love_anime_id_set = set(chain(*anime_dict.values()))

    # 从喜欢的全部番剧 ID 集合中剔除已经看过的番剧 ID
    # 余下的就是喜欢但未看过的番剧 ID
    unlook_love_anime_id_set = whole_love_anime_id_set.difference(
            set(love_anime_id_list))
    # 获取喜欢但未看过的番剧 ID 列表
    unlook_love_anime_id_list = list(unlook_love_anime_id_set)

    # 随机选择其中的一个番剧 ID
    random_anime_id = choice(unlook_love_anime_id_list)
    # 获取番剧名称及其简介的 SQL 语句
    sql = 'SELECT name, brief FROM anime WHERE id = {}'.format(random_anime_id)
    cursor.execute(sql)
    # 将查询结果构成字典返回
    name, brief = cursor.fetchall()[0]
    result = {'name': name, 'brief': brief}
    db.close()
    return result

if __name__ == '__main__':
    print(recommand(1))
