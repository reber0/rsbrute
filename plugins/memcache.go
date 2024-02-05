/*
 * @Author: reber
 * @Mail: reber0ask@qq.com
 * @Date: 2023-10-08 10:57:23
 * @LastEditTime: 2024-02-05 18:00:48
 */
package plugins

import (
	"fmt"
	"net"
	"strings"
	"time"

	"github.com/reber0/goutils"
	"github.com/reber0/rsbrute/global"
	"github.com/remeh/sizedwaitgroup"
	"go.uber.org/ratelimit"
)

type MemCacheBrute struct {
	Name      string
	Limiter   ratelimit.Limiter
	WaitGroup sizedwaitgroup.SizedWaitGroup
	TempIP    []string // 检测未授权，测试过的 ip 加在这个里面
}

// New
func NewMemCacheBruteBrute(rate int) *MemCacheBrute {
	return &MemCacheBrute{
		Name:      "MemCacheBrute",
		Limiter:   ratelimit.New(rate),
		WaitGroup: sizedwaitgroup.New(rate),
		TempIP:    make([]string, 0, 10000),
	}
}

// GetName
func (p *MemCacheBrute) GetName() string {
	return p.Name
}

// Run
func (p *MemCacheBrute) Run() {
	goutils.Red("只测试未授权，密码爆破待开发")
	for _, payload := range global.Payloads {
		if !goutils.IsInCol(p.TempIP, payload.IP) {
			p.CheckUNauth(payload)
			break
		}

		p.Limiter.Take()
		p.WaitGroup.Add()
		go p.Worker(payload)
	}
	p.WaitGroup.Wait()
}

func (p *MemCacheBrute) Worker(payload global.Payload) {
	defer p.WaitGroup.Done()

	// 连接到服务器
}

func (p *MemCacheBrute) CheckUNauth(payload global.Payload) {
	p.TempIP = append(p.TempIP, payload.IP)

	// 连接到服务器
	connStr := fmt.Sprintf("%s:%d", payload.IP, payload.Port)
	conn, err := net.Dial("tcp", connStr)
	if err != nil {
		fmt.Println("连接失败:", err)
		return
	}
	defer conn.Close()

	conn.SetReadDeadline(time.Now().Add(time.Second * 5))
	fmt.Fprintf(conn, "stats\r\n")

	// 读取服务器的响应并打印
	buffer := make([]byte, 1024)
	n, err := conn.Read(buffer)
	if err != nil {
		goutils.Green(fmt.Sprintf("[-] %s:%d 空 空", payload.IP, payload.Port))
	} else {
		response := string(buffer[:n])
		if strings.Contains(response, "STAT") {
			goutils.Red(fmt.Sprintf("[+] %s:%d 空 空", payload.IP, payload.Port))
			global.Results = append(
				global.Results,
				global.Payload{IP: payload.IP, Port: payload.Port, UserName: "空", PassWord: "空"},
			)
		} else {
			goutils.Green(fmt.Sprintf("[-] %s:%d 空 空", payload.IP, payload.Port))
		}
	}

	conn.Close()
}
