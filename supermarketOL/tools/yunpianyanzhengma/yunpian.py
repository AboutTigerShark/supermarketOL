# coding=utf-8
import json

import requests


class YunPian(object):
    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = 'https://sms.yunpian.com/v2/sms/single_send.json'

    def send_sms(self, code, mobile):
        params = {
            'apikey': self.api_key,
            'mobile': mobile,
            'text': '【林武彬】您的验证码是{0}。如非本人操作，请忽略本短信'.format(code)
        }

        response = requests.post(self.single_send_url, data=params)
        dict_text = json.loads(response.text)
        return dict_text

# if __name__ == '__main__':
#     yunpian = YunPian()
#     yunpian.send_sms()