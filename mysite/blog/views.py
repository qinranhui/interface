from django.shortcuts import render
from blog.common import get_sign,get_access_token,get_sign_md5,get_hr_token,refreshToken
from django.http import HttpResponse
import time
import requests

def get_city():
    timestamp = time.time()     #时间戳
    timestamp1 = int(round(timestamp * 1000))  #毫秒级时间戳
    url = 'https://api.xinrenxinshi.com/v3/common/citys?'

    headers = {
        'access_token':get_access_token(int(timestamp))
    }
    #需要签名的数据
    data = {
        'timestamp':timestamp1,
    }
    #增加sign
    data['sign'] = get_sign(data) 

    result = requests.get(url,headers=headers,params=data).json()
    return result 

    '''
        Interface 员工基础列表
    '''         
def get_employee():
    timestamp = time.time()     #时间戳
    timestamp1 = int(round(timestamp * 1000))  #毫秒级时间戳
    url = 'https://api.xinrenxinshi.com/v3/employee/employeeSimpleList?'

    headers = {
        'access_token':get_access_token(int(timestamp))
    }

    data = {
        'fetchChild':1,
        'offset':0,
        'size':100,
        'status':1,
        'timestamp':timestamp1,
    }
    data['sign'] = get_sign(data) 

    result = requests.get(url,headers=headers,params=data).json()
    return result

def add_brand(brand):
    timestamp = time.time()     #时间戳
    timestamp1 = int(round(timestamp * 1000))
    url = 'https://dj.reconova.com//areaAppAction!addBrand.action?'
    headers = {
        'Authorization':get_hr_token(timestamp1),
    }
    data = {
        'phoneNo':'HSadmin',
        'password':'123456',
        'areaname':brand,
        'vi':'00400300200',
    }
    data['key'] = get_sign_md5(data)

    result = requests.post(url,headers=headers,data=data).json()
    return result 


def demo(request):
    
    print(add_brand('IDO')) 
    #print(refreshToken())
    return HttpResponse("ok")