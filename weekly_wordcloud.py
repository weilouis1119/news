import pymysql
import pandas as pd
from datetime import datetime, date
from datetime import timedelta
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import jieba
import jieba.analyse

def wordJieba(news):
    word = []
    for i in news:
        jieba.analyse.set_stop_words('stopWords.txt')
        key_words=jieba.analyse.extract_tags(i, topK=10, withWeight=False, allowPOS=())
        for j in key_words:
            word.append(j)
    return word


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


conn = pymysql.connect(host="localhost",user='name', password='password',db='news', charset='utf8')
sql = 'show tables;'
df = pd.read_sql(sql, conn)

weekago = (date.today() - timedelta(7)).strftime('%Y%m%d')
udn_list = []
free_list = []
chinatimes_list = []
for i in df['Tables_in_news']:
    if 'udn' in i:
        time = i.replace('udn','')[:-2]
        if int(weekago) <= int(time):
            sql = 'select * from %s' % i
            df = pd.read_sql(sql, conn)
            udn_list += df['0'].tolist()
    if 'free' in i:
        time = i.replace('free','')[:-2]
        if int(weekago) <= int(time):
            sql = 'select * from %s' % i
            df = pd.read_sql(sql, conn)
            free_list += df['0'].tolist()
    if 'chinatimes' in i:
        time = i.replace('chinatimes','')[:-2]
        if int(weekago) <= int(time):
            sql = 'select * from %s' % i
            df = pd.read_sql(sql, conn)
            chinatimes_list += df['0'].tolist()

conn.close()


Wordcloud('img/udn_weekly.png', wordJieba(udn_list))
Wordcloud('img/free_weekly.png', wordJieba(free_list))
Wordcloud('img/chinatimes_weekly.png', wordJieba(chinatimes_list))



