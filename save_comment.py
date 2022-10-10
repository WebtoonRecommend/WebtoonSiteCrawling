# https://m.blog.naver.com/stu5073/221801367202 참고
import pandas as pd
from collections import deque

# selenium 라이브러리의 webdriver를 가져온다.
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
s = Service('./chromedriver.exe')
options=webdriver.ChromeOptions() 
options.add_experimental_option('excludeSwitches',['enable-logging']) 

import sqlite3
con = sqlite3.connect('./test.db')
cur = con.cursor()
# con.execute("DROP TABLE IF EXISTS webtoon_comment")
# comment url에 필요한 웹툰ID를 가져온다.
webtooninfo_from_db = pd.read_sql("SELECT * FROM webtoon_info", con, index_col=None)
comment_from_db = pd.read_sql("SELECT * FROM webtoon_comment", con, index_col=None)
comments = comment_from_db['웹툰ID'].drop_duplicates



def collector(sql, id, wtitle, k):
    driver = webdriver.Chrome(service=s, options=options)
    # html로딩이 되지 않았다면 최대 1초를 기다린다.
    driver.implicitly_wait(1)
    drivers.append(driver)

    # 댓글 페이지로 이동한다. 웹툰ID 및 회차 정보로 이루어져 있다.
    url = 'https://comic.naver.com/comment/comment?titleId='+str(id)+'&no='+str(k)
    driver.get(url)
    
    # 웹툰ID,웹툰제목,회차,댓글,좋아요/싫어요 수 수집
    webtoon = id
    webtoon_title = wtitle
    num = k
    reviews = driver.find_elements(By.CSS_SELECTOR,'.u_cbox_contents')
    likes = driver.find_elements(By.CSS_SELECTOR,'.u_cbox_cnt_recomm')
    hates = driver.find_elements(By.CSS_SELECTOR,'.u_cbox_cnt_unrecomm')
    # 총 n개의 댓글이 수집되므로 해당 댓글 수만큼 for문을 돕니다.
    for i in range(len(reviews)):
        # for문을 돌며, 웹툰ID,웹툰제목,댓글별 회차,댓글,좋아요/싫어요를 저장
        print(reviews[i].text)
        
        # INSERT문 실행
        cur.execute(sql, ('0',str(webtoon),str(webtoon_title),str(num),reviews[i].text,likes[i].text,hates[i].text))
        # sql 쿼리 실행 후 반드시 commit!
        con.commit()

    # 크롤링 속도 향상을 위해, 탭을 15개씩 열고 닫고를 반복함
    if len(drivers)>15:
        driver.quit()
        drivers.clear()

    print(str(webtoon), str(num) + '화 베댓 수집 완료')


drivers=deque()
# webtoon_comment table INSERT문 양식
sql = "INSERT INTO webtoon_comment VALUES(?,?,?,?,?,?,?)"
for id,wtitle,j in zip(webtooninfo_from_db['웹툰ID'][:], webtooninfo_from_db['이름'][:], webtooninfo_from_db['회차'][:]):
    if id in comments:
        continue
    
    j = int(j)
    if j<10:
        # 총 회차가 9개 이하라면 모든 회차에서 댓글을 가져온다.
        _range = range(1,j+1)
    else:
        # 최신 10개 회차에서 댓글을 가져온다.
        _range = range(j-9,j+1)
    
    for k in _range:
        collector(sql, id, wtitle, k)
