import requests
import json
import urllib.parse
from config import conf
from lib import itchat
from common.log import logger

# baseUrl = 'http://192.168.10.6:8080/paa-boot/'
baseUrl = conf().get("paa_boot_url", "https://api3.foryouai.com/")
paa_boot_key = conf().get("paa_boot_key", "")
headers = {
    'Content-Type-Type': 'application/json',
    'Authorization': paa_boot_key
}

def accountBindingByReceiver(receiver):
    """
    判断用户是否已登录
    :param receiver：微信会话id
    :return 登录状态
    """
    login_state = checkLoginByReceiver(receiver)
    if login_state != 1:
        appid = conf().get("wechat_appid")
        # params = {
        #     'receiver': receiver
        # }
        # encoded_receiver = urllib.parse.urlencode(params)
        # miniappurl = f"你还未注册或登录，请先点击以下地址注册或登！weixin://dl/business/?appid={appid}&path=pages/index/index&{encoded_receiver}&env_version=trial"
        url = f"receiver={receiver}"
        encoded_url = urllib.parse.quote_plus(url)
        miniappurl = f"你还未注册或登录绑定，请先点击以下‘真好-AI亲子教育私人助理’微信小程序链接注册或登录！weixin://dl/business/?appid={appid}&path=pages/index/index&query={encoded_url}"
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

def getDialogueNum(receiver):
    """
    查询积分
    :param receiver：微信会话id
    :return 剩余积分
    """
    url = baseUrl + 'sys/api/customer/getFreeNumTotal'
    params = {
        'key': receiver,
        'keyType': 3
    }

    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        result = response.json()
        # print(result)
        return result
    else:
        return 0

def deductDialogueNum(receiver):
    """
    扣除积分
    :param receiver：微信会话id
    :return 扣除是否成功
    """
    url = baseUrl + 'sys/api/customer/deductDialogueNum'
    params = {
        'key': receiver,
        'keyType': 3
    }

    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        result = response.json()
        logger.info("[WX] receiver={}对话次数扣除成功!".format(receiver))
        # print(result)
        # return result
    else:
        logger.error("[WX] Error: receiver={}对话次数扣除失败! ".format(receiver))

def checkVip(receiver):
    """
    查询是否是会员
    :param receiver：微信会话id
    :return 是否是会员
    """
    url = baseUrl + 'sys/api/customer/checkVipByKey'
    params = {
        'key': receiver,
        'keyType': 3
    }

    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        result = response.json()
        logger.info("[WX] receiver={}查询是否为会员成功!".format(receiver))
        print(result)
        vip=result['result']['isVip']
        return vip
    else:
        logger.error("[WX] Error: receiver={}查询是否为会员失败! ".format(receiver))
        return 0


# if __name__ == "__main__":
#     sing=accountBindingByReceiver('@9bb17cc879842edfcf6abc19f107f22d')
#     print(sing)