# 1.2 web网页的基础

## 1.2.1 网页组成

&emsp;&emsp; 我们平常所看到的网页由三部分组成，分别为HTML，CSS，JavaScript.三者在网页中分别扮演不同的作用。HTML是用来搭建网页的结构；CSS用来控制网页的外观；JavaScript用来控制网页的行为

## 1.2.2 HTML

- 简介

&emsp;&emsp;HTML（HyperText Markup Language，超文本标记语言）是一种用于创建网页的标准标记语言。

- 文档结构

  ```HTML
  <!DOCTYPE html>  # 文档声明，位于HTML文档第一行，在<html>之前,表明该文档为HTML5文档。
  <html>  # HTML根标签，所有网页标签都包含在<html></html>中
  	<head>...</head>  # HTML头文档，存放所有头部元素。
  	<body>...</body>  # 存放网页主要内容
  </html>
  ```

- 标签

&emsp;&emsp;HTML文件主要由标签组成，我们按功能来介绍一些基本的标签。

  - 基础标签

    | 标签          | 描述               |
    | ------------- | ------------------ |
    | <!DOCTYPE>    | 文档类型           |
    | \<html>       | HTML 文档          |
    | \<head>       | 头文档信息         |
    | \<title>      | 文档标题           |
    | \<body>       | 文档的主体         |
    | \<h1> ~ \<h6> | HTML 一级~六级标题 |
    | \<p>          | 段落               |
    | \<br>         | 换行               |
    | \<!--...-->   | 注释               |

  - 基础标签示例：

  ```HTML
  <!DOCTYPE html>
  <html>
  
  <head>
    <title>文档标题</title>
  </head>
  
  <body>
  
  <h1>标题1</h1>
  <br>
  <h2>标题2</h2>
  <br>
  <h3>标题3</h3>
  <h4>标题4</h4>
  <h5>标题5</h5>
  <h6>标题6</h6>
  
  <!--注释-->
  <p>这是一个段落</p>
  
  </body>
  </html>
  ```

  - 图片标签

    | 标签      | 描述               |
    | --------- | ------------------ |
    | \<img>    | 图像               |
    | \<map>    | 图像映射           |
    | \<area>   | 图像地图内部的区域 |
    | \<canvas> | 图形               |

  - 图片标签示例

    ```HTML
    <html>
    <body>
    
    <img src="图片地址"/>
    
    </body>
    </html>
    ```

  - 链接

    | 标签    | 描述                 |
    | ------- | -------------------- |
    | \<a>    | 锚                   |
    | \<link> | 文档与外部资源的关系 |
    | \<nav>  | 导航链接             |

  - 链接示例

    ```HTML
    <html>
    <body>
    
    <a href="http://www.baidu.com">This is a link</a>
    
    </body>
    </html>
    ```

  - 表单

    | 标签        | 说明                     |
    | ----------- | ------------------------ |
    | \<form>     | HTML 表单                |
    | \<input>    | 输入控件                 |
    | \<textarea> | 多行的文本输入控件       |
    | \<button>   | 按钮                     |
    | \<select>   | 选择列表（下拉列表）     |
    | \<optgroup> | 选择列表中相关选项的组合 |
    | \<option>   | 选择列表中的选项         |
    | \<label>    | input 元素的标注         |
    | \<fieldset> | 围绕表单中元素的边框     |
    | \<legend>   | fieldset 元素的标题      |
    | \<datalist> | 下拉列表                 |
    | \<keygen>   | 生成密钥                 |
    | \<output>   | 输出类型                 |

    - 表单示例：

    ```html
    <!DOCTYPE html>
    <html>
    <body>
    
    <form>
    First name:<br>
    <input type="text" name="firstname" value="Data">
    <br>
    Last name:<br>
    <input type="text" name="lastname" value="Whale">
    <br><br>
    <input type="submit" value="Submit">
    </form> 
    
    </body>
    </html>
    ```

  - 其他一些常见的标签

    | 标签       | 描述                   |
    | ---------- | ---------------------- |
    | \<div>     | 文档中的节             |
    | \<dialog>  | 对话框或窗口           |
    | \<footer>  | section 或 page 的页脚 |
    | \<frame>   | 框架集的窗口或框架     |
    | \<header>  | section 或 page 的页眉 |
    | \<li>      | 列表内容               |
    | \<menu>    | 菜单                   |
    | \<object>  | 内嵌对象               |
    | \<param>   | 对象参数               |
    | \<script>  | 客户端脚本             |
    | \<section> | 选择列表（下拉列表）   |
    | \<source>  | 媒介源                 |
    | \<span>    | 文档的节               |
    | \<style>   | 样式信息               |
    | \<video>   | 视频                   |

## 1.2.3 CSS

- 简介

&emsp;&emsp;CSS，指的是Cascading Style Sheet(层叠样式表)，是用来控制网页外观的一门技术。CSS从出现到现在，经历了CSS1.0、CSS2.0、CSS2.1和CSS3.0.

- 引入方式

&emsp;&emsp;对于CSS的引入方式一般有三种方式。分别为外部样式表、内部样式表和行内样式表。下面将为大家详细介绍三种引入方式。

  - 外部样式表
  
      - 将CSS和HTML代码分别存在不同的文件中，然后在HTML中使用link标签引入CSS文件。此种方式是导入CSS的最好方式，能够提高网站的性能和可维护性。
  
      - 引入方式
  
        ``````html
        <link rel="stylesheet" type="text/css" href="图片的路径">
        ``````
  
  
  - 内部样式表
     - 将HTML代码和CSS代码放在同一个HTML文件中。此种方法不推荐使用。
  
     - 引入方式
  
       ``````html
       <style type="text/css">
           '''''''
       </style>	
       ``````
     
  - 行内样式表
  	- 将HTML代码和CSS代码放在同一个HTML文件中，但CSS是在每个元素的内部定义的。此种方式也会导致网站的可读性和可维护性变差，但元素的样式恒定时，此种方式是更好的选择。
  	
  	- 引入方式
  	
  	  ``````html
  	  <div style="color:black;" ></div>
  	  ``````
  	
  
- CSS选择器

&emsp;&emsp;在CSS中，可以用CSS选择器定位节点，同时并对节点进行外观的更改。在爬虫中，我们也可以用CSS选择器进行网页数据的解析提取。此节很重要，在后面的章节中，会经常出现，希望大家多加练习。以下是常用的语法规则，其他的太多，不便列出，还请大家自己去寻找
	
|     选择器                | 例子             |    说明                                      |
	  | ------------------ | --------------- | ---------------------------------------- |
	  | .class             | .first          | 选择所有class="first"的元素              |
	  | #id                | #first          | 选择所有id="first"的元素                 |
	  | *                  | *               | 选择所有的元素                           |
	  | element            | p               | 选择所有<p>元素                          |
	  | element,element    | div,p           | 选择所有<div>元素和<p>元素               |
	  | element element    | div p           | 选择<div>元素内的所有<p>元素             |
	  | [attribute]        | [first]         | 选择所有带first属性的元素                |
	  | [attribute=value]  | [first=blank]   | 选择所有使用first="blank"的元素          |
	  | :link              | a:link          | 选择所有 未访问的链接                    |
	  | [attribute^=value] | a[src^="https"] | 选择每一个src属性的值以“https"开头的元素 |
	

## 1.2.4 JavaScript

&emsp;&emsp;JavaScript,也就是我们平常经常听到的JS。它主要是控制网页的行为和动态的数据加载。在JS逆向中，会用到很多关于JavaScript的知识。如果要想深入学习爬虫的知识，还是需要学习一些JavaScript的知识。
&emsp;&emsp;由于篇幅的原因，这里不便给出具体的教程。现在，网上的学习的资源有很多，大家可以根据需要自行学习。我这这里，也为大家推荐一份文档教程。如想学习，请点击[查看更多](https://es6.ruanyifeng.com/)


## 1.2.5 总结

&emsp;&emsp;本小节，我们学习了 Html 和 Css 相关知识。这些知识，在编写爬虫中有些许帮助，希望伙伴们好好学习。如想了解更多关于前端的知识。请点击[查看更多](https://developer.mozilla.org/zh-CN/docs/Web)

------

参考内容：

- w3school
- 百度百科-Web网页
- 菜鸟教程
- 绿叶学习网