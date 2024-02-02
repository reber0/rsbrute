/*
 * @Author: reber
 * @Mail: reber0ask@qq.com
 * @Date: 2023-10-08 10:49:16
 * @LastEditTime: 2023-10-12 14:57:20
 */
package entry

import (
	"os"

	"github.com/reber0/goutils"
	"github.com/reber0/rsbrute/global"
	"github.com/reber0/rsbrute/plugins"
)

// AppInit 初始化
func AppInit() {
	global.RootPath, _ = os.Getwd()
	global.Log = goutils.NewLog().IsShowCaller(true).IsToFile(true).L()
	global.Option = &global.Opt{}

	// 解析参数
	ParseOptions()

	// 初始化插件
	global.Plugins = make(map[string]global.Plugin)
	global.Payloads = make([]global.Payload, 0, 10000)
	global.Results = make([]global.Payload, 0, 1000)

	plugins.InitPlugin()
}
