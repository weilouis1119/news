# 說明：固定時間爬取即時新聞製成文字雲，用flask架構網站，並租用AWS EC2 來部署網站

# 文件說明：

news.py : 爬取新聞內容、斷詞製作文字雲、將斷詞結果放入資料庫，待日後使用

app.py : flask 

template : 放html的資料夾

requiriments.txt : 使用套件及版本

free.csv、chinatimes.csv、udn.csv : 前100則新聞標題及網址

free.png、chinatimes.png、udn.png : 前100則新聞標題及網址
