import logging

# 爬取的代理IP初始化最高分
MAX_SCORE = 50

# Default Log Configurations
LOG_LEVEL = logging.INFO
LOG_FORMAT = '%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s : %(message)s'
LOG_DATEFMT = '%Y-%m-%d %H:%M:%S'
LOG_FILENAME = 'log.log'

# Proxy Validate Timeout
VALIDATE_TIMEOUT = 10

# MongoDB 
MONGODB_URL = 'mongodb://localhost:27017/'
MONGODB_DB_NAME = 'proxies_pool'
MONGODB_COLLECTION_NAME = 'proxies'

# 爬虫库
PROXY_SPIDERS = [
    'core.proxy_spider.proxy_spiders.XiLaDaiLiSpider',
    'core.proxy_spider.proxy_spiders.KuaiDaiLiSpider'
]

# 运行爬虫的间隔时间(小时)
RUN_SPIDERS_INTERVAL = 12

# 检测数据库中代理IP可用性的异步任务的开启数量
PROXY_TEST_ASYNC_TASK_AMOUNT = 10