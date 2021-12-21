import requests,time,re
from urllib import parse
from bs4 import BeautifulSoup
#屏蔽https报错
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
 
header = {
    'Cookie': '*******添加用户cookie**************',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': '***添加用户Agent***************',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Content-Length': '211',
    'Origin': 'https://www.t00ls.cc',
    'Referer': 'https://www.t00ls.cc/login.html',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Te': 'trailers',
    'Connection': 'close',
  }

username = '登录名'
password = '登录密码'
question = '问题'#'母亲的名字','爷爷的名字','父亲出生的城市','您其中一位老师的名字','您个人计算机的型号','您最喜欢的餐馆名称','驾驶执照的最后四位数字'
answer = '答案'

question_num = {
    '母亲的名字':'1',
    '爷爷的名字':'2',
    '父亲出生的城市':'3',
    '您其中一位老师的名字':'4',
    '您个人计算机的型号':'5',
    '您最喜欢的餐馆名称':'6',
    '驾驶执照的最后四位数字':'7'
}
login_url = 'https://www.t00ls.cc/login.html' #国内
                                             #国外 https://www.t00ls.net/login.html
sign_in_url = 'https://www.t00ls.cc/members-profile-14344.html'#修改成自己的签到页面
qiandao_url = 'https://www.t00ls.cc/ajax-sign.json'
sign_data = {
    'username' : username,
    'password' : password,
    'questionid': question_num[question],
    'answer' : answer,
    'formhash' : '40526fac',
    'loginsubmit' : '登录',
    'redirect' : 'https://www.t00ls.cc',
    'cookietime' : '2592000'
}
s = requests.session()
#  登录
def login():
    s.post(url=login_url,data=sign_data,verify=False,headers=header,timeout=5)
# 获取签到页面的数据
def sign_page_text():
    sign_page_text = s.get(sign_in_url, verify=False).text
    return sign_page_text
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

# 获取已签到的天数
def get_qiandao_days(sign_in_later_page):
    soup = BeautifulSoup(sign_in_later_page,'html.parser')
    days = soup.find_all('input',{'class':'btn signbtn'})[0]['value']
    return days
# 自动签到log
def log(time,result):
    with open('log.txt','a+') as f:
        f.write(f'{time}       {result}\n')

if __name__ == '__main__':
    start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    login()
    qiandao_text_befor = sign_page_text()
    qiandao_result = qian_dao(page_text=qiandao_text_befor)
    qiandao_text_later = sign_page_text()
    result = get_qiandao_days(sign_in_later_page=qiandao_text_later)
    if qiandao_result == 1:
        qiandao_stat = f'签到成功：  {result}'
        print(qiandao_stat)
        log(start_time,qiandao_stat)
    else:
        qiandao_stat = f'签到失败，不可重复签到：  {result}'
        print(qiandao_stat)
        log(start_time, qiandao_stat)
