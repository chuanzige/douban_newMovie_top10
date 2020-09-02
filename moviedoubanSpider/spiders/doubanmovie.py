from lxml import etree
import requests

import scrapy


class DoubanmovieSpider(scrapy.Spider):
    # 爬虫id 唯一
    name = 'doubanmovie'
    # 允许采集的域名(所有采集的数据仅限在当前域名下)
    allowed_domains = ['movie.douban.com']
    # 开始采集的网站
    start_urls = ['https://movie.douban.com/chart/']

    # 解析响应的数据，可以理解为一个http请求的的response
    # 一级信息->电影简介
    def parse(self, response):
        # 整个div的数据
        divResultList = response.xpath("//div[@class='pl2']")
        for result in divResultList:
            data = {}
            name = result.xpath(".//a/text()").extract_first().replace('/', '').strip()
            aliasName = result.xpath(".//a/span/text()").extract_first()
            info = result.xpath(".//p/text()").extract_first()
            rank = result.xpath(".//span[@class='rating_nums']/text()").extract_first()
            rankPeople = result.xpath(".//span[@class='pl']/text()").extract_first()
            linkUrl = result.xpath(".//a/@href").extract_first()
            data['name'] = name
            data['aliasName'] = aliasName
            data['info'] = info
            data['rank'] = rank
            data['rankPeople'] = rankPeople
            data['linkUrl'] = linkUrl
            yield scrapy.Request(url=linkUrl, callback=self.movieDetail, meta={'data': data})

    # 二级信息->电影详情
    def movieDetail(self, response):
        # 上级信息
        data = response.meta['data']
        movieDetail = {}
        # 电影剧情
        description = response.xpath("//div[@class='indent']/span/text()").extract_first().strip()
        movieDetail['description'] = description
        data['movieDetail'] = movieDetail
        # 短评列表后缀url
        suffixUrl = response.xpath("//div[@id='hot-comments']/a/@href").extract_first()
        # 短评列表完整url
        shortReviewUrl = data['linkUrl'] + suffixUrl
        yield scrapy.Request(url=shortReviewUrl, callback=self.shortReviewFor, meta={'data': data})

    # 循环三级评论信息url 交给处理三级信息
    def shortReviewFor(self, response):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
        }
        data = response.meta['data']
        shortReviewBaseUrl = response.url
        limit = 20
        start = 20
        shortReviewList = []
        while True:
            url = shortReviewBaseUrl + "&start=" + str(start) + "&limit=" + str(limit)
            start = start + 20
            res = requests.get(url=url, headers=headers).content.decode('utf8')
            xpathHtml = etree.HTML(res)
            evaluateList = xpathHtml.xpath("//div[@class='comment-item']")
            if len(evaluateList) < 20:
                break
            for evaluate in evaluateList:
                shortReviewMap = {}
                # 评价人的姓名
                people = evaluate.xpath(".//span[@class='comment-info']/a/text()")
                # 评级时间
                time = str(evaluate.xpath(".//span[@class='comment-time ']/text()")[0]).replace("\\n", "").strip()
                # 评价内容
                content = evaluate.xpath(".//span[@class='short']/text()")
                shortReviewMap['people'] = people
                shortReviewMap['time'] = time
                shortReviewMap['content'] = content
                shortReviewList.append(shortReviewMap)
            print("url========================================================" + url)
        data['shortReviewList1111'] = shortReviewList
        print(data)
        yield data
