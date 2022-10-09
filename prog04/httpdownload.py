import socket
import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--url", dest='host', help="URL")
parser.add_argument("--remote-file", dest='download', help="path file")
args = parser.parse_args()

HOST = args.host
PORT = 80
remote_file = args.download

if HOST and remote_file:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST,PORT))
    header =  ( f'GET /{remote_file} HTTP/1.1\r\n'
                f'Host: {HOST}\r\n'
                f'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0\r\n'
                f'Accept: */*\r\n'
                f'Accept-Language: en-US,en;q=0.5\r\n'
                f'Accept-Encoding: gzip, deflate\r\n\r\n'
    )

    s.send(header.encode())
    total_data=[]
    data = s.recv(8192)
    while (len(data) > 0):
        total_data.append(data)
        data = s.recv(8192)
    data = b''.join(total_data)

    if b"HTTP/1.1 200 OK" in data:
        size = re.findall(b"Content-Length: ([0-9]+)\r\n", data)[0].decode()
        print("Kích thước file: " + size + " bytes")

        reply = b''
        headers =  reply.split(b'\r\n\r\n')[0]
        image = reply[len(headers)+4:]
        file_name = remote_file.split("/")[-1]
        f = open(f"anh/{file_name}", "wb")
        f.write(image)
        f.close()
    else:
        print("Không tồn tại file ảnh.")
        exit()
else:
    parser.print_help()