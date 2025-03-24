import json
import requests
import os
import psutil
from datetime import datetime


class Image:
    def __init__(self, object_name: str = None, img_url: str = None):
        self.objectName = object_name
        self.img_url = img_url

    def json(self):
        return json.dumps(self.__dict__)


class UserMsg:
    def __init__(self, text=None, image=None):
        self.text = text
        self.image = image


class DingTalkWebhook:
    def __init__(self, text, phones, webhook_id=None, webhook_url=None):
        self.text = text
        self.phones = phones
        self.webhook_id = webhook_id
        self.webhook_url = webhook_url


def custom_serializer(obj):
    if isinstance(obj, Image):
        return obj.json()
    raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')


class ParamTest:
    def __init__(self, dict):
        self.dict = dict

    def get(self, key):
        return self.dict.get(key)


class Rtn(dict):
    def __init__(self, code=None, msg=None):
        # self.code = code
        # self.msg = msg
        super().__init__()
        self['code'] = code
        self['msg'] = msg

    @classmethod
    def success(cls, msg=""):
        return Rtn(code=200, msg=msg)

    @classmethod
    def fail(cls, msg=""):
        return Rtn(code=500, msg=msg)

    @classmethod
    def fail_with_code(cls, code=500, msg=""):
        return Rtn(code=code, msg=msg)

    def set_code(self, code):
        self['code'] = code
        return self

    def set_msg(self, msg):
        self['msg'] = msg
        return self

class ZhiwoUserCauseException(Exception):

    def __init__(self, message):
        super().__init__(message)

class ZhiwoAssistant:

    def __init__(self, param):
        self.param = param
        if param.get('authorization') is None or len(param.get('authorization')) == 0:
            raise ValueError('authorization参数不能为空')
        profile = param.get('authorization').split('#')[0]
        call_remote = param.get('authorization').split('#')[1] == 'call_remote'
        self.authorization = param.get('authorization').split('#')[2]
        self.refBusinessKey = param.get('refBusinessKey')
        if not call_remote:
            self.base_url = "http://localhost:8080"
        elif profile == 'test':
            self.base_url = "https://core-apigateway-test.renliwo.com/dep-service"
        elif profile == 'uat':
            self.base_url = "https://uat-core.renliwo.com/dep-service"
        elif profile == 'pro':
            self.base_url = 'https://alipay-bu-gw-prod.renliwo.com/dep-service'
        else:
            raise ValueError('未知使用环境')

    def send_ding_talk_webhook(self, text, phones, webhook_id=None, webhook_url=None):
        ding_talk_webhook = DingTalkWebhook(text, phones, webhook_id, webhook_url)
        self.send_msg(ding_talk_webhook=ding_talk_webhook)

    def send_user_msg(self, text: str):
        # user_msg = UserMsg(text, self.mode, self.conversationMainId)
        self.send_msg(user_msg_text=text)

    def send_msg(self, user_msg_text: str = None, image: Image = None, ding_talk_webhook: DingTalkWebhook = None):
        headers = {
            'Authorization': self.authorization,
            'refBusinessKey': self.refBusinessKey,
            'Content-Type': 'application/json'
        }

        multi_msg = {}
        if user_msg_text is not None or image is not None:
            user_msg = UserMsg(text=user_msg_text, image=image)
            multi_msg['user_msg'] = user_msg.__dict__
        if ding_talk_webhook is not None:
            multi_msg['ding_talk_webhook'] = ding_talk_webhook.__dict__

        if not multi_msg:
            return False

        url = self.base_url + '/appsdk/sendMsg'
        data_json = json.dumps(multi_msg, default=custom_serializer)
        response = requests.request('POST', url, headers=headers, data=data_json)
        if response.status_code != 200:
            print(f'发送消息 {data_json} 响应码不是200, {response.text}')
            return False
        else:
            response_json = response.json()
            response_code = response_json.get('code')
            if response_code != '200':
                print(f'发送消息 {data_json} 状态码不是200 response:{json.dumps(response_json)}')
                return False
            else:
                return True

    def get_sql_data_by_job_number(self, jobNumber, param=None):
        headers = {
            'Authorization': self.authorization,
            'refBusinessKey': self.refBusinessKey,
            'Content-Type': 'application/json'
        }

        payload = {
            'jobNumber': jobNumber,
            'paramJson': json.dumps(param)
        }

        url = self.base_url + '/appsdk/getSqlDataByJobNumber'
        data_json = json.dumps(payload)
        response = requests.request('POST', url, headers=headers, data=data_json)
        if response.status_code != 200:
            print(f'查询sql {data_json} 响应码不是200, {response.text}')
            return None
        else:
            response_json = response.json()
            response_code = response_json.get('code')
            if response_code != '200':
                print(f'查询sql {data_json} 状态码不是200 response:{json.dumps(response_json)}')
                return None
            else:
                result = response_json.get("result")
                if result is None:
                    print(f'查询sql {data_json} result为空 response:{json.dumps(response_json)}')
                    return None
                else:
                    return result

    def http_call(self, httpMethod, url, headers, data):
        request_params = {
            "headersMap": headers,
            "url": url,
            "httpMethod": httpMethod,
            "body": data
        }

        request_headers = {
            'Authorization': self.authorization,
            'refBusinessKey': self.refBusinessKey,
            'Content-Type': 'application/json'
        }

        request_params_str = json.dumps(request_params)
        response = requests.request("POST", self.base_url + "/appsdk/httpCall",
                                    headers=request_headers, data=request_params_str)

        return response

    def get_process_info(self, pid=os.getpid()):
        try:
            # 根据 PID 获取进程对象
            process = psutil.Process(pid)
            # 构建当前进程的信息字典
            process_info = {
                'pid': process.pid,
                'name': process.name(),
                'create_time': datetime.fromtimestamp(process.create_time()).strftime('%Y-%m-%d %H:%M:%S'),
            }
            # 获取当前进程的子进程
            children = process.children()
            if len(children) > 0:
                process_info['children'] = []
                for child in children:
                    # 递归调用函数获取子进程的树形结构
                    child_info = self.get_process_info(child.pid)
                    process_info['children'].append(child_info)
            return process_info
        except psutil.NoSuchProcess:
            print(f"具有 PID {pid} 的进程不存在。")
            return None
        except psutil.AccessDenied:
            print(f"没有权限访问具有 PID {pid} 的进程。")
            return None

    # 上报进程信息
    def record_process_info(self, pid=os.getpid()):
        process_info = self.get_process_info(pid)
        log = {
            'processInfo': json.dumps(process_info)
        }
        self.record(log)

    def record(self, log):
        headers = {
            'Authorization': self.authorization,
            'refBusinessKey': self.refBusinessKey,
            'Content-Type': 'application/json'
        }

        payload = json.dumps(log)

        url = self.base_url + '/appsdk/record'
        response = requests.request('POST', url, headers=headers, data=payload)
        if response.status_code != 200:
            print(f'上报日志 响应码不是200, {response.text}')
        else:
            response_json = response.json()
            response_code = response_json.get('code')
            if response_code != '200':
                print(f'上报日志 状态码不是200 response:{json.dumps(response_json)}')

    def __str__(self):
        return f'ZhiwoAssistant(refBusinessKey={self.refBusinessKey}, authorization={self.authorization}, base_url={self.base_url})'


# python setup.py sdist build
# twine upload dist/*

if __name__ == '__main__':
    a=Rtn.success()
    b=Rtn.fail()
    c=Rtn.fail("error")
    d=Rtn.fail_with_code(100, "error")
    d.set_code(1000)

    # raise ZhiwowoException('参数校验错误')
    raise ZhiwowoException('参数校验错误', code=100)
    # mode:0-正常消息 1-debug 2-调度测试
    # param = ParamTest({
    #     'refBusinessKey': 'BK1888138540634738688',
    #     'authorization': 'test#call_remote#Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJBUFAxODY2MDE1ODY3MjkzMjc0MTEyOm9rOm51bGw6bnVsbDpudWxsIiwiaWF0IjoxNzM5MjUzMzU3LCJleHAiOjE3MzkyNjA1NTd9.sI56knlcwPbo2blbVdv_e0upnR__4acTw39MSXYJbFAC55IrDFmeIDy-wBvP29i1s201W4N3T5vcC_j-r7wO3Q'
    # })
    # assistant = ZhiwoAssistant(
    #     param
    # )
    # sql_data = assistant.get_sql_data_by_job_number('JOB1862406221601050625', '5007 5008')
    # assistant.send_user_msg('请扫码登录')
    # assistant.record_process_info()
    # assistant.send_user_msg('请扫码登录')
    # assistant.send_msg(image=Image(object_name='image/2024/4/img1849344913033007104.png'))
