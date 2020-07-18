from flask import Flask, request, render_template
import json

from core.db.mongo_pool import MongoPool
from utils.log import logger


class ProxyAPI_Flask(object):

    def __init__(self, count):
        self.count = count
        self.app = Flask(__name__, template_folder="../assets/templates")
        self.mongo_pool = MongoPool()

        @self.app.route('/')
        @self.app.route('/index')
        def index():
            return render_template("index.html")

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

        @self.app.route('/disable_domain')
        def disable_domain():
            ip = request.args.get('ip')
            domain = request.args.get('domain')

            if ip is None:
                return '请提供IP参数\n'
            if domain is None:
                return '请提供domain参数\n'

            self.mongo_pool.disable_domain(ip, domain)
            return f"{ip} 禁用域名 {domain} 成功"

    def run(self):
        self.app.run('0.0.0.0', port=16888)

    @classmethod
    def start(cls):
        pf = cls(100)
        logger.info('*****************Flask启动在localhost:16888端口，监听中*****************')
        pf.run()


if __name__ == '__main__':
    ProxyAPI_Flask.start()
