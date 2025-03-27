import oss2
from src.long_utils.storage import SSconfig


class OssBase(object):
    def __init__(self, config: SSconfig):
        self.access_key_id = config.access_key_id
        self.access_key_secret = config.access_key_secret
        self.bucket_url = config.bucket_url
        self.bucket_name = config.bucket_name
        self._bucket = None

    @property
    def bucket(self):
        if not self._bucket:
            auth = oss2.Auth(self.access_key_id, self.access_key_secret)
            self._bucket = oss2.Bucket(auth, self.bucket_url, self.bucket_name)
        return self._bucket
