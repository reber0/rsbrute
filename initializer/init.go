/*
 * @Author: reber
 * @Mail: reber0ask@qq.com
 * @Date: 2023-10-08 10:49:16
 * @LastEditTime: 2024-02-04 16:15:22
 */
package initializer

import (
	"os"
	"path/filepath"

	"github.com/reber0/goutils"
	"github.com/reber0/rsbrute/core"
	"github.com/reber0/rsbrute/global"
)

// AppInit 初始化
func AppInit() {
	global.RootPath, _ = os.Getwd()

	// data/log 目录
	logDir := filepath.Join(global.RootPath, "data", "log")
	os.MkdirAll(logDir, 0755)

	global.Log = goutils.NewLog().
		SetInfoFile(filepath.Join(logDir, "info.log")).
		SetErrorFile(filepath.Join(logDir, "error.log")).
		IsShowCaller(true).
		IsToFile(true).
		L()
	global.Option = &global.Opt{}

	// 解析参数
	ParseOptions()

	// 初始化插件
	global.Plugins = make(map[string]global.Plugin)
	global.Payloads = make([]global.Payload, 0, 10000)
	global.Results = make([]global.Payload, 0, 1000)

	core.InitPlugin()
}
