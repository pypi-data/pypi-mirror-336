import aioredis

from bald_spider import Request
from bald_spider.duplicate_filter import BaseFilter
from bald_spider.utils.log import get_logger
from bald_spider.utils.request import request_fingerprint


class AioRedisFilter(BaseFilter):
    def __init__(self, redis_key, client, debug, stats, log_level, save_fp):
        logger = get_logger(f"{self}", log_level)
        super().__init__(logger, stats, debug)  # 重载父类方法
        self.redis_key = redis_key
        self.redis = client
        self.save_fp = save_fp


    @classmethod
    def create_instance(cls, crawler):
        redis_url = crawler.settings.get("REDIS_URL")
        decode_responses = crawler.settings.getbool("DECODE_RESPONSES")
        o = cls(redis_key=f"{crawler.settings.get('PROJECT_NAME')}:{crawler.settings.get('REDIS_KEY')}",
                client=aioredis.from_url(redis_url, decode_responses=decode_responses),
                debug=crawler.settings.getbool("FILTER_DEBUG"),
                save_fp=crawler.settings.getbool("SAVE_FP"),
                stats=crawler.stats,
                log_level=crawler.settings.get("LOG_LEVEL")
                )
        return o

    async def requested(self, request: Request) -> bool:
        fp = request_fingerprint(request)
        if await fp in self.redis.sismember(self.redis_key, fp):
            return True
        await self.add(fp)
        return False

    async def add(self, fp):
        await self.redis.sadd(self.redis_key, fp)

    def __str__(self):
        return "AioRedisFilter"

    def __contains__(self, item):
        return self.redis.sismember(self.redis_key, item)

    async def closed(self):
        if not self.save_fp:
            self.redis.delete(self.redis_key)













































