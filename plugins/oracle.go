/*
 * @Author: reber
 * @Mail: reber0ask@qq.com
 * @Date: 2023-10-08 10:54:43
 * @LastEditTime: 2024-02-05 15:30:33
 */
package plugins

import (
	"database/sql"
	"fmt"
	"log"
	"strings"

	"github.com/reber0/goutils"
	"github.com/reber0/rsbrute/global"
	"github.com/remeh/sizedwaitgroup"
	go_ora "github.com/sijms/go-ora/v2"
	"go.uber.org/ratelimit"
)

type OracleBrute struct {
	Name      string
	Limiter   ratelimit.Limiter
	WaitGroup sizedwaitgroup.SizedWaitGroup
	TempIP    []string            // 检测未授权，测试过的 ip 加在这个里面
	SidList   map[string][]string // 用于存储 sid
}

// New
func NewOracleBrute(rate int) *OracleBrute {
	return &OracleBrute{
		Name:      "OracleBrute",
		Limiter:   ratelimit.New(rate),
		WaitGroup: sizedwaitgroup.New(rate),
		TempIP:    make([]string, 0, 10000),
		SidList:   make(map[string][]string),
	}
}

// GetName
func (p *OracleBrute) GetName() string {
	return p.Name
}

// Run
func (p *OracleBrute) Run() {
	for _, payload := range global.Payloads {
		if !goutils.IsInCol(p.SidList, payload.IP) {
			p.GuessSid(payload)
			if len(p.SidList[payload.IP]) == 0 {
				goutils.Green(fmt.Sprintf("[-] %s:%d 未猜测到 sid，无法爆破", payload.IP, payload.Port))
			}
		}
		// 如果没有猜到 sid，跳过扫描，因为连接 oracle 必须提供 sid
		if len(p.SidList[payload.IP]) == 0 {
			continue
		} else {
			if !goutils.IsInCol(p.TempIP, payload.IP) {
				p.CheckUNauth(payload)
			}

			p.Limiter.Take()
			p.WaitGroup.Add()
			go p.Worker(payload)
		}
	}
	p.WaitGroup.Wait()
}

func (p *OracleBrute) Worker(payload global.Payload) {
	defer p.WaitGroup.Done()

	for _, sid := range p.SidList[payload.IP] {
		urlOptions := map[string]string{"SID": sid}
		connStr := go_ora.BuildUrl(payload.IP, payload.Port, "", payload.UserName, payload.PassWord, urlOptions)
		db, err := sql.Open("oracle", connStr)
		if err != nil {
			log.Fatalln("error:", err)
		} else {
			if err = db.Ping(); err != nil {
				fmt.Println(err)
				goutils.Green(fmt.Sprintf("[-] %s:%d/%s %s %s", payload.IP, payload.Port, sid, payload.UserName, payload.PassWord))
			} else {
				goutils.Red(fmt.Sprintf("[+] %s:%d/%s %s %s", payload.IP, payload.Port, sid, payload.UserName, payload.PassWord))
				payload.Note = "sid: " + sid
				global.Results = append(global.Results, payload)
			}
		}
		db.Close()
	}
}

func (p *OracleBrute) GuessSid(payload global.Payload) {
	var _sid []string

	sidSlice := []string{
		"XE", "ORCL", "TEST", "TEST10G", "DEMO", "DEV", "PRD", "PROD",
		"DBA", "MYDB", "ORA", "ORACLE", "SALES", "SAMPLE", "SAP",
	}
	for _, sid := range sidSlice {
		urlOptions := map[string]string{"SID": sid}
		connStr := go_ora.BuildUrl(payload.IP, payload.Port, "", payload.UserName, payload.PassWord, urlOptions)
		db, err := sql.Open("oracle", connStr)
		if err != nil {
			log.Fatalln("error:", err)
		} else {
			if err := db.Ping(); err != nil {
				// ORA-01017: invalid username/password; logon denied
				// ORA-12505: TNS:listener does not currently know of SID given in connect descriptor
				if strings.Contains(err.Error(), "ORA-01017") {
					_sid = append(_sid, sid)
				}
				if strings.Contains(err.Error(), "ORA-12505") {
					// goutils.Red("error sid")
				}
			} else {
				_sid = append(_sid, sid)
			}
			db.Close()
		}
	}

	p.SidList[payload.IP] = _sid
}

func (p *OracleBrute) CheckUNauth(payload global.Payload) {
	p.TempIP = append(p.TempIP, payload.IP)

	for _, sid := range p.SidList[payload.IP] {
		for _, UserName := range []string{"sys", "test"} {
			urlOptions := map[string]string{"SID": sid}
			connStr := go_ora.BuildUrl(payload.IP, payload.Port, "", payload.UserName, "", urlOptions)
			db, err := sql.Open("oracle", connStr)
			if err != nil {
				log.Fatalln("error:", err)
			} else {
				if err = db.Ping(); err != nil {
					goutils.Green(fmt.Sprintf("[-] %s:%d/%s %s 空", payload.IP, payload.Port, sid, UserName))
				} else {
					goutils.Red(fmt.Sprintf("[+] %s:%d/%s %s 空", payload.IP, payload.Port, sid, UserName))
					global.Results = append(
						global.Results,
						global.Payload{IP: payload.IP, Port: payload.Port, UserName: UserName, PassWord: "空", Note: "sid: " + sid},
					)
				}
			}
			db.Close()
		}
	}
}
