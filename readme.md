# README

### 1、工具

###### ①pycharm

###### ②Try XPath

###### ③Burp suite

### 2、分析签到流程

通过实际的登录流程，配合bup抓包分析，确定脚本签到需要的几个步骤：

#### a、登录

###### ①session保持会话

```python
s = requests.session()
```



###### ②携带登录数据请求登录页面

```python
login_url = 'https://www.t00ls.cc/login.html' #国内
                                             #国外 https://www.t00ls.net/login.html
sign_data = {
    'username' : username,
    'password' : password,
    'questionid': question_num[question],
    'answer' : answer,
    'formhash' : '40526fac',
    'loginsubmit' : '提交',
    'redirect' : 'https://www.t00ls.cc',
    'cookietime' : '2592000'
}
#  登录
def login():
    s.post(url=login_url,data=sign_data,verify=False,headers=header,timeout=5)
```



#### b、签到

###### ①获取签到状态（一天没签/断签可补签/已签到）



###### ②判断是否可以进行签到，可以签到 则 获取签到按钮的onclick属性值(提交数据的时候会携带onclick属性值里面的一组特征字符串来判断，数据来路是否正确。)

###### ③携带onclick值，提交

```python
# 签到
def qian_dao(page_text):
    soup = BeautifulSoup(page_text,'html.parser')
    qiandao = soup.find_all('input',{'class': 'btn signbtn'})
    try:
        if len(qiandao) == 1:
            if qiandao[0]['value'] == '签到领TuBi':
                #一天都没签的情况
                qiandao_onclick = re.findall('\(\'(.*)\'\)',qiandao[0]['onclick'])
            elif '已签到' in  qiandao[0]['value']:
                #连续签到的情况
                return '不可重复签到'

        elif len(qiandao) == 2:
            #存在漏签，可补签的情况
            qiandao_onclick = re.findall('\(\'(.*)\'\)', qiandao[1]['onclick'])
        qiandao_data = {
            'formhash':qiandao_onclick[0],
            'signsubmit':'apply'
        }
        qiandao_state = s.post(url=qiandao_url,data=qiandao_data,verify=False,timeout=5).text
        print(qiandao_state)
        print('1QWE')
        if 'success' in qiandao_state:
            return 1
        else:
            return 0

    except:
        exit(print(r'未知错误，脚本执行失败！'))
```

#### c、获取签到后的数据，并返回签到结果

###### ①重新请求签到页面，xpth提取签到天数，并返回签到情况，写入log

```python
def login():
    s.post(url=login_url,data=sign_data,verify=False,headers=header,timeout=5)
```

```python
        qiandao_stat = f'签到成功：  {result}'
        print(qiandao_stat)
        log(start_time,qiandao_stat)
    else:
        qiandao_stat = f'签到失败，不可重复签到：  {result}'
        print(qiandao_stat)
        log(start_time, qiandao_stat)
```

### 3、完整代码

![image-20210915102048782](https://gitee.com/little-magician/picture-resources/raw/master/MarkDown%20/image-20210915102048782.png)
