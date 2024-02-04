/*
 * @Author: reber
 * @Mail: reber0ask@qq.com
 * @Date: 2023-10-08 10:54:29
 * @LastEditTime: 2024-02-04 16:19:29
 */
package plugins

import (
	"database/sql"
	"fmt"
	"log"

	_ "github.com/go-sql-driver/mysql"
	"github.com/reber0/goutils"
	"github.com/reber0/rsbrute/global"
	"github.com/remeh/sizedwaitgroup"
	"go.uber.org/ratelimit"
)

type MysqlBrute struct {
	Name      string
	Limiter   ratelimit.Limiter
	WaitGroup sizedwaitgroup.SizedWaitGroup
	UNauthIP  []string // 检测未授权，测试过的 ip 加在这个里面
}

// New
func NewMysqlBrute(rate int) *MysqlBrute {
	return &MysqlBrute{
		Name:      "MysqlBrute",
		Limiter:   ratelimit.New(rate),
		WaitGroup: sizedwaitgroup.New(rate),
	}
}

// GetName
func (p *MysqlBrute) GetName() string {
	return p.Name
}

// Run 全端口扫描插件
func (p *MysqlBrute) Run() {
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

func (p *MysqlBrute) Worker(payload global.Payload) {
	defer p.WaitGroup.Done()

	dataSourceName := fmt.Sprintf("%s:%s@tcp(%s:%d)/mysql", payload.UserName, payload.PassWord, payload.IP, payload.Port)
	db, err := sql.Open("mysql", dataSourceName)
	if err != nil {
		log.Fatalln("error:", err)
	} else {
		if err = db.Ping(); err != nil {
			goutils.Green(fmt.Sprintf("[-] %s:%d %s %s", payload.IP, payload.Port, payload.UserName, payload.PassWord))
		} else {
			goutils.Red(fmt.Sprintf("[+] %s:%d %s %s", payload.IP, payload.Port, payload.UserName, payload.PassWord))
			global.Results = append(global.Results, payload)
		}
	}

	db.Close()
}

func (p *MysqlBrute) CheckUNauth(payload global.Payload) {
	p.UNauthIP = append(p.UNauthIP, payload.IP)

	for _, UserName := range []string{"root", "test"} {
		dataSourceName := fmt.Sprintf("%s:%s@tcp(%s:%d)/mysql", UserName, "", payload.IP, payload.Port)
		db, err := sql.Open("mysql", dataSourceName)
		if err != nil {
			log.Fatalln("error:", err)
		} else {
			if err = db.Ping(); err != nil {
				goutils.Green(fmt.Sprintf("[-] %s:%d %s 空", payload.IP, payload.Port, UserName))
			} else {
				goutils.Red(fmt.Sprintf("[+] %s:%d %s 空", payload.IP, payload.Port, UserName))
				global.Results = append(
					global.Results,
					global.Payload{IP: payload.IP, Port: payload.Port, UserName: UserName, PassWord: "空"},
				)
			}
		}

		db.Close()
	}
}
