/*
 * @Author: reber
 * @Mail: reber0ask@qq.com
 * @Date: 2023-10-08 10:55:08
 * @LastEditTime: 2024-02-05 16:13:23
 */
package plugins

import (
	"database/sql"
	"fmt"
	"log"
	"net/url"

	_ "github.com/lib/pq"
	"github.com/reber0/goutils"
	"github.com/reber0/rsbrute/global"
	"github.com/remeh/sizedwaitgroup"
	"go.uber.org/ratelimit"
)

type PgSQLBrute struct {
	Name      string
	Limiter   ratelimit.Limiter
	WaitGroup sizedwaitgroup.SizedWaitGroup
	TempIP    []string // 检测未授权，测试过的 ip 加在这个里面
}

// New
func NewPgSQLBrute(rate int) *PgSQLBrute {
	return &PgSQLBrute{
		Name:      "PgSQLBrute",
		Limiter:   ratelimit.New(rate),
		WaitGroup: sizedwaitgroup.New(rate),
		TempIP:    make([]string, 0, 10000),
	}
}

// GetName
func (p *PgSQLBrute) GetName() string {
	return p.Name
}

// Run
func (p *PgSQLBrute) Run() {
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

func (p *PgSQLBrute) Worker(payload global.Payload) {
	defer p.WaitGroup.Done()

	connStr := fmt.Sprintf("postgres://%s:%s@%s:%d/postgres?sslmode=disable", payload.UserName, url.QueryEscape(payload.PassWord), payload.IP, payload.Port)
	db, err := sql.Open("postgres", connStr)
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

func (p *PgSQLBrute) CheckUNauth(payload global.Payload) {
	p.TempIP = append(p.TempIP, payload.IP)

	for _, UserName := range []string{"postgres", "test"} {
		connStr := fmt.Sprintf("postgres://%s:%s@%s:%d/postgres?sslmode=disable", UserName, "", payload.IP, payload.Port)
		db, err := sql.Open("postgres", connStr)
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
