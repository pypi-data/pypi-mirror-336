# anigamerpy 0.2.0
[動畫瘋](https://ani.gamer.com.tw/)爬蟲工具

## 下載
```
pip install anigamerpy
```

## 使用方式
本模組可獲取兩種資料

* 新番資料

即動畫瘋首頁的所有動畫
```python
from anigamerpy import anime
from loguru import logger

data = anime.Anime().new_anime().data

#0為第一筆資料 1為第二筆資料 以此類推
logger.info(data[0]['name']) #動畫名
logger.info(data[0]['watch_count']) #目前觀看次數
logger.info(data[0]['episode']) #目前集數
logger.info('https://ani.gamer.com.tw/' + data[0]['href']) #動畫連結
logger.info(data[0]['image']) #圖片
```

* 搜尋資料

獲取搜尋的結果
```python
from anigamerpy import anime
from loguru import logger

data = anime.Anime().search_anime(keyword='bang dream').data #需加入搜尋關鍵字 請使用字串來搜尋

#0為第一筆資料 1為第二筆資料 以此類推
logger.info(data[0]['name']) #動畫名
logger.info(data[0]['watch_count']) #觀看次數
logger.info(data[0]['episode']) #集數
logger.info(str(data[0]['years'])[3:]) #年分
logger.info('https://ani.gamer.com.tw/' + data[0]['href']) #動畫連結
logger.info(data[0]['image']) #圖片
logger.info(data[0]['tags']) #標籤
```

* 所有動畫

動畫瘋內的所有動畫
參數ID請參考[此Json檔](https://raw.githubusercontent.com/Sakuya0502/anigamerpy/refs/heads/main/anigamerpy/json/allanime_data.json)
```python
from anigamerpy import anime
from loguru import logger

'''
[ 參數 ]
all_anime()內含有許多參數，以下說明各個參數的功能:
1.tags 動畫屬性 需為list list內需為整數ID且最多五項
2.category 動畫類型 需為整數ID
3.target 動畫對象 需為整數ID
4.sort 排列方式 需為整數ID (空值或1為依年份排列 2為依月人氣排序)
5.page 頁數 需為整數 空值為第一頁
[ 提示 ]
1.all_anime()內若為空，則返回所有動畫標籤內第一頁之內容
2.參數可以不用全部都使用，可僅使用其中幾個
3.以上參數若某項為空則代表顯示該頁籤之全部結果
'''
data = anime.Anime().all_anime().data #請參照上方

#0為第一筆資料 1為第二筆資料 以此類推
logger.info(data[0]['name']) #動畫名
logger.info(data[0]['watch_count']) #觀看次數
logger.info(data[0]['episode']) #集數
logger.info(str(data[0]['years'])[3:]) #年分
logger.info('https://ani.gamer.com.tw/' + data[0]['href']) #動畫連結
logger.info(data[0]['image']) #圖片
logger.info(data[0]['tags']) #標籤
```

## 其他
若有發現任何bug或是問題，請開issue

## License
本專案使用 MIT LICENSE

MIT © [Sakuya0502](https://github.com/Sakuya0502/anigamerpy/blob/main/LICENSE)