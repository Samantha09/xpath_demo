from lxml import etree
import requests
import re

BASE_DOMAiN = 'http://www.ygdy8.net'
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
}
url = 'http://www.ygdy8.net/html/gndy/dyzz/list_23_1.html'

def get_detail_urls(url):
    """获取详情页面URL"""
    detail_urls = []
    response = requests.get(url, headers=HEADERS)
    # requests库，默认使用自己猜测的编码去解码抓下来的网址，当编码猜测错误时，
    # 就会产生乱码，此时我们使用content，之后自己手工解码
    # print(response.text)
    text = response.text  # 乱码对爬虫程序没有任何影响
    html = etree.HTML(text)

    detail_urls_list = html.xpath("//table[@class='tbspan']//a/@href")
    detail_urls_list = list(map(lambda url:BASE_DOMAiN+url, detail_urls_list))
    return detail_urls_list

def parse_detail_page(url):
    movie_list = []
    movie = {}
    response = requests.get(url, headers=HEADERS)
    # print(response.content.decode('utf8'))
    text = response.content.decode('gbk')
    html = etree.HTML(text)
    title = html.xpath("//div[@class='title_all']//font[@color='#07519a']/text()")[0]
    movie["title"] = title

    zoom = html.xpath("//div[@id='Zoom']")[0]
    imgs = zoom.xpath(".//img/@src")
    movie["cover"] = imgs[0]
    movie["screenshot"] = imgs[1]

    infos = zoom.xpath("//text()")
    for index, info in enumerate(infos):
        if info.startswith("◎片　　长"):
            info = info.replace("◎片　　长", "").strip()
            movie["片长"] = info
        elif info.startswith("◎豆瓣评分"):
            info = re.findall(r'.*?([0-9].*?)[/].*?', info)
            if len(info) != 0:
                info = info[0]
                movie["豆瓣评分"] = float(info)
        elif info.startswith("◎主　　演"):
            info = info.replace("◎主　　演", "").strip()
            actors_list = [info]
            for x in (index+1, len(infos)-1):
                actor = infos[x].strip()
                if actor.startswith("◎"):
                    break
                if actor.strip() != '':
                    actors_list.append(actor)
            movie["主演"] = actors_list
        movie_list.append(movie)
    return movie_list




def spider():
    """爬取详情页"""
    url_list = []
    base_url = 'http://www.ygdy8.net/html/gndy/dyzz/list_23_{}.html'
    for x in range(1, 8):
        # 爬取前7页
        url = base_url.format(x)
        details_urls = get_detail_urls(url)
        for detail_url in details_urls:
            # 遍历一页当中所有电影的详情页
            print(detail_url)
            movie = parse_detail_page(detail_url)

    print(movie)


if __name__ == '__main__':
    spider()



