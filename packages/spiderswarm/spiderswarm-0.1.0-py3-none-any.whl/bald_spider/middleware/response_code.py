# coding: utf-8
# 状态码收集，对响应的预处理

from bald_spider.utils.log import get_logger


class ResponseCodeStats:
    def __init__(self, stats, log_level):
        self.logger = get_logger(self.__class__.__name__, log_level)
        self.stats = stats

    @classmethod
    def create_instance(cls, crawler):
        o = cls(
            stats=crawler.stats,
            log_level=crawler.settings.get("LOG_LEVEL")
        )
        return o

    def process_response(self, request, response, spider):
        self.stats.inc_value(f"stats_code/count/{response.status}")
        # 因为状态码是每一个都要收集，所以不能用info
        self.logger.debug(f"Got Response from <{response.status} {request.url}>")
        return response
