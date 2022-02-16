# 3.4 Item编写与应用

&emsp;&emsp;在上一小节中，我们只完成了Spider
代码的一部分编写。我们学完本小节，我们将编写Items文件中的代码同时对spider
中的代码进行完善。让我们开始本小节的学习吧！！！

## 3.4.1 Item的介绍

&emsp;&emsp;在编写Items文件中的代码前，我们需要了解下Item。现在将为大家进行介绍。

&emsp;&emsp;爬虫的目标就是从网页中提取结构化的数据。而在Scrapy框架中，Spider
将会返回一个将抓取的数据作为键值对的Item对象。在Scrapy框架中，有多种类型的Item
可以选择。但我们要记住一点，我们所编写接收Item的代码，应该适用于任何Item对象类型。在下面列出Scrapy
支持Item类型。

- Item类型
  - Dictionaries
  - Item objects
  - Dataclass objects
  - attr.s objects

&emsp;&emsp;由于我们这个项目只用到Item objects，我们在这里就来详细介绍下。

**Item objects**其实有点像python中的字典，同时也提供了类似字典的API
。我们来看下官方的文档,我对此做出一些翻译。翻译有些不准确，仅供参考。

**class** scrapy.item.Item([arg ])

&emsp;&emsp;Item objects replicate the standard dict API,
including its __init__ method.
（Item对象复制了标准的dictAPI,包括他的__init__方法。）

&emsp;&emsp;Item allows defining field names, so that:
(Item允许定义字段名，)

  - KeyError is raised when using 
undefined field names .(当使用未定义的字段名时，将引发KeyError.)
  - Item exporters can export all fields by default even 
     if the first scraped object does not have values for all of
them(在默认情况下，Item输出器能够输出所有字段，即使第一个抓取的对象没有任何字段值。)
  
&emsp;&emsp;Item also allows defining field metadata, which 
    can be 
    used to customize serialization.
(Item也允许定义字段元数据，该字段元数据可用于自定义序列化。)

&emsp;&emsp;trackref tracks Item objects to help find 
memory leaks 
(trackref跟踪Item对象以帮助查找内存泄露。).

Item对象除了提供字典的方法，也提供了以下API：
  - copy()
  - deepcopy()
  - fields 
    一个字典包含Item
    对象中所包含的所有字段，不仅仅是被填充的。字典中的键是字段名；值是在item中声明的Field对象。

&emsp;&emsp;上面我们引用了Scrapy官方文档中对Item
的介绍。我在描述中肯可能有些许错误。希望小伙伴们能看看官方文档。

##3.4.2 Item的编写
在上面我们已经了解Item，现在我们开始进行编写吧！！！我们在项目文件夹中找的items.py文件。原始代码如下：
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
在上面的代码中我们可以看到一个import语句和一个继承了Scrapy.
Item对象的TutorialItem类。在TutorialItem
类中，已经给出了代码示例，我们可以按照给出的示例来编写我们的代码。

在项目一开始，我们就确定了我们抓取数据的目标-抓取所有电影的电影名称、上映时间、分类、评分。因此，根据我们的需要来定义字段名。下面给出代码
```python
import scrapy

class TutorialItem(scrapy.Item):
    name = scrapy.Field() #定义电影名
    time = scrapy.Field()
    category = scrapy.Field()
    grade = scrapy.Field()
    
```

现在，我们的item.py就已经编写完成了，现在让我们把关注点回到Scrapy的编写。

## 3.4.3 Item应用与Spider完善

我们在spider中使用我们定义的TutorialItem类，我们就需要在quotes.
py中导入此类。在quotes.py中输入下面的代码。
```python
from tutorial.items import TutorialItem
```
然后，我们在QuotesSpider类下面编写一个parse_detail方法
```python
class QuotesSpider(scrapy.Spider):
    #此处省略。。。。
    def parse_detail(self,response):
        pass
```
我们要使用我们定义的Item类，我们就要实例化，然后对定义的字段值进行赋值。由于item
和字典相似，我们可以用给字典赋值的方式进行赋值。
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
我们编写xpath语句，为其字段赋值。我们在写好Xpath后，可以使用Scrapy shell进行验证。好了，我们整个quotes.
py代码已经写好了。我们这一小节的任务也就完成了。完整的代码请点击[完整代码](../../codes/ch03/tutorial/tutorial/spiders/quotes.py)

## 3.4.4 总结
&emsp;&emsp;在本小节中，我我们学习Item,并编写了item.
py文件，同时也对上一节为编写的部分进行完善。下一小节，我们将要对爬取的数据存储到数据库中,并学习Item 
Pipelines相关知识，并编写pipelines.py文件。

- 参考资料：
  - 《pyhon3网络爬虫实战第二版》
  - [Scrapy官方文档](https://docs.scrapy.org/en/2.5/)