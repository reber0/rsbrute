/*
 * @Author: reber
 * @Mail: reber0ask@qq.com
 * @Date: 2023-10-08 10:59:15
 * @LastEditTime: 2024-02-04 17:13:09
 */
package plugins

import (
	"fmt"
	"strings"
	"time"

	"github.com/reber0/goutils"
	"github.com/reber0/rsbrute/global"
	"github.com/remeh/sizedwaitgroup"
	"go.uber.org/ratelimit"
	"golang.org/x/crypto/ssh"
)

type SSHBrute struct {
	Name      string
	Limiter   ratelimit.Limiter
	WaitGroup sizedwaitgroup.SizedWaitGroup
}

// New
func NewSSHBrute(rate int) *SSHBrute {
	return &SSHBrute{
		Name:      "SSHBrute",
		Limiter:   ratelimit.New(rate),
		WaitGroup: sizedwaitgroup.New(rate),
	}
}

// GetName
func (p *SSHBrute) GetName() string {
	return p.Name
}

// Run 全端口扫描插件
func (p *SSHBrute) Run() {
	for _, payload := range global.Payloads {
		p.Limiter.Take()
		p.WaitGroup.Add()
		go p.Worker(payload)
	}
	p.WaitGroup.Wait()
}

func (p *SSHBrute) Worker(payload global.Payload) {
	defer p.WaitGroup.Done()

	config := &ssh.ClientConfig{
		User:            payload.UserName,
		Auth:            []ssh.AuthMethod{ssh.Password(payload.PassWord)},
		HostKeyCallback: ssh.InsecureIgnoreHostKey(), // 忽略主机密钥
		Timeout:         10 * time.Second,
	}
	addr := fmt.Sprintf("%s:%d", payload.IP, payload.Port)

	// 作为客户端连接 SSH 服务器
	client, err := ssh.Dial("tcp", addr, config)
	if err != nil {
		if strings.Contains(err.Error(), "connection reset by peer") { // 重试一次
			// 作为客户端连接 SSH 服务器
			client1, err := ssh.Dial("tcp", addr, config)
			if err != nil {
				goutils.Green(fmt.Sprintf("[-] %s:%d %s %s", payload.IP, payload.Port, payload.UserName, payload.PassWord))
			} else {
				goutils.Red(fmt.Sprintf("[+] %s:%d %s %s", payload.IP, payload.Port, payload.UserName, payload.PassWord))
				global.Results = append(global.Results, payload)

				client1.Close()
			}
		} else {
			goutils.Green(fmt.Sprintf("[-] %s:%d %s %s", payload.IP, payload.Port, payload.UserName, payload.PassWord))
		}
	} else {
		goutils.Red(fmt.Sprintf("[+] %s:%d %s %s", payload.IP, payload.Port, payload.UserName, payload.PassWord))
		global.Results = append(global.Results, payload)

		client.Close()
	}
}
