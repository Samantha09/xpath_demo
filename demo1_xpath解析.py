import requests
from lxml import etree

url = 'http://www.baidu.com/'

def get_html():
    """获取html"""
    response = requests.get(url)

    return response.content.decode('utf8')

def demo1(html_str):
    """使用xpath解析html"""
    htmlElement = etree.HTML(html_str)
    print(etree.tostring(htmlElement, encoding='utf8').decode('utf8'))

def parse_renren_file():
    """parse只会解析不会补充标签,这里使用parse没有补全而出错"""
    parser = etree.HTMLParser(encoding='utf8')
    htmlElement = etree.parse('./renren.html', parser=parser)
    print(etree.tostring(htmlElement, encoding='utf8').decode('utf8'))

if __name__ == '__main__':
    # html_str = get_html()
    # demo1(html_str)
    parse_renren_file()
