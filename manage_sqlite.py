# sqlite 쿼리용 py파일
import sqlite3
con = sqlite3.connect('./test.db')
cur = con.cursor()

import pandas as pd



# sql 쿼리문 실행
# drop, create 문을 실행할 때 사용하는 코드
sql = """
DROP TABLE IF EXISTS webtoon_comment
"""
cur.executescript(sql)

# pandas to sql
# 새로운 table을 생성할 때 사용하는 코드
data = pd.DataFrame(data=[], columns=['웹툰ID','제목','회차','댓글','좋아요','싫어요'])
data.to_sql('webtoon_comment',con)
