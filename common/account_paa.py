import requests
import json
import urllib.parse
from config import conf
from lib import itchat
from common.log import logger

baseUrl = 'http://192.168.10.6:8080/paa-boot/'
headers = {
    'Content-Type-Type': 'application/json',
    'Authorization': 'dd05f1c54d63749eda95f9fa6d49v442a'
}

def accountBindingByReceiver(receiver):
    login_state = checkLoginByReceiver(receiver)
    if login_state != 1:
        appid = conf().get("wechat_appid")
        params = {
            'receiver': receiver
        }
        encoded_receiver = urllib.parse.urlencode(params)
        miniappurl = f"你还未注册或登录，请先点击以下地址注册或登！weixin://dl/business/?appid={appid}&path=pages/index/index&{encoded_receiver}"
        itchat.send(miniappurl, toUserName=receiver)
        logger.info("[WX] sendMsg={}, receiver={}".format(miniappurl, receiver))

    return login_state


# if response.status.status_code == 200:
    #     result = response.json()
    #     print(result)
    # else:
    #     print('Error:', response.status_code)

def checkLoginByReceiver(receiver):
    url = baseUrl + 'sys/api/customer/loginByReceiver'
    params = {
        'receiver': receiver
    }

    response = requests.get(url, params=params, headers=headers)
    # return response
    if response.status_code == 200:
        result = response.json()
        # print(result)
        if result['code'] == 200:
            return 1
        else:
            return 0
    else:
        return 0
        # print('Error:', response.status_code)

# if __name__ == "__main__":
#     sing=accountBindingByReceiver('@9bb17cc879842edfcf6abc19f107f22d')
#     print(sing)