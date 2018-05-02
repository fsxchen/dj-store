import requests


class YunPian(object):
    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = "https://sms.yunpian.com/v2/sms/single_send.json"

    def send_msg(self, code, mobile):
        parmas = {
            "apikey": self.api_key,
            "mobile": mobile,
            "text": "验证码{code}".format(code=code)
        }
        response = requests.post(self.single_send_url, parmas)
        import json
        print(json.loads(response.text))
        return json.loads(response.text)

if __name__ == "__main__":
    yp = YunPian("d6c4ddbf50ab36611d2f52041a0b949e")
    yp.send_msg("3389", 17710525152)
