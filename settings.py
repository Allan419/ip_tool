import logging

# 默认初始化最高分
MAX_SCORE = 50

# Default Log Configurations
LOG_LEVEL = logging.INFO
LOG_FORMAT = '%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s : %(message)s'
LOG_DATEFMT = '%Y-%m-%d %H:%M:%S'
LOG_FILENAME = 'log.log'
LOG_PROXY_SPIDER = 'ProxySpider.log'

# Proxy Validate Timeout
VALIDATE_TIMEOUT = 10

# MongoDB 
MONGODB_URL = 'mongodb://localhost:27017/'
MONGODB_DB_NAME = 'proxies_pool'
MONGODB_COLLECTION_NAME = 'proxies'

PROXY_SPIDERS = [
    'core.proxy_spider.proxy_spiders.XiLaDaiLiSpider',
    'core.proxy_spider.proxy_spiders.KuaiDaiLiSpider'
]

# 运行爬虫的间隔时间
RUN_SPIDERS_INTERVAL = 12
