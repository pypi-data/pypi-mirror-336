from typing import Set, Optional, TextIO
import os
from bald_spider.duplicate_filter import BaseFilter
from bald_spider.utils.log import get_logger


class MemoryFilter(BaseFilter):
    def __init__(self, crawler):
        self.fingerprints: Set[str] = set()
        debug: bool = crawler.settings.getbool("FILTER_DEBUG")
        logger = get_logger(f"{self}", crawler.settings.get("LOG_LEVEL"))
        super().__init__(logger, crawler.stats, debug)
        self._file: Optional[TextIO] = None
        self.set_file(crawler.settings.get("REQUEST_DIR"))

    def __str__(self):
        return "MemoryFilter"

    def add(self, fp):
        self.fingerprints.add(fp)
        if self._file:
            self._file.write(fp + "\n")

    def __contains__(self, item):
        return item in self.fingerprints

    def set_file(self, item):
        return item in self.fingerprints

    def set_file(self, request_dir):
        if request_dir:
            self._file = open(os.path.join(request_dir, "request_fingerprints.txt"), "a+")
            self._file.seek(0)
            self.fingerprints.update(fp.strip() for fp in self._file)

    async def closed(self):
        if self._file:
            self._file.close()
# 使用集合进行过滤，因为不允许重复
# crawler中没必要持有一份过滤器，在哪里实例化，取决于过滤器要在那里用，本质上说，是在调度器上用的

































