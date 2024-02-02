/*
 * @Author: reber
 * @Mail: reber0ask@qq.com
 * @Date: 2022-11-01 15:23:49
 * @LastEditTime: 2023-10-09 17:17:29
 */
package global

var (
	ServicePortDict = map[string]int{
		"ssh": 22, "ftp": 21, "telnet": 23, "rlogin": 513,
		"mysql": 3306, "mssql": 1433, "oracle": 1521, "pgsql": 5432, "redis": 6379, "mongodb": 27017, "memcache": 11211,
		"ldap": 389, "winrm": 5985, "vnc": 5901, "rdp": 3389, "smb": 445, "snmp": 161,
		"smtp": 25, "pop": 110,
		"tomcat": 443,
	}
)
