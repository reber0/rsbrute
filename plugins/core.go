/*
 * @Author: reber
 * @Mail: reber0ask@qq.com
 * @Date: 2023-10-12 11:20:39
 * @LastEditTime: 2024-02-02 17:13:15
 */

package plugins

import (
	"github.com/reber0/rsbrute/global"
)

// 插件初始化
func InitPlugin() {
	registerPlugin("ftp", NewFtpBrute(global.Option.Rate))
	registerPlugin("mysql", NewMysqlBrute(global.Option.Rate))
	registerPlugin("redis", NewRedisBrute(global.Option.Rate))
	registerPlugin("mongodb", NewMongoDBBrute(global.Option.Rate))
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
