#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 16:47:42 2019

@author: zelord
"""

import urllib
import time
import requests
import json
from pprint import pprint
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import parse, Element
import pandas as pd

col = ['address1',
 'address2',
 'applcbedt',
 'applcendt',
 'areano',
 'buldmgtno1',
 'buldmgtno2',
 'buldnm',
 'buldprpos',
 'divgroundfloorcnt',
 'divundgrndfloorcnt',
 'elevatorno',
 'elvtrasignno',
 'elvtrdivnm',
 'elvtrformnm',
 'elvtrkindnm',
 'elvtrmgtno1',
 'elvtrmgtno2',
 'elvtrmodel',
 'elvtrresmptde',
 'elvtrstts',
 'frstinstallationde',
 'inspctinstt',
 'installationde',
 'installationplace',
 'lastinspctde',
 'lastinspctkind',
 'lastresultnm',
 'liveload',
 'manufacturername',
 'manufacturertelno',
 'mnfcturcpnycd',
 'mntcpnycd',
 'mntcpnynm',
 'mntcpnytelno',
 'partcpntnm',
 'partcpnttelno',
 'partcpnttelno',
 'ratedspeed',
 'shuttlefloorcnt',
 'sigungucd',
 'standardkey',
 'zipcd1',
 'zipcd2']

data = pd.read_csv("은평구.csv",encoding='euc-kr')  # 은평구만뽑은정

eledata = pd.read_csv("eledata.csv",encoding='euc-kr' )
eledata = eledata[['buld_nm','sido','sigungu','승강기번호','주소','고장','고장일자']]

def get_eleno(eledata):
    result = []
    for i in range(len(eledata)):
        ServiceKey = "ZfVGPgxKmjZ1wBCvUsS10mjKkay5vX1PhMSBbqOsarGw33eJeE%2BrMOtRtmtTmV4eJGI0n%2BlYIqrxK5VKJrdwEg%3D%3D"
        url = "http://openapi.elevator.go.kr/openapi/service/ElevatorInformationService/getElevatorList?ServiceKey=" + ServiceKey
        sido = eledata.iloc[i]['sido']
        sigungu = eledata.iloc[i]['sigungu']
        buld_nm = eledata.iloc[i]['buld_nm']
        url = str(url) + "&sido=" + str(sido) +"&sigungu=" + str(sigungu) +"&buld_nm=" + str(buld_nm)
        print(i,len(eledata), url)
        req = requests.get(url)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        elevatorno_list = soup.find_all('elevatorno')
        try:
            result.append(str(elevatorno_list[0].text))
        except:
            result.append("A")
    eledata['real_number'] = result
    return eledata

def make_row(soup):
    temp = {}
    for i in col:
        if soup.find_all(i):
            temp[i] = soup.find_all(i)[0].text
        else :
            temp[i] = ''
    return temp

result_data = get_eleno(data)
result_data.to_csv("result.csv",encoding='euc-kr',index=False)
result_data = result_data[result_data['real_number'] != "A"]

eleno_list = result_data['real_number']
eleno = list(set(eleno_list))

df = pd.DataFrame(index=[0])
for i in range(len(eleno)):
    print(eleno[i])
    ServiceKey = "ZfVGPgxKmjZ1wBCvUsS10mjKkay5vX1PhMSBbqOsarGw33eJeE%2BrMOtRtmtTmV4eJGI0n%2BlYIqrxK5VKJrdwEg%3D%3D"
    url2 = "http://openapi.elevator.go.kr/openapi/service/ElevatorInformationService/getElevatorView?ServiceKey=" + ServiceKey
    url2 = url2 + "&elevator_no=" + str(eleno[i])
    time.sleep(1)
    req = requests.get(url2)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    temp = make_row(soup)
    df2 = pd.DataFrame(temp, index=[i])
    print(len(eledata), df2)
    df = pd.concat([df,df2])
    
df.to_csv("final_result.csv",encoding='euc-kr',index=False)