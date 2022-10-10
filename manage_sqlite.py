# sqlite 쿼리용 py파일
import sqlite3
con = sqlite3.connect('./test.db')
cur = con.cursor()

import pandas as pd



# sql 쿼리문 실행
# drop, create 문을 실행할 때 사용하는 코드
sql = """
DROP TABLE IF EXISTS webtoon_info_2
"""
cur.executescript(sql)

# pandas to sql
# 새로운 table을 생성할 때 사용하는 코드
# data = pd.DataFrame(data=[], columns=['웹툰ID','제목','회차','댓글','좋아요','싫어요'])
webtooninfo_from_db = pd.read_sql("SELECT * FROM webtoon_info", con)
# print (webtooninfo_from_db)
# # 킹받네...
# webtooninfo_from_db = webtooninfo_from_db.drop_duplicates(subset=['웹툰ID'])
# webtooninfo_from_db.to_sql('webtoon_info',con,if_exists='replace')
print(webtooninfo_from_db)
