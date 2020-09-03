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
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
    }

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
        longUrl = response.xpath("//section[@id='reviews-wrapper']/p/a/@href").extract_first()
        # 短评列表完整url
        shortReviewUrl = data['linkUrl'] + suffixUrl
        # 影评列表完整url
        longReviewUrl = data['linkUrl'] + longUrl
        data['longLinkUrl'] = longReviewUrl
        yield scrapy.Request(url=shortReviewUrl, callback=self.shortReview, meta={'data': data})

    # 三级信息->短评列表
    def shortReview(self, response):
        data = response.meta['data']
        shortReviewBaseUrl = response.url
        print(shortReviewBaseUrl)
        limit = 20
        start = 20
        shortReviewList = []
        while True:
        # for i in range(1):
            url = shortReviewBaseUrl + "&start=" + str(start) + "&limit=" + str(limit)
            start = start + 20
            res = requests.get(url=url, headers=self.headers).content.decode('utf8')
            xpathHtml = etree.HTML(res)
            xpathList = xpathHtml.xpath("//div[@class='comment-item']")
            if len(xpathList) < 20:
                break
            for xpathResult in xpathList:
                result = {}
                # 评价人的姓名
                people = xpathResult.xpath(".//span[@class='comment-info']/a/text()")
                # 评级时间
                time = str(xpathResult.xpath(".//span[@class='comment-time ']/text()")[0]).replace("\\n", "").strip()
                # 评价内容
                content = xpathResult.xpath(".//span[@class='short']/text()")
                result['people'] = people
                result['time'] = time
                result['content'] = content
                shortReviewList.append(result)
            print("url========================================================" + url)
        data['shortReviewList1111'] = shortReviewList
        longLinkUrl = data['longLinkUrl']
        yield scrapy.Request(url=longLinkUrl, callback=self.longReview, meta={'data': data})

    # 四级信息->影评列表
    def longReview(self, response):
        data = response.meta['data']
        longReviewUrl = response.url
        start = 20
        longReviewList = []
        while True:
        # for i in range(1):
            url = longReviewUrl + "?start="+str(start)
            start = start+20
            res = requests.get(url=url, headers=self.headers).content.decode('utf8')
            xpathHtml = etree.HTML(res)
            xpathList = xpathHtml.xpath("//div[@class='main review-item']")
            if len(xpathList) < 20:
                break
            for xpathResult in xpathList:
                result = {}
                # 评价人姓名
                name = xpathResult.xpath(".//header/a[@class='name']/text()")
                # 评级
                score = xpathResult.xpath(".//span[1]/@title")
                # 评价时间
                time = xpathResult.xpath(".//span[2]")
                # 评价标题
                title = xpathResult.xpath(".//div[@class='main-bd']/h2/a/text()")
                # 评价详情链接
                linkUrl = str(xpathResult.xpath(".//div[@class='main-bd']/h2/a/@href")[0])
                # 评价详情
                content = self.longReviewContentDetail(linkUrl)
                result['name'] = name
                result['score'] = score
                result['time'] = time
                result['title'] = title
                result['linkUrl'] = linkUrl
                result['content'] = content
                longReviewList.append(result)
                pass
        data['longReviewList'] = longReviewList
        yield data

    # 影评详情内容
    def longReviewContentDetail(self, url):
        detail = {}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
        }
        res = requests.get(url=url, headers=headers).content.decode('utf8')
        xpathHtml = etree.HTML(res)
        xpathList = xpathHtml.xpath("//div[@id='link-report']")
        detail['content'] = str(xpathList[0].xpath(".//p/text()"))
        detail['contentImageUrl'] = xpathList[0].xpath(".//div[@class='image-wrapper']//img/@src")
        return detail

