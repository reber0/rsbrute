/*
 * @Author: reber
 * @Mail: reber0ask@qq.com
 * @Date: 2023-10-08 10:54:38
 * @LastEditTime: 2024-02-05 13:42:19
 */
package plugins

import (
	"database/sql"
	"fmt"
	"log"

	_ "github.com/denisenkom/go-mssqldb"
	"github.com/reber0/goutils"
	"github.com/reber0/rsbrute/global"
	"github.com/remeh/sizedwaitgroup"
	"go.uber.org/ratelimit"
)

type MSSQLBrute struct {
	Name      string
	Limiter   ratelimit.Limiter
	WaitGroup sizedwaitgroup.SizedWaitGroup
	TempIP    []string // 检测未授权，测试过的 ip 加在这个里面
}

// New
func NewMSSQLBrute(rate int) *MSSQLBrute {
	return &MSSQLBrute{
		Name:      "MSSQLBrute",
		Limiter:   ratelimit.New(rate),
		WaitGroup: sizedwaitgroup.New(rate),
		TempIP:    make([]string, 0, 10000),
	}
}

// GetName
func (p *MSSQLBrute) GetName() string {
	return p.Name
}

// Run
func (p *MSSQLBrute) Run() {
	for _, payload := range global.Payloads {
		if !goutils.IsInCol(p.TempIP, payload.IP) {
			p.CheckUNauth(payload)
		}

		p.Limiter.Take()
		p.WaitGroup.Add()
		go p.Worker(payload)
	}
	p.WaitGroup.Wait()
}

func (p *MSSQLBrute) Worker(payload global.Payload) {
	defer p.WaitGroup.Done()

	dataSourceName := fmt.Sprintf("%s:%s@%s:%d?database=master&connection+timeout=10", payload.UserName, payload.PassWord, payload.IP, payload.Port)
	conn, err := sql.Open("mssql", dataSourceName)
	if err != nil {
		log.Fatalln("error:", err)
	} else {
		if err = conn.Ping(); err != nil {
			goutils.Green(fmt.Sprintf("[-] %s:%d %s %s", payload.IP, payload.Port, payload.UserName, payload.PassWord))
		} else {
			goutils.Red(fmt.Sprintf("[+] %s:%d %s %s", payload.IP, payload.Port, payload.UserName, payload.PassWord))
			global.Results = append(global.Results, payload)
		}
	}

	conn.Close()
}

func (p *MSSQLBrute) CheckUNauth(payload global.Payload) {
	p.TempIP = append(p.TempIP, payload.IP)

	for _, UserName := range []string{"sa", "test"} {
		dataSourceName := fmt.Sprintf("%s:%s@%s:%d?database=master&connection+timeout=10", UserName, "", payload.IP, payload.Port)
		conn, err := sql.Open("mssql", dataSourceName)
		if err != nil {
			log.Fatalln("error:", err)
		} else {
			if err = conn.Ping(); err != nil {
				goutils.Green(fmt.Sprintf("[-] %s:%d %s %s", payload.IP, payload.Port, payload.UserName, payload.PassWord))
			} else {
				goutils.Red(fmt.Sprintf("[+] %s:%d %s %s", payload.IP, payload.Port, payload.UserName, payload.PassWord))
				global.Results = append(global.Results, payload)
			}
		}

		conn.Close()
	}
}
