# 3.3 Spiders编写

&emsp;&emsp;上一小节，我们创建了项目文件夹。项目文件夹中有如下五个文件：quotes.py、items.py、middlewares.py、pipelines.py、settings.py.本小节，主要为大家介绍并编写此部分的代码。

## 3.3.1 初识spiders

&emsp;&emsp;我们先看下quotes.py文件的内容。新建的初始文件内容如下：
```python
import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.com']
    start_urls = ['http://quotes.com/']

    def parse(self, response):
        pass

```
&emsp;&emsp;在quotes.py文件里，Scrapy 已经自动生成了一些内容。 QuotesSpider 继承了 Scrapy.Spider 的类，类中有三个属性，一个方法。

- **name**: 你自己的指定的爬虫名，在命令行中已经指定了。这个属性的值必须是唯一的。
- **allowed_domains**: 一个可选的字符串列表，其中包含允许爬取的域名。如果初始或后续的请求链接不是这个域名下的，则请求会被过滤。
- **start_urls**: 一个 url 列表，Spider 将从此列表中的 url 开始爬取。初始的请求由它来定义。
- **parse**：parse是Spider的一个默认方法。不指定处理方法时，则默认被调用用来处理Response。


## 3.3.2 Spider类再认识
&emsp;&emsp;经过上面的学习，相信你对 Spider 已经有了一些认识。但如果想要实现自己的需求，我们还需要充分了解下 Spider类。

&emsp;&emsp;**Spider类定义了如何抓取某个网站，包括如何抓取（是否要follow
链接）和如何提取结构化数据。换句话说，Spider是你定义抓取和分析特定网站的地方。**

&emsp;&emsp;Spider整个抓取过程如下：

  1. 生成初始请求，抓取第一个url（start_urls中的），并对该请求的响应指定回调函数。

  2. 在回调函数内，解析响应网页并返回Items对象、Request对象、或者可迭代的Items、Requests 对象。 返回的 Requests（可能包含相同的回调函数）由Scrapy下载，然后由指定的回调函数处理该 Request 的响应。

  3. 在回调函数中，我们可以使用 Selectors(Scrapy中自带的对象，在后面会介绍。)，也可以使用 Lxml、Beautiful soup4等，提取结构化数据，返回一个Item。

  4. 最后，存储Spider返回的Items。它可以存储在数据库中，也可以通过Feed Exports等形式存入文件。

&emsp;&emsp;循环以上步骤，我们就可以完成一个网站的爬取。接下来，让我们详细地看下Spider类

> class scrapy.spiders.Spider

&emsp;&emsp;这是最基础的 Spider 类,所有其他的 Spider （自己写的和Scrapy提供的）都需要继承此 Spider类。它不提供任何特殊的功能。它只提供了一个默认的 **start_requests方法** 实现。该方法从 **start_urls** 属性中发送 Request，并为每个响应对象调用回调方法。下面是Spider类的属性和方法的简略介绍。具体使用和介绍，请查看Scrapy官方文档。
- **name**: **str**， 定义爬虫名字。
- **allowed_domains**：**list**，是由允许抓取的站点的字符串组成的列表。
- **start_urls**：**list**，Spider 定义开始抓取的url的列表，初始请求从这里生成。
- **custom_settings**：**dict** 定义本Spider
  的设置，此设置会覆盖项目的全局设置，而此设置必须在初始化前被更新，所以它必须定义成类变量。
- **crawler**：该属性由from_crawler()
  类方法在初始化类后设置的。Crawler 对象中包含了很多项目组件，利用它我们可以获取项目的配置信息。
- **settings**：一个 Settings 对象，利用它我们可以直接获取项目的全局设置变量。
- **logger**：该属性用 Spider的名字创建 python 日志。你可以使用它发送日志信息。
- **from_crawler(crawler, \*args, \*\*kwargs)**
  ：此方法是Scrapy用来创建Spider的类方法。
- **start_requests()**：此方法用于生成初始请求，使用start_urls里面的url来构造Request。默认是GET请求，如果使用POST请求，我们需要重写此方法。
- **parse(response)**：此方法是 Scrapy 处理 Response 的默认回调。
- **log(message[, level, component])**：此方法通过Scrapy日志记录器记录日志信息。
- **closed(reason)**：Spider关闭时，该方法会被调用。

&emsp;&emsp;上面是此类的所有属性和方法。Scrapy中还提供了一些Spider
类，用于处理特殊的情况。具体的用法就不再介绍了，小伙伴们可以自行学习。

## 3.3.3 代码编写

&emsp;&emsp;我们使用的爬虫网站为https://ssr1.scrape.center/,
在第二章中，我们就已经见到这个网站，同时分析了该网站的url
构成规则。在这里就不过多介绍了，我们直接上代码！！！
```python
import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.com']
    start_urls = ['http://quotes.com/']

    def parse(self, response):
        pass

```
&emsp;&emsp;在这里，我们设置 allow_domains 为ssr1.scrape.center,由于需要获取整个网站全部电影的详情页，我们对 start_requests 方法进行重写。

```python
import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['ssr1.scrape.center']
    base_url = 'https://ssr1.scrape.center'
    max_page = 10  # 由于我们网页的最大页数是10

    def start_requests(self):
        """实现翻页功能，手动发起请求。"""
        for i in range(1, self.max_page + 1):
            url = f'{self.base_url}/page/{i}'  # 构建每页的url，实现翻页功能。
            yield Request(url=url, callback=self.parse_index) #手动发起请求。

```
&emsp;&emsp;这时Spider已经实现了翻页的功能，每一页面所对应的url都获得一个响应，同时使用所对应parse_index()方法解析每个页面。接下来，编写parse_index()方法。这里使用 Xpath 语法进解析，你也可以用 CSS 选择器来进行解析。
```python
import scrapy
class QuotesSpider(scrapy.Spider):
    #---此处代码与上面相同，不再给出。---
    def parse_index(self,response):
        """解析页面，获得页面中每个电影的链接，并发起请求"""
        #使用下xpath获取所有含有属性为href的标签
        hrefs =  response.xpath('//*[@id="index"]/div[1]/div[[1]/div//a/@href')
        #遍历所所得href属性值的标签，使用getall()方法获得其值，否则是一个选择器对象列表。
        for href in hrefs.getall():
            #使用urljoin方法拼接完整的url
            new_url = response.urljoin(href)
            # 手动发起请求，并调用parse_page方法
            yield Request(url=new_url,callback=self.
                          parse_page)

```
&emsp;&emsp;上面我们实现了 parse_index() 方法，获取了href的值，并形成完整的url。通过手动发起请求，对所对应的响应调用parse_page()方法。我们在写 Xpath 和 Css 时，可以借助浏览器开发者工具。在编写后，为验证其语句的正确性，可以使用 Scrapy shell 来进行验证。下面将给出具体的用法。

1. 在终端中输入下面的命令激活 Scrapy 命令行工具。

```commandline
scrapy shell
```
2. 使用fetch(url)函数。

```python
fetch(需要测试的url)
```

3. 输入 Xpath 或者 Css 语句。以上面的选取内容为例。
```python
hrefs = response.xpath('//*[@id="index"]/div[1]/div[[1]/div//a/@href')
```

4. 查看结果是否与预期相符合。根据需要进行更改。

&emsp;&emsp;好了，我们 parse_index() 方法已经编写完成了，同时还学习了scrapy shell的简单使用。 Scrapy shell 具体的使用方法可以查看Scrapy的官方文档，这里不多叙述。Scrapy shell 工具对项目中代码的调式还是很好的，希望大家能够掌握！！！

&emsp;&emsp;
本节完成了Spider 的部分编写，因为下面部分的编写会涉及到其他内容，我们在下一节中继续。在下一个小节中，我们就会完成整个 Spider 的编写。

## 3.3.4 总结

&emsp;&emsp;
在本小节中，我们介绍了Spider类的属性和方法，同时并编写了一部分代码。还简单介绍了Scrapy shell的使用。不知道大家学会了吗？

-------
- 参考资料
  - 《python3网络爬虫开发实战第二版》
  - Scrapy官方文档
