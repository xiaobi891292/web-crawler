# 3.6 项目设置与运行
&emsp;&emsp;
在上一小节中，我们完成了对项目主体代码的编写。但我们怎么样去运行项目？怎样去自定义一些设置呢？本小节将会为你解决这个疑惑。

## 3.6.1项目设置
&emsp;&emsp;
在Scrapy中，可以自定义一些设置，以满足于我们的需求。例如，我们在终端不想输出日志，只保留错误信息，又或者爬虫是否遵守robots.txt协议等，这些都可以自定义化。

### 3.6.1.1指定设置
&emsp;&emsp;使用Scrapy时,可以通过SCRAPY_SETTINGS_MODULE来告诉Scrapy哪些设置正在被使用。SCRAPY_SETTINGS_MODULE的值应该是Python路径语法**myproject.
settings**。同时，设置模块应该在搜索路径上。

### 3.6.1.2使用设置
&emsp;&emsp;scrapy中的设置更改有着不同的方法，这些方法优先级不同。下面根据优先级列出了方法。
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
- 在设置模块（settings.py）中设置。
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
&emsp;&emsp;此次项目中，我们自定义了以下设置来满足我们的需求。
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
``` text
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
由于篇幅原因，内容不再一一列出
 2022-03-01 18:02:46 [scrapy.core.engine] INFO: Spider closed (finished)
 
```

3. 现在看下设置LOG_LEVEL的结果。
	```commandline
	D:\web-crawler\codes\ch03\tutorial>
	```
&emsp;&emsp;在上面我们可以看到，控制台没有输出任何信息，说明没有报错。因此我们在进行项目运行时，可以设置日志等级为error
。在进行项目调试时，可以采取默认的等级，通过日志信息，帮助我们了解项目的运行情况。


## 3.6.4小结
&emsp;&emsp;在本小节中，我们简单学习了项目的设置，对项目的设置进行自定义化。同时，运行项目并查看运行结果。不知道大家学会了没？


- 参考资料
  - [Scrapy官方文档](https://docs.scrapy.org/en/2.5/)
