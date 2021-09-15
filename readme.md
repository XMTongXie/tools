# USAGE


### 1、输入访问地址

```python
login_url = 'https://www.t00ls.cc/login.html' #国内 登录页面
                                              #国外 https://www.t00ls.net/login.html
sign_in_url = 'https://www.t00ls.cc/members-profile-14344.html'#修改成自己的签到页面
qiandao_url = 'https://www.t00ls.cc/ajax-sign.json'   #签到数据提交页面
```

### 2、添加用户cookie

```python
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0',
    'Origin': 'https://www.t00ls.cc',
    'Referer': 'https://www.t00ls.cc/login.html',
    'Cookie': '填写用户cookie'   ##添加用户cookie
  }
```

### 3、完善登录信息

```python
username = '登录名'
password = '登录密码'
question = '问题'#'母亲的名字','爷爷的名字','父亲出生的城市','您其中一位老师的名字','您个人计算机的型号','您最喜欢的餐馆名称','驾驶执照的最后四位数字'
answer = '答案'
```

## 4、配置自动签到

##### ①、在自己的云服务器添加crontab任务

```
 crontab  -e  #为当前用户添加crontab任务  如图从右到左，设置每年，每月，每天，6,16,20点钟，1分钟的时候执行脚本。
```



![image-20210915104417568](https://gitee.com/little-magician/picture-resources/raw/master/MarkDown%20/image-20210915104417568.png)
![image-20210915110050208](https://gitee.com/little-magician/picture-resources/raw/master/MarkDown%20/image-20210915110050208.png)

##### ②、可能导致脚本执行不成功的原因：

###### a、在配置crontab任务的时候最好是root用户

###### b、脚本中、trontab中，涉及到路径的，要修改成绝对路径

