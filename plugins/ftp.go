/*
 * @Author: reber
 * @Mail: reber0ask@qq.com
 * @Date: 2023-10-08 10:54:24
 * @LastEditTime: 2024-02-04 15:02:40
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
	UNauthIP  []string // 检测未授权，测试过的 ip 加在这个里面
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
		if !goutils.IsInCol(p.UNauthIP, payload.IP) {
			p.CheckUNauth(payload)
		}

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
			goutils.Green(fmt.Sprintf("[-] %s %d %s %s", payload.IP, payload.Port, payload.UserName, payload.PassWord))
		} else {
			goutils.Red(fmt.Sprintf("[+] %s %d %s %s", payload.IP, payload.Port, payload.UserName, payload.PassWord))
		}
		conn.Quit()
	}
}

func (p *FtpBrute) CheckUNauth(payload global.Payload) {
	p.UNauthIP = append(p.UNauthIP, payload.IP)

	// 测试匿名登录
	conn, err := ftp.Dial(fmt.Sprintf("%s:%d", payload.IP, payload.Port))
	if err != nil {
		global.Log.Error(err.Error())
	} else {
		// 登录
		if err = conn.Login("anonymous", "anonymous"); err != nil {
			goutils.Green(fmt.Sprintf("[-] %s %d anonymous anonymous", payload.IP, payload.Port))
		} else {
			goutils.Red(fmt.Sprintf("[+] %s %d anonymous anonymous", payload.IP, payload.Port))
		}
		conn.Quit()
	}

	// 测试空密码
	for _, UserName := range []string{"root", "test", "ftp", "admin"} {
		// 拨号连接 FTP
		conn, err := ftp.Dial(fmt.Sprintf("%s:%d", payload.IP, payload.Port))
		if err != nil {
			global.Log.Error(err.Error())
		} else {
			// 登录
			if err = conn.Login(UserName, ""); err != nil {
				goutils.Green(fmt.Sprintf("[-] %s %d %s 空", payload.IP, payload.Port, UserName))
			} else {
				goutils.Red(fmt.Sprintf("[+] %s %d %s 空", payload.IP, payload.Port, UserName))
			}
			conn.Quit()
		}
	}
}
