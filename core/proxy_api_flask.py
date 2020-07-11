from flask import Flask, request
import json

from core.db.mongo_pool import MongoPool

class ProxyAPI_Flask(object):

    def __init__(self, count):
        self.count = count
        self.app = Flask(__name__)
        self.mongo_pool = MongoPool()

        @self.app.route('/random')
        def random():
            protocol = request.args.get('protocol')
            domain = request.args.get('domain')
            proxy = self.mongo_pool.random_proxy(protocol, domain, count=self.count)

            if protocol:
                return f"{protocol}://{proxy.ip}:{proxy.port}"
            else:
                return f"{proxy.ip}:{proxy.port}"

        @self.app.route('/proxies')
        def proxies():
            protocol = request.args.get('protocol')
            domain = request.args.get('domain')
            proxies = self.mongo_pool.get_proxies(protocol, domain, count=self.count)
            # 将Proxy对象列表转化为字典列表
            proxies = [proxy.__dict__ for proxy in proxies]
            # 将字典变为json返回
            return json.dumps(proxies)


    def run(self):
        self.app.run('0.0.0.0',port=16888)

if __name__ == '__main__':
    pa = ProxyAPI_Flask(50)
    pa.run()

    