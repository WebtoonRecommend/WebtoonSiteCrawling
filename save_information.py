import pandas as pd
import requests
from bs4 import BeautifulSoup

import sqlite3
con = sqlite3.connect('./test.db')
cur = con.cursor()
# # .to_sql(): pandas의 dataFrame이 table을 생성하면서 저장되기 때문에 그 전에 table을 지워둔다.
# con.execute("DROP TABLE IF EXISTS webtoon_info")

# comment url에 필요한 웹툰ID를 가져온다.
webtoon_from_db = pd.read_sql("SELECT * FROM webtoon", con, index_col=None)
webtooninfo_from_db = pd.read_sql("SELECT * FROM webtoon_info", con, index_col=None)

# dataFrame 생성
data = pd.DataFrame(data=[], columns=['웹툰ID','이름','작가','설명','장르','이용가','썸네일','회차'])
print('783518' in list(webtooninfo_from_db['웹툰ID']))


def naver(data, id):
    # 웹툰 전체목록 링크로 들어가 html을 받아오고 parsing한다.
    url = 'https://comic.naver.com/webtoon/list?titleId='+str(id)
    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    
    # 웹툰 상세정보를 추출한다.
    detail = soup.select_one('.comicinfo')
    # print(html)
    # print(detail)
    thum = soup.select_one('.thumb img').get('src')
    wtitle = detail.select_one('.title').text
    wwrt_nm = detail.select_one('.wrt_nm').text.lstrip()
    wdetail = detail.select_one('div.detail > p').text
    wgenre = detail.select_one('.genre').text
    if detail.select_one(".detail_info").find_all("span",{'class':'age'}):
        wage = detail.select_one('.age').text
    else:
        wage = ('전체연령가')
    
    # print(thum,wtitle,wwrt_nm,wdetail,wgenre,wage)
    # 웹툰 회차정보는 최신화의 링크에서 추출한다.
    episode = soup.select_one('td.title > a').get('href').split("no=")[1].split('&')[0]
    # print(episode)
    
    print(id)
    temp = []
    temp.append(id)
    temp.append(wtitle)
    temp.append(wwrt_nm)
    temp.append(wdetail)
    temp.append(wgenre)
    temp.append(wage)
    temp.append(thum)
    temp.append(episode)
    print(temp)
    
    # 가져온 정보를 dataFrame에 추가한다.
    temp = pd.DataFrame(data=[temp], columns=data.columns)
    data = pd.concat([data,temp])
    
    return data



# 웹툰 상세정보를 dataFrame에 저장한다.
for id in webtoon_from_db['웹툰ID'][:]:
    if id in list(webtooninfo_from_db['웹툰ID']):
        continue
    data = naver(data, id)

# webtoon_info 테이블에 저장한다. 
data.to_sql('webtoon_info',con,if_exists='append')