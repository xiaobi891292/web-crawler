# 3.5Item Pipeline介绍和编写

&emsp;&emsp;在上一节中，我们学习了 Item，并对其进行代码的编写。不知道小伙伴们掌握了没？本小节，我们将学习**Item 
Pipeline**，并实现将数据存储到数据库中的功能。让我们来一起了解下吧！！！

## 3.5.1 Item Pipeline简单介绍

&emsp;&emsp;Item Pipeline 是一个 python 类，它接收一个 Item,
并且对其执行操作。同时，决定该 Item 是否继续执行，还是被丢弃。整个流程就是，当 spider 抓取一个 Item 时，该Item传递给 Item 
Pipeline。在 Item Pipeline 中，根据我们定义的方法进行处理该 Item。可以说，Item Pipeline 是处理 Item 的中间件。

&emsp;&emsp;在Item Pipeline中，我们可以实现以下功能：

- 清洗HTML数据
- 验证数据（检查Item中是否包含该字段）
- 检查是否重复（删除重复的Item）
- 将抓取的数据存入数据库

## 3.5.2 Item Pipeline详细介绍

&emsp;&emsp;上面介绍了Item Pipeline的具体用处，那我们如何来自定义一个符合所需功能的Item 
Pipelien呢？

&emsp;&emsp;正如前面所说，每个Item Pipeline都是一个python类。它必须实现以下方法：

- **process_item(self,item,spider)**

      1.每个Item Pipeline都会调用此方法。
      2.该方法必须返回Item类型的值或者抛出一个DropItem异常。
      3.被删除Item将不再被其他的Item Pipeline继续处理。

&emsp;&emsp;除了必须要实现的方法外，它还有另外三个方法：
- **open_spider(self,spider)**

        1.该方法将在Spider开启时被自动调用。
        2.我们可以在此方法下做一些初始化的操作。比如开启数据库的连接，文件的打开等。
- **close_spider(self,spider)**

        1.该方法将在Spider关闭时被自动调用。
        2.我们可以在此方法下做一些收尾操作。比如数据库的关闭，文件的关闭等。
- **from_crawler(cls,crawler)**

        1.该方法是个类方法，如果它存在将会从一个crawler中创建一个Pipeline实例。
        2.通过此Crawler对象，我们可以拿到Scrapy所有核心组件，例如全局的配置信息。
        3.crawler参数：使用此管道的爬虫程序。

## 3.5.3 Item Pipeline编写
&emsp;&emsp;上面我们已经对Item 
Pipeline 进行了深度介绍，不知道小伙伴掌握了没？如果没掌握的话，也没事。下面我们将编写代码，我们可以利用这次机会来加深下对Item 
Pipeline 的认识。

在项目目录中找到pipelines.py文件，我们将在该文件中编写代码。在没编写前，文件是这个样子的。
```python
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class TutorialPipeline:
    def process_item(self, item, spider):
        return item
```
可以看到，文件已经自动生成了一些内容。一个TutorialPipeline的类，以及一个process_item
方法。文件中有一些注释，有助于我们了解该文件，注释中也提供了相关学习文档的地址。

为了实现需求，我们把爬取的内容存储到Mysql中，在文件中写入以下代码
```python
import pymysql
```
接着，在settings.py文件中，我们设置关于Mysql的配置信息。Scrapy抓取网站时，默认遵循robotx协议，
这样可能会导致我们想要抓取的数据抓取不到，因此我们把它给关闭。同时设置请求头，请求头默认是被注释掉的，我们取消注释并给它重新赋值。
```python
LOCALHOST = 'localhost'
USER = '你的账号名'
PASSWORD = '你的密码'
DATABASE = '你自己的数据库名'
ROBOTSTXT_OBEY = False
USER_AGENT = '你自己的UESR_AGENT'
```
我们调用 from_crawler 类方法，从而在 Item Pipeline 中拿到这些配置信息。
```python
class TutorialPipeline:
    @classmethod
    def from_crawler(cls,crawler):
        """从设置中，获取数据库中的设置"""
        cls.localhost = crawler.settings.get('LOCALHOST')
        cls.user = crawler.settings.get('USER')
        cls.password = crawler.settings.get('PASSWORD')
        cls.database = crawler.settings.get('DATABASE')
        return cls()
```
经过上面的设置，我们已经从设置中拿到Mysql的配置信息，现在可以开始连接数据库了。这里使用open_spider方法连接Mysql。
```python
    def open_spider(self, spider):
        """该方法再Spider打开时被调用，连接数据库"""
        self.db = pymysql.connect(host=self.localhost, user=self.user, password=self.password,database=self.database)
        self.cursor = self.db.cursor()  #创建一个游标对象。
        sql = "CREATE TABLE IF NOT EXISTS movie (name varchar(255),time varchar(255),grade char(8),category varchar(255))"#编写sql语句，在scrapytutorial数据库中movie表中创建字段名
        self.cursor.execute(sql)
```
编写open_spider方法下的代码后，我们将数据插入Mysql中。
```python
    def process_item(self, item, spider):
        """该方法被每一个item pipeline组件调用，插入数据"""
        name = item["name"]  #从item中获取name所对应的值
        time = item["time"]  #从item中获取time所对应的值
        grade = item["grade"]  #从item中获取grade所对应的值
        category = ''     #由于抓取的内容是个列表，我们需要对其拼接。
        for i in item["category"]:
            category = category + "," + i
        insert_sql = 'INSERT INTO movie (name,time,grade,category) VALUES (%s,%s,%s,%s)'
        try:
            self.cursor.execute(insert_sql,(name,time,grade,category))  
            #执行indser_sql语句
            self.db.commit()
            #将语句进行提交
        except:
            self.db.rollback() #如果出现错误，进行数据库的回滚
        return item  #返回一个item 如果有其他的item pipeeline根据优先级可以再处理该item
```
最后，进行一个收尾工作，我们使用close_spider方法
```python
    def close_spider(self, spider):
        """该函数在Spider关闭时被调用"""
        self.cursor.close() #关闭游标对象
        self.db.close()  #断开数据库连接
```
至此，代码编写完成。但如果想要启用我们编写的Item Pipeline，还需要激活它。激活操作也是在设置中进行的，在settings.
py中找到ITEM_PIPELINES,在默认情况下，这部分是被注释掉的。我们取消注释，将其开启。
```python
ITEM_PIPELINES = {
   'tutorial.pipelines.TutorialPipeline': 300,
}
```
可以看到，ITEM_PIPELINES是一个字典，字典中的键就是我们自定义的Item pipeline，根据上述格式来编写即可。`项目名.
pipelines.你自己定义的item pipeline的类名`。字典的值，取整数1-1000范围。数值越小，有优先级越高。

&emsp;&emsp;好了，代码已经编写完成了。完整的代码请点击查看[完整代码](https://xiaobi891292.github.io/web-crawler/#/codes/ch03/pipelines.md)


## 3.5.4 小结
&emsp;&emsp;本小节，我们学习了Item 
Pipeline的相关知识，同时编写代码完成了需求。我们的项目也就到此完成了。下一小节中，我们将会介绍其他的Scrapy
相关知识，帮助小伙伴们更好地学会Scrpay。

- 参考资料
  - 《pyhon3网络爬虫实战第二版》
  - [Scrapy官方文档](https://docs.scrapy.org/en/2.5/)