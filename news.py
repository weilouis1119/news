import requests
import json
from bs4 import BeautifulSoup
import jieba
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 自由
urls = []
titles = []
headers = {'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}

#第一頁
res = requests.get('https://news.ltn.com.tw/ajax/breakingnews/world/1', headers=headers)
for i in range(20):
    dic = json.loads(res.text)['data'][i]
    title = dic['title']
    url = dic['url']
    titles.append(title)
    urls.append(url)
#第2-6頁
for page in range(2,6):
    res = requests.get('https://news.ltn.com.tw/ajax/breakingnews/world/%s' % str(page), headers=headers)
    dic = json.loads(res.text)['data']
    for i in dic:
        title = dic[i]['title']
        url = dic[i]['url']
        urls.append(url)
        titles.append(title)

news = []
for url in urls:
    res = requests.get(url, headers=headers)
    bs = BeautifulSoup(res.text, 'html.parser')
    text = ''
    for i in bs.find('div', class_='text boxTitle boxText').find_all('p'):
        if '<p class="' not in str(i) and '武漢肺炎專區' not in i.text:
            text += i.text
    
    news.append(text)
# 讀入停用詞檔
stopWords = []
with open('stopWords.txt', 'r', encoding='UTF-8') as file:
    for data in file.readlines():
        data = data.strip()
        stopWords.append(data)

word = []
for i in range(len(news)):
    for j in jieba.cut(news[i], cut_all=False, HMM=True):
        if j not in stopWords:
            word.append(j)
print('free done')
# 中時

chinatimes_titles = []
chinatimes_urls = [] 
for page in range(1,6):
    url = 'https://www.chinatimes.com/realtimenews/?page=%s&chdtv' % str(page)
    res = requests.get(url, headers=headers)
    bs = BeautifulSoup(res.text, 'html.parser')
    for i in bs.find('ul', class_ = 'vertical-list list-style-none').find_all('li'):
        if 'class="odd' not in str(i):
            tag = i.find('h3').find('a')
            title = tag.text
            url ='https://www.chinatimes.com' + tag['href']
            chinatimes_titles.append(title)
            chinatimes_urls.append(url)

chinatimes_news = []
for url in chinatimes_urls[:]:
    text = ''
    res = requests.get(url, headers=headers)
    bs = BeautifulSoup(res.text, 'html.parser')
    tag = bs.find('div', class_ = 'article-body').find_all('p')
    for t in tag:
        text += t.text.replace('\n', '')
    chinatimes_news.append(text)
        



chinatimes_word = []
for i in range(len(chinatimes_news)):
    for j in jieba.cut(chinatimes_news[i], cut_all=False, HMM=True):
        if j not in stopWords:
            chinatimes_word.append(j)
print('chinatimes done')

# 聯合

# In[55]:


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


# In[57]:


udn_news = []
for url in udn_urls[:]:
    try:
        text = ''
        res = requests.get(url, headers=headers)
        bs = BeautifulSoup(res.text, 'html.parser')
        tag = bs.find('div', class_ = 'article-content__paragraph').find_all('p')
        for i in tag:
            if '疫情專題' not in i.text:
                text += i.text
        text = text.replace('\n', '')
        udn_news.append(text)       
    except:
        None


# In[65]:


udn_word = []
for i in range(len(udn_news)):
    for j in jieba.cut(udn_news[i], cut_all=False, HMM=True):
        if j not in stopWords:
            udn_word.append(j)

print('udn done')

titleFree_df = pd.DataFrame({'title':titles,'url':urls})
titleFree_df.to_csv('free.csv', index=False)

titleChinatimes_df = pd.DataFrame({'title':chinatimes_titles,'url':chinatimes_urls})
titleChinatimes_df.to_csv('chinatimes.csv', index=False)

titleUdn_df = pd.DataFrame({'title':udn_titles,'url':udn_urls})
titleUdn_df.to_csv('udn.csv', index=False)
print('title and url done')

# wordcloud
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

Wordcloud('free', word)
Wordcloud('chinatimes', chinatimes_word)
Wordcloud('udn', udn_word)
print('word cloud done')
engine = create_engine("mysql+pymysql://louis:q7a4z1cc@127.0.0.1:3306/news")
nowTime = datetime.now().strftime('%Y%m%d%H')
word_df = pd.DataFrame(word)
word_df.to_sql('free%s' % nowTime, engine, index=False)
print('word to sql done')

nowTime = datetime.now().strftime('%Y%m%d%H')
chinatimes_df = pd.DataFrame(chinatimes_word)
chinatimes_df.to_sql('chinatimes%s' % nowTime,engine,index=False) 
print('chinatimes word to sql')

nowTime = datetime.now().strftime('%Y%m%d%H')
udn_df = pd.DataFrame(udn_word)
udn_df.to_sql('udn%s' % nowTime,engine,index=False) 

print('Done')



