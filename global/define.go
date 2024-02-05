/*
 * @Author: reber
 * @Mail: reber0ask@qq.com
 * @Date: 2022-01-05 11:23:54
 * @LastEditTime: 2024-02-02 17:35:35
 */
package global

import (
	"embed"

	"go.uber.org/zap"
)

// Opt 参数
type Opt struct {
	Help        bool
	Version     string
	ShowVersion bool

	IP         string
	TargetFile string
	Port       int

	User        string
	Pwd         string
	UserFile    string
	PwdFile     string
	UserPwdFile string

	ServiceType string
	Rate        int
	TimeOut     int
}

type Plugin interface {
	GetName() string
	Run()
}

type Payload struct {
	IP       string
	Port     int
	UserName string
	PassWord string
	Note     string
}

var (
	RootPath string
	Log      *zap.Logger
	Option   *Opt

	Plugins  map[string]Plugin
	Payloads []Payload
	Results  []Payload

	// 打包到二进制的静态文件
	Dict embed.FS
)
