```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait  # 用于显示等待
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import json  # 用于处理json数据
import os
import logging

BASE_URL = 'https://spa1.scrape.center/page/{page}'
# 设置存储目录
RESULTS_DIR = 'results'
# 设置抓取的页数
ALL_PAGE = 2
# 设置等待时间
TIMEOUT = 10
logging.basicConfig(level=logging.INFO)

driver = webdriver.Edge()
# 由于需要等待网页元素的加载，使用webDriverWait。
wait = WebDriverWait(driver, timeout=TIMEOUT)


def request_page(url, location, condition):
    """func：用于请求每个页面
       url:页面的url
       location:页面某个元素的位置
       condition：等待条件"""
    try:
        # 请求页面
        driver.get(url)
        # 设置等待
        wait.until(condition(location))
        # 若出现报错，日志打印信息
    except TimeoutException:
        logging.error('请求 %s 错误', url, exc_info=True)


def request_index(page):
    """func:请求分页
       page:每个分页的页数"""
    page_url = BASE_URL.format(page=page)
    request_page(page_url, location=(
        By.XPATH, '//*[@id="index"]/div[1]/div[1]/div//a'), condition=EC.presence_of_element_located)


def parse_href():
    """提取每个电影详情页的url"""
    # 寻找分页中的所有电影所在的div下的a标签，大家可以自行查看
    elements = driver.find_elements(
        By.XPATH, '//*[@id="index"]/div[1]/div[1]/div/div[1]/div[1]/div[1]/a')
    for element in elements:
        yield element.get_attribute('href')


def parse_detail(url):
    """func:提取详情页中的数据
       url:详情页的url"""
    # 请求页面
    request_page(url, location=(
        By.XPATH, '//*[@id="detail"]/div[1]/div/div/div[1]/div/div[2]/a/h2'), condition=EC.presence_of_element_located)
    name = driver.find_element(
        By.XPATH, '//*[@id="detail"]/div[1]/div/div/div[1]/div/div[2]/a/h2').text
    class_list = driver.find_elements(
        By.XPATH, '//*[@id="detail"]/div[1]/div/div/div[1]/div/div[2]/div[1]//span')
    classs = [i.text for i in class_list]
    image = driver.find_element(By.CSS_SELECTOR, '.cover').get_attribute('src')
    time = driver.find_element(
        By.XPATH, '//*[@id="detail"]/div[1]/div/div/div[1]/div/div[2]/div[3]/span').text
    score = driver.find_element(By.CSS_SELECTOR, '.score').text
    return {
        'url': url,
        'name': name,
        'classs': classs,
        'image_url': image,
        'time': time,
        'score': score
    }


if not os.path.exists(RESULTS_DIR):
    os.makedirs(RESULTS_DIR)


def save_data(data):
    """func：用于保存数据
       data:parse_detail返回的数据"""
    name = data.get('name')
    data_path = f'{RESULTS_DIR}/{name}.json'
    json.dump(data, open(data_path, 'w', encoding='utf-8'), ensure_ascii=False,
              indent=2)


if __name__ == '__main__':
    for i in range(1, ALL_PAGE + 1):
        request_index(i)
        detail_list = parse_href()
        for detail_url in list(detail_list):
            result = parse_detail(detail_url)
            save_data(result)
    driver.close()
```