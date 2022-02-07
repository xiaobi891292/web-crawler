# 1.4 正则表达式

## 1.4.1 什么是正则表达式？

正则表达式（Regular Expression），简称RE，最早起源于unix，是一种文本模式，通常用于字符串的过滤。它描述了一种字符串匹配的模式，包括普通字符和特殊字符。

## 1.4.2 应用场景

1. 文本检索
2. 文本替换
3. 数据验证

## 1.4.3 语法

以字符串"abc.c!ac1bb f"为例

|   字符   | 匹配内容                                                     | 实例         | 匹配结果 |
| :------: | ------------------------------------------------------------ | ------------ | -------- |
| 普通字符 | 匹配自身                                                     | abc          | abc      |
|    .     | 除换行符"\n"外，匹配任意字符                                 | ab.          | abc      |
|    \     | 转义符                                                       | c\.c         | c.c      |
|  [...]   | 字符集。对应位置为字符集中的任意字符。字符集中的字符可以全部列出，也可以给一个范围。 | a[abc]c      | abc      |
|  [^...]  | 匹配除字符集外的所有字符                                     | a[^efg]c     | abc      |
|    \d    | 数字 [0-9]                                                   | c\db         | c1b      |
|    \D    | 非数字[^\d]                                                  | a\Db         | abc      |
|    \s    | 空白字符 [<空格> \t\r\\n\\f\\v]                              | b\sf         | b f      |
|    \S    | 非空白字符 [^\s]                                             | a\Sc         | abc      |
|    \w    | 单词字符 [A-Za-z0-9_]                                        | a\wc         | abc      |
|    \W    | 非单词字符 [^\w]                                             | b\Wf         | b f      |
|    *     | 匹配前一个字符0或无数次                                      | c1b*         | c1bb c1  |
|    +     | 匹配前一个字符1或无数次                                      | c1b*         | c1bb     |
|    ?     | 匹配前一个字符0或1次                                         | c1b?         | c1 c1b   |
|   {m}    | 匹配前一个字符m次                                            | c1b{2}       | c1bb     |
|  {m,n}   | 匹配前一个字符m~n次,m、n可省略，m默认为0，n默认为无穷        | c1b{1,2}     | c1b c1bb |
|    ^     | 匹配字符串开头。多行模式中，为匹配每一行开头                 | ^abc         | abc      |
|    $     | 匹配字符串末尾。多行模式中，为匹配每一行末尾                 | b f$         | b f      |
|    \A    | 仅匹配字符串开头。                                           | \Aabc        | abc      |
|    \Z    | 仅匹配字符串末尾。                                           | b f\Z        | b f      |
|  &#124;  | &#124; 左右表达式任意匹配一个                                | abc&#124;def | abc      |

* 以上仅介绍了一些简单的语法，复杂语法需求可自行百度。

## 1.4.4 Re库

Re库是python的标准库，采用raw string类型表示正则表达式。

- Re库的主要功能函数：
  
  - 编译正则表达式
    
    - re.compile():用于编译正则表达式，生成一个 Pattern 对象
      
      `re.compile(pattern, flags=0)`
    
  - 查询
  
    - re.match():从<u>第一个字符</u>开始匹配正则表达式，返回Match对象。若匹配失败，则返回None
  
      `re.match(pattern, string, flags=0)`
  
    - re.search():搜索第一个满足条件的字符串，查找到第一个停止，返回Match对象
  
      `re.search(pattern, string, flags=0)`
  
     - re.findall():搜索所有满足条件的字符串
  
       `re.findall(pattern,string,flags=0)`
  
     - re.finditer():返回所有与正则表达式相匹配的字符串，返回形式为迭代器。
  
       `re.finditer(pattern, string, flags=0)`
  
   - 检索和替换
  
      - re.sub():替换满足条件的字符串
  
        `re.sub(pattern,repl,string,count=0,flags=0)`
  
   - 分割
  
      - re.split():将一个字符串按正则表达式匹配结果进行分割，返回list
  
        `re.split(pattern,string,maxsplit=0,flags=0)`
      
  - 修饰符
  
      - |        |                                                  |
          | :----- | ------------------------------------------------ |
          | 修饰符 | 描述                                             |
          | re.I   | 忽略大小写匹配                                   |
          | re.L   | 实现本地化识别匹配，不太常用。                   |
          | re.M   | 设置后，以'^'匹配字符串和每一行的开始；'$'则相反 |
          | re.S   | 让' . '匹配任何字符，包含换行符                  |
          | re.A   | 让\w,\W,\b,\B,\d,\D,\s和\S知匹配ASCII            |
          | re.X   | 这个标记匀许你使用灵活的形式编写正则表达式。     |
  
      - 
  
- Re库的通用参数：

  | 参数    | 说明                                                         |
  | ------- | ------------------------------------------------------------ |
  | pattern | 匹配的正则表达式                                             |
  | string  | 待匹配的字符串                                               |
  | flag    | 标志位，用于控制正则表达式的匹配方式，如：是否区分大小写、多行匹配等 |

  

- Re库的match对象:

  - Match对象的属性：
  
    | 属性    | 说明                   |
    | ------- | ---------------------- |
    | .string | 待匹配的文本           |
    | .re     | 匹配时使用的正则表达式 |
    | .pos    | 匹配到的文本的开始位置 |
    | .endpos | 匹配到的文本的结束位置 |
  
  - Match对象的方法：
  
    | 方法      | 说明                                                         |
    | --------- | ------------------------------------------------------------ |
    | .group()  | 返回匹配后的字符串，详情见实例部分                           |
    | .groups() | 返回一个包含所有小组字符串的元组，从 1 到 所含的小组号。     |
    | .start()  | 匹配字符串在原始字符串的开始位置                             |
    | .end()    | 匹配字符串在原始字符串的结束位置                             |
    | .span()   | 返回匹配字符串在原始字符串的起止位置。格式为：（start(), .end()） |

- Re库代码实例

  - 编译正则表达式
  
    ```python
    import re
    p = re.compile('\d*[a-zA-Z]*') # 由于正则自带了compile，也可直接 p = r'\d*[a-zA-Z]*'。
    ```
  
  - 查询
  
    ```python
    import re
    
    """
    查询：match、search、findall、finditer
    区别:
    match:从字符串s的第一个字符开始匹配，第一个字符不符合正则，则匹配失败，返回NONE
    search:匹配整个字符串，找到一个符合正则的匹配，则停止。
    findall:前两者返回第一次匹配到内容，findall返回所有匹配的内容
    finditer:与findall相同，以迭代器形式返回
    """
    
    s = "abc.c!ac1bb f"
    p = r'(\d*)([a-zA-Z]*)'  # 匹配数字+英文字母的组合
    m = re.match(p, s) 
    m = re.search(p, s) 
    
    # match对象
    print(m.string)
    """ abc.c!ac1bb f """
    print(m.group())  # 匹配整体结果 
    """ abc """
    print(m.group(0))  # group(0) 同 group
    """ abc """
    print(m.group(1))  # group每个括号为一组，group(1)返回匹配结果中第一个括号(\d*)对应的内容 
    """ '' """
    print(m.group(2))  # group(2)返回匹配结果中第一个括号(\d*)对应的内容 
    """ abc """
    print(m.group(3))  # 由于只有两组，group(3)报错 
    """ 报错 """
    print(m.span())
    """ (0,3) """
    
    p = r'(\d*[a-zA-Z]*)'  
    print(re.findall(p, s))  # 若p是compile所得，也可用 p.findall(s)
    """['abc', '', 'c', '', 'ac', '1bb', '', 'f', '']"""
    print(re.finditer(p, s))
    """<callable_iterator object at 0x0000024CA34B3AC0>"""
    print(list(re.finditer(p,s)))
    """[<re.Match object; span=(0, 3), match='abc'>, <re.Match object; span=(3, 3), match=''>, <re.Match object; span=(4, 5), match='c'>, <re.Match object; span=(5, 5), match=''>, <re.Match object; span=(6, 8), match='ac'>, <re.Match object; span=(8, 11), match='1bb'>, <re.Match object; span=(11, 11), match=''>, <re.Match object; span=(12, 13), match='f'>, <re.Match object; span=(13, 13), match=''>]"""
    ```
  
  - 检索和替换 sub
  
    ```python
    import re
    
    s = "abc.c!ac1bb f"
    # 删除字符串s中的数字，即把s中的数字替换为""
    p = r'(\d*)'
    repl = ""
    print(re.sub(p,repl,s,count=0)) # count:模式匹配后替换的最大次数，默认0,表示替换所有的匹配
    ```
  
  - 分割 split
  
    ```python
    import re
    
    s = "abc.c!ac1bb f"
    print(re.split('!', s))
    """['abc.c', 'ac1bb f']"""
    ```

--------------------------------------------------------------------------------------

正则测试网站：
https://regexr-cn.com/  https://c.runoob.com/front-end/854/



参考内容：

1.菜鸟教程
2.百度百科-正则表达式
