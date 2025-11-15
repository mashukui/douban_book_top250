# 一、爬虫对象-豆瓣读书TOP250
今天我们分享一期python爬虫案例讲解。爬取对象是，豆瓣读书TOP250排行榜数据：
https://book.douban.com/top250
​![豆瓣网页](https://img2023.cnblogs.com/blog/2864563/202306/2864563-20230629144119465-2121319967.png)

开发好python爬虫代码后，爬取成功后的csv数据，如下：
​![结果数据](https://img2023.cnblogs.com/blog/2864563/202306/2864563-20230629144139765-1246817392.png)

代码是怎样实现的爬取呢？下面逐一讲解python实现。

# 二、python爬虫代码讲解
首先，导入需要用到的库：
```python
import requests  # 发送请求
from bs4 import BeautifulSoup  # 解析网页
import pandas as pd  # 存取csv
from time import sleep  # 等待时间
```
然后，向豆瓣读书网页发送请求：
```python
res = requests.get(url, headers=headers)
```
利用BeautifulSoup库解析响应页面：
```python
soup = BeautifulSoup(res.text, 'html.parser')
```
用BeautifulSoup的select函数，（css解析的方法）编写代码逻辑，部分核心代码：
```python
name = book.select('.pl2 a')[0]['title']  # 书名
book_name.append(name)
bkurl = book.select('.pl2 a')[0]['href']  # 书籍链接
book_url.append(bkurl)
star = book.select('.rating_nums')[0].text  # 书籍评分
book_star.append(star)
star_people = book.select('.pl')[1].text  # 评分人数
star_people = star_people.strip().replace(' ', '').replace('人评价', '').replace('(\n', '').replace('\n)',
                                                                                                 '')  # 数据清洗
book_star_people.append(star_people)
```
最后，将爬取到的数据保存到csv文件中：
```python
def save_to_csv(csv_name):
	"""
	数据保存到csv
	:return: None
	"""
	df = pd.DataFrame()  # 初始化一个DataFrame对象
	df['书名'] = book_name
	df['豆瓣链接'] = book_url
	df['作者'] = book_author
	df['译者'] = book_translater
	df['出版社'] = book_publisher
	df['出版日期'] = book_pub_year
	df['价格'] = book_price
	df['评分'] = book_star
	df['评分人数'] = book_star_people
	df['一句话评价'] = book_comment
	df.to_csv(csv_name, encoding='utf8')  # 将数据保存到csv文件
```
其中，把各个list赋值为DataFrame的各个列，就把list数据转换为了DataFrame数据，然后直接to_csv保存。
这样，爬取的数据就持久化保存下来了。

# 三、讲解视频
同步讲解视频：[【python爬虫】利用python爬虫爬取豆瓣读书TOP250的数据！](https://www.zhihu.com/zvideo/1464515550177546240)

# 四、作者声明

本源码首发公众号“**老男孩的平凡之路**”，后台回复“**豆瓣读书250**”免费即可获取。![二维码-公众号放底部](https://github.com/user-attachments/assets/74c114a1-bc14-4561-8c79-7c7290c960f2)

源码免费开源。如对你有帮助，请给项目点个star✨，或者打赏作者。

用户的支持将是我持续创作的最大动力！<img width="1528" height="918" alt="收款码v2" src="https://github.com/user-attachments/assets/0dab2a08-d7e0-4cc7-af5d-bd197107fb2a" />


____
我是 [@马哥python说](https://github.com/mashukui) ，一名10年程序猿，持续分享python干货中！
