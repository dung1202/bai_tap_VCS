#!/usr/bin/env python3

import socket 
import argparse, re

parser = argparse.ArgumentParser()
parser.add_argument("--url",dest="host", help="url")
parser.add_argument("--user",dest="username", help="user")
parser.add_argument("--password",dest="password", help="password")
# parser.usage = parser.format_help()
args = parser.parse_args()

HOST = args.host
PORT = 80
user = args.username
password = args.password
PATH = "/wp-login.php"

if HOST and user and password:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST,PORT))
        
        body = f'log={user}&pwd={password}'
        request = ( f'POST {PATH} HTTP/1.1\r\n'
                    f'Host: {HOST}\r\n'
                    f'Content-Type: application/x-www-form-urlencoded\r\n'
                    f'Content-Length: {len(body)}\r\n'
                    f'Connection: close\r\n\r\n'
                    f'{body}\r\n')

        s.sendall(request.encode())
        buf = b''
        chunk = s.recv(1024)
        while len(chunk) != 0:
            buf += chunk
            chunk = s.recv(1024)
        res = buf.decode()
        # print(res)
        
        ktra_cookie = re.findall("wordpress_logged_in_", res)
        if ktra_cookie:
            print(f"User {user} đăng nhập thành công ")
        else:
            print(f"User {user} đăng nhập thất bại")
else:
    parser.print_help()