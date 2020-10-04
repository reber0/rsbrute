# RServiceBrute

[![platform](https://img.shields.io/static/v1?label=platform&message=macOS&color=172b43)](https://github.com/reber0/Rpscan/tree/master)
[![python](https://img.shields.io/static/v1?label=python&message=3.7&color=346fb0)](https://www.python.org/)
[![Oracle Instant Client](https://img.shields.io/static/v1?label=Oracle%20Instant%20Client&message=11.2&color=e35949)](https://www.oracle.com/database/technologies/instant-client/downloads.html)

### 功能

* 解析给定参数

* 生成字典列表

  * 指明字典则加载给定的字典，否则加载默认字典

  * 生成的字典形如 [(ip,port,user,pwd), (ip,port,user,pwd)]

* 加载爆破服务的对应模块

* 多线程爆破

### 安装必要模块

* pip install -r requirements.txt

* 设置 oracle(爆破 oracle 的话需要进行下面的设置)

  * pip3 install cx_Oracle

    出现下面的错误可以安装 xcode 解决：xcode-select --install

    ```
    xcrun: error: invalid active developer path (/Library/Developer/CommandLineTools), missing xcrun at: /Library/Developer/CommandLineTools/usr/bin/xcrun
        error: command 'clang' failed with exit status 1
    ```

  * 设置 oracle 客户端

    * 下载 Oracle Instant Client

      去 [这里](https://www.oracle.com/database/technologies/instant-client/downloads.html) 根据你自己的系统下载相应的 Oracle Instant Client，我下载的是 [instantclient-basiclite-macos.x64-11.2.0.4.0.zip](https://download.oracle.com/otn/mac/instantclient/11204/instantclient-basiclite-macos.x64-11.2.0.4.0.zip) 

    * 解压 Oracle Instant Client

      ```
      unzip x instantclient-basiclite-macos.x64-11.2.0.4.0.zip
      sudo mkdir /opt/oracle && sudo mv instantclient_11_2 /opt/oracle
      cd /opt/oracle/instantclient_11_2
      ln -s libclntsh.dylib.11.1 libclntsh.dylib
      ln -s libocci.dylib.11.1 libocci.dylib
      ```

    * 配置 Oracle Instant Client，我用的 zsh，修改的 ～/.zshrc

      ```
      export ORACLE_HOME="/opt/oracle/instantclient_11_2"
      export DYLD_LIBRARY_PATH=$ORACLE_HOME
      export LD_LIBRARY_PATH=$ORACLE_HOME
      ```

### 使用

```
➜  python3 rsbrute.py -h
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

### 使用
```
➜  python3 rsbrute.py -s ssh -i 10.11.11.11 -l reber -P ~/pwd.txt -t 1
[22:26:49] Start brute ssh ... 
[22:26:51] [-] 10.11.11.11 22 reber admin 
[22:26:52] [-] 10.11.11.11 22 reber root 
[22:26:52] [*] 10.11.11.11 22 reber 123456 
[22:27:04] [-] 10.11.11.11 22 reber test 
[22:27:16] [-] 10.11.11.11 22 reber ftp 
[22:27:18] [-] 10.11.11.11 22 reber mysql 
[('10.11.11.11', 22, 'reber', '123456')]
```
