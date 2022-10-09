import socket
from bs4 import BeautifulSoup
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--url", dest="host", help="url")
args = parser.parse_args()

if args.host:
    HOST = args.host
    PORT = 80
    PATH = "/"
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        link = (f"GET {PATH} HTTP/1.1\r\n" +
                f"Host: {HOST}\r\n" + f"Connection: close\r\n\r\n")
        link = link.encode()
        s.sendall(link)
        buf = b''
        chunk = s.recv(1024)
        while len(chunk) != 0:
            buf += chunk
            chunk = s.recv(1024)
    res = buf.decode()
    res = BeautifulSoup(res, "html.parser")
    print(f"Title: {res.title.string.split()[0]}")
else:
    parser.print_help()
# blogtest.vnprogramming.com
