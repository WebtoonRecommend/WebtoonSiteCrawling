import pandas as pd
import requests
from bs4 import BeautifulSoup

import sqlite3
con = sqlite3.connect('./test.db')
cur = con.cursor()
# # .to_sql(): pandas의 dataFrame이 table을 생성하면서 저장되기 때문에 그 전에 table을 지워둔다.
# con.execute("DROP TABLE IF EXISTS all_webtoon")

# dataFrame 생성
data = pd.DataFrame(data=[], columns=['웹툰ID','제목','링크','이미지링크','별점','완결'])



def naver(data,abc):
    # 웹툰 전체목록 링크로 들어가 html을 받아오고 parsing한다.
    url = 'https://comic.naver.com/webtoon/creationList?prefix='+abc
    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    # 각각의 웹툰 정보에 해당하는 html 부분을 리스트에 담는다.
    my_webtoons = soup.select(
        '.img_list >li'
        )
    print(my_webtoons[0])
    for my_webtoon in my_webtoons[:]:
        # 각각의 웹툰마다 웹툰제목,웹툰ID,링크,이미지링크를 가져온다.
        titleTag = my_webtoon.select_one('.thumb > a') 
        imageTag = my_webtoon.select_one('.thumb > a > img') 
        ratingTag = my_webtoon.select_one('.rating_type > strong')
        print(imageTag.get('title'))
        print(type(imageTag.get('src')))
        
        temp = []
        # 웹툰ID는 웹툰 링크에서 추출한다.
        temp.append(titleTag.get('href').split("titleId=")[1])
        temp.append(titleTag.get('title'))
        temp.append(titleTag.get('href'))
        temp.append(imageTag.get('src'))
        temp.append(ratingTag.text)
        if titleTag.find_all("img",{'class':'finish'}):
            temp.append('1')
        else:
            temp.append('0')
        print(temp)
        
        # 가져온 정보를 dataFrame에 추가한다.
        temp = pd.DataFrame(data=[temp], columns=data.columns)
        data = pd.concat([data,temp])
    
    # print(soup,data)
    print(data)
    return data

# 가나다순 url 인자값
abcs = ['가','나','다','라','마','바','사','아','자','차','카','타','파','하','A','1']
# 웹툰 정보를 dataFrame에 저장한다.
for abc in abcs:
    data = naver(data,abc)
# 중복된 웹툰은 하나만 남기고 제거한다.(ex.화,목 연재 웹툰)
data = data.drop_duplicates(['웹툰ID'])
# webtoon 테이블에 저장한다.
data.to_sql('webtoon',con,if_exists='replace',index=False)
# print("/webtoon/list?titleId=758037&weekday=mon".split("titleId=")[1].split("&")[0])