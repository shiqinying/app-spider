import json
from .douyin_mongo import mongo_douyin

def response(flow):
    if 'aweme/v1/user/follower/list/' in flow.request.url:
        for _ in json.loads(flow.response.text)['followers']:
            user = {'type':'douyin'}
            user['share_id'] = _.get('uid')
            user['user_id'] = _.get('short_id')
            user['name'] = _.get('nickname')
            mongo_douyin.insert_user(user)
            print(user)
