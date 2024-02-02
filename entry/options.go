/*
 * @Author: reber
 * @Mail: reber0ask@qq.com
 * @Date: 2023-10-09 13:27:53
 * @LastEditTime: 2023-11-17 13:26:26
 */
// Package
// Author: reber
// Mail: reber0ask@qq.com
// Date: 2023-06-09 15:41:38
// LastEditTime: 2023-06-13 10:06:22

package entry

import (
	"flag"
	"fmt"
	"os"
	"strings"

	"github.com/reber0/goutils"
	"github.com/reber0/rsbrute/global"
)

// ParseOptions 解析命令行参数，得到所有参数信息
func ParseOptions() {
	global.Option.Version = "0.01"

	flag.Usage = usage // 改变默认的 Usage
	flag.BoolVar(&global.Option.Help, "h", false, "帮助信息")
	flag.BoolVar(&global.Option.ShowVersion, "V", false, "版本信息")
	flag.StringVar(&global.Option.IP, "i", "", "目标 IP")
	flag.StringVar(&global.Option.TargetFile, "iL", "", "目标 IP 文件")
	flag.IntVar(&global.Option.Port, "port", 0, "目标端口")
	flag.StringVar(&global.Option.User, "l", "", "用户名")
	flag.StringVar(&global.Option.Pwd, "p", "", "密码")
	flag.StringVar(&global.Option.UserFile, "L", "", "用户名文件")
	flag.StringVar(&global.Option.PwdFile, "P", "", "密码文件")
	flag.StringVar(&global.Option.UserPwdFile, "C", "", "用户名密码文件")
	flag.StringVar(&global.Option.ServiceType, "s", "", "爆破的服务类型")
	flag.IntVar(&global.Option.Rate, "r", 10, "频率")
	flag.IntVar(&global.Option.TimeOut, "t", 10, "超时")

	flag.Parse() // 通过调用 flag.Parse() 来对命令行参数进行解析

	checkOption()
}

func usage() {
	fmt.Printf(`Usage: %s [-h] [-i ip] [-port port] [-l username] [-p password]
	[-s ServiceType] [-r Rate] [-t TimeOut]`, os.Args[0])
	fmt.Println()
	fmt.Println("Options:")
	flag.PrintDefaults() // 调用 PrintDefaults 打印前面定义的参数列表。
}

func checkOption() {
	if global.Option.ShowVersion {
		fmt.Printf("Version %s\n", global.Option.Version)
		os.Exit(0)
	}
	if global.Option.Help {
		flag.Usage()
		os.Exit(0)
	}

	if !(global.Option.IP != "" || global.Option.TargetFile != "") {
		goutils.Red("The arguments -i or -iL is required, please provide !")
		flag.Usage()
		os.Exit(0)
	}
	ServiceTypes := []string{
		"ssh", "ftp", "telnet", "rlogin",
		"mysql", "mssql", "oracle", "pgsql", "redis", "mongodb", "memcache",
		"ldap", "winrm", "vnc", "rdp", "smb", "snmp",
		"smtp", "pop",
		"tomcat",
	}
	if strings.Compare(global.Option.ServiceType, "") == 0 {
		goutils.Red("The arguments -s is required, please provide !")
		os.Exit(0)
	}
	if !goutils.IsInCol(ServiceTypes, global.Option.ServiceType) {
		goutils.Red("服务类型只能为：")
		goutils.Red("  [ssh, ftp, telnet, rlogin]")
		goutils.Red("  [mysql, mssql, oracle, pgsql, redis, mongodb, memcache]")
		goutils.Red("  [ldap, winrm, vnc, rdp, smb, snmp]")
		goutils.Red("  [smtp, pop]")
		goutils.Red("  [tomcat]")
		os.Exit(0)
	}
	if global.Option.Port == 0 {
		global.Option.Port = global.ServicePortDict[global.Option.ServiceType]
	}
}
