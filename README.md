# 定時爬取即時新聞製成文字雲，用flask架構網站，並租用AWS EC2 來部署網站

# 網頁呈現：

http://35.76.188.119:8080/

# 功能描述：

1.使用requests+bs4 爬取自由、中時、聯合三家新聞網的即時新聞。其中自由、聯合網頁使用ajax技術，因此直接去抓存放資料的網址。

2.python 連接 mysql資料庫，將斷詞結果存到資料庫中，待日後擴充使用，ex:製作一週新聞文字雲

3.使用jieba對新聞內容斷詞並製作文字雲

4.使用Flask將文字雲、新聞標題放上網頁

5.租用AWS EC2 虛擬機，來部署網站

# 文件說明：

news.py : 爬取新聞內容、斷詞製作文字雲、將斷詞結果放入資料庫，待日後使用

app.py : flask 

template : 放html的資料夾

stopWosrd.txt : 停用詞，放斷詞後無意義的詞彙，ex：你、我、儘管、也許等

requirements.txt : 使用套件及版本

free.csv、chinatimes.csv、udn.csv : 前100則新聞標題及網址

free.png、chinatimes.png、udn.png : 即時文字雲圖檔

free_chart.png、chinatimes_chart.png、udn_chart.png 新聞分類圖檔

