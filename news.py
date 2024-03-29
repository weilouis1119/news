import requests
import json
from bs4 import BeautifulSoup
import jieba
import jieba.analyse
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import matplotlib as mpl
from matplotlib import pyplot as plt
from PIL import Image

def chart(types, name):
    dic = {}
    dic = {i :types.count(i) for i in types}
    mpl.rcParams[u'font.sans-serif'] = ['SimHei']
    mpl.rcParams['axes.unicode_minus'] = False
    plt.figure(figsize=(6,6))
    plt.title('新聞類別分析', fontsize=25)
    plt.pie(list(dic.values()),labels=list(dic.keys()),labeldistance = 1.1, startangle = 90, counterclock = False, textprops = {"fontsize" : 12})
    plt.savefig('img/%s_bar.png' % name, transparent=True)

def text_jieba(news):
    word = []
    for i in news:
        jieba.analyse.set_stop_words('stopWords.txt')
        key_words=jieba.analyse.extract_tags(i, topK=10, withWeight=False, allowPOS=())
        for j in key_words:
            word.append(j)
    return word

def Wordcloud(filename, textList, name):
   afterFilter_SpaceSplit = " ".join(textList)    
   wc = WordCloud(mode='RGBA',
                  background_color="rgba(255, 255, 255, 0)",  
                  max_words=500,                 
                  max_font_size=60,           
                  font_path='78992571833.ttc',
                  random_state=42,             
                  prefer_horizontal=5)
   wc.generate(afterFilter_SpaceSplit)
   plt.figure(figsize=(10,8))
   plt.title('%s新聞文字雲' % name, fontsize=40, pad=30)
   plt.imshow(wc)
   plt.axis("off")
   plt.savefig(filename, transparent=True)

# 自由電子報新聞爬蟲
urls = []
titles = []
types = []
headers = {'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}

# 第一頁
res = requests.get('https://news.ltn.com.tw/ajax/breakingnews/all/1', headers=headers)
for i in range(20):
    dic = json.loads(res.text)['data'][i]
    title = dic['title']
    url = dic['url']
    typ = dic['type_cn']
    titles.append(title)
    urls.append(url)
    types.append(typ)
# 第2-6頁
for page in range(2,6):
    res = requests.get('https://news.ltn.com.tw/ajax/breakingnews/all/%s' % str(page), headers=headers)
    dic = json.loads(res.text)['data']
    for i in dic: 
        title = dic[i]['title']
        url = dic[i]['url']
        typ = dic[i]['type_cn']
        if typ == False:
            typ = ''
        urls.append(url)
        titles.append(title)
        types.append(typ)
news = []
for url in urls:
    res = requests.get(url, headers=headers)
    bs = BeautifulSoup(res.text, 'html.parser')
    text = ''
    for i in bs.find('div', class_='text').find_all('p'):
        if '<p class="' not in str(i) and '武漢肺炎專區' not in i.text:
            text += i.text
    news.append(text)
print('free done')

# 中時電子報新聞爬蟲
chinatimes_titles = []
chinatimes_urls = []
chinatimes_types = [] 
for page in range(1,6):
    url = 'https://www.chinatimes.com/realtimenews/?page=%s&chdtv' % str(page)
    res = requests.get(url, headers=headers)
    bs = BeautifulSoup(res.text, 'html.parser')
    for i in bs.find('ul', class_ = 'vertical-list list-style-none').find_all('li'):
        if 'class="odd' not in str(i):
            tag = i.find('h3').find('a')
            title = tag.text
            typ = i.find('div', class_='category').text
            url ='https://www.chinatimes.com' + tag['href']
            chinatimes_titles.append(title)
            chinatimes_urls.append(url)
            chinatimes_types.append(typ)

chinatimes_news=[]
for url in chinatimes_urls[:]:
    text = ''
    res = requests.get(url, headers=headers)
    bs = BeautifulSoup(res.text, 'html.parser')
    tag = bs.find('div', class_ = 'article-body').find_all('p')
    for t in tag:
        text += t.text.replace('\n', '')
    chinatimes_news.append(text)
print('chinatimes done')

# 聯合新聞網新聞爬蟲
udn_titles = []
udn_urls = []
for i in range(1, 6):
    url = 'https://udn.com/api/more?page=%s&id=&channelId=1&cate_id=0&type=breaknews&totalRecNo=12929' % str(i)
    res = requests.get(url, headers=headers)
    for j in range(20):
        dic = json.loads(res.text)['lists'][j]
        title = dic['title']
        url = 'https://udn.com' + dic['titleLink']
        udn_titles.append(title)
        udn_urls.append(url)

udn_news = []
udn_types = []
for url in udn_urls[:]:
    try:
        text = ''
        res = requests.get(url, headers=headers)
        bs = BeautifulSoup(res.text, 'html.parser')
        typ = bs.find('section', class_='article-content__info').find_all('a')[1].text
        tag = bs.find('div', class_ = 'article-content__paragraph').find_all('p')
        for i in tag:
            if '疫情專題' not in i.text:
                text += i.text
        text = text.replace('\n', '')
        udn_news.append(text)
        udn_types.append(typ)       
    except:
        None
print('udn done')

# 存新聞網址及標題
titleFree_df = pd.DataFrame({'title':titles,'url':urls})
titleFree_df.to_csv('title_and_url/free.csv', index=False)

titleChinatimes_df = pd.DataFrame({'title':chinatimes_titles,'url':chinatimes_urls})
titleChinatimes_df.to_csv('title_and_url/chinatimes.csv', index=False)

titleUdn_df = pd.DataFrame({'title':udn_titles,'url':udn_urls})
titleUdn_df.to_csv('title_and_url/udn.csv', index=False)
print('title and url done')

# 類別分析圖表製作
chart(types, 'free')
chart(chinatimes_types, 'chinatimes')
chart(udn_types, 'udn')
print('chart done')

# 斷詞與文字雲製作
Wordcloud('img/free', text_jieba(news), '自由電子報')
Wordcloud('img/chinatimes', text_jieba(chinatimes_news), '中時電子報')
Wordcloud('img/udn', text_jieba(udn_news), '聯合新聞網')
print('word cloud done')

# 連接資料庫
engine = create_engine("mysql+pymysql://name:password@127.0.0.1:3306/news")
nowTime = datetime.now().strftime('%Y%m%d%H')
word_df = pd.DataFrame(news)
word_df.to_sql('free%s' % nowTime, engine, index=False)
print('word to sql done')

chinatimes_df = pd.DataFrame(chinatimes_news)
chinatimes_df.to_sql('chinatimes%s' % nowTime,engine,index=False) 
print('chinatimes word to sql')

udn_df = pd.DataFrame(udn_news)
udn_df.to_sql('udn%s' % nowTime,engine,index=False) 

print('Done')
