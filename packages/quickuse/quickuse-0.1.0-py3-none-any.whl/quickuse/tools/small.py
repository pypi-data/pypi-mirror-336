
import requests
import json
import os
from typing import Callable, List, Dict, Any

class DDMessage:
    """
    DingDing_POST类用于向钉钉发送POST请求。
    """
    def __init__(self):
        """
        初始化DingDing_POST类。

        参数:
        token (str): 钉钉机器人的token。
        """
        token = os.environ.get("DD_TOKEN")
        self.host = f"https://oapi.dingtalk.com/robot/send?access_token={token}"

    def send(self,role: str, content: str):
        """
        向钉钉发送文本消息.
        参数:
        role (str): 信号发出者 可以使用Agent System Majordomo
        content (str): 消息内容。
        返回:
        None
        """
        assert role in ["Agent", "System", "Majordomo"]
        
        content = f"{role} : {content}"
        data = {"msgtype": "text", "text": {"content": content}}
        requests.post(self.host, data=json.dumps(data), headers={'Content-Type': 'application/json'})

import os

def send_message_via_dd(role: str, content: str):
    """
    通过钉钉机器人发送消息。

    参数:
    role (str): 信号发出者，可以是 "Agent", "System", 或 "Majordomo"。
    content (str): 要发送的消息内容。

    返回:
    None
    """
    # 确保环境变量中有钉钉机器人的token
    if not os.environ.get("DD_TOKEN"):
        raise ValueError("Environment variable 'DD_TOKEN' is not set.")

    # 创建DDMessage实例
    dd_message = DDMessage()

    # 发送消息
    dd_message.send(role, content)


import setproctitle
from loguru import logger 
import getpass
from datetime import datetime

def setprocesstitle(name):
    setproctitle.setproctitle(name)

def exec_str(code:str,local_vars:dict = {})->dict:
    # local_vars 入参
    # code 代码
    
    exec(code, globals(), local_vars)
    return local_vars

def password(key):
    return getpass.getpass(f'{key} input:')

def get_today():
    # 获取本地时间
    local_time = datetime.today()
    # print("本地时间:", local_time)
    return local_time
