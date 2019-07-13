import json
import re
from mitmproxy import ctx

URL = "h5/mtop.taobao.wsearch.h5search"
page = 0
num = 0


def response(flow):
    global num, page
    if URL in flow.request.url:
        raw_text = flow.response.text
        text = re.sub("\)", "", re.sub("mtopjsonp\d+\(", "", raw_text))
        page += 1
        for _ in json.loads(text)["data"]["listItem"]:
            goods = {}
            goods["area"] = _.get("area")
            goods["price"] = _.get("price")
            goods["nick"] = _.get("nick")
            goods["name"] = _.get("name")
            num += 1
            # ctx.log.info(json.dumps(goods))
            # ctx.log.warn(str(num))
            print(goods)
print('total page: ',page)
print('total num: ',num)
