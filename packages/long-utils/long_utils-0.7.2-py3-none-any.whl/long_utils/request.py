import requests
from requests.adapters import HTTPAdapter

requests.packages.urllib3.disable_warnings()  # 不打印安全警告


class Request(object):
    def __init__(self, max_retries=3, keep_alive=True, headers: dict = None):
        """
        :param max_retries: 最大重试次数
        :param keep_alive:
            设置为`True`时，requests库会尝试使用HTTP连接池来复用连接，这有助于提高性能和效率，因为建立和关闭TCP连接是一个耗时的操作。
            将其设置为`False`，那么每次发送请求后，连接都会被关闭。这可能在某些情况下是有用的，例如当你希望确保每次请求都是独立的或当你希望强制释放资源。
        :param headers:
        """
        self.max_retries = max_retries
        self.keep_alive = keep_alive
        if not headers:
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0"
            headers = {
                'User-Agent': user_agent
            }
        self.headers = headers
        self._session = None

    @property
    def session(self):
        if not self._session:
            session = requests.Session()
            session.keep_alive = self.keep_alive  #
            if self.headers:
                session.headers.update(self.headers)
            # 增加重试连接次数
            session.mount('http://', HTTPAdapter(max_retries=3))
            session.mount('https://', HTTPAdapter(max_retries=3))
            self._session = self
        return self._session
