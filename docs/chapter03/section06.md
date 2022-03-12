# 3.6 项目设置与运行
&emsp;&emsp;
我们在上一小节中，我们已经对项目的主体代码已经编写完成。但我们怎么样去运行我们的项目呢？怎样去自定义一些设置呢？本小节，将会为小伙伴们解决这个疑惑。

## 3.6.1项目设置
&emsp;&emsp;
在Scrapy中，我们可以自定义一些设置，以满足于我们的需求。例如，我们在终端不想输出日志，只保留错误信息或者设置请求头又或者时否遵守robots.
txt协议等，这些都可以自定义化。

### 3.6.1.1指定设置
&emsp;&emsp;当我们使用Scrapy时,我们必须告诉Scrapy正在使用那些设置。我们可以使用SCRAPY_SETTINGS_MODULE
。对于SCRAPY_SETTINGS_MODULE的值应该是Python路径语法**myproject.
settings**。同时，设置模块应该在搜索路径上。

### 3.6.1.2使用设置
&emsp;&emsp;我们有不同的方式去更改设置，但不同的方式有不同的优先级。下面将按优先级的顺序进行列出。
- 通过命令行进行设置。
```commandline
scrapy crawl myspider -s LOG_FILE=scrapy.log
```
- 每个爬虫的设置。例如在quotes.py中设置
```python
class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    custom_settings = {
        'SOME_SETTING':'some value',
    }
```
- 在设置模块中设置即在我们创建的项目中的settings.py中进行设置。
- 每个命令的默认设置。
```text
每个Scrapytool命令行都有自己的默认设置，默认设置将覆盖全局设置。
这些命令行工具的命令设置可以在命令类的default_settings属性中指定。
```
- 默认全局设置。
```text
全局的默认设置在scrapy.settings.default_settings模块。
```
### 3.6.1.3内置设置
&emsp;&emsp;在Scrapy中，已经内置了许多设置。由于篇幅和水平的原因，在这里就不再过多介绍。如需深入了解，可以参考[Built-in 
settings reference。](https://docs.scrapy.org/en/2.5/topics/settings.html)

### 3.6.1.4编写设置
&emsp;&emsp;在此次的项目中，我们需要进行自定义设置来满足我们的需求。下面将详细给出。
- USER_AGENT设置
```python
#USER_AGENT = '你自己的浏览器上的USER_AGENT'
```
- ROBOTSTXT_OBEY设置
```python
ROBOTSTXT_OBEY = False #True表示遵守，False表示不遵守
```
- LOG_LEVEL
```python
LOG_LEVEL = 'ERROR'#默认是DEBUG
```
&emsp;&emsp;对于此次项目的设置我们就编写完成了。对于其他的设置，可以根据你的需求进行更改。

## 3.6.2项目运行
&emsp;&emsp;在上面我们已经编写完项目的设置。现在我们就开始运行我们项目吧！！！ 
1. 我们打开命令行，输入以下命令。quotes是我们定义爬虫的名字。
```commandline
scrapy crawl quotes 
```
2. 我们来看下输出的结果。我们先看下不设置LOG_LEVEL时的结果。
``` commandline
2022-03-01 17:53:06 [scrapy.utils.log] INFO: Scrapy 2.5.0 started (bot: tutorial)
2022-03-01 17:53:06 [scrapy.utils.log] INFO: Versions: lxml 4.6.3.0, libxml2 2.9.5, cssselect 1.1.0, parsel 1.6.0, w3lib 1.22.0, Twisted 21.7.0, Pytho
n 3.8.10 (default, May 19 2021, 13:12:57) [MSC v.1916 64 bit (AMD64)], pyOpenSSL 20.0.1 (OpenSSL 1.1.1k  25 Mar 2021), cryptography 3.4.7, Platform Wi
ndows-10-10.0.19042-SP0
2022-03-01 17:53:06 [scrapy.utils.log] DEBUG: Using reactor: twisted.internet.selectreactor.SelectReactor
2022-03-01 17:53:06 [scrapy.crawler] INFO: Overridden settings:
{'BOT_NAME': 'tutorial',
 'NEWSPIDER_MODULE': 'tutorial.spiders',
 'SPIDER_MODULES': ['tutorial.spiders']}
2022-03-01 17:53:06 [scrapy.extensions.telnet] INFO: Telnet Password: dec945a1b95a9a0c
2022-03-01 17:53:06 [scrapy.middleware] INFO: Enabled extensions:
['scrapy.extensions.corestats.CoreStats',
 'scrapy.extensions.telnet.TelnetConsole',
 'scrapy.extensions.logstats.LogStats']
2022-03-01 17:53:06 [scrapy.middleware] INFO: Enabled downloader middlewares:
['scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware',
 'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware',
 'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware',
 'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware',
 'scrapy.downloadermiddlewares.retry.RetryMiddleware',
 'scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware',
 'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware',
 'scrapy.downloadermiddlewares.redirect.RedirectMiddleware',
 'scrapy.downloadermiddlewares.cookies.CookiesMiddleware',
 'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware',
 'scrapy.downloadermiddlewares.stats.DownloaderStats']
2022-03-01 17:53:06 [scrapy.middleware] INFO: Enabled spider middlewares:
['scrapy.spidermiddlewares.httperror.HttpErrorMiddleware',
 'scrapy.spidermiddlewares.offsite.OffsiteMiddleware',
 'scrapy.spidermiddlewares.referer.RefererMiddleware',
 'scrapy.spidermiddlewares.urllength.UrlLengthMiddleware',
 'scrapy.spidermiddlewares.depth.DepthMiddleware']
2022-03-01 17:53:06 [scrapy.middleware] INFO: Enabled item pipelines:
['tutorial.pipelines.TutorialPipeline']
2022-03-01 17:53:06 [scrapy.core.engine] INFO: Spider opened
2022-03-01 17:53:07 [scrapy.extensions.logstats] INFO: Crawled 0 pages (at 0 pages/min), scraped 0 items (at 0 items/min)
2022-03-01 17:53:07 [scrapy.extensions.telnet] INFO: Telnet console listening on 127.0.0.1:6023
2022-03-01 17:53:57 [scrapy.downloadermiddlewares.retry] DEBUG: Retrying <GET https://ssr1.scrape.center/page/3> (failed 1 times): [<twisted.python.fa
ilure.Failure twisted.internet.error.ConnectionLost: Connection to the other side was lost in a non-clean fashion: Connection lost.>]
2022-03-01 17:53:57 [scrapy.downloadermiddlewares.retry] DEBUG: Retrying <GET https://ssr1.scrape.center/page/1> (failed 1 times): [<twisted.python.fa
ilure.Failure twisted.internet.error.ConnectionLost: Connection to the other side was lost in a non-clean fashion: Connection lost.>]
2022-03-01 17:53:57 [scrapy.downloadermiddlewares.retry] DEBUG: Retrying <GET https://ssr1.scrape.center/page/2> (failed 1 times): [<twisted.python.fa
ilure.Failure twisted.internet.error.ConnectionLost: Connection to the other side was lost in a non-clean fashion: Connection lost.>]
2022-03-01 17:53:57 [scrapy.core.engine] DEBUG: Crawled (200) <GET https://ssr1.scrape.center/page/8> (referer: None)
2022-03-01 17:53:57 [scrapy.core.engine] DEBUG: Crawled (200) <GET https://ssr1.scrape.center/page/10> (referer: None)
2022-03-01 17:54:02 [scrapy.core.engine] DEBUG: Crawled (200) <GET https://ssr1.scrape.center/page/1> (referer: None)
2022-03-01 17:54:02 [scrapy.core.engine] DEBUG: Crawled (200) <GET https://ssr1.scrape.center/page/3> (referer: None)
2022-03-01 17:54:02 [scrapy.core.engine] DEBUG: Crawled (200) <GET https://ssr1.scrape.center/page/2> (referer: None)
2022-03-01 17:54:02 [scrapy.core.engine] DEBUG: Crawled (200) <GET https://ssr1.scrape.center/page/9> (referer: None)
2022-03-01 17:54:07 [scrapy.downloadermiddlewares.retry] DEBUG: Retrying <GET https://ssr1.scrape.center/page/5> (failed 1 times): [<twisted.python.fa
ilure.Failure twisted.internet.error.ConnectionLost: Connection to the other side was lost in a non-clean fashion: Connection lost.>]
2022-03-01 17:54:12 [scrapy.extensions.logstats] INFO: Crawled 6 pages (at 6 pages/min), scraped 0 items (at 0 items/min)
2022-03-01 17:54:17 [scrapy.downloadermiddlewares.retry] DEBUG: Retrying <GET https://ssr1.scrape.center/page/6> (failed 1 times): [<twisted.python.fa
ilure.Failure twisted.internet.error.ConnectionLost: Connection to the other side was lost in a non-clean fashion: Connection lost.>]
2022-03-01 17:54:17 [scrapy.downloadermiddlewares.retry] DEBUG: Retrying <GET https://ssr1.scrape.center/page/4> (failed 1 times): [<twisted.python.fa
ilure.Failure twisted.internet.error.ConnectionLost: Connection to the other side was lost in a non-clean fashion: Connection lost.>]
2022-03-01 17:54:17 [scrapy.downloadermiddlewares.retry] DEBUG: Retrying <GET https://ssr1.scrape.center/page/7> (failed 1 times): [<twisted.python.fa
ilure.Failure twisted.internet.error.ConnectionLost: Connection to the other side was lost in a non-clean fashion: Connection lost.>]
2022-03-01 17:55:17 [scrapy.core.engine] DEBUG: Crawled (200) <GET https://ssr1.scrape.center/detail/71> (referer: https://ssr1.scrape.center/page/8)
2022-03-01 17:55:17 [scrapy.core.engine] DEBUG: Crawled (200) <GET https://ssr1.scrape.center/detail/73> (referer: https://ssr1.scrape.center/page/8)
2022-03-01 17:55:32 [scrapy.extensions.logstats] INFO: Crawled 8 pages (at 2 pages/min), scraped 0 items (at 0 items/min)
2022-03-01 17:55:47 [scrapy.downloadermiddlewares.retry] DEBUG: Retrying <GET https://ssr1.scrape.center/page/5> (failed 2 times): [<twisted.python.fa
ilure.Failure twisted.internet.error.ConnectionLost: Connection to the other side was lost in a non-clean fashion: Connection lost.>]
2022-03-01 17:56:17 [scrapy.downloadermiddlewares.retry] DEBUG: Retrying <GET https://ssr1.scrape.center/detail/81> (failed 1 times): [<twisted.python
.failure.Failure twisted.internet.error.ConnectionLost: Connection to the other side was lost in a non-clean fashion: Connection lost.>]
2022-03-01 17:56:17 [scrapy.downloadermiddlewares.retry] DEBUG: Retrying <GET https://ssr1.scrape.center/detail/11> (failed 1 times): [<twisted.python
.failure.Failure twisted.internet.error.ConnectionLost: Connection to the other side was lost in a non-clean fashion: Connection lost.>]
2022-03-01 17:56:17 [scrapy.core.engine] DEBUG: Crawled (200) <GET https://ssr1.scrape.center/detail/91> (referer: https://ssr1.scrape.center/page/10)

2022-03-01 17:56:17 [scrapy.core.engine] DEBUG: Crawled (200) <GET https://ssr1.scrape.center/detail/72> (referer: https://ssr1.scrape.center/page/8)
2022-03-01 17:56:17 [scrapy.core.scraper] DEBUG: Scraped from <200 https://ssr1.scrape.center/detail/73>
{'category': ['剧情'],
 'grade': '8.9',
 'name': '十二怒汉 - 12 Angry Men',
 'time': '1957-04-13 上映'}
2022-03-01 17:56:17 [scrapy.core.scraper] DEBUG: Scraped from <200 https://ssr1.scrape.center/detail/71>
{'category': ['剧情', '家庭', '传记'],
 'grade': '8.9',
 'name': '当幸福来敲门 - The Pursuit of Happyness',
 'time': '2008-01-17 上映'}
2022-03-01 17:56:32 [scrapy.extensions.logstats] INFO: Crawled 10 pages (at 2 pages/min), scraped 2 items (at 2 items/min)
2022-03-01 17:56:48 [scrapy.core.engine] DEBUG: Crawled (200) <GET https://ssr1.scrape.center/detail/21> (referer: https://ssr1.scrape.center/page/3)
2022-03-01 17:56:48 [scrapy.downloadermiddlewares.retry] DEBUG: Retrying <GET https://ssr1.scrape.center/detail/74> (failed 1 times): [<twisted.python
.failure.Failure twisted.internet.error.ConnectionLost: Connection to the other side was lost in a non-clean fashion: Connection lost.>]
2022-03-01 17:57:18 [scrapy.downloadermiddlewares.retry] DEBUG: Retrying <GET https://ssr1.scrape.center/detail/92> (failed 1 times): [<twisted.python
.failure.Failure twisted.internet.error.ConnectionLost: Connection to the other side was lost in a non-clean fashion: Connection lost.>]
2022-03-01 17:57:18 [scrapy.core.scraper] DEBUG: Scraped from <200 https://ssr1.scrape.center/detail/91>
{'category': ['奇幻', '冒险'],
 'grade': '9.0',
 'name': "哈利·波特与魔法石 - Harry Potter and the Sorcerer's Stone",
 'time': '2002-01-26 上映'}
2022-03-01 17:57:18 [scrapy.core.scraper] DEBUG: Scraped from <200 https://ssr1.scrape.center/detail/72>
{'category': ['动画', '奇幻', '冒险'],
 'grade': '8.9',
 'name': '幽灵公主 - もののけ姫',
 'time': '1998-05-01 上映'}
2022-03-01 17:57:33 [scrapy.extensions.logstats] INFO: Crawled 11 pages (at 1 pages/min), scraped 4 items (at 2 items/min)
2022-03-01 17:57:48 [scrapy.downloadermiddlewares.retry] DEBUG: Retrying <GET https://ssr1.scrape.center/page/7> (failed 2 times): [<twisted.python.fa
ilure.Failure twisted.internet.error.ConnectionLost: Connection to the other side was lost in a non-clean fashion: Connection lost.>]
2022-03-01 17:57:48 [scrapy.downloadermiddlewares.retry] DEBUG: Retrying <GET https://ssr1.scrape.center/page/4> (failed 2 times): [<twisted.python.fa
ilure.Failure twisted.internet.error.ConnectionLost: Connection to the other side was lost in a non-clean fashion: Connection lost.>]
2022-03-01 17:57:48 [scrapy.core.scraper] DEBUG: Scraped from <200 https://ssr1.scrape.center/detail/21>
{'category': ['西部', '冒险'],
 'grade': '9.1',
 'name': '黄金三镖客 - Il buono, il brutto, il cattivo.',
 'time': '1966-12-23 上映'}
2022-03-01 17:58:28 [scrapy.extensions.logstats] INFO: Crawled 11 pages (at 0 pages/min), scraped 5 items (at 1 items/min)
2022-03-01 17:58:38 [scrapy.downloadermiddlewares.retry] DEBUG: Retrying <GET https://ssr1.scrape.center/page/6> (failed 2 times): [<twisted.python.fa
ilure.Failure twisted.internet.error.ConnectionLost: Connection to the other side was lost in a non-clean fashion: Connection lost.>]
2022-03-01 17:58:38 [scrapy.core.engine] DEBUG: Crawled (200) <GET https://ssr1.scrape.center/detail/82> (referer: https://ssr1.scrape.center/page/9)
2022-03-01 17:58:38 [scrapy.downloadermiddlewares.retry] DEBUG: Retrying <GET https://ssr1.scrape.center/detail/75> (failed 1 times): [<twisted.python
.failure.Failure twisted.internet.error.ConnectionLost: Connection to the other side was lost in a non-clean fashion: Connection lost.>]
2022-03-01 17:58:38 [scrapy.downloadermiddlewares.retry] DEBUG: Retrying <GET https://ssr1.scrape.center/detail/22> (failed 1 times): [<twisted.python
.failure.Failure twisted.internet.error.ConnectionLost: Connection to the other side was lost in a non-clean fashion: Connection lost.>]
2022-03-01 17:58:38 [scrapy.downloadermiddlewares.retry] DEBUG: Retrying <GET https://ssr1.scrape.center/detail/12> (failed 1 times): [<twisted.python
.failure.Failure twisted.internet.error.ConnectionLost: Connection to the other side was lost in a non-clean fashion: Connection lost.>]
2022-03-01 17:58:38 [scrapy.downloadermiddlewares.retry] DEBUG: Retrying <GET https://ssr1.scrape.center/detail/1> (failed 1 times): User timeout caus
ed connection failure: Getting https://ssr1.scrape.center/detail/1 took longer than 180.0 seconds..
2022-03-01 17:58:58 [scrapy.core.scraper] DEBUG: Scraped from <200 https://ssr1.scrape.center/detail/82>
{'category': ['喜剧', '科幻', '动画'],
 'grade': '9.0',
 'name': '机器人总动员 - WALL·E',
 'time': '2008-06-27 上映'}
 .......由于篇幅原因，就不再给出。
 2022-03-01 18:02:46 [scrapy.core.engine] INFO: Spider closed (finished)
```
3. 现在看下设置LOG_LEVEL的结果。

```commandli
PS D:\web-crawler\codes\ch03\tutorial>
```
&emsp;&emsp;在上面我们可以看到控制台没有输出任何信息，说明没有报错。因此我们在进行项目运行时，可以设置日志等级为error
。在进行项目调试是，我们可以采取默认的等级，通过日志信息，来帮助我们来了解项目的运行情况。


## 3.6.4小结
&emsp;&emsp;在本小节中，我们简单学习了项目的设置，并对项目的设置进行自定义化。同时，并运行了项目，查看运行的结果。不知道大家学会了没？


- 参考资料
  - [Scrapy官方文档](https://docs.scrapy.org/en/2.5/)