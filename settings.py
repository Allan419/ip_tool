import logging

# 默认初始化最高分
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
