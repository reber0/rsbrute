# RServiceBrute

多协议弱口令爆破工具（Go CLI），支持 SSH、FTP、Telnet、MySQL、MSSQL、Oracle、PostgreSQL、Redis、MongoDB、MemCache、LDAP、WinRM、VNC、RDP、SMB、SNMP、SMTP、POP、Tomcat 等服务的批量弱口令检测。

内置常用用户名 / 密码字典（通过 `go:embed` 打包到二进制，无需额外文件）。

## 编译

```bash
# rsbrute 不在 go.work 中，编译需加 GOWORK=off
GOWORK=off go build -o rsbrute .
```

## 用法

```bash
./rsbrute -h
```

输出示例：

```
Usage: ./rsbrute [-h] [-i ip] [-port port] [-l username] [-p password]
        [-s ServiceType] [-r Rate] [-t TimeOut]
Options:
  -C string        用户名密码文件
  -L string        用户名文件
  -P string        密码文件
  -V               版本信息
  -h               帮助信息
  -i string        目标 IP
  -iL string       目标 IP 文件
  -l string        用户名
  -p string        密码
  -port int        目标端口
  -r int           频率（默认 10）
  -s string        爆破的服务类型
  -t int           超时（默认 10）
```

### 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `-i` | 目标 IP（与 `-iL` 二选一，必填） | — |
| `-iL` | 目标 IP 文件，每行一个 IP（与 `-i` 二选一，必填） | — |
| `-s` | 服务类型（必填），可选值见下表 | — |
| `-port` | 目标端口，不指定时按服务类型取默认端口 | 服务默认端口 |
| `-l` | 单个用户名 | — |
| `-p` | 单个密码 | — |
| `-L` | 用户名文件 | — |
| `-P` | 密码文件 | — |
| `-C` | 用户名密码文件（`username:password` 格式） | — |
| `-r` | 并发频率（每秒请求数） | 10 |
| `-t` | 连接超时（秒） | 10 |
| `-h` | 帮助信息 | — |
| `-V` | 版本信息 | — |

### 支持的服务类型

| 分组 | 服务 |
|------|------|
| 远程登录 | ssh, ftp, telnet, rlogin |
| 数据库 | mysql, mssql, oracle, pgsql, redis, mongodb, memcache |
| 目录/管理 | ldap, winrm, vnc, rdp, smb, snmp |
| 邮件 | smtp, pop |
| Web | tomcat |

### 服务默认端口

| 服务 | 端口 | 服务 | 端口 |
|------|------|------|------|
| ssh | 22 | mysql | 3306 |
| ftp | 21 | mssql | 1433 |
| telnet | 23 | oracle | 1521 |
| rlogin | 513 | pgsql | 5432 |
| redis | 6379 | mongodb | 27017 |
| memcache | 11211 | ldap | 389 |
| winrm | 5985 | vnc | 5901 |
| rdp | 3389 | smb | 445 |
| snmp | 161 | smtp | 25 |
| pop | 110 | tomcat | 443 |

## 运行示例

```bash
# 编译
GOWORK=off go build -o rsbrute .

# 爆破单个 SSH
./rsbrute -i 192.168.1.10 -s ssh -l root -P passwords.txt

# 爆破多个 IP 的 Redis
./rsbrute -iL targets.txt -s redis

# 指定端口和并发频率
./rsbrute -i 192.168.1.10 -port 2222 -s ssh -l root -p 123456 -r 20 -t 5
```

## 运行目录

程序启动时会在当前工作目录下创建 `data/log/` 目录，日志写入：

- `data/log/info.log` — 普通日志
- `data/log/error.log` — 错误日志
