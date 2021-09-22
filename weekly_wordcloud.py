import pymysql
import pandas as pd
from datetime import datetime, date
from datetime import timedelta
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def Wordcloud(filename, textList):
    afterFilter_SpaceSplit = " ".join(textList)    
    wc = WordCloud(background_color="white",  
                    max_words=500,                 
                   max_font_size=60,           
                   font_path='78992571833.ttc',
                   random_state=42,             
                   prefer_horizontal=5)
    wc.generate(afterFilter_SpaceSplit)
    plt.figure(figsize=(10,5))
    plt.imshow(wc)
    plt.axis("off")
    plt.savefig(filename)


conn = pymysql.connect(host="localhost",user='louis', password='q7a4z1cc',db='news', charset='utf8')
sql = 'show tables;'
df = pd.read_sql(sql, conn)

weekago = (date.today() - timedelta(7)).strftime('%Y%m%d')
udn_list = []
for i in df['Tables_in_news']:
    if 'udn' in i:
        time = i.replace('udn','')[:-2]
        if int(weekago) <= int(time):
            sql = 'select * from %s' % i
            df = pd.read_sql(sql, conn)
            udn_list += df['0'].tolist()
conn.close()

Wordcloud('udn_weekly.png', udn_list[:500000])



