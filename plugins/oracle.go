/*
 * @Author: reber
 * @Mail: reber0ask@qq.com
 * @Date: 2023-10-08 10:54:43
 * @LastEditTime: 2023-11-17 12:58:04
 */
package plugins

import (
	"database/sql"
	"fmt"
	"log"

	_ "github.com/sijms/go-ora/v2"
)

func OracleTest() {
	db, err := sql.Open("oracle", "oracle://utest:ptest@localhost:1521/xe")
	if err != nil {
		log.Fatalln("error:", err)
		return
	}
	defer db.Close()

	err = db.Ping()
	if err != nil {
		log.Fatal(err)
	} else {
		fmt.Println("Connected to database!")
	}
}
