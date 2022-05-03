# 3.4 Item编写与应用

&emsp;&emsp;在上一小节中，我们只完成了 Spider 代码的一部分编写。本小节将编写Items文件中的代码，同时对 Spider 中的代码进行完善。让我们开始本小节的学习吧！！！

## 3.4.1 Item的介绍

&emsp;&emsp;在编写 Items 文件中的代码前，我们先来了解下 Item。

&emsp;&emsp;爬虫的目的是从网页中提取结构化的数据。在 Scrapy 框架中，Spider 会返回抓取的数据作为键值对的 Item 
对象。Scrapy 框架中有多种类型的Item可以选择。但我们要记住一点，我们编写出的接收 Item 的代码，应该适用于任何 Item 对象类型。下面列出了 
Scrapy 支持 Item 类型。

- Item类型
  - Dictionaries
  - Item objects
  - Dataclass objects
  - attr.s objects

&emsp;&emsp;由于本项目只用到了 Item objects，这里就Item objects具体展开。

&emsp;&emsp;**Item objects** 其实有点像 python 中的字典，官方提供了类似字典的API。括号中为翻译内容，可能不准确，仅供参考。

**class** scrapy.item.Item([arg])

- Item objects replicate the standard dict API, including its __init__ method.
（Item对象复制了标准的dictAPI,包括它的__init__方法。）

- Item allows defining field names, so that: (Item允许定义字段名)

  - KeyError is raised when using 
undefined field names .(当使用未定义的字段名时，将引发KeyError.)
  - Item exporters can export all fields by default even 
     if the first scraped object does not have values for all of
     them(在默认情况下，Item输出器能够输出所有字段，即使第一个抓取的对象没有任何字段值。)

- Item also allows defining field metadata, which can be used to customize serialization.
(Item也允许定义字段元数据，该字段元数据可用于自定义序列化。)

- trackref tracks Item objects to help find memory leaks 
(trackref跟踪Item对象以帮助查找内存泄露。).

Item对象除了提供字典的方法，也提供了以下API：
  - copy()
  - deepcopy()
  - fields 一个字典包含Item对象中所包含的所有字段，不仅仅是被填充的。字典中的键是字段名；值是在item中声明的Field对象。

&emsp;&emsp;上面我们引用了Scrapy官方文档中对Item的介绍，描述中可能有些许错误，具体以官方文档为准。

## 3.4.2 Item的编写
&emsp;&emsp;通过上面的学习，想必你已经了解 Item，现在开始进行编写吧！！！在项目文件夹中找到 items.py 文件并打开。原始代码如下：
  ```python
# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

  ```
&emsp;&emsp;原始代码中，有一个import语句和一个继承了Scrapy.Item对象的TutorialItem类。可以按照TutorialItem
类中给出的代码示例来编写代码。

&emsp;&emsp;还记得第二小节中，我们设定的目标吗？-抓取所有电影的电影名称、上映时间、分类、评分。因此，我们根据需要来定义字段名。下面给出代码
```python
import scrapy

class TutorialItem(scrapy.Item):
    name = scrapy.Field() #定义电影名
    time = scrapy.Field()
    category = scrapy.Field()
    grade = scrapy.Field()
    
```

至此，我们的 items.py 就已经编写完成了，现在让我们把关注点回到 Scrapy 的编写。

## 3.4.3 Item应用与Spider完善

我们希望在spider中使用自定义的 TutorialItem 类，因此要在quotes.py中进行导入。在 quotes.py 中输入下面的代码。
```python
from tutorial.items import TutorialItem
```
然后，在QuotesSpider类下面编写一个parse_detail方法
```python
class QuotesSpider(scrapy.Spider):
    #此处省略。。。。
    def parse_detail(self,response):
        pass
```
我们要使用自定义的Item类，就要进行实例化，然后对定义的字段值赋值。item和字典相似，我们可以用相同的方式进行item赋值。
```python
class QuotesSpider(scrapy.Spider):
    #此处省略。。。。
    def parse_detail(self,response):
        item = TutorialItem()
        item['name'] = response.xpath('//*[@id="detail"]/div[1]/div/div/div[1]/div/div[2]/a/h2/text()').get()
        item['time'] = response.xpath('//*[@id="detail"]/div[1]/div/div/div[1]/div/div[2]/div[3]/span/text()').get()
        item['grade'] = response.xpath('//*[@id="detail"]/div[1]/div/div/div[1]/div/div[3]/p[1]/text()').get()
        item['category'] = response.xpath('//*[@id="detail"]/div[1]/div/div/div[1]/div/div[2]/div[1]//span/text()').getall()
        yield item
```
我们编写xpath语句，为其字段赋值。写好Xpath后，可以使用Scrapy shell进行验证。到这里，整个quotes.py代码编写完毕，本小节的任务也就完成了。完整的代码请点击[完整代码](https://xiaobi891292.github.io/web-crawler/#/codes/ch03/quotes.md)


## 3.4.4 总结

&emsp;&emsp;在本小节中，我们学习 Item,并编写了 item.
py文件，同时也对上一节为编写的内容进行完善。下一小节，我们会将爬取的数据存储到数据库中,并学习Item Pipelines相关知识，编写 pipelines.py 文件。

------- 

- 参考资料：
  - 《pyhon3网络爬虫实战第二版》
  - [Scrapy官方文档](https://docs.scrapy.org/en/2.5/)