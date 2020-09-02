基于Scrapy 2.3.0和requests爬取的豆瓣新片排行榜top10

爬虫逻辑解析：
一级：获取豆瓣新片榜top10电影基本信息
    yield->二级
        二级：获取电影的描述信息
            yield->三级
                三级：获取电影的短评列表(拼接下一页的url+requests循环分页获取)
                    yield->MongoDB存储       
                    
本人博客地址:https://blog.csdn.net/u013600907