from common.request import HttpRequest
import random,json

def get_selNotAuditIptList():
    req = HttpRequest()
    url = "http://10.1.1.71:9999/auditcenter/api/v1/ipt/selNotAuditIptList"
    headers = {'Content-Type': "application/json"}
    param = {}
    res = req.post_json(url, param)
    if res['data']['engineInfos']:
        engineids = [i['id'] for i in res['data']['engineInfos']]
        # print(engineids)
        random_engineid = random.choice(engineids)
        print(random_engineid)
        url = 'http://10.1.1.71:9999/auditcenter/api/v1/ipt/orderList' + '?id=' + str(random_engineid)
        orderlist = req.get(url)
        print(orderlist['data'])
        gps = list(orderlist['data'].keys())
        gp = [i for i in list(orderlist['data'].keys()) if orderlist['data'][i][0]['auditMarkStatus'] is None]
        # for i in gps:
        #     print(i)
        #     print(orderlist['data'][i][0])
        #     print(orderlist['data'][i][0]['auditMarkStatus'])
            # print(type(orderlist['data'][i][0]))


        para = {
            "groupOrderList": [{
                "auditBoList": [],
                "groupNo": gp[0],
                "auditInfo": "必须修改",
                "auditStatus": 0,
                "engineId": random_engineid,
                "orderType": 1
            }]
        }
        aa = req.post_json('http://10.1.1.71:9999/auditcenter/api/v1/ipt/auditSingle',para)
        print(aa)

        print(gps[0])
    # s = 0
    # for i in res['data']['taskNumList']:
    #     # print(i['taskNum'])
    #     s += i['taskNum']
    # print(s)


if __name__ == '__main__':
    get_selNotAuditIptList()
