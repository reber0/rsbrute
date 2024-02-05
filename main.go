/*
 * @Author: reber
 * @Mail: reber0ask@qq.com
 * @Date: 2023-10-08 10:50:15
 * @LastEditTime: 2024-02-05 17:55:56
 */

package main

import (
	"embed"

	"github.com/reber0/rsbrute/core"
	"github.com/reber0/rsbrute/entry"
	"github.com/reber0/rsbrute/global"
)

//go:embed dict/*
var dict embed.FS

func main() {
	// 设置 embed
	global.Dict = dict

	entry.AppInit()

	core.Run()
}
