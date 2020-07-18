from multiprocessing import Process

from core.proxy_spider.run_spiders import RunSpider
from core.proxy_test import ProxyTest
from core.proxy_api_flask import ProxyAPI_Flask


def run():
    """启用多线程分别运行RunSpider， ProxyTest，ProxyAPI_Flask   
    """
    # 定义要启动的进程的列表
    process_list = [Process(target=RunSpider.start), Process(target=ProxyTest.start),
                    Process(target=ProxyAPI_Flask.start)]

    for process in process_list:
        # 设置守护进程 后台运行
        process.daemon = True
        process.start()

    for process in process_list:
        process.join()


if __name__ == '__main__':
    run()
