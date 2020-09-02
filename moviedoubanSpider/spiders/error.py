# import scrapy
#
#
# class DoubanmovieSpider(scrapy.Spider):
#     # 爬虫id 唯一
#     name = 'doubanmovie'
#     # 允许采集的域名(所有采集的数据仅限在当前域名下)
#     allowed_domains = ['movie.douban.com']
#     # 开始采集的网站
#     start_urls = ['https://movie.douban.com/chart/']
#
#     # 解析响应的数据，可以理解为一个http请求的的response
#     # 一级信息->电影简介
#     def parse(self, response):
#         # 整个div的数据
#         divResultList = response.xpath("//div[@class='pl2']")
#         i = 1
#         for result in divResultList:
#             data = {}
#             name = result.xpath(".//a/text()").extract_first().replace('/', '').strip()
#             aliasName = result.xpath(".//a/span/text()").extract_first()
#             info = result.xpath(".//p/text()").extract_first()
#             rank = result.xpath(".//span[@class='rating_nums']/text()").extract_first()
#             rankPeople = result.xpath(".//span[@class='pl']/text()").extract_first()
#             linkUrl = result.xpath(".//a/@href").extract_first()
#             # print("电影名称:" + name)
#             # print("电影别名:" + aliasName)
#             # print("电影简介:" + info)
#             # print("电影评分:" + rank)
#             # print("评分人数:" + rankPeople)
#             # print("链接:" + linkUrl)
#             # print("\n")
#             i = i + 1
#             data['name'] = name
#             data['aliasName'] = aliasName
#             data['info'] = info
#             data['rank'] = rank
#             data['rankPeople'] = rankPeople
#             data['linkUrl'] = linkUrl
#             yield scrapy.Request(url=linkUrl, callback=self.movieDetail, meta={'data': data})
#
#     # 二级信息->电影详情
#     def movieDetail(self, response):
#         # 上级信息
#         data = response.meta['data']
#         movieDetail = {}
#         # 电影剧情
#         description = response.xpath("//div[@class='indent']/span/text()").extract_first().strip()
#         movieDetail['description'] = description
#         data['movieDetail'] = movieDetail
#         # 短评列表后缀url
#         suffixUrl = response.xpath("//div[@id='hot-comments']/a/@href").extract_first()
#         # 短评列表完整url
#         shortReviewUrl = data['linkUrl'] + suffixUrl
#         yield scrapy.Request(url=shortReviewUrl, callback=self.shortReviewFor, meta={'data': data})
#
#     # 循环三级评论信息url 交给处理三级信息
#     def shortReviewFor(self, response):
#         data = response.meta['data']
#         print(data['name'])
#         shortReviewBaseUrl = response.url
#         limit = 20
#         for i in range(20):
#             print(i)
#             url = shortReviewBaseUrl + "&start=" + str(self.start) + "&limit=" + str(limit)
#             print("url========================================================" + url)
#             self.start = self.start + 20
#             yield scrapy.Request(url=url, callback=self.shortReviewList)
#         data['shortReviewList1111'] = self.tempList
#         print(data)
#         self.tempList = []
#         self.start = 20
#
#     # 临时存放的评论列表
#     tempList = []
#     start = 20
#
#     # 三级信息->短评列表
#     def shortReviewList(self, response):
#         # 评价列表
#         evaluateList = response.xpath("//div[@class='comment-item']")
#         shortReviewList = []
#         for evaluate in evaluateList:
#             shortReviewMap = {}
#             # 评价人的姓名
#             people = evaluate.xpath(".//span[@class='comment-info']/a/text()").extract_first()
#             # 评级时间
#             time = str(evaluate.xpath(".//span[@class='comment-time ']/text()").extract_first()).replace("\n",
#                                                                                                          "").strip()
#             # 评价内容
#             content = evaluate.xpath(".//span[@class='short']/text()").extract()
#             shortReviewMap['people'] = people
#             shortReviewMap['time'] = time
#             shortReviewMap['content'] = content
#             shortReviewList.append(shortReviewMap)
#         self.tempList += shortReviewList
#         pass
