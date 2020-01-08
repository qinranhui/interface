from blog import models
import requests
import time
import hmac
from hashlib import sha1,md5
import base64

# Create your views here.
#*********公用接口***********
#获取参数
def get_parameter(parameterKey):

    result = models.systemParameter.objects.get(parameterKey = parameterKey).__dict__['parameterValue']

    return result

#*********薪人薪事（HR）公用接口***********
#接口取token，存数据库
def get_token():

    data = {
        'grant_type':get_parameter("grant_type"),
        'client_id':get_parameter("appKey"),
        'client_secret':get_parameter("appSecret"),
    }
    url = 'https://api.xinrenxinshi.com/authorize/oauth/token?'

    token = requests.post(url,data).json()['access_token']

    save_parameter('access_token',token)  #存token
    save_parameter('update_time',str(int(time.time())))

    return token

#*********薪人薪事（HR）公用接口***********
#获取access_token，超时重新获取
def get_access_token(timestamp):

    expiry_time = int(get_parameter("update_time")) + int(get_parameter("expiry_time"))

    if timestamp > expiry_time:
        get_token()

    access_token = get_parameter("access_token")

    return access_token


#*********公用接口***********
#参数签名hmac-SHA1,返回二进制
def get_sign(data):

    data = format_data(sort(data))

    key = get_parameter("appSecret")

    encrypt = hmac.new(key.encode(),data.encode(),sha1).digest()

    return str(base64.b64encode(encrypt))[2:-1]


#*********公用接口***********
#格式化数据
def format_data(data):

    string1 = ''

    for key,value in data.items():
        string = str(key) + '=' + str(value) 
        string1 += '&' + string

    result = string1[1:]

    return result

#*********公用接口***********
#参数名称Acsii码排序
def sort(data):

    data1 = {}
    lists = (sorted(data))

    for i in range(len(sorted(data))):
        data1[lists[i]] = data[lists[i]]
    
    result = data1

    return result

#*********公用接口***********
#存参数到系统表
def save_parameter(key,value):
    models.systemParameter.objects.filter(parameterKey = key).update(parameterValue = value)

#*********瑞为云平台（客流系统）公用接口***********
#获取访问令牌
def get_visitor_token():

    data = {
        'clientId':get_parameter("clientId"),
        'clientSecret':get_parameter("clientSecret"),
        'grantType':get_parameter("grant_type")
    }
    url = "https://dj.reconova.com/oauthAction!token.action?"

    result = requests.post(url,data).json()['data']

    token = result["token"]

    save_parameter("token",token)
    save_parameter("tokenEffectiveDate",result["tokenEffectiveDate"])
    save_parameter("refreshToken",result["refreshToken"])
    save_parameter("effectiveDate",result["effectiveDate"])

    return token

#*********瑞为云平台（客流系统）公用接口***********
#刷新令牌
def refreshToken():

    data = {
        'clientId':get_parameter("clientId"),
        'refreshToken':get_parameter("refreshToken"),
        'grantType':get_parameter("grant_type")
    }
    url = "https://dj.reconova.com/oauthAction!refreshToken.action?"

    result = requests.post(url,data).json()['data']

    token = result["token"]

    save_parameter("token",token)
    save_parameter("tokenEffectiveDate",result["tokenEffectiveDate"])
    save_parameter("refreshToken",result["refreshToken"])
    save_parameter("effectiveDate",result["effectiveDate"])

    return requests.post(url,data).json()

#*********瑞为云平台（客流系统）公用接口***********
def get_hr_token(timestamp):

    if timestamp > int(get_parameter("tokenEffectiveDate")):
        refreshToken = refreshToken()
        if refreshToken["success"] == 0:
            result = get_visitor_token()

    else:
        result = get_parameter("token")

    return result

#*********公用接口***********
#参数签名md5,返回32位
def get_sign_md5(data):
    data = format_data(sort(data))
    md5str = md5()
    md5str.update(data.encode())
    return md5str.hexdigest()

    