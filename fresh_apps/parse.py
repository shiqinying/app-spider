import json


def response(flow):
    """
    TODO
    1响应失败处理策略
    2代理ip写入脚本
    :param flow:
    :return:
    """

    url_youxian = "https://as-vip.missfresh.cn/as/home/category/classifyProductInfo"
    url_dingdong = "https://maicai.api.ddxq.mobi/homeApi/categoriesDetail"
    url_jingdongdaojia = "https://gw-o2o.jddj.com/client"
    if flow.request.url.startswith(url_youxian):
        for _ in json.loads(flow.response.text)["data"]["cellList"]:
            item = {}
            item["secondGroupName"] = _.get("secondGroupName", "")
            if _.get("normalProducts"):
                product = _.get("normalProducts")
                item["name"] = product.get("name", "")
                try:
                    item["price_noVip"] = (
                        product.get("pricePro").get("noVip").get("price") / 100
                    )
                except:
                    item["price_noVip"] = ""
                try:
                    item["price_vip"] = (
                        product.get("pricePro").get("vip").get("price") / 100
                    )
                except:
                    item["price_vip"] = ""

                item["skuCategory"] = product.get("skuCategory", "")
                item["subtitle"] = product.get("subtitle")
                try:
                    item["promotionTag"] = product.get("promotionTag").get("name")
                except:
                    item["promotionTag"] = ""
                item["image"] = product.get("image")
                print(item)


    if flow.request.url.startswith(url_dingdong):
        text = json.loads(flow.response.text)
        try:
            cate_1 = text["data"]["ad_id"]
        except:
            cate_1 = ''
        for _ in text["data"]["cate"]:
            cate_2 = _["name"]
            for product in _["products"]:
                item2 = {}
                item2["cate_1"]=cate_1
                item2["cate_2"]=cate_2
                item2["name"]=product.get('name','')
                item2["origin_price"]=product.get('origin_price','')
                item2["price"]=product.get('price','')
                item2["vip_price"]=product.get('vip_price','')
                item2["spec"]=product.get('spec','')
                item2["small_image"]=product.get('small_image','')
                item2["total_sales"]=product.get('total_sales','')
                print(item2)
