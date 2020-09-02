Scrapy 2.3.0 and requests are on the top10 of the Scrapy new projects list

Crawler logic analysis:
Level 1: get basic information of top10 films on douban new film list
    Yield - > 2
        Level 2: Get descriptive information about the movie
            Yield - > 3
                Level 3: Get short list of movie reviews (get the url for next page + Requests for cyclic paging)
                    The yield - > MongoDB

My blog: https://blog.csdn.net/u013600907