import pymysql
import pandas as pd
import re
from datetime import datetime, date
from datetime import timedelta

weekago = int((date.today() - timedelta(7)).strftime('%Y%m%d%H'))

conn = pymysql.connect(host="localhost",user='name', password='password',db='news', charset='utf8')
cursor = conn.cursor()
sql = 'show tables;'
df = pd.read_sql(sql, conn)
for i in df['Tables_in_news']:
    if int(re.search('[0-9]+', i).group()) < weekago:
        sql = 'Drop TABLE %s ' % i
        cursor.execute(sql)
conn.commit()              
conn.close()
