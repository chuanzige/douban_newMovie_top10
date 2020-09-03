from fake_useragent import UserAgent


# 随机切换UserAgent中间件
class UserAgentMiddleware(object):

    def __init__(self, crawler):
        super(UserAgentMiddleware, self).__init__()
        self.ua = UserAgent(verify_ssl=False)
        self.ua_type = crawler.settings.get("RANDOM_UA_TYPE", "random")

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):

        def get_user_agent():
            return getattr(self.ua, self.ua_type)
        request.headers.setdefault('User-Agent', get_user_agent())
