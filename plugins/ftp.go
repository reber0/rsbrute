/*
 * @Author: reber
 * @Mail: reber0ask@qq.com
 * @Date: 2023-10-08 10:54:24
 * @LastEditTime: 2023-10-12 18:02:31
 */
package plugins

import (
	"fmt"

	"github.com/jlaffaye/ftp"
	"github.com/reber0/goutils"
	"github.com/reber0/rsbrute/global"
	"github.com/remeh/sizedwaitgroup"
	"go.uber.org/ratelimit"
)

type FtpBrute struct {
	Name      string
	Limiter   ratelimit.Limiter
	WaitGroup sizedwaitgroup.SizedWaitGroup
}

// New
func NewFtpBrute(rate int) *FtpBrute {
	return &FtpBrute{
		Name:      "FtpBrute",
		Limiter:   ratelimit.New(rate),
		WaitGroup: sizedwaitgroup.New(rate),
	}
}

// GetName
func (p *FtpBrute) GetName() string {
	return p.Name
}

// Run 全端口扫描插件
func (p *FtpBrute) Run() {
	for _, payload := range global.Payloads {
		p.Limiter.Take()
		p.WaitGroup.Add()
		go p.Worker(payload)
	}
	p.WaitGroup.Wait()
}

func (p *FtpBrute) Worker(payload global.Payload) {
	defer p.WaitGroup.Done()

	// 拨号连接 FTP
	conn, err := ftp.Dial(fmt.Sprintf("%s:%d", payload.IP, payload.Port))
	if err != nil {
		global.Log.Error(err.Error())
	} else {
		// 登录
		if err = conn.Login(payload.UserName, payload.PassWord); err != nil {
			goutils.Green(fmt.Sprintf("[-] %s %d %s %s %s", payload.IP, payload.Port, payload.UserName, payload.PassWord, err.Error()))
		} else {
			goutils.Red(fmt.Sprintf("[+] %s %d %s %s", payload.IP, payload.Port, payload.UserName, payload.PassWord))
		}
	}

	conn.Quit()
}
