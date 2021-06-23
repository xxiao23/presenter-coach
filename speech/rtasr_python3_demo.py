# -*- encoding:utf-8 -*-

import sys
import hashlib
from hashlib import sha1
import hmac
import base64
from socket import *
import json, time, threading
from websocket import create_connection
import websocket
from urllib.parse import quote
import logging

# reload(sys)
# sys.setdefaultencoding("utf8")
logging.basicConfig()

base_url = "ws://rtasr.xfyun.cn/v1/ws"
app_id = ""
api_key = ""
file_path = r"./test_zhi-zhenhao_1min.wav"

pd = "edu"

end_tag = "{\"end\": true}"


class Client():
    def __init__(self):
        ts = str(int(time.time()))
        tt = (app_id + ts).encode('utf-8')
        md5 = hashlib.md5()
        md5.update(tt)
        baseString = md5.hexdigest()
        baseString = bytes(baseString, encoding='utf-8')

        apiKey = api_key.encode('utf-8')
        signa = hmac.new(apiKey, baseString, hashlib.sha1).digest()
        signa = base64.b64encode(signa)
        signa = str(signa, 'utf-8')

        self.ws = create_connection(base_url + "?appid=" + app_id + "&ts=" + ts + "&signa=" + quote(signa))
        self.trecv = threading.Thread(target=self.recv)
        self.trecv.start()

    def send(self, file_path):
        file_object = open(file_path, 'rb')
        try:
            index = 1
            while True:
                chunk = file_object.read(1280)
                if not chunk:
                    break
                self.ws.send(chunk)

                index += 1
                time.sleep(0.04)
        finally:
            file_object.close()

        self.ws.send(bytes(end_tag.encode('utf-8')))
        print("send end tag success")

    def recv(self):
        try:
            seg_id = 0
            while self.ws.connected:
                result = str(self.ws.recv())
                if len(result) == 0:
                    print("receive result end")
                    break
                    
                result_dict = json.loads(result)
                # 解析结果
                if result_dict["action"] == "started":
                    print("handshake success, result: " + result)

                if result_dict["action"] == "result":
                    result = json.loads(result_dict["data"])
                    if result['cn']['st']['type'] == "0":
                        #with open('zhi_new/seg_id_' + str(seg_id) + '.json', 'w') as json_file:
                            #json.dump(result, json_file)
                        bg = int(result['cn']['st']['bg'])
                        txt = result['cn']['st']['rt'][0]['ws']

                        for i in range(len(txt)):
                            word = txt[i]['cw'][0]['w']
                            wb = int(txt[i]['wb'])
                            we = int(txt[i]['we'])
                            actual_wb = bg + wb * 10
                            actual_we = bg + we * 10
                            print(actual_wb, " ", actual_we, " ", word)
                    seg_id = seg_id + 1
                if result_dict["action"] == "error":
                    print("rtasr error: " + result)
                    self.ws.close()
                    return
        except websocket.WebSocketConnectionClosedException:
            print("receive result end")

    def close(self):
        self.ws.close()
        print("connection closed")


if __name__ == '__main__':
    client = Client()
    client.send(file_path)
