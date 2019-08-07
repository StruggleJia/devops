package main

import (
	"bytes"
	"encoding/json"
	"errors"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
)

type WeChatToken struct {
	AccessToken	string `json:"access_token"`
	ExpiresIn	int	`json:"expires_in"`
}

type WeChatOpenID struct {
	Total int `json:"total"`
	Count int `json:"count"`
	Data  struct {
		Openid []string `json:"openid"`
	} `json:"data"`
	NextOpenid string `json:"next_openid"`
}

type SendFakeID struct {
	Userlist []interface{} `json:"user_list"`
}

type UserInfo struct {
	UserInfoList []struct {
		Subscribe      int           `json:"subscribe"`
		Openid         string        `json:"openid"`
		Nickname       string        `json:"nickname"`
		Sex            int           `json:"sex"`
		Language       string        `json:"language"`
		City           string        `json:"city"`
		Province       string        `json:"province"`
		Country        string        `json:"country"`
		Headimgurl     string        `json:"headimgurl"`
		SubscribeTime  int           `json:"subscribe_time"`
		Remark         string        `json:"remark"`
		Groupid        int           `json:"groupid"`
		TagidList      []interface{} `json:"tagid_list"`
		SubscribeScene string        `json:"subscribe_scene"`
		QrScene        int           `json:"qr_scene"`
		QrSceneStr     string        `json:"qr_scene_str"`
	} `json:"user_info_list"`
}

type SendWeChatInfo struct {
	Touser string `json:"touser"`
	Template_id string `json:"template_id"`
	Url string `json:"url"`
	Data map[string]map[string]string `json:"data"`
}

type ReturnInfo struct {
	Errcode int    `json:"errcode"`
	Errmsg  string `json:"errmsg"`
	Msgid   int64  `json:"msgid"`
}

type WeChatMSG struct {
	AppID string
	SecretID string
	token string
	fakeID []string
}

const g_token_url string  = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s"
const g_fakeid_url string = "https://api.weixin.qq.com/cgi-bin/user/get?access_token=%s"
const g_userinfo_url string = "https://api.weixin.qq.com/cgi-bin/user/info/batchget?access_token=%s"
const g_sendtemplate_url string = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s"

func (we *WeChatMSG)getToken() error {
	appid := we.AppID
	secret := we.SecretID
	url := fmt.Sprintf(g_token_url,appid,secret)

	resp, err := http.Get(url)
	if err != nil {
		fmt.Println(err)
	}
	defer resp.Body.Close()
	body, err := ioutil.ReadAll(resp.Body)
	//fmt.Println(string(body))
	m := new(WeChatToken)
	err = json.Unmarshal(body, &m)
	if err != nil {
		return err
	} else {
		we.token = m.AccessToken
		return nil
	}

}

func (we *WeChatMSG)getFakeID() error {
	url := fmt.Sprintf(g_fakeid_url,we.token)
	resp, err := http.Get(url)
	if err != nil{
		fmt.Println(err)
	}
	body, err := ioutil.ReadAll(resp.Body)
	m := new(WeChatOpenID)
	err = json.Unmarshal(body, &m)
	if err != nil {
		//fmt.Println(err)
		return err
	} else {
		we.fakeID = m.Data.Openid
		return nil
	}
}

func (we *WeChatMSG)GetUserInfo() (*UserInfo,error) {
	var err error
	err = we.getFakeID()
	if err != nil {
		return &UserInfo{}, err
	}
	send_url := fmt.Sprintf(g_userinfo_url,we.token)
	var openidlist []interface{}
	m := new(map[string]string)
	for _, v := range we.fakeID{
		*m = map[string]string{}
		(*m)["openid"] = v
		openidlist = append(openidlist, *m)
		//fmt.Println(openidlist)
	}
	post_data := SendFakeID{
		Userlist:openidlist,
	}
	jsonBytes, err := json.Marshal(post_data)
	if err != nil{
		return &UserInfo{}, err
	} else {
		req := bytes.NewBuffer(jsonBytes)
		request, _ := http.NewRequest("POST", send_url, req)
		request.Header.Set("Content-type", "application/json")
		client := &http.Client{}
		response, _ := client.Do(request)
		if response.StatusCode == 200 {
			body, _ := ioutil.ReadAll(response.Body)
			//fmt.Println(string(body))
			m := new(UserInfo)
			err = json.Unmarshal(body, &m)
			return m,nil
		}
		return &UserInfo{}, nil
	}
}

func (we *WeChatMSG)SendMessage(tofakeid string, subject string, textinfo string) error {
	send_url := fmt.Sprintf(g_sendtemplate_url,we.token)
	m := new(SendWeChatInfo)
	m.Touser = tofakeid
	m.Template_id = "dPK9AMSFBK83cb4uiyohoLOGu3g1j0mxsIGXJEqRoRg"
	m.Url = "http://weixin.qq.com/download"
	m.Data = make(map[string]map[string]string)
	m.Data["first"] = map[string]string{
		"value" : subject,
		"color" : "#ff0000",
	}
	m.Data["keyword1"] = map[string]string{
		"value" : "WARING",
		"color" : "#173177",
	}
	m.Data["keyword2"] = map[string]string{
		"value" : textinfo,
		"color" : "#173177",
	}
	jsonBytes, err := json.Marshal(m)
	if err != nil{
		return err
	} else {
		req := bytes.NewBuffer(jsonBytes)
		request, _ := http.NewRequest("POST", send_url, req)
		request.Header.Set("Content-type", "application/json")
		client := &http.Client{}
		response, _ := client.Do(request)
		if response.StatusCode == 200 {
			body, _ := ioutil.ReadAll(response.Body)
			m := new(ReturnInfo)
			err = json.Unmarshal(body, &m)
			if m.Errmsg == "ok"{
				return nil
			}

		}

		return errors.New("Send failed cause unknow reason.")
	}
}

func NewWeChatMSG (appid string,secret string) *WeChatMSG {
	we := new(WeChatMSG)
	we.AppID = appid
	we.SecretID = secret
	var err error
	err = we.getToken()
	if err != nil {
		log.Fatalln(err)
	}
	return we
}

func main(){
	we := NewWeChatMSG("appid","secret")
	fmt.Println(we.GetUserInfo())
	err := we.SendMessage("fakeid","subject","textinfo")
	if err != nil {
		log.Fatalln(err)
	}
}