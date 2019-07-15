import pymongo
from pymongo.collection import Collection
from config import *

class Mongo:

    def __init__(
        self,
        database,
        host=MONGO_HOST,
        username=MONGO_USER,
        password=MONGO_PWD,
        port=MONGO_PORT,
    ):
        """
        建立连接，初始化db对象
        :param database:
        :param host:
        :param username:
        :param password:
        :param port:
        """

        try:
            uri = "mongodb://{0}:{1}@{2}:{3}/".format(username, password, host, port)
            client = pymongo.MongoClient(uri)
            self.db = client[database]
        except Exception as e:
            print(e.args)

    def insert(self, collection_name, item, filter_field):
        """
        如果存在就更新
        如果不存在就插入
        :param collection_name: 集合名称
        :param item: 入库item
        :param filter_field:查询条件
        :return:
        """
        condition = {filter_field: collection_name[filter_field]}
        collection = self.db[collection_name]
        if collection.find_one(condition):
            collection.update_one(condition, {"$set": item})
            print("更新：", collection_name[filter_field])
        else:
            collection.insert_one(item)
            print("插入", collection_name[filter_field])

    def close(self):
        """
        mongodb 是否需要手动关闭连接？？？
        :return:
        """
        pass

if __name__=="__main__":
    """
    使用方法：
    使用前创建数据库和集合
    """
    item = {
        'name':'面包',
        'price':'13.8',
        'image':'https://www.baidu.com'
    }
    mongo = Mongo('shengxian')
    mongo.insert('dingdong',item,'name')
