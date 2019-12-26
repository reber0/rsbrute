# RServiceBrute

### 安装模块
pip install -r requirements.txt

### 使用
```
usage: rsbrute.py [-h] [-i HOST] [-iL HOST_FILE] [-l USER] [-p PWD]
                  [-C USER_PWD_FILE] [-L USER_FILE] [-P PWD_FILE]
                  [--port PORT] -s
                  {ssh,ftp,mysql,mssql,oracle,pgsql,redis,mongodb,memcache,ldap,winrm}
                  [-t THREAD_NUM] [-T TIMEOUT]

optional arguments:
  -h, --help            show this help message and exit
  -i HOST               target ip
  -iL HOST_FILE         target file name, one ip per line
  -l USER               login with LOGIN username
  -p PWD                login with LOGIN password
  -C USER_PWD_FILE      colon separated "login:pass" format, instead of -L/-P
  -L USER_FILE          load several usernames from FILE
  -P PWD_FILE           load several passwords from FILE
  --port PORT           give the target port
  -s {ssh,ftp,mysql,mssql,oracle,pgsql,redis,mongodb,memcache,ldap,winrm}
                        the type of service to scan
  -t THREAD_NUM         the number of threads, default 10
  -T TIMEOUT            wait time per login attempt over all threads

Examples:
  python3 rsbrute.py -s ssh -i 59.108.35.123
  python3 rsbrute.py -s ssh -i 192.168.3.123 -l root -p 123456
  python3 rsbrute.py -s ssh -i 192.168.3.123 -l root -P pwd_dict.txt
```

### 引用
```
import sys
sys.path.append('/path/to/Rsbrute')

from Rsbrute import ComHostPortUserPwd
from Rsbrute import LoadModule

args = {"host":"59.108.35.198", "port":22, "service_type":"ssh", "user":"reber", "pwd_file":"a.txt"}
chpup = ComHostPortUserPwd(args)
hpup = chpup.generate()
# print(hpup)

lm = LoadModule(args)
result = lm.start_brute(hpup)
```
