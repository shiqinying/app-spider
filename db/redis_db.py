# 安装 pip install redis

import redis
from config import *


redis_client = redis.StrictRedis(host=REDIS_HOST,port=REDIS_PORT,password=REDIS_PWD,decode_responses=True)