# 2.2 Lxml和Beautiful Soup介绍

&emsp;&emsp;在上一小节中，我们介绍了Requests的使用。通过Requests,我们可以获得网页的源代码，但是我们怎么从网页的源代码中获得我们的所需的的数据呢？本小节介绍的内容，就会帮助我们实现这个功能。现在让我们一起学习一下吧！！！

## 2.2.1 Lxml介绍

&emsp;&emsp;Lxml是python的一个解析库，支持对HTML和XML的解析，同时支持Xpath解析。Xpath解析是我们本小节的重点。由于Lxml 对C语言库 libxml2和 libxslt进行绑定，因此它在解析页面时效率很高。如果我们解析网页时，想使用xpath语法来获得我们想要的数据，那么Lxml将是个很好的选择。

### 2.2.1.1安装
在使用lxml之前，我们需要安装它。我们可以通过下面的命令进行安装。
```commandline
pip isntall lxml
```
在安装完成后，我们就可以使用它了。

### 2.2.1.2 Xpath介绍
&emsp;&emsp;XPath即为XML路径语言（XML Path Language），它是一种用来确定XML文档中某部分位置的语言。Xpath的选择功能非常强大，不仅提供了基于路径的表达式的选取，也提供了一些内置的函数处理一些特殊化的数据。

### 2.2.1.3 Xpath表达式
&emsp;&emsp;那么，我们应该编写Xpath路径表达式呢？怎么将它应用到爬虫的网页解析中呢？下面我们来看下关于Xpath的常用路径表达式。

|表达式		|描述						|
|--			|--							|
|nodename	|选取此节点的所有节点		|
|/			|从当前节点选取直接子节点	|
|//			|从当前节点选择子孙节点		|
|.			|选取当前节点				|
|..			|选取当前节点的父节点		|
|@			|选取属性					|

&emsp;&emsp;看到这个表格，我们可能还不会用，并不理解其中的意思。那么我将结合代码为大家详细讲解。我们先首先写出一个html代码，为我们测试使用。代码如下
```html
<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8">
		<title>测试</title>
	</head>
	<body>
		<div class="tushu">
			<ul class="mui-table-view">
					<li class="mui-table-view-cell">
						<a class="mui-navigate-right" href="https://baike.baidu.com/item/%E6%B0%B4%E6%B5%92%E4%BC%A0/348">
							水浒传
						</a>
						<p>水浒传的人物有哪些？</p>
					</li>
					<li class="mui-table-view-cell">
						<a class="mui-navigate-right" href="https://baike.baidu.com/item/%E7%BA%A2%E6%A5%BC%E6%A2%A6/15311?fr=aladdin">
							 红楼梦
						</a>
						<p>红楼梦的人物有哪些？</p>
					</li>
					<li class="mui-table-view-cell">
						<a class="mui-navigate-right" href="https://baike.baidu.com/item/%E8%A5%BF%E6%B8%B8%E8%AE%B0/5723">
							 西游记
						</a>
						<p>西游记的任务有哪些？</p>
					</li>
				</ul>
			****
		</div>
	</body>
</html>
```

- nodename 
nodename(节点名称) 如果我们想选取body标签下的所有标签，我们可以写出Xpath表达式。
``` python
from lxml import etree
ceshi = '''
上面的html代码
'''
html = etree.HTML(ceshi) # 把html文本转换为Element对象
#选取body的所有节点
body_node = html.xpath('//body')
#输出内容 [<Element body at 0x1b2c99c8b00>]
#由于在body下，我们只有一个div标签，所以我们只能选择到一个。
```

- 从当前节点选取直接字节点(/) 我们选择body下的div下的ul标签，我们可以写出表达式。
```python
from lxml import etree
ceshi = '''
上面的html代码'''
html = etree.HTML(ceshi)
ul = html.xpath('//body/div/ul')
# 输出内容 [<Element ul at 0x1dad812a2c0>]
```

- 从当前节点选取子孙节点 我们选择body下的ul标签（//）。

```python
ul = html.xpath('//body//ul')


# 输出结果 ：[<Element ul at 0x18fbf514bc0>]
```
&emsp;&emsp;在这里，我们看到。两者都是选择ul标签，我们所用的表达式是不同的。原因是在用//body/div/ul
'选择时，我们都是根据标签的层级关系来的，是不可以忽略层级关系的。因此当我们使//body/ul时，我们是选择不到的。而使用//body//ul
时，我们可以忽略其层级关系。

- 选取当前节点(.)

比如我们在解析时，我们在一个表达式中已经选取了一个节点，在另一个表达式继续使用所选择的节点。我们就可以用到。
```python
li_list = html.xpath('//body/div/ul/li')
for li in li_list:
    a = li.xpath('./a')
    print(a)
# 输出结果：[<Element a at 0x1b9be934d00>]
# [<Element a at 0x1b9be934ec0>]
# [<Element a at 0x1b9be934e80>]
```
- 选取当前节点的父节点(..)

当我们选择到ul标签时，我们想要获得它的父节点div时，我们就可以用到。
```python
ul = html.xpath('.//body/div/ul')[0]
# 为什么会使用[0]呢？原因是每个xpath函数，返回的是一个包含element的列表。由于只有一个ul标签，故使用[0]
div = ul.xpath('..')
# 输出结果 ：[<Element div at 0x2976f6f4d40>]
```
- 选取属性(@)

如果我们选择第一个a标签的href属性值时，我们可以用到。
```python
href = html.xpath('.//body/div/ul/li[1]/a/@href')
print(href)
# 输出结果：['https://baike.baidu.com/item/%E6%B0%B4%E6%B5%92%E4%BC%A0/348']
```

### 2.2.1.4 Xpath常用用法
- 属性匹配

在我们网页解析的时候，我们想要选择一些具有特定属性的链接。我们可以通过 @ 
实现我们的需求。比如在给的例子中，我们想选取class属性为mui-table-view的ul标签，我们就可以这样实现。
```python
ul = html.xpath('//body/div/ul[@class="mui-table-view"]')
print(ul)

```
输出结果如下：
```text
[<Element ul at 0x12495738a00>]
```
- 选取文本

在我们网页解析时，我们想要获取标签下的文本信息。我们可以使用如下方式。如我们想获得ul标签下第一个li标签下的a标签的文本。
```python
text = html.xpath('//body/div/ul/li[1]/a/text()')
print(text)

```
输出结果如下：
```text
['\n                            水浒传\n                        ']
```
由于在源代码中a标签下的文本中含有空格和换行，我们在选取文本时，我们都将其获得了。如要获得其文本，就需要对其进行处理。

- 按序选择

在网页解析中，我们回到一个标签下有好几个相同的元素。我们只想要其中的一个元素。那么，我们怎么选取呢。下面的代码可以实现。还是以上面的html为例
```python
from lxml import etree

ceshi = '''
上面的代码'''
html = etree.html(ceshi)

# 选取ul标签的第一个li标签
first_li = html.xpath('//body/div/ul/li[1]')

# 选取最后一个li标签
last_li = html.xpath('//body/div/ul/li[last()]')

# 选取位置小于2的li标签
result = html.xpath('//body/div/ul/li[position()<2]')
```

&emsp;&emsp;
好了xpath
的介绍就到这里，不知道大家掌握没？如果没掌握，也没有关系，我们在实战中就会有更深的体会，帮助你理解。下面我们来介绍另一个网页解析的包Beautiful 
Soup。

## 2.2.2 Beautiful Soup介绍
&emsp;&emsp;我们在上面介绍 Xpath 的使用，如果你只想掌握 Xpath,那么你就可以进入下一章节的学习了。因为 Lxml 和 Beautiful Soup 两者的作用是一样的，都是解析网页，从网页中提取我们所需要的数据。如果你要问那个更好，我也说不准那个更好，但只要我们目的解决了就好了。

### 2.2.2.1 Beautiful Soup简介
&emsp;&emsp;Beautiful Soup 是一个可以从HTML或XML文件中提取数据的 Python 库。它可以和你喜欢的解析器配合工作来导航、搜索、修改分析树等功能。

### 2.2.2.2 Beautiful Soup安装
我们在终端输入一下命令就可以安装了
```commandline
pip install beautifulsoup4
```
同时，我们也可以下载它的源码，通过 setup.py 进行安装。
```commandline
Python setup.py install
```
Beautiful Soup支持Python标准库中的HTML解析器,还支持一些第三方的解析器。我们可以根据自己的喜好，去选择解析器。对于第三方的解析器，我们需要进行安装。
- lxml解析器
	- 对于Windonws系统，我们可以用下面的命令进行安装。
	```commandline
	pip install lxml
	```
	- 对于linux系统，我们可以用下面的系统进行安装
	```commandline
	apt-get install python-lxml
	```
-  html5lib解析器
	- 对于Windonws系统，我们可以用下面的命令进行安装。
	```commandline
	pip install html5lib
	```
	- 对于Linux系统，我们可以用下面的命令进行安装。
	```commandline
	apt-get install python-html5lib
	```

在这里，我推荐大家用lxml做为解析器。因为它速度很快，同时它文档容错能力强。

### 2.2.2.3 Beautiful Soup 使用

#### 2.2.2.3.1基本使用

我们只要将我们所需要的解析的文档传入BeautifulSoup的构造方法中，同时指定我们所需要的解析器的类型，我们就可以得到一个bs4.BeautifulSoup对象。这时，我们就可以采取一定的规则进行数据的提取。

首先，我们来引入一个测试的文档，供我们学习之用。下面的文档来自于官方的文档。
``` html
<html><head><title>The Dormouse's story</title></head>
    <body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p

```

我们看到，这时的html文档的结构不是完整的，不过不用担心。BeautifulSoup会帮我们修复它。这也是前面提到的容错能力强的体现。

```python
from bs4 import BeautifulSoup
soup = BeautifulSoup(ceshi,'lxml')
# 第一个参数是我们需要解析的html，也可以是个文档对象
# 如果是文档对象我们可以这样写
# soup = BeautifulSoup(open(ceshi.html),'lxml')
# 第二个参数，是我们的所选择的解析器。我们这里选择是lxml。也可以选择html5lib作为解析器。

```


#### 2.2.2.3.2节点选择
我们在访问文档树时，我们可以通过调用节点的名称，就可以选择对应的节点。如果我们想选取titlle节点，我们可以用如下写法。
``` python
from bs4 import BeautifulSoup
soup = BeautifulSoup(ceshi,'lxml')
print(soup.title)
```
输出结果如下：
```text
<title>The Dormouse's story</title>
```
我们可以看到，我们选中了这个节点。那它的类型是什么呢？我们输入下面的代码进行查看。
```python
print(type(soup.title))
```
输出结果如下：
```text
<class 'bs4.element.Tag'>
```
我们可以看到是一个Tag对象。在每个选中的节点中，我们都是一个Tag对象。Tag对象中有着很多属性和方法。我们会逐一进行介绍。注意的是，我们在使用节点选择时，我们只能获得到第一次出现的节点。

#### 2.2.2.3.3 Tag属性
- 一般属性
	- name属性 利用name属性，我们可以获得其节点的名称。

	对应的代码
```python
print(soup.title.name)
```
	输出效果如下：
```text
title
```
	我们可以看到，我们获得到我们所对应节点的名字。
	- attrs属性

	对于一个Tag对象，可能会有多个属性。例如id class属性。如果我们想获取所选节点的属性，我们可以这样写。代码如下：
```python
print(soup.p.attrs)
```
	输出结果如下：
```text
{'class': ['title']}
```
	我们可以看到输出的结果是一个字典形式，包含的是节点的属性与所对应的值。我们要选取属性的值，我们可以这样写。
```python
print(soup.p.attrs['class'])
```
	输出结果如下：
```text
['title']
```
	- string属性

	如果我们Tag对象中，只有一个 NavigableString类型的子节点，我们可以使用如下方法获得子节点。这里 NavigableString 其实是节点中包含的节点内容。我们获取title节点下的内容。代码如下：
```python
print(soup.title.string)
```
	输出结果如下：
```text
The Dormouse's story
```
	可以看到我们拿到了title节点下所对应的文本内容。
	
	如果一个节点下仅有一个子节点,那么这个tag也可以使用 .string 方法获得对应的文本。如第一个p节点下。代码如下：
```python
print(soup.p.string)
```
	输出结果如下：
```text
	The Dormouse's story
```
**注意，如果一个节点下，有多个节点，这时我们无法直接调用string属性获取文本内容.**
	- strings属性

	如果一个节点下有多个字符串，我们可以使用strings属性构造循环获得。代码如下：
```python
	for i in soup.strings:
		print(i)
```

	- stripped_strings属性

	如果节点下有多个字符串，同时包含空格和换行，我们可以使用如下的方法。代码如下：
```python
	for i in soup.stripped_strings:
		print(i)
```

- 子节点
	- contents属性

	Tag的 contents 属性可以将tag的子节点以列表的方式输出。代码如下：
	```python
	print(soup.body.contents)
	```
	输出效果如下：
```text
['\n', <p class="title"><b>The Dormouse's story</b></p>, '\n', <p class="story">Once upon a time there were three little sisters; and their names were
	<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
	<a class="sister" href="http://example.com/lacie" id="link2">Lacie</a> and
	<a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>;
	and they lived at the bottom of a well.</p>, '\n', <p class="story">...</p>, '\n']
```
	- children属性

	Tag对象将tag的子节点返回一个可迭代对象，我们可以使用循环输出内容，代码如下：
```python
	for i in soup.body.children:
	    print(i)
```
	输出结果如下：
```text
	<p class="title"><b>The Dormouse's story</b></p>
	<p class="story">Once upon a time there were three little sisters; and their names were
	<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
	<a class="sister" href="http://example.com/lacie" id="link2">Lacie</a> and
	<a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>;
	and they lived at the bottom of a well.</p>
```
	
- 父节点

	查看我们示例代码，我们可以看到对于一个节点，也就是tag，都有父节点。我们可以通过一下两个tag属性获得。

	- parent属性

	通过parent属性，我们可以获得某个元素的父节点。代码如下：
```python
	print(soup.p.parent)
```
	输出效果如下：
```text
	<body>
	<p class="title"><b>The Dormouse's story</b></p>
	<p class="story">Once upon a time there were three little sisters; and their names were
	<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
	<a class="sister" href="http://example.com/lacie" id="link2">Lacie</a> and
	<a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>;
	and they lived at the bottom of a well.</p>
	<p class="story">...</p>
	</body>
```
	我们可以看到我们获得了p节点的父节点，也就是body节点。
	
	- parents属性

	通过parents属性，我们可以递归查到某个元素的父节点的父节点，也就是祖先节点。代码如下：
```python
	for i in soup.p.parents:
	    print(i.name)
```
	输出结果如下:
```text
	body
	html
	[document]
```

- 兄弟节点

	前面我们获得了父节点，子节点。那么我们应该怎么获得每个节点的兄弟节点（也就是同级节点）？我们可以用下面两个属性。
	- next_sibling和next_siblings属性

	next_sibling属性来查看节点的下一个兄弟节点。代码如下：
	```python
	print(soup.b.next_sibling)
	```
	输出结果如下：
	```text
	None
	```
	为什么会返回None呢？当然是没有查到同级的元素了。如果你相信，你可查看下。对于next_siblings属性是获得后面的所有兄弟节点，这里就不具体介绍。
	
	- previous_sibling和previous_siblings属性

	previous_sibling属性来查看节点的上一个兄弟节点。代码如下：
```python
	print(soup.a.previous_sibling)
```
	输出结果如下：
	```text
	Once upon a time there were three little sisters; and their names were
	```
&emsp;&emsp;为什么是一个字符串呢？这里我们要说一下。Beautiful Soup将复杂HTML文档转换成一个复杂的树形结构,每个节点都是Python对象,所有对象可以归纳为4种: Tag , NavigableString , BeautifulSoup , Comment .对于一个节点中的文本来说，它则是一个NavigableString对象。而在调用 previous_sibling 属性时，我们获得的是这个对象的上一个对象。对于 previous_siblings 属性是获得后面的所有兄弟节点，这里就不具体介绍。
	
#### 2.2.3.4 搜索方法
&emsp;&emsp;Beautiful Soup定义了很多方法。在这里，我们将着重学习 find()和 find_all()两个方法。对于其他的方法，请大家自行学习。

- find_all方法
	
	find_all方法的作用是返回当前节点的所有的子节点，以列表的形式返回。首先我们先看下它的API：
	> find_all( name , attrs , recursive , string , **kwargs )
	- name参数

		作用：name 参数可以查找所有名字为 name 的节点,字符串对象会被自动忽略掉。name参数接收字符串类型，正则表达式，还有列表类型。
		
		简单使用：
```python
	#搜索名为title的节点
	print(soup.find_all('title'))
```
		输出结果如下：
```text
[<title>The Dormouse's story</title>]
```
	- attrs参数
	
		作用：attrs参数可以根据属性来进行查找相对应的节点。
		
		简单使用：
```python
	#搜索第一个p节点
	print(soup.find_all(attrs={'class':'title'}))
```
		输出结果如下：
```text
[<p class="title"><b>The Dormouse's story</b></p>]
```
		我们可以看到，我们在使用attrs时，我们传入的是一个字典类型。返回的是符合条件的所有节点。如果一个节点有两个属性，不知道你会不会写呢？
		
	- recursive参数
	
		作用：recursive的值是一布尔类型的。默认是True，搜索当前节点的所有子孙节点；如果是False，则搜索当前节点的所有直接子节点。
		
		简单使用：
```python
print(soup.find_all("title", recursive=True))
print(soup.find_all('title', recursive=False))
```
		输出结果如下：
```text
[<title>The Dormouse's story</title>]
[]
```

	- string参数

		作用：通过string参数，我们可以搜索到文档中的字符串内容。string参数接收字符串类型，正则表达式，还有列表类型。
		
		简单使用
```python
print(soup.find_all(string='Elsie'))
print(soup.find_all(string=["Tillie", "Elsie", "Lacie"]))
print(soup.find_all(string=re.compile("Dormouse")))
```
		输出结果：
```text
['Elsie']
['Elsie', 'Lacie', 'Tillie']
["The Dormouse's story", "The Dormouse's story"]
```

	- **kwargs
	
		作用：find_all中内置了一些关键词参数。通过关键词参数，简化一些代码或者提供一种搜索方式。
		
		简单使用：
```python
#如果一个指定名字的参数不是搜索内置的参数名,搜索时会把该参数当作指定名字tag的属性来搜索
print(soup.find_all(id='lin2'))
#我们也可以按照css类名来进行选择，这时需要用到_class关键词参数。
print(soup.find_all(class_='sister')
```
		输出结果如下：
```text
[<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>]
[<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>, <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>, <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]
```
好了，我们已经把find_all方法介绍完了。现在来看下find方法。

- find方法

	find方法的作用是返回当前节点的。对于多个节点，默认返回第一个。我们来看下API：
	> find( name , attrs , recursive , string , **kwargs )

	我们可以看到，参数跟find_all参数是相同，具体的介绍就不再介绍了。只要你掌握了fina_all方法，那么find方法你也会轻而易举地掌握。
	
- 其他的方法

	除了上面的两种方法外还有如下几种方法，我将他们进行简单列举出来。希望对大家有些帮助。
|方法					|作用							|
|--						|--								|
|find_parents			|返回所有祖先点					|
|find_parent			|返回直接父节点					|
|find_next_siblings		|返回后面的所有兄弟节点			|
|find_next_sibling		|返回后面第一个兄弟节点			|
|find_previous_siblings	|返回前面的所有兄弟节点			|
|find_previous_sibling	|返回前面的第一个兄弟节点		|
|find_all_next			|返回节点后面所有符合条件的节点	|
|find_next				|返回后面第一个符合条件的节点	|
|find_all_previous		|返回前面所有符合条件的节点		|
|find_all_previou		|返回前面第一个符合条件的节点	|

#### 2.2.3.5 CSS选择器
&emsp;&emsp;对于Beautiful Soup，它提供了另外一种方式来选择节点。那就是CSS选择器。如果你了解前端开发，你肯定会知道它的强大之处。

首先，让我们先看下CSS选择器的常见语法规则。

|语法				|解释			|
|--					|--				|
|div（标签名）		|元素选择器		|
|#标签的id			|id选择器		|
|.标签的类的值		|class选择器	|
|标签 标签的子标签	|后代选择器		|
|选择器,选择器		|群组选择器		|

那我们应该怎么使用呢？在Beautiful Soup中，如果我们使用CSS选择器，我们使用到一个select方法，传入相对应的CSS选择选择器即可。下面将给出一些例子，供大家体会。

- 元素选择器

	例子：选择p标签
```python
	soup.select('p')
```
- id选择器
	
	例子：选择id为link1的a标签
```python 
	soup.select('#link1')
```
- class选择器
	
	例子：选择class的值为story的p标签
```python
	soup.select('.story')
```

- 后代选择器
	
	例子：选择第一个p标签的子标签
```python
	soup.select('p b')
```
- 群组选择器
	
	例子：选择class为title的p标签和class为sister的a标签
```python
	soup.select('.title,.sister')
```


## 2.2.2小节
&emsp;&emsp;本小节，我们学习了两个网页数据的解析方式于和工具，分别为 Lxml 和 Beautiful Soup。他们两个各有优点，我们不需要全部掌握，只掌握其中一个即可。在这里，告诉你个小技巧，现在，每个浏览器内置了开发者工具，我们可以选取对应的元素，复制其响应的Xpath或者CSS选择器。

- 参考内容
	- 《python3网络爬虫开发实战第二版》
	- [Beautiful Soup官方文档](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
	- [绿叶学习网](http://www.lvyestudy.com/css)