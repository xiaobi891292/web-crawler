import scrapy
from tutorial.items import TutorialItem
from time import sleep


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['ssr1.scrape.center']
    base_url = 'https://ssr1.scrape.center'
    max_page = 10  # 由于我们网页的最大页数是10

    def start_requests(self):
        """实现翻页功能，手动发起请求。"""
        for i in range(1, self.max_page + 1):
            url = f'{self.base_url}/page/{i}'  # 构建每页的url，实现翻页功能。
            sleep(5)
            yield scrapy.Request(url=url, callback=self.parse_index)

    def parse_index(self, response):
        """解析页面，获得页面中每个电影的链接，并发起请求"""
        # 使用下xpath获取所有含有属性为href的标签
        hrefs = response.xpath(
            '//*[@id="index"]/div[1]/div[1]/div/div/div/div[1]/a/@href')
        # //*[@id="index"]/div[1]/div[1]
        # 遍历所所得href属性值的标签，使用getall()方法获得其值，否则是一个选择器对象列表。
        for href in hrefs.getall():
            # 使用urljoin方法拼接完整的url
            new_url = response.urljoin(href)
            # 手动发起请求，并调用parse_page方法
            sleep(5)
            yield scrapy.Request(url=new_url, callback=self.parse_detail)

    def parse_detail(self, response):
        item = TutorialItem()
        item['name'] = response.xpath(
            '//*[@id="detail"]/div[1]/div/div/div[1]/div/div[2]/a/h2/text('
            ')').get()
        item['time'] = response.xpath(
            '//*[@id="detail"]/div[1]/div/div/div[1]/div/div[2]/div['
            '3]/span/text()').get()
        item['grade'] = response.xpath(
            '//*[@id="detail"]/div[1]/div/div/div[1]/div/div[3]/p[1]/text('
            ')').re_first(
            r"\d.+")
        # 由于使用get函数获得匹配效果中含有换行符和空格,因此我们改用正则来提取。提供了两种一个是re，返回的是个数据列表
        # 另一个是re_first返回的是单个数据。具体的测试可以用scrapy shell命令。
        item['category'] = response.xpath(
            '//*[@id="detail"]/div[1]/div/div/div[1]/div/div[2]/div['
            '1]//span/text()').getall()
        yield item