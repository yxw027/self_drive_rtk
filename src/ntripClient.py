#coding=utf-8
import socket
import serial
import base64
import time
import Queue as queue
# import queue


class ntripClient():
    
    def __init__(self, mount_pt='sweet', ser_port='/dev/ttyS6', bps=115200, host='117.184.129.18', port=8061):
        print('ntrip init')
        # 下发串口
        self.ser=serial.Serial(ser_port, bps)
        # 连接ntrip caster
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))
        # ntrip 协议头
        username = "sweet"  
        password = 'dian123456'
        pwd = base64.b64encode("{}:{}".format(username, password).encode('ascii'))
        pwd = pwd.decode('ascii')
        self.header = \
            "GET /%s HTTP/1.1\r\n" % mount_pt + \
            "User-Agent: NTRIP client.py/0.1\r\n" + \
            "Authorization: Basic {}\r\n\r\n".format(pwd)


    def recv_from_svr(self):
        # RTCM 消息接收
        while True:
            pre_t =time.time()
            head_flag = False
            try:
                dat = self.s.recv(1056) 
                # print(dat)
            except socket.error:
                print('err')
                dat = []
            if len(dat) > 0:
                self.ser.write(dat)
        self.s.close()

    def run(self):
        # 主程序
        while True:
            # ntrip挂载
            print("Header sending... \n")
            self.s.send(self.header.encode('ascii'))
            print("Waiting answer...\n")
            data = self.s.recv(12).decode('ascii')
            if len(data) == 0:
                continue
            if 'OK' in data: 
                break
            time.sleep(1)
        self.recv_from_svr()


if __name__ == '__main__':
    n = ntripClient(mount_pt='sweet_bds', ser_port='/dev/ttyUSB0')
    n.run()
