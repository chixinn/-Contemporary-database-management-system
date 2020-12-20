import pymongo
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from pymongo.errors import BulkWriteError



def init_db(treasures):
    # 数据库信息由test.py获得
    # 建立unique索引
    treasureTest=[{'name': 'kwdro', 'level': 31, 'type': 'working'}, 
{'name': 'rdjvl', 'level': 3, 'type': 'working'}, {'name': 'czifa', 'level': 52, 'type': 'working'}, {'name': 'mljay', 'level': 57, 'type': 'working'}, {'name': 'ozehx', 'level': 20, 'type': 'working'}, {'name': 'yhbxa', 'level': 51, 'type': 'working'}, {'name': 'vjwbc', 'level': 37, 'type': 'working'}, {'name': 'xpyzb', 'level': 10, 'type': 'working'}, {'name': 'nrloe', 'level': 40, 'type': 'working'}, {'name': 'jahcy', 'level': 40, 'type': 'working'}, 
{'name': 'sfhod', 'level': 48, 'type': 'working'}, {'name': 'aoubx', 'level': 14, 'type': 'working'}, {'name': 'lhsgt', 'level': 14, 'type': 'working'}, {'name': 'ewjsc', 'level': 34, 'type': 'working'}, {'name': 'qwndo', 'level': 26, 'type': 'working'}, {'name': 'wknpf', 'level': 37, 'type': 'working'}, {'name': 'kbdhl', 'level': 25, 'type': 'working'}, {'name': 'bsolk', 'level': 57, 'type': 'working'}, {'name': 'kusra', 'level': 56, 'type': 'working'}, {'name': 'uwmkb', 'level': 31, 'type': 'working'}, {'name': 'fjgnz', 'level': 16, 'type': 'working'}, {'name': 'luckd', 'level': 45, 'type': 'working'}, {'name': 'aoryt', 'level': 4, 'type': 'working'}, {'name': 'pflvt', 'level': 55, 'type': 'working'}, 
{'name': 'tkbug', 'level': 51, 'type': 'working'}, {'name': 'sazcn', 'level': 17, 'type': 'working'}, {'name': 'hjuqn', 'level': 11, 'type': 'working'}, {'name': 'ptbro', 'level': 11, 'type': 'working'}, {'name': 'myojx', 'level': 26, 'type': 'working'}, {'name': 'xjimw', 'level': 34, 'type': 'working'}, {'name': 'buwjo', 'level': 17, 'type': 'fortune'}, {'name': 'bpvwf', 'level': 24, 'type': 'fortune'}, {'name': 'njcqy', 'level': 3, 'type': 'fortune'}, {'name': 'vmqyf', 'level': 22, 'type': 'fortune'}, {'name': 'jnxpd', 'level': 23, 'type': 'fortune'}, {'name': 'jyiuf', 'level': 42, 'type': 'fortune'}, {'name': 'heztb', 'level': 47, 'type': 'fortune'}, {'name': 'xpuvz', 'level': 7, 'type': 'fortune'}, {'name': 'osfdr', 'level': 56, 'type': 'fortune'}, {'name': 'tsgrx', 'level': 28, 'type': 'fortune'}, {'name': 'gvkxl', 'level': 59, 'type': 'fortune'}, {'name': 'pocqm', 'level': 8, 'type': 'fortune'}, {'name': 'siqxe', 'level': 36, 'type': 'fortune'}, {'name': 'bxhst', 'level': 6, 'type': 'fortune'}, {'name': 'krmht', 'level': 41, 'type': 'fortune'}, {'name': 'tyaxj', 'level': 19, 'type': 'fortune'}, {'name': 'mfvkz', 'level': 56, 'type': 'fortune'}, {'name': 'rwdmb', 'level': 46, 'type': 'fortune'}, {'name': 'qzvcw', 'level': 48, 'type': 'fortune'}, {'name': 'yqpjh', 'level': 13, 'type': 'fortune'}, {'name': 'obkue', 'level': 49, 'type': 'fortune'}, {'name': 'pbzfe', 'level': 26, 'type': 'fortune'}, {'name': 'ofevi', 'level': 32, 'type': 'fortune'}, 
{'name': 'ilwbt', 'level': 13, 'type': 'fortune'}, {'name': 'jdpqo', 'level': 2, 'type': 'fortune'}, {'name': 'lfghv', 'level': 41, 'type': 'fortune'}, {'name': 'xekgs', 'level': 49, 'type': 'fortune'}, {'name': 'rnytv', 'level': 21, 'type': 'fortune'}, {'name': 'zhgpo', 'level': 59, 'type': 'fortune'},
{"name":"rope","level":10,"type":"working"},{"name":"dice","level":9,"type":"fortune"},
                            {"name":"diya","level":9,"type":"fortune"}

]
    treasures.create_index([("name", pymongo.ASCENDING)], unique=True)
    try:
        treasures.insert_many(treasureTest)
        print("宝物信息库已更新!")
    except BulkWriteError or DuplicateKeyError:
        print("宝物信息库重复更新!!")


    
if __name__ == "__main__":
    print("welcome!")