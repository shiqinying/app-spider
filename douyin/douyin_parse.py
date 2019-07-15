import json
# from .douyin_mongo import mongo_douyin

def response(flow):
    print('#######################')
    if 'aweme/v1/user/follower/list/' in flow.request.url:
        print("*************************")
        for _ in json.loads(flow.response.text)['followers']:
            user = {}
            user['name'] = _.get('nickname')
            user['share_id'] = _.get('uid')
            user['user_id'] = _.get('short_id')
            # mongo_douyin.insert_user(user)
            print(user)
            print(1)
