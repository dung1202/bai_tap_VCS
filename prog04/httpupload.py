#!/usr/bin/env python3

import socket
import argparse
import re
import magic
from bs4 import BeautifulSoup
import urllib.request

parser = argparse.ArgumentParser()
parser.add_argument("--url", dest="host", help="url")
parser.add_argument("--user", dest="username", help="user")
parser.add_argument("--password", dest="password", help="password")
parser.add_argument("--local-file", dest="file", help="path file")
# parser.usage = parser.format_help()
args = parser.parse_args()

HOST = args.host
PORT = 80
user = args.username
password = args.password
pathFile = args.file
PATH = "/wp-login.php"


def readFileImage(filename):
    with open(filename, "rb") as f:
        return f.read()


mime = magic.Magic(mime=True)


def getCookie(listCookie):
    string_cookie = ""
    for cookie in listCookie:
        string_cookie += cookie + '; '
    string_cookie = string_cookie[:-2]
    return string_cookie


def getCookieUpdate(listCookie, response):
    newCookies = re.findall(r"Set-Cookie: (.*?)[;|\r\n]", response)
    for cookie in newCookies:
        if cookie not in listCookie:
            listCookie.append(cookie)


if HOST and user and password and pathFile:
    read_file = readFileImage(pathFile)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        listCookie = ["wordpress_test_cookie=WP+Cookie+check"]
        body = f'log={user}&pwd={password}'
        request = (f'POST {PATH} HTTP/1.1\r\n'
                   f'Host: {HOST}\r\n'
                   f'Content-Type: application/x-www-form-urlencoded\r\n'
                   f'Content-Length: {len(body)}\r\n'
                   f'Cookie: {getCookie(listCookie)}\r\n'
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
            getCookieUpdate(listCookie, res)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s1:
                s1.connect((HOST, PORT))
                request_anh = (
                    f'GET /wp-admin/media-new.php/ HTTP/1.1\r\n'
                    f'Host: {HOST}\r\n'
                    f'Upgrade-Insecure-Requests: 1\r\n'
                    f'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0\r\n'
                    f'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*\r\n'
                    f'Cookie: {getCookie(listCookie)}\r\n'
                    f'Connection: close\r\n'
                    f'\r\n'
                )
                s1.sendall(request_anh.encode())
                buf = b''
                chunk = s1.recv(1024)
                while len(chunk) != 0:
                    buf += chunk
                    chunk = s1.recv(1024)
                res = buf.decode()
                getCookieUpdate(listCookie, res)
                params = re.search(
                    '"multipart_params":.*_wpnonce":"[0-9a-z]+"', res)

                wp_nonce = re.search(
                    '(?<=_wpnonce":")[a-z0-9]{10}', params.group())
                id = re.search('(?<=post_id":)[0-9]', params.group())
                id = id.group()
                # print(wp_nonce)
                wp_nonce = wp_nonce.group()
                # print(id.group(), wp_nonce, params.group())/
                # print(res)
                WebKitFormBoundaryXXX = "---------------------------335679337115370071493285990705"
                file_name = pathFile.split("\\")[-1]
                p1 = (
                    f'--{WebKitFormBoundaryXXX}\r\n'  # WebKitFormBoundaryXXX
                    f'Content-Disposition: form-data; name="async-upload"; filename="{file_name}"\r\n'
                    f'Content-Type: {mime.from_file(pathFile)}\r\n\r\n')

                p2 = ('\r\n'
                      f'--{WebKitFormBoundaryXXX}\r\n'
                      f'Content-Disposition: form-data; name="html-upload"\r\n\r\n'
                      f'Upload\r\n'
                      f'--{WebKitFormBoundaryXXX}\r\n'
                      f'Content-Disposition: form-data; name="post_id"\r\n\r\n'
                      f'{id}\r\n'
                      f'--{WebKitFormBoundaryXXX}\r\n'
                      f'Content-Disposition: form-data; name="_wpnonce"\r\n\r\n'
                      f'{wp_nonce}\r\n'
                      f'--{WebKitFormBoundaryXXX}\r\n\r\n'
                      f'Content-Disposition: form-data; name="_wp_http_referer"\r\n'
                      f'/wp-admin/media-new.php\r\n'
                      f'--{WebKitFormBoundaryXXX}--\r\n')
                body = b''.join([p1.encode(), read_file, p2.encode()])
                request = (
                    f'POST /wp-admin/media-new.php/ HTTP/1.1\r\n'
                    f'Host: {HOST}\r\n'
                    f'Cache-Control: max-age=0\r\n'
                    f'Content-Length: {len(body)}\r\n'
                    f'Upgrade-Insecure-Requests: 1\r\n'
                    f'Content-Type: multipart/form-data; boundary={WebKitFormBoundaryXXX}\r\n'
                    f'User-Agent: User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0\r\n'
                    f'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*\r\n'
                    f'Accept-Encoding: gzip, deflate\r\n'
                    f'Accept-Language: en-US,en;q=0.9\r\n'
                    f'Cookie: {getCookie(listCookie)}\r\n'
                    f'Connection: close\r\n\r\n'
                )
                request = b''.join([request.encode(), body])
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
                    s2.connect((HOST, PORT))
                    s2.sendall(request)
                    buf = b''
                    chunk = s2.recv(1024)
                    while len(chunk) != 0:
                        buf += chunk
                        chunk = s2.recv(1024)
                    res = buf.decode()
                    # getCookieUpdate(listCookie, res)
                    # print(res)
                    if "Upload-Attachment-ID" in res:
                        anh_id = res.split("\r\n")[10].split(" ")[1]
                        webUrl  = urllib.request.urlopen(f'http://blogtest.vnprogramming.com/?attachment_id={anh_id}')
                        res = BeautifulSoup(webUrl.read(), "html.parser")
                        print(f"Upload success. File upload url: {res.img['src']}")        
        else:
            print(f"User {user} đăng nhập thất bại")
else:
    parser.print_help()