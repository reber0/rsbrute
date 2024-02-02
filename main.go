/*
 * @Author: reber
 * @Mail: reber0ask@qq.com
 * @Date: 2023-10-08 10:50:15
 * @LastEditTime: 2024-02-02 18:18:19
 */

package main

import (
	"embed"

	"github.com/reber0/rsbrute/entry"
	"github.com/reber0/rsbrute/global"
)

//go:embed dict/*
var dict embed.FS

func main() {
	// 设置 embed
	global.Dict = dict

	entry.AppInit()

	entry.Run()
}
