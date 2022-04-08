# 2.4 基础爬虫案例实战
&emsp;&emsp;
经过前三小节的学习，虽然你学习爬虫工具的使用，但终究没有编写一个完整的爬虫程序。本节内容，你将会看到整个爬虫编写的过程，巩固前面学习的内容。

## 2.4.1 准备工作

- 安装 Rython3.8
- 安装 Requests库
- 安装 Lxml 或者 Beautiful soup
- 安装 Mysql 和 Pymysql

## 2.4.2 爬取目标

&emsp;&emsp;本次实战以静态网页为案例进行爬取，链接为：https://ssr1.scrape.center/。 这是一个关于电影信息的网站

![image-01](../images/chapter02/01.png)

点击电影标题会进入该电影的详情页

![image-02](../images/chapter02/02.png)

我们这次实战的目标是：

1. 利用 Requests 爬取这个站点每一页的电影列表，顺着列表再爬取每个电影的详情页
2. 用 Lxml 或者 Beautiful Soup提取每部电影的名称、封面、类别、上映时间、评分等内容
3. 把以上爬取的内容保存到 MySQL 数据库中

## 2.4.3 爬取列表页

&emsp;&emsp;首先我们需要观察列表页的结构和翻页规则，访问https://ssr1.scrape.center/ 
，按F12打开浏览器开发者工具，在 Elements 中我们可以看到网页的 html 源代码

![image-03](../images/chapter02/03.png)

我们可以看到每一个 class 为 el-card 的 div 标签对应一个电影的页面

![image-04](../images/chapter02/04.png)

鼠标点击开发者工具中的鼠标按钮，在移到点击会跳转进入电影详情页的电影标题位置，可以查看 html 这部分元素

```html
<a data-v-7f856186="" href="/detail/1" class="name">
	<h2 data-v-7f856186="" class="m-b-sm">霸王别姬 - Farewell My Concubine</h2>
</a>
```

你可以看到这对应的是一个 a 标签而且带有 href 属性，这是一个超链接，其中href的值是/detail/1，这是一个相对于网站根目录https
://ssr1.scrape.center/的路径，因此点击这个a标签就会跳转到https://ssr1.scrape.center/detail/1，再看看详情页对应的url也是https://ssr1.scrape.center/detail/1 ,
你多观察多几个条目，你就会发现电影详情页的url都是https://ssr1.scrape.center/detail/+数字 的这种规律。



接下来我们找翻页的逻辑

![image-05](../images/chapter02/05.png)

在翻页处故技重施，我们知道翻页对应的超链接就是https://ssr1.scrape.center/page/+页数 这种套路

总结：

我们知道了访问所有页面的 URL 的构造规律，我们就可以使用 Requests 去请求相应的网站。

不同的分页的 URL 的构造规律：

https://ssr1.scrape.center/page/+页数

电影详情页的 url 的构造规律：

https://ssr1.scrape.center/detail/+数字



## 2.4.3 代码实现

### 2.4.3.1 列表页的爬取

完成列表页的爬取，可以按这两个步骤来实现

1. 遍历所有页码，构造10页的索引页 URL
2. 从每个索引页，分析提取每个电影的详情页 URL

代码如下：

```python
import requests
import logging
from lxml import etree
from urllib.parse import urljoin


# 设置日志等级，具体的用法可以参见官方 logging 文档
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

# 设置基础变量，用大写表示。
BASE_URL = 'https://ssr1.scrape.center' #初始的 url 
TOTAL_PAGE = 10 #总的分页数

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
        # 创建一条事件级别为ERROR的日志记录
        logging.error('get invalid status code %s while scraping %s', response.status_code, url)
    except requests.RequestException:
        #创建一条事件级别为ERROR的日志记录
        logging.error('error occurred while scraping %s', url, exc_info=True)


def scrape_index(page):
    """参数： page
    功能：接收page参数,构造列表页的url，实现对列表页的爬取"""
    index_url = f'{BASE_URL}/page/{page}'
    return scrape_page(index_url)


# 我们知道 a 标签里面的 href 属性与网站的根目录拼接正好是电影详情页的url，因此我们把所有a标签的 href 属性找出来。这里函数的结尾使用了yield，使得函数变成一个迭代器。

def parse_index(html):
    """html：网页的源代码，字符串形式
    功能：实现对列表页的解析，获得电影详情页的 url"""
    #将html字符串转换为可用xpath解析的对象
    tree = etree.HTML(html)  
    
    # 获得列表页中每个电影所对应的div标签
    divs = tree.xpath('//*[@id="index"]/div[1]/div[1]/div')
    for div in divs:
        # 解析网页，获得每个电影的href属性的值，解析后获得的值是个列表。
        href = div.xpath('./div/div/div[1]/a/@href')[0] 
        # 调用 urljoin 方法构造电影详情页的 url 
        detail_url = urljoin(BASE_URL, href)
        logging.info('get detail url %s', detail_url)
        yield detail_ur


def main():
    """根据TOTAL_PAGE进行遍历，logging.info()输出详情页"""
    for page in range(1, TOTAL_PAGE + 1):
        index_html = scrape_index(page)
        detail_urls = parse_index(index_html)
        logging.info('detail urls %s', list(detail_urls))

if __name__ == '__main__':
    main()
```

### 2.4.3.2 详情页爬取

首先我们打开第一个详情页https://ssr1.scrape.center/detail/1

老规矩F12查看源码

先确定我们要爬取的内容

鼠标点击

![image-06](../images/chapter02/06.png)

然后移到想要爬取的内容，单击可查看源码,下面是两个例子，其他的大家可以自行寻找。

封面：

![image-07](../images/chapter02/07.png)




类别：

![image-08](../images/chapter02/08.png)

我们知道每个数据的位置，接下来我们继续编写解析详情页的代码。

```python

def scrape_detail(url):
    """url：详情页的url 
    功能：获得详情页的html代码"""
    return scrape_page(url)


def parse_detail(html):
    """html：详情页的html代码，字符串类型
    功能：解析详情页，返回包含数据的字典"""
    tree = etree.HTML(html)
    #封面的url
    cover_url = tree.xpath(
        '//*[@id="detail"]/div[1]/div/div/div[1]/div/div[1]/a/img/@src')[0]
    #电影的名称
    name = tree.xpath(
        '//*[@id="detail"]/div[1]/div/div/div[1]/div/div[2]/a/h2/text()')[0]
    # 电影的类别
    categories = tree.xpath(
        '//*[@id="detail"]/div[1]/div/div/div[1]/div/div[2]/div[1]//span/text()')
    # 对所获得的电影类别，进行处理
    categories = '-'.join(categories)
    # 电影的上映时间
    published_ats = tree.xpath(
        '//*[@id="detail"]/div[1]/div/div/div[1]/div/div[2]/div[3]/span/text()')
    # 判断电影的上映时间是否为空，如果不为空，则等于本身；否则为空的字符串
    published_at = published_ats if published_ats else ''
    # 评分
    score = tree.xpath(
        '//*[@id="detail"]/div[1]/div/div/div[1]/div/div[3]/p[1]/text()')[0]
    # 除去字符周围的空格
    score = score.strip()

    return {
        'cover': cover_url,
        'name': name,
        'categroies': categories,
        'published_at': published_at,
        'score': score
    }

'''
根据TOTAL_PAGE进行遍历，logging.info()输出数据
'''
def main():
    for page in range(1, TOTAL_PAGE + 1):
        index_html = scrape_index(page)
        detail_urls = parse_index(index_html)
        for detail_url in detail_urls:
            detail_html = scrape_detail(detail_url)
            data = parse_detail(detail_html)
            logging.info('get detail data %s', data)


if __name__ == '__main__':
    main()
```



### 4.3使数据插入Mysql数据库

现在改造一下，使得爬虫的数据插入数据库

```python
import pymysql

def connectDB():
    """ 
        连接本地数据库
    """
    dbhost = "127.0.0.1"
    dbname = "你自己的数据库名"
    dbuser = "your mysql username"
    dbpassword = "your mysql password"
    # 此处添加charset='utf8'是为了在数据库中显示中文，此编码必须与数据库的编码一致
    db = pymysql.connect(host=dbhost, user=dbuser, password=dbpassword, 
                         database = dbname, charset='utf8')
    return db


def create_table():
    """创建电影表"""
    cursor = connectDB().cursor()
    #如果存在 movie 表，则删除
    cursor.execute("DROP TABLE IF EXISTS movie")

    #创建 movie表
    sql = """
        create table movie(
        cover varchar(256),
        name varchar(256),
        categories varchar(256),
        published_at varchar(256),
        score varchar(16));
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
def insert_function(cover, name, categories, published_at,score):
    """将数据插入到数据库中"""
    db_insert = connectDB()
    cursor_insert = db_insert.cursor()
    insert_sql = 'insert into movie (cover, name, categories, published_at,  score)values(%s, %s, %s, %s, %s)'
    cursor_insert.execute(insert_sql, (cover, name, categories, published_at, drama, score))
    DB_insert.commit()
    DB_insert.close()



def main():
    """根据TOTAL_PAGE进行遍历，logging.info()输出数据"""
    create_table()
    for page in range(1, TOTAL_PAGE + 1):
        index_html = scrape_index(page)
        detail_urls = parse_index(index_html)
        for detail_url in detail_urls:
            detail_html = scrape_detail(detail_url)
            data = parse_detail(detail_html)
            insert_function(data['cover'], data['name'], data['categories'], data['published_at'], data['score'])
            logging.info('get detail data %s', data)
        # logging.info('detail urls %s', list(detail_urls))

if __name__ == '__main__':
    main()
```



### 2.4.4 完整代码
&emsp;&emsp;上面我们对整个代码进行分步的实现，下面是完整的代码。

```python
import requests
from lxml import etree
import logging
from urllib.parse import urljoin
import pymysql
from time import sleep
import random

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')

BASE_URL = 'https://ssr1.scrape.center'
TOTAL_PAGE = 10


def scrape_page(url):
    logging.info('scraping %s....', url)
    try:
        sleep(random.randint(1, 5))
        response = requests.get(url)

        if response.status_code == 200:
            return response.text
        logging.error('get invalid status code %s while scraping %s',
                      response.status_code, url)
    except requests.RequestException:
        logging.error('error occurred while scraping %s', url, exc_info=True)


def scrape_index(page):
    index_url = f'{BASE_URL}/page/{page}'
    return scrape_page(index_url)


def parse_index(html):
    tree = etree.HTML(html)
    divs = tree.xpath('//*[@id="index"]/div[1]/div[1]/div')
    for div in divs:
        href = div.xpath('./div/div/div[1]/a/@href')[0]
        detail_url = urljoin(BASE_URL, href)
        logging.info('get detail url %s', detail_url)
        yield detail_url


def scrape_detail(url):
    """获取详情页的html"""
    return scrape_page(url)


def parse_detail(html):
    """提取详情页的数据"""
    tree = etree.HTML(html)
    cover_url =tree.xpath('//*[@id="detail"]/div[1]/div/div/div[1]/div/div[1]/a/img/@src')[0]
    # cover = requests.get(cover_url).content
    name = tree.xpath(
        '//*[@id="detail"]/div[1]/div/div/div[1]/div/div[2]/a/h2/text()')[0]
    categories = tree.xpath(
        '//*[@id="detail"]/div[1]/div/div/div[1]/div/div[2]/div[1]//span/text()')
    categories = '-'.join(categories)
    published_ats = tree.xpath(
        '//*[@id="detail"]/div[1]/div/div/div[1]/div/div[2]/div[3]/span/text()')
    published_at = published_ats if published_ats else ''
    score = tree.xpath(
        '//*[@id="detail"]/div[1]/div/div/div[1]/div/div[3]/p[1]/text()')[0]
    score = score.strip()
    return {'cover'       : cover_url, 'name': name, 'categroies': categories,
            'published_at': published_at, 'score': score,
            }


def connectDB():
    dbhost = "localhost"
    dbName = "xxxx"
    dbuser = "xxxx"
    dbpassword = "xxxxx"
    # 此处添加charset='utf8'是为了在数据库中显示中文，此编码必须与数据库的编码一致
    db = pymysql.connect(host=dbhost, user=dbuser, password=dbpassword,
                         database=dbName, )
    return db


def create_table():
    cursor = connectDB().cursor()
    # 如果存在movie表，则删除
    cursor.execute("DROP TABLE IF EXISTS movie")

    # 创建movie表
    sql = """
        create table movie(
        cover varchar(256),
        name varchar(256),
        categories varchar(256),
        published_at varchar(256),
        score varchar(16));
    """

    try:
        # 执行SQL语句
        cursor.execute(sql)
        print("创建电影表成功")
    except Exception as e:
        print("创建电影表失败：case%s" % e)


def insert_function(cover, name, categories, published_at, score):
    DB_insert = connectDB()
    cursor_insert = DB_insert.cursor()
    insert_sql = 'insert into movie (cover, name, categories, published_at, score) values (%s, %s, %s, %s, %s)'

    cursor_insert.execute(insert_sql,
                          (cover, name, categories, published_at, score))
    DB_insert.commit()
    DB_insert.close()


def main():
    create_table()
    for page in range(1, TOTAL_PAGE + 1):
        index_html = scrape_index(page)
        detail_urls = parse_index(index_html)
        for detail_url in detail_urls:
            detail_html = scrape_detail(detail_url)
            data = parse_detail(detail_html)
            insert_function(data['cover'], data['name'], data['categroies'],
                            data['published_at'], data['score'])


if __name__ == '__main__':
    main()

```