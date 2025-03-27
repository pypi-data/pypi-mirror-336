# -*- coding: UTF-8 -*-
import requests
import re


def parse_cipcc(ip=None):
    url = f"http://www.cip.cc/{ip}" if ip else "http://www.cip.cc/"
    try:
        response = requests.get(url, headers={"User-Agent": "curl/7.79.1"})
        response.raise_for_status()

        # 解析关键字段
        result = {}
        for line in response.text.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().replace(' ', '')
                value = value.strip()
                if key in ["IP", "地址", "运营商", "数据二", "数据三", "URL"]:
                    result[key] = value

        if '地址' in result:
            result['地区'] = result['地址'].split(' ', 2)
        return result

    except requests.RequestException as e:
        return {"error": f"请求失败：{str(e)}"}
    except Exception as e:
        return {"error": f"解析错误：{str(e)}"}

def main(greeting):
    print(greeting)
    return greeting

if __name__ == "__main__":
    main("hello world")