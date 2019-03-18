#!/usr/bin/env python
#coding:utf-8
#code by struggle
#this script openid must <= 10000
import urllib2
import json
import time

class Weixin(object):
    def __init__(self, appid, secretid):
        self.appid = appid
        self.secretid = secretid
    
    def get_token(self):
        try:
            tokenouput = urllib2.urlopen('https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (self.appid, self.secretid))
            return eval(tokenouput.read())['access_token']
        except:
            return

    def get_fakeid_list(self, tokenid):
        try:
            fakeid_output = urllib2.urlopen('https://api.weixin.qq.com/cgi-bin/user/get?access_token=' + tokenid)
            return eval(fakeid_output.read())['data']['openid']
        except:
            pass
    
    def get_user_info(self, tokenid, post_data_list):
        post_data_info = {}
        user_info = {}
        send_url = 'https://api.weixin.qq.com/cgi-bin/user/info/batchget?access_token=' + tokenid
        post_data_info['user_list'] = post_data_list
        post_data = json.dumps(post_data_info)
        send_req = urllib2.Request(send_url, post_data)
        send_post = urllib2.urlopen(send_req)
        for i in eval(send_post.read())['user_info_list']:
           user_info[i['openid']] = i['nickname']
        return user_info

    def get_user_dict(self, tokenid, fakeidlist):
        post_data_list = []
        post_data_list_all = []
        all_user_info = {}
        for i in fakeidlist:
            a = {}
            a['openid'] = i
            a['lang'] = 'zh_CN'
            post_data_list.append(a)

        if len(post_data_list) > 100:
            for i in range(0, len(post_data_list), 100):
                post_data_list_all.append(post_data_list[i:i+100])
            for i in post_data_list_all:
                userinfo = self.get_user_info(tokenid, i)
                all_user_info.update(userinfo)
                time.sleep(5)
        else:
            userinfo = self.get_user_info(tokenid, post_data_list)
            all_user_info = userinfo
        return all_user_info
        

    def send_wx(self, tokenid, tofakeid, subject, textinfo, tempid='dPK9AMSFBK83cb4uiyohoLOGu3g1j0mxsIGXJEqRoRg', color_text='#ff0000' ,sevrity='WARING'):
        try:
            send_url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=' + tokenid
            post_data =json.dumps({
            'touser':tofakeid,
            'template_id':tempid,
            'url':'http://weixin.qq.com/download',
            'data':{
            'first':{
            'value':subject,
            'color':color_text
                    },
            'keyword1':{
            'value':sevrity,
            'color':'#173177'
                    },
            'keyword2':{
            'value':textinfo,
            'color':'#173177'
                    }
                }             
                                })
            send_req = urllib2.Request(send_url,post_data)
            send_post = urllib2.urlopen(send_req)
            return send_post.read()
        except:
            return

if __name__ == "__main__":
    pass