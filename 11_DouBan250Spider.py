# 程序功能：爬取豆瓣读数TOP250的数据
# 原创作者: @马哥python说
import requests  # 发送请求
from bs4 import BeautifulSoup  # 解析网页
import pandas as pd  # 存取csv
from time import sleep  # 等待时间

book_name = []  # 书名
book_url = []  # 书籍链接
book_star = []  # 书籍评分
book_star_people = []  # 评分人数
book_author = []  # 书籍作者
book_translater = []  # 书籍译者
book_publisher = []  # 出版社
book_pub_year = []  # 出版日期
book_price = []  # 书籍价格
book_comment = []  # 一句话评价


def get_book_info(url, headers):
	"""
	获取豆瓣书籍详情数据
	:param url: 爬取地址
	:param headers: 爬取请求头
	:return: None
	"""
	res = requests.get(url, headers=headers)
	soup = BeautifulSoup(res.text, 'html.parser')
	for book in soup.select('.item'):
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

		# 没有一句话评价，比如倒数第二名，君主论
		if book.select('.quote span'):
			book_comment.append(book.select('.quote span')[0].text)
		else:
			book_comment.append(None)

		info = book.select('.pl')[0].text.split('/')
		if len(info) == 5:  # 正常情况
			book_author.append(info[0])
			book_translater.append(info[1])
			book_publisher.append(info[2])
			book_pub_year.append(info[3])
			book_price.append(str(info[4]))
		elif len(info) == 4:  # 没有译者，比如：第一名，红楼梦
			book_author.append(info[0])
			book_translater.append(None)
			book_publisher.append(info[1])
			book_pub_year.append(info[2])
			book_price.append(str(info[3]))
		elif len(info) == 6:  # 有2个价格，比如：第一页，福尔摩斯探案全集（上中下）
			book_author.append(info[0])
			book_translater.append(info[1])
			book_publisher.append(info[2])
			book_pub_year.append(info[3])
			book_price.append(str(info[4]) + '/' + str(info[5]))
		elif len(info) == 3:  # 没有作者，且没有译者，比如：第5页，十万个为什么
			book_author.append(None)
			book_translater.append(None)
			book_publisher.append(info[0])
			book_pub_year.append(info[1])
			book_price.append(str(info[2]))
		else:
			pass


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
	df.to_csv(csv_name, encoding='utf_8_sig')  # 将数据保存到csv文件


if __name__ == "__main__":
	# 定义一个请求头
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
	# 开始爬取豆瓣数据
	for i in range(10):  # 爬取共10页，每页25条数据
		page_url = 'https://book.douban.com/top250?start={}'.format(str(i * 25))
		print('开始爬取第{}页，地址是:{}'.format(str(i + 1), page_url))
		get_book_info(page_url, headers)
		sleep(2)  # 等待2秒
	# 保存到csv文件
	save_to_csv(csv_name="BookDouban250.csv")
