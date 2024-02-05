/*
 * @Author: reber
 * @Mail: reber0ask@qq.com
 * @Date: 2023-10-12 14:50:24
 * @LastEditTime: 2024-02-05 15:46:46
 */
package core

import (
	"fmt"

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

// 插件初始化
func InitPlugin() {
	registerPlugin("ftp", plugins.NewFtpBrute(global.Option.Rate))
	registerPlugin("mysql", plugins.NewMysqlBrute(global.Option.Rate))
	registerPlugin("redis", plugins.NewRedisBrute(global.Option.Rate))
	registerPlugin("mongodb", plugins.NewMongoDBBrute(global.Option.Rate))
	registerPlugin("ssh", plugins.NewSSHBrute(global.Option.Rate))
	registerPlugin("oracle", plugins.NewOracleBrute(global.Option.Rate))
	registerPlugin("pgsql", plugins.NewPgSQLBrute(global.Option.Rate))
}

// 插件注册
func registerPlugin(pluginID string, plg global.Plugin) {
	global.Plugins[pluginID] = plg
}

// 插件执行
func ExecPlugin(pluginID string) {
	if len(global.Payloads) > 0 {
		plugin, ok := global.Plugins[pluginID]
		if !ok {
			global.Log.Error("插件未注册: " + plugin.GetName())
			return
		}

		global.Log.Info("执行插件: " + plugin.GetName())
		plugin.Run()
	}
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
	ExecPlugin(global.Option.ServiceType)

	// 输出结果
	goutils.Red("结果：")
	for _, result := range global.Results {
		res, _ := goutils.Go2JsonStr(result)
		fmt.Println(res)
	}
}
