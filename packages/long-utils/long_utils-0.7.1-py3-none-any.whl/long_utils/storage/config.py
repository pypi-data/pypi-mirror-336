class CosConfig(object):
    def __init__(self, region, secret_id, secret_key, bucket, token=None):
        self.region = region
        self.secret_id = secret_id
        self.secret_key = secret_key
        self.bucket = bucket
        self.token = token

    @property
    def region(self):
        return self.region

    @region.setter
    def region(self, value):
        self.region = value

    @property
    def secret_id(self):
        return self.secret_id

    @secret_id.setter
    def secret_id(self, value):
        self.secret_id = value

    @property
    def secret_key(self):
        return self.secret_key

    @secret_key.setter
    def secret_key(self, value):
        self.secret_key = value

    @property
    def bucket(self):
        return self.bucket

    @bucket.setter
    def bucket(self, value):
        self.bucket = value

    @property
    def token(self):
        return self.token

    @token.setter
    def token(self, value):
        self.token = value


class SSconfig(object):
    def __init__(self, access_key_id, access_key_secret, bucket_url, bucket_name):
        self._access_key_id = access_key_id
        self._access_key_secret = access_key_secret
        self._bucket_url = bucket_url
        self._bucket_name = bucket_name

    @property
    def access_key_id(self):
        return self._access_key_id

    @access_key_id.setter
    def access_key_id(self, value):
        self._access_key_id = value

    @property
    def access_key_secret(self):
        return self._access_key_secret

    @access_key_secret.setter
    def access_key_secret(self, value):
        self._access_key_secret = value

    @property
    def bucket_url(self):
        return self._bucket_url

    @bucket_url.setter
    def bucket_url(self, value):
        self._bucket_url = value

    @property
    def bucket_name(self):
        return self._bucket_name

    @bucket_name.setter
    def bucket_name(self, value):
        self._bucket_name = value
