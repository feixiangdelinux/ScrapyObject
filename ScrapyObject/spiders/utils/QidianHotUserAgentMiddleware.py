# 导入UserAgenMiddleware组件模块
from fake_useragent import UserAgent
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware


# 设置随机设置user-agent
class QidianHotUserAgentMiddleware(UserAgentMiddleware):
    # 继承UserAgentMiddleware
    def process_request(self, request, spider):
        ua = UserAgent()
        # 生成随机的UserAgent
        request.headers['User-Agent'] = ua.random
        print(request.headers['User-Agent'])
