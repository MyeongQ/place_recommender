import pymysql
import pandas as pd
import numpy as np

def makeCsv():
    con = pymysql.connect(host='localhost', user='root', password='1234',
                          db='previsitor', charset='utf8')  # 한글처리 (charset = 'utf8')

    # STEP 3: Connection 으로부터 Cursor 생성
    cur = con.cursor()

    # STEP 4: SQL문 실행 및 Fetch
    sql = "SELECT UserId FROM previsitor.reviews GROUP BY UserId HAVING COUNT(*) > 4"
    cur.execute(sql)
    # 데이타 Fetch
    rows = np.array((pd.DataFrame(cur.fetchall())))
    print(rows)  # 전체 rows
    users = "("
    for row in rows:
        users += str(row[0])+", "

    print(users)
    users = users[:-2]+")"

    sql = "SELECT PlaceId, UserId, rating FROM previsitor.reviews WHERE UserId IN " + users
    cur.execute(sql)
    rows = pd.DataFrame(cur.fetchall())
    print(rows)

    rows.to_csv("../dataset/user-movie-ratings.csv", index=False)
    # STEP 5: DB 연결 종료
    con.close()

makeCsv()