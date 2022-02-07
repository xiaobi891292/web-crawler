import requests
import logging
import re
from urllib.parse import urljoin
import pymysql
import multiprocessing


'''
定义基础变量
设置日志等级和日志格式
'''
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

BASE_URL = 'https://ssr1.scrape.center'
TOTAL_PAGE = 10

'''
判断状态码是否是200，如果是，直接返回页面的HTML代码，如果不是，则输出错误日志信息
同时实现了requests库的异常处理，在logging库中error方法里设置了exc_info=True，可以打印出Traceback错误堆栈信息
'''
def scrape_page(url):
    logging.info('scraping %s...', url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        # 创建一条严重级别为ERROR的日志记录
        logging.error('get invalid status code %s while scraping %s', response.status_code, url)
    except requests.RequestException:
        #创建一条严重级别为ERROR的日志记录
        logging.error('error occurred while scraping %s', url, exc_info=True)

'''
接收page参数，实现列表页URL拼接，同时调用scrape_page()函数实现页面爬取
'''
def scrape_index(page):
    index_url = f'{BASE_URL}/page/{page}'
    return scrape_page(index_url)

'''
我们先前指导知道a标签里面的href属性与网站的根目录拼接正好是电影详情页的url
因此我们用正则把所有a标签的href属性找出来
<a.*?href="(.*?)".*?class="name">
.*?是非贪婪匹配任意字符，也就是找上面那种格式中()内的内容
使用re.findall()找到html内所有匹配的值
这里函数的结尾使用了yield，使得函数变成一个对象，一个迭代器
'''
def parse_index(html):
    pattern = re.compile('<a.*?href="(.*?)".*?class="name">')
    items = re.findall(pattern, html)
    if not items:
        return []
    for item in items:
        detail_url = urljoin(BASE_URL, item)
        logging.info('get detail url %s', detail_url)
        yield detail_url

'''
获取html页面
'''
def scrape_detail(url):
    return scrape_page(url)

'''
根据正则表达式提取所需数据
返回数据字典
'''
def parse_detail(html):
    cover_pattern = re.compile('class="item.*?<img.*?src="(.*?)".*?class="cover">', re.S)
    cover = re.search(cover_pattern, html).group(1).strip() if re.search(cover_pattern, html) else None

    name_pattern = re.compile('<h2.*?class="m-b-sm">(.*?)</h2>')
    name = re.search(name_pattern, html).group(1).strip() if re.search(name_pattern, html) else None

    categories_pattern = re.compile('<button.*?category.*?<span>(.*?)</span>', re.S)
    categories = re.findall(categories_pattern, html) if re.findall(categories_pattern, html) else []

    published_at_pattern = re.compile('(\d{4}-\d{2}-\d{2})\s?上映')
    published_at = re.search(published_at_pattern, html).group(1).strip() if re.search(published_at_pattern, html) else None

    drama_pattern = re.compile('<div.*?class="drama".*?<p.*?>(.*?)</p>', re.S)
    drama = re.search(drama_pattern, html).group(1).strip() if re.search(drama_pattern, html) else None

    score_pattern = re.compile('<p.*?score.*?>(.*?)</p>', re.S)
    score = re.search(score_pattern, html).group(1).strip() if re.search(score_pattern, html) else None

    return {
        'cover': cover,
        'name': name,
        'categories': str(categories),
        'published_at': published_at,
        'drama': drama,
        'score': score
    }

'''
0、本地mysql建立cui_spider数据库
1、连接本地数据库
2、建立游标
'''
def connectDB():
    dbhost = "127.0.0.1"
    dbName = "cui_spider"
    dbuser = "root"
    dbpassword = "Tywlcyj_12$%"
    # 此处添加charset='utf8'是为了在数据库中显示中文，此编码必须与数据库的编码一致
    db = pymysql.connect(host=dbhost, user=dbuser, password=dbpassword, database = dbName, charset='utf8')
    return db

'''
创建电影表
'''
def create_table():
    cursor = connectDB().cursor()
    #如果存在student表，则删除
    cursor.execute("DROP TABLE IF EXISTS movie")

    #创建student表
    sql = """
        create table movie(
        cover varchar(256),
        name varchar(256),
        categories varchar(256),
        published_at varchar(256),
        drama varchar(2048),
        score varchar(10));
    """

    try:
        # 执行SQL语句
        cursor.execute(sql)
        print("创建电影表成功")
    except Exception as e:
        print("创建电影表失败：case%s"%e)

'''
写一个插入函数
'''
def insert_function(cover, name, categories, published_at, drama, score):
    DB_insert = connectDB()
    cursor_insert = DB_insert.cursor()
    insert_sql = 'insert into movie (cover, name, categories, published_at, drama, score)values(%s, %s, %s, %s, %s, %s)'
    cursor_insert.execute(insert_sql, (cover, name, categories, published_at, drama, score))
    DB_insert.commit()
    DB_insert.close()


'''
根据TOTAL_PAGE进行遍历，logging.info()输出数据
'''
def main(page):
    index_html = scrape_index(page)
    detail_urls = parse_index(index_html)
    for detail_url in detail_urls:
        detail_html = scrape_detail(detail_url)
        data = parse_detail(detail_html)
        insert_function(data['cover'], data['name'], data['categories'], data['published_at'], data['drama'], data['score'])
        logging.info('get detail data %s', data)

if __name__ == '__main__':
    create_table()
    pool = multiprocessing.Pool()
    pages = range(1, TOTAL_PAGE + 1)
    pool.map(main, pages)
    pool.close()
    pool.join()