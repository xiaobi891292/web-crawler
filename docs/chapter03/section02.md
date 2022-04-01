# 3.2 Scrapy讲解

&emsp;&emsp;经过上一小节的学习，我们已经了解一些Scrapy框架的架构、数据流的过程。以下的小节中，将会为大家呈现一个完整的使用 Scrapy 框架进行数据抓取的全过程。在实现数据抓取的过程中，我也会为大家介绍 Scrapy 知识，让大家能够更快地掌握Scrapy框架，以实现自己的需求。现在我们就开始吧！！！

## 3.2.1 安装与准备

&emsp;&emsp;在我们开始写代码前，我们需要安装Scrapy框架和Pymysql
库（数据存储会用到）。对于pymysql,我们在前面的章节中，我们已经安装了，就不再介绍了。安装Scrapy
框架，我们一般在命令行中输入以下命令：

```commandline
pip install scrapy
```
## 3.2.2 目标确定

&emsp;&emsp;
在项目开始前，要明确所需数据是什么？爬取的网站是什么？用什么样的数据存储方式来存储所需数据？只有当目标确定了，效率才会更高。现在将为小伙伴们说明一下本次Scrapy项目的目标。
- 使用Scrapy框架进行数据爬取。
- 爬取的静态网页是：https://ssr1.scrape.center/
- 爬取数据：抓取所有电影的电影名称、上映时间、分类、评分。
- 数据存储：采用Mysql数据库进行存储。

## 3.2.3 项目创建

&emsp;&emsp;
目标已经确定了，现在让我们开始吧！！！首先用命令行创建一个项目，命令形式如下：

> scrapy startproject myproject [project_dir]

&emsp;&emsp;其中，myproject 为项目名称。project_dir 为项目所在文件夹的名称。如果设置了 project_dir，就会在 project_dir
目录下创建项目文件夹（myproject）。如果不设置，则 project_dir 与 myproject 同名。

&emsp;&emsp;接下来，我们创建一个名为tutorial项目。在终端中输入命令：
```commandline
scrapy startproject tutorial
```


&emsp;&emsp;运行完毕后，将在终端窗口看到如下代码：
```commandline
New Scrapy project 'tutorial', using template directory 'd:\conda\lib\site-packages\scrapy\templates\project', created in:
    D:\tutorial（你自己的项目路径）

You can start your first spider with:
    cd tutorial
    scrapy genspider example example.com
```
tutorial文件夹下，会生成如下内容：
```text
|——tutorial
|   |—— __init__.py 
|   |—— items.py #定义了Item数据结构，在这里定义Item。
|   |—— middlewares.py #定义Spider Middlewares和Downloader Middlewares的实现
|   |—— pipelines.py #定义Item Pipeline的实现
|   |—— settings #定义了项目的全局配置
|   |—— spiders #定义一个个Spider的实现。每个Spider对应一个Python实现。
|       |—— __init.py
|——scrapy.cfg
```

输入以下命令，进入文件夹中：
```commandline
cd tutorial
```
然后输入以下命令：
```commandline
scrapy genspider quotes quotes.com
```

&emsp;&emsp;tutorial/tutorial/spiders中多出了一个文件quotes.py，该文件用于编写爬虫的规则和要提取的内容。

&emsp;&emsp;
此时，小伙伴有可能会有疑惑，为什么要运行这个命令，这个命令是否可以更改？这个命令那些是根据自己的需要更改的？我们先来解释下这个命令。官方文档给出这条命令的语法为：

> scrapy genspider [-t template] name domain
- name:你设置的爬虫名称。
- domain:用于生成allowed_domains 和 start_urls 属性。我们在后面会看到。
- \[-t template\]:该参数提供了一些爬虫模板，用于特殊需求的抓取。分别为basic、crawl 、csvfeed、 xmlfeed。如果不设置，则为默认的模板。

&emsp;&emsp;你可能又会问了，为什么在我们这个项目中不需要设置模板？原因很简单，使用基本的模板就可以满足我们的需求了。其他模板的具体介绍和用法，小伙伴们可以自行阅读文档，进行学习。

## 3.2.4 总结
&emsp;&emsp;本小节，我们学习了 Scrapy 项目的前期准备，了解了Scrapy 项目的文件结构,
并开始了一些项目的步骤。下一章节，就会来编写代码了，小伙伴们，做好准备哦！！

--------
- 参考资料
  - 《python3网络爬虫开发实战》
  - Scrapy官方文档
