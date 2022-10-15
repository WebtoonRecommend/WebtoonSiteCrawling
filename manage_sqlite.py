# sqlite 쿼리용 py파일
import sqlite3
con = sqlite3.connect('./test.db')
cur = con.cursor()

import pandas as pd



# sql 쿼리문 실행
# drop, create 문을 실행할 때 사용하는 코드
# sql = """
# ALTER TABLE webtoon_info ADD  COLUMN "플랫폼" TEXT;
# UPDATE webtoon_info SET "플랫폼"="네이버"
# """
sql = """
DROP TABLE IF EXISTS webtoon_info_join;
CREATE TABLE webtoon_info_join
AS
SELECT 
  webtoon_info."웹툰ID" ,
  webtoon_info."이름" ,
  webtoon_info."작가" ,
  webtoon_info."설명" ,
  webtoon_info."장르" ,
  webtoon_info."이용가" ,
  webtoon_info."회차" ,
  webtoon."별점" , 
  webtoon."완결" , 
  webtoon_info."플랫폼" ,
  webtoon."링크" , 
  webtoon."이미지링크" , 
  webtoon_info."썸네일" 
  
  FROM webtoon_info
  INNER JOIN webtoon
  ON webtoon_info."웹툰ID" = webtoon."웹툰ID"
"""
cur.executescript(sql)

# pandas to sql
# 새로운 table을 생성할 때 사용하는 코드
# data = pd.DataFrame(data=[], columns=['웹툰ID','제목','회차','댓글','좋아요','싫어요'])
webtoon_from_db = pd.read_sql("SELECT * FROM webtoon", con)
webtooninfo_from_db = pd.read_sql("SELECT * FROM webtoon_info", con)
# print (webtooninfo_from_db)
# # 킹받네...
# webtooninfo_from_db = webtooninfo_from_db.drop_duplicates(subset=['웹툰ID'])
# webtooninfo_from_db.to_sql('webtoon_info',con,if_exists='replace')
print(webtooninfo_from_db)
