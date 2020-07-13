from settings import MAX_SCORE

class Proxy(object):
    def __init__(self, ip, port, protocol=-1, nick_type=-1, speed=-1, 
                 area=None, score=MAX_SCORE, disabled_domains=[]):
        self.ip = ip
        self.port = port
        # 支持协议 support 'http':'protocol=0; 'https':'protocol=1';both: 'protocol=2'
        self.protocol = protocol
        # 匿名程度 '高匿名':nick_type=0; '匿名':nick_type=1; '透明':nick_type=2 
        self.nick_type = nick_type
        self.speed = speed
        self.area = area
        self.score = score
        self.disabled_domains = disabled_domains

    # def __str__(self):
        # return str(self.__dict__)

    def url(self):
        return f"{self.ip}:{self.port}"

if __name__ == "__main__":
    p = Proxy('88.88.88.88', '88')      
    print(p.__dict__) 
