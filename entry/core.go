/*
 * @Author: reber
 * @Mail: reber0ask@qq.com
 * @Date: 2023-10-12 14:50:24
 * @LastEditTime: 2024-02-02 18:19:50
 */
package entry

import (
	"bytes"
	"fmt"
	"strconv"
	"strings"

	"github.com/reber0/goutils"
	"github.com/reber0/rsbrute/global"
	"github.com/reber0/rsbrute/plugins"
)

type IPPort struct {
	IP   string
	Port int
}

type UserPwd struct {
	UserName string
	PassWord string
}

func Run() {
	// 合成测试 data
	IPPortList := ComIPPort()
	UserPwdList := ComUserPwd()
	for _, IPPort := range IPPortList {
		for _, UserPwd := range UserPwdList {
			global.Payloads = append(global.Payloads, global.Payload{
				IP:       IPPort.IP,
				Port:     IPPort.Port,
				UserName: UserPwd.UserName,
				PassWord: UserPwd.PassWord,
			})
		}
	}

	// 调用插件
	plugins.ExecPlugin(global.Option.ServiceType)

	// 输出结果
	goutils.Red("结果：")
	for _, result := range global.Results {
		fmt.Printf("%s:%d %s %s\n", result.IP, result.Port, result.UserName, result.PassWord)
	}
}

// 合成 ip、port
func ComIPPort() []IPPort {
	var port int
	var ipList []string
	var IPPortList []IPPort

	if global.Option.Port != 0 {
		port = global.Option.Port
	} else {
		port = global.ServicePortDict[global.Option.ServiceType]
	}

	if global.Option.IP != "" {
		ipList = goutils.ParseIP(global.Option.IP)
	}
	if global.Option.TargetFile != "" {
		targetList := goutils.FileEachLineRead(global.Option.TargetFile)
		for _, target := range targetList {
			ipList = append(ipList, goutils.ParseIP(target)...)
		}
	}

	for _, ip := range ipList {
		if goutils.IsPortOpenSyn(ip, strconv.Itoa(port)) {
			IPPortList = append(IPPortList, IPPort{IP: ip, Port: port})
		} else {
			global.Log.Error(fmt.Sprintf("%s:%d port is not open", ip, port))
		}
	}

	return IPPortList
}

// 合成 user、pwd
func ComUserPwd() []UserPwd {
	var UserPwdList []UserPwd

	switch {
	case global.Option.User != "" && global.Option.Pwd != "":
		UserPwdList = append(UserPwdList, UserPwd{UserName: global.Option.User, PassWord: global.Option.Pwd})
	case global.Option.User != "" && global.Option.PwdFile != "":
		{
			pwdList := goutils.FileEachLineRead(global.Option.PwdFile)
			for _, pwd := range pwdList {
				pwd = strings.ReplaceAll(pwd, "<user>", global.Option.User)
				pwd = strings.ReplaceAll(pwd, "<null>", "")
				UserPwdList = append(UserPwdList, UserPwd{UserName: global.Option.User, PassWord: pwd})
			}
		}
	case global.Option.UserFile != "" && global.Option.Pwd != "":
		{
			userList := goutils.FileEachLineRead(global.Option.UserFile)
			for _, user := range userList {
				UserPwdList = append(UserPwdList, UserPwd{UserName: user, PassWord: global.Option.Pwd})
			}
		}
	case global.Option.UserFile != "" && global.Option.PwdFile != "":
		{
			userList := goutils.FileEachLineRead(global.Option.UserFile)
			pwdList := goutils.FileEachLineRead(global.Option.PwdFile)
			for _, user := range userList {
				for _, pwd := range pwdList {
					pwd = strings.ReplaceAll(pwd, "<user>", user)
					pwd = strings.ReplaceAll(pwd, "<null>", "")
					UserPwdList = append(UserPwdList, UserPwd{UserName: user, PassWord: pwd})
				}
			}
		}
	default:
		{
			var userList []string
			var pwdList []string

			dataUser, err := global.Dict.ReadFile("dict/" + global.Option.ServiceType + "_user.txt")
			if err != nil {
				global.Log.Error(err.Error())
			}
			dataUser = bytes.ReplaceAll(dataUser, []byte("\r\n"), []byte("\n"))
			for _, line := range bytes.Split(dataUser, []byte("\n")) {
				userList = append(userList, string(line))
			}

			dataPwd, err := global.Dict.ReadFile("dict/" + global.Option.ServiceType + "_pwd.txt")
			if err != nil {
				global.Log.Error(err.Error())
			}
			dataPwd = bytes.ReplaceAll(dataPwd, []byte("\r\n"), []byte("\n"))
			for _, line := range bytes.Split(dataPwd, []byte("\n")) {
				pwdList = append(pwdList, string(line))
			}

			for _, user := range userList {
				for _, pwd := range pwdList {
					pwd = strings.ReplaceAll(pwd, "<user>", user)
					pwd = strings.ReplaceAll(pwd, "<null>", "")
					UserPwdList = append(UserPwdList, UserPwd{UserName: user, PassWord: pwd})
				}
			}
		}
	}

	// 对 UserPwdList 去重
	seen := make(map[string]struct{})
	var unique []UserPwd
	for i := range UserPwdList {
		key := fmt.Sprintf("%s-%s", UserPwdList[i].UserName, UserPwdList[i].PassWord)
		if _, ok := seen[key]; ok {
			continue
		}
		seen[key] = struct{}{}
		unique = append(unique, UserPwdList[i])
	}

	return unique
}
