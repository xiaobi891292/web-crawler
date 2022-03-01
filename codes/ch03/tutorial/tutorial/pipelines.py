# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymysql


class TutorialPipeline:
    @classmethod
    def from_crawler(cls, crawler):
        """从设置中，获取数据库中的设置"""
        cls.localhost = crawler.settings.get('LOCALHOST')
        cls.user = crawler.settings.get('USER')
        cls.password = crawler.settings.get('PASSWORD')
        cls.database = crawler.settings.get('DATABASE')
        return cls()

    def open_spider(self, spider):
        """该方法再Spider打开时被调用，连接数据库"""
        self.db = pymysql.connect(host=self.localhost, user=self.user,
                                  password=self.password,
                                  database=self.database)
        self.cursor = self.db.cursor()  # 创建一个游标对象。
        sql = "CREATE TABLE IF NOT EXISTS movie (name varchar(255)," \
              "time varchar(255),grade char(8),category varchar(255))"  #
        # 编写sql语句，在scrapytutorial数据库中movie表中创建字段名
        self.cursor.execute(sql)  # self.db.commit()

    def process_item(self, item, spider):
        """该方法被每一个item pipeline组件调用，插入数据"""
        name = item["name"]
        time = item["time"]
        grade = item["grade"]
        category = ''
        for i in item["category"]:
            category = category + "," + i
        insert_sql = 'INSERT INTO movie (name,time,grade,category) VALUES(%s,' \
                     '%s,%s,%s)'
        try:
            self.cursor.execute(insert_sql, (name, time, grade, category))
            self.db.commit()
        except:
            self.db.rollback()
        return item

    def close_spider(self, spider):
        """该函数在Spider关闭时被调用"""
        self.cursor.close()
        self.db.close()