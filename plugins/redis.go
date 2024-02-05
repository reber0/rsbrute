/*
 * @Author: reber
 * @Mail: reber0ask@qq.com
 * @Date: 2023-10-08 10:55:35
 * @LastEditTime: 2024-02-05 13:42:27
 */
package plugins

import (
	"context"
	"fmt"
	"strings"

	"github.com/reber0/goutils"
	"github.com/reber0/rsbrute/global"
	"github.com/redis/go-redis/v9"
	"github.com/remeh/sizedwaitgroup"
	"go.uber.org/ratelimit"
)

type RedisBrute struct {
	Name      string
	Limiter   ratelimit.Limiter
	WaitGroup sizedwaitgroup.SizedWaitGroup
	TempIP    []string // 检测未授权，测试过的 ip 加在这个里面
}

// New
func NewRedisBrute(rate int) *RedisBrute {
	return &RedisBrute{
		Name:      "RedisBrute",
		Limiter:   ratelimit.New(rate),
		WaitGroup: sizedwaitgroup.New(rate),
		TempIP:    make([]string, 0, 10000),
	}
}

// GetName
func (p *RedisBrute) GetName() string {
	return p.Name
}

func (p *RedisBrute) Run() {
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

func (p *RedisBrute) Worker(payload global.Payload) {
	defer p.WaitGroup.Done()

	opt := redis.Options{
		Addr:     fmt.Sprintf("%s:%d", payload.IP, payload.Port),
		Password: payload.PassWord, // no password set
		DB:       0,                // use default DB
	}
	rdb := redis.NewClient(&opt)

	status := rdb.Ping(context.TODO()).String()
	if strings.Contains(status, "PONG") {
		goutils.Red(fmt.Sprintf("[+] %s:%d %s", payload.IP, payload.Port, payload.PassWord))
		global.Results = append(global.Results, payload)
	} else {
		goutils.Green(fmt.Sprintf("[-] %s:%d %s", payload.IP, payload.Port, payload.PassWord))
	}

	rdb.Close()
}

func (p *RedisBrute) CheckUNauth(payload global.Payload) {
	p.TempIP = append(p.TempIP, payload.IP)

	opt := redis.Options{
		Addr:     fmt.Sprintf("%s:%d", payload.IP, payload.Port),
		Password: "", // no password set
		DB:       0,  // use default DB
	}
	rdb := redis.NewClient(&opt)

	status := rdb.Ping(context.TODO()).String()
	if strings.Contains(status, "PONG") {
		goutils.Red(fmt.Sprintf("[+] %s:%d %s", payload.IP, payload.Port, "空"))
		global.Results = append(
			global.Results,
			global.Payload{IP: payload.IP, Port: payload.Port, UserName: "空", PassWord: "空"},
		)
	} else {
		goutils.Green(fmt.Sprintf("[-] %s:%d %s", payload.IP, payload.Port, "空"))
	}

	rdb.Close()
}
