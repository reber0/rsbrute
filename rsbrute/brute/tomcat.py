#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: reber
@Mail: reber0ask@qq.com
@Date: 2019-05-22 15:30:07
@LastEditTime : 2021-03-16 15:34:48
'''

import base64
import requests

from .baseclass import BruteBaseClass


class BruteForce(BruteBaseClass):
    """BruteForce"""

    def worker(self, payload):
        if self.flag:
            host, port, user, pwd = payload
            user_pwd = "{}:{}".format(user, pwd)
            try:
                url = "http://{}:{}/manager/html".format(host, port)
                Authorization = "Basic " + base64.b64encode(user_pwd.encode("utf-8")).decode("utf-8")
                headers = {
                    "Authorization": Authorization
                }
                resp = requests.get(url, headers=headers)
            except Exception as e:
                hook_msg((False, host, port, user, pwd))
            else:
                if resp.status_code == 200:
                    hook_msg((True, host, port, user, pwd))
                else:
                    hook_msg((False, host, port, user, pwd))

