# 2.3 Mysql介绍与使用
&emsp;&emsp;在前面两小节中，我们分别学习了如何从网页中获得源代码，如何从源代码中获得我们想要的数据，那么我们怎么存储我们的数据呢？其实对于数据的存储，有好几种存储方式。较为简单的是存储在本地，如 txt、csv等。我们还可以存储在数据库中，例如 Mysql、MongoDB、Redis等。本章节我们将主要介绍将数据存储在 Mysql 中。

## 2.3.1准备工作
1. 安装好Mysql。若不知道如何安装，请查看[参考资料](https://cuiqingcai.com/31069.html)
2. 对于数据库的可视化，可以选用 dbeaver 。它是免费的，而且在功能上能满足我们的需求。具体的下载地址请点击[下载](https://dbeaver.io/download/)
3. 安装上述两个软件后安装Pymysql.
	
	运行下面的命令即可安装
```commandline
pip install pymysql
```


## 2.3.2 SQL语句
&emsp;&emsp;我们需要使用到数据库，那我们应该需要懂点Sql语句，以帮助我们在项目中的使用。我们不需要了解太多，我们只需要了解一些简单的操作，例如，如何创建表，如何进行数据的增删改查。现在就让我们来一起学习吧！在学习之前，请确保准备工作已经完成了。

- 连接数据库

	我们在开始学习之前，我们需要启动我们的Mysql服务。在中终端中输入以下命令：

```commandline
net start mysql80
```
这里输入可能会遇到错误，那是因为终端的权限不够，请设置管理员权限打开。这里 mysql80 你可以根据你安装时的设置进行选择。
	
接着，我们连接数据库。输入下面的命令：
```commandline
mysql -u root -p
```
然后，输入我们的密码就可以实现连接了。
	
- 创建数据库
```text
CREATE database 数据库名;
```	

- 查看数据库
```text
SHOW database;
```

- 选择数据库
```
USE 数据库名;
```

- 创建表
```text
CREATE TABLE customers
(cust_id int NOT NULL AUTO_INCREMENT,
 cust_name char(50) NOT NULL,
 PRIMARY KEY (cust_id)
);
```
初看一眼，可能会有点懵，让我们一点点了解它。 我们可以看到表的名字紧跟在 TABLE后面，对数据库表中的定义在括号里。第一个是定义的列名，第二个是数据的类型，第三个定义时否为空值，PRIMARY KEY定义数据库的主键，AUTO_INCREMENT告诉mysql,本列每当增加一行，自动增加。

- 删除表
```sql
DROP TABLE 表名;
```

- 插入数据
```sql
INSERT INTO customers(cust_id,
cust_name)
VALUES('1','xiaoming');
```

- 删除数据 删除特定的行
```sql
DELETE FROM customers
WHERE cust_id = 1;
```


- 检索数据
```sql
SELECT cust_id
FROM customers;  检索单个列
SELECT cust_id,cust_name
FROM customers;  检索多个列
```

&emsp;&emsp;上面只是sql语句的简单描述，更多的请看对应的书籍。我们简单了解下以上这些，就可以进行下一步的学习了。


## 2.3.3Pymysql使用
&emsp;&emsp;我们使用Python操作数据库，离不开pymysql的使用。下面为大家介绍pymysql的使用。希望小伙伴们能够掌握。
- 连接数据库
```python
conn = pymysql.connect(host='localhost',uesr='root',port='3306',passwd='xxxx',database='ceshi')
```
这里我们使用 connect 方法创建一个连接对象。host 参数为运行的 IP，由于我们运行在本地，所以填 localhost；user参数为用户名；port参数为端口号，默认为3306；passwd参数为密码，database连接的数据库名。

- 创建游标对象
```python
cursor = conn.cursor()
```

- 执行SQL语句
```python
cursor.execute('执行的SQL语句')
```

- 关闭数据库连接
```python
conn.close()
```

- 插入，删除 更新数据

对于这种操作，其实实际上就是执行sql语句。在编写SQL语句，传入到execute中，同时，还要调用commit方法即可。下面以一个例子，编写相应的代码。我们往数据库中创建一个customer的表，表中含有cust_id 和 cust_name两列。然后我们往里面进行插入新的值。代码如下
```python
import pymysql
# 连接数据库ceshi
conn = pymysql.connect(host='localhost', user='root',
                       port=3306, passwd='891292', database='ceshi')
# 创建游标对象
cursor = conn.cursor()
# 编写创建表的SQL语句
sql = "CREATE TABLE customer(cust_id int NOT NULL AUTO_INCREMENT,cust_name char(50) NULL,PRIMARY KEY (cust_id))"
# 编写插入语句，后面的值用格式化字符串代替
sql_insert = 'INSERT INTO customer (cust_id,cust_name) VALUES (%s,%s)'
# 执行sql语句
cursor.execute(sql)
try:
    # 执行sql_insert语句，同时传递值
    cursor.execute(sql_insert, (1, '小明'))
# 提交插入语句
    conn.commit()
except:
    # 如果发生错误进行回滚，表示什么操作没有执行。
    conn.rollback()
# 关闭数据库
conn.close()
```
对于删除，更新,跟插入数据是相似的，这里就不再介绍了。还希望小伙伴能自己亲手敲一下，看一下效果。
	
## 2.3.4总结
&emsp;&emsp;本小节，简单介绍sql语句和pymysql的使用。对于dbeaver没用做介绍，大家可以自行摸索。它还是非常不错的。知识不多，但我们还是多敲代码。

- 参考资料
	- 《pyton3网络爬虫开发实战第2版》
	- 《MYSQL必知必会》