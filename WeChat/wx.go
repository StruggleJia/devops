package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
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

func main(){
	token := GetToken() //获取token
	fakeid := GetFakeID(token) //获取fakeid数组
	GetUserInfo(token, fakeid) //通过fakeid数组，获取用户信息
	SendMessage(token,"youfakeid","test","test") //发送微信信息
}

func GetToken() string {
	const appid string  = "appid" //需要修改成你的appid
	const secretid string = "secretid"  //需要修改成你的secretid
	const url string  = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=" + appid + "&secret=" + secretid

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
		fmt.Println(err)
		return ""
	} else {
		return m.AccessToken
	}

}

func GetFakeID(token string) []string {
	url := "https://api.weixin.qq.com/cgi-bin/user/get?access_token=" + token
	resp, err := http.Get(url)
	if err != nil{
		fmt.Println(err)
	}
	body, err := ioutil.ReadAll(resp.Body)
	m := new(WeChatOpenID)
	err = json.Unmarshal(body, &m)
	if err != nil {
		//fmt.Println(err)
		return []string{}
	} else {
		return m.Data.Openid
	}
}

func GetUserInfo(token string, fakeidlist []string){
	send_url := "https://api.weixin.qq.com/cgi-bin/user/info/batchget?access_token=" + token
	var openidlist []interface{}
	m := new(map[string]string)
	for _, v := range fakeidlist{
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
		fmt.Println(err)
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
			for _, a := range m.UserInfoList{
				fmt.Println(a.Openid + " " + a.Nickname)
			}
		}

	}
}

func SendMessage(tokenid string, tofakeid string, subject string, textinfo string){
	send_url := "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=" + tokenid
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
		fmt.Println(err)
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
				fmt.Println("发送成功")
			}

		}
	}
}
