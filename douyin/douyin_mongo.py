import pymongo
from pymongo.collection import Collection


HOST = 'localhost'
PORT = 27017

class MongoDouyin():

    def __init__(self, host, port):
        self.client = pymongo.MongoClient(host=host, port=port)
        self.db = self.client['douyin']

    def insert_user(self,user):
        #{'type':'douyin','name':'xiaowang','user_id':'666666','share_id':'888888888'}
        collection = Collection(self.db,'douyin_user')
        return collection.insert_one(user)

    def find_user(self,name):
        collection = Collection(self.db, 'douyin_user')
        return collection.find_one({'name': name})

    def find_one_and_delete(self):
        collection = Collection(self.db, 'douyin_user')
        return collection.find_one_and_delete({'type':'douyin'})

    def update_user(self, user):
        collection = Collection(self.db, 'douyin_user')
        collection.update_one({'share_id': user['share_id']}, {'$set': user})


mongo_douyin = MongoDouyin(host=HOST, port=PORT)

if __name__ == "__main__":

    mongo_douyin.find_user()

