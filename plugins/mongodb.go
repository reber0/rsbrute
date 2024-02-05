/*
 * @Author: reber
 * @Mail: reber0ask@qq.com
 * @Date: 2023-10-08 10:57:38
 * @LastEditTime: 2024-02-05 15:41:42
 */
package plugins

import (
	"context"
	"fmt"

	"github.com/reber0/goutils"
	"github.com/reber0/rsbrute/global"
	"github.com/remeh/sizedwaitgroup"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
	"go.uber.org/ratelimit"
)

type MongoDBBrute struct {
	Name      string
	Limiter   ratelimit.Limiter
	WaitGroup sizedwaitgroup.SizedWaitGroup
	TempIP    []string // 检测未授权，测试过的 ip 加在这个里面
}

// New
func NewMongoDBBrute(rate int) *MongoDBBrute {
	return &MongoDBBrute{
		Name:      "MongoDBBrute",
		Limiter:   ratelimit.New(rate),
		WaitGroup: sizedwaitgroup.New(rate),
		TempIP:    make([]string, 0, 10000),
	}
}

// GetName
func (p *MongoDBBrute) GetName() string {
	return p.Name
}

// Run
func (p *MongoDBBrute) Run() {
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

func (p *MongoDBBrute) Worker(payload global.Payload) {
	defer p.WaitGroup.Done()

	connStr := fmt.Sprintf("mongodb://%s:%s@%s:%d/", payload.UserName, payload.PassWord, payload.IP, payload.Port)
	opt := options.Client().ApplyURI(connStr)
	client, err := mongo.Connect(context.TODO(), opt)
	if err != nil {
		goutils.Green(fmt.Sprintf("[-] %s:%d %s %s", payload.IP, payload.Port, payload.UserName, payload.PassWord))
	} else {
		if err = client.Ping(context.TODO(), nil); err != nil {
			goutils.Green(fmt.Sprintf("[-] %s:%d %s %s", payload.IP, payload.Port, payload.UserName, payload.PassWord))
		} else {
			goutils.Red(fmt.Sprintf("[+] %s:%d %s %s", payload.IP, payload.Port, payload.UserName, payload.PassWord))
			global.Results = append(global.Results, payload)
		}
	}
}

func (p *MongoDBBrute) CheckUNauth(payload global.Payload) {
	p.TempIP = append(p.TempIP, payload.IP)

	connStr := fmt.Sprintf("mongodb://%s:%d/", payload.IP, payload.Port)
	opt := options.Client().ApplyURI(connStr)
	client, err := mongo.Connect(context.TODO(), opt)
	if err != nil {
		goutils.Green(fmt.Sprintf("[-] %s:%d 空 空", payload.IP, payload.Port))
	} else {
		if err = client.Ping(context.TODO(), nil); err != nil {
			goutils.Green(fmt.Sprintf("[-] %s:%d 空 空", payload.IP, payload.Port))
		} else {
			goutils.Red(fmt.Sprintf("[+] %s:%d 空 空", payload.IP, payload.Port))
			global.Results = append(
				global.Results,
				global.Payload{IP: payload.IP, Port: payload.Port, UserName: "空", PassWord: "空"},
			)
		}
	}
}
