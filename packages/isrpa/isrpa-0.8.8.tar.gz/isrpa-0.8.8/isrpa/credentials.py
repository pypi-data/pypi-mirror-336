import os

import requests


def store_key(key_name,key_value,user_name):
    """
        用户凭证存储
        key_name:凭证key
        key_value:凭证value
        user_name:用户名

    """
    address = os.environ.get("address", "192.168.12.249")
    url = f"http://{address}/console/api/user_credentials"
    print(url)
    headers = {
        'Content-Type': 'application/json',  # 说明请求体是 JSON 格式
    }
    # 请求体的数据
    data = {
        'certificate_key': key_name,
        'certificate_value': key_value,
        'user_name': user_name
    }
    print(data)
    requests.post(url, headers=headers, json=data)

def get_key(key_name, user_name):
    """
        获取用户凭证
        key_name：凭证key
        user_name:用户名称
    """
    address = os.environ.get("address", "192.168.12.249")
    url = f"http://{address}/console/api/user_credentials?certificate_key={key_name}&user_name={user_name}"
    print(url)
    response = requests.get(url)
    if response.status_code != 200:
        print("请求失败，状态码：", response.status_code)
        return "failure"
    json = response.json()

    return json['certificate_value']

def delete_key(key_name,user_name):
    """
        删除凭证
        key_name：凭证key
        user_name:用户名称
    """
    address = os.environ.get("address", "192.168.12.249")
    url = f"http://{address}/console/api/user_credentials"
    print(url)
    headers = {
        'Content-Type': 'application/json',  # 说明请求体是 JSON 格式
    }
    # 请求体的数据
    data = {
        'certificate_key': key_name,
        'user_name': user_name
    }
    print(data)
    requests.delete(url, headers=headers, json=data)

def list(user_name):
    """
        获取所有凭证key
        user_name:用户名称
    """
    address = os.environ.get("address", "192.168.12.249")
    url = f"http://{address}/console/api/user_credentials/list?user_name={user_name}"
    print(url)
    response = requests.get(url)
    if response.status_code != 200:
        print("请求失败，状态码：", response.status_code)
        return "failure"
    json = response.json()

    return json

def exist(key_name, user_name):
    """
        获取用户凭证
        key_name：凭证key
        user_name:用户名称
    """
    address = os.environ.get("address", "192.168.12.249")
    url = f"http://{address}/console/api/user_credentials?certificate_key={key_name}&user_name={user_name}"
    print(url)
    response = requests.get(url)
    if response.status_code != 200:
        return False


    return True

if __name__ == '__main__':
    print(exist("ccc","zhouly@i-search.com.cn"))