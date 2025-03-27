import mimetypes
import os
import time
from oss2 import CaseInsensitiveDict
import oss2
from long_utils.storage.aliyun.oss_base import OssBase
from long_utils.storage.config import SSconfig
from long_utils.utils import str_to_md5
from oss2 import SizedFileAdapter, determine_part_size
from oss2.models import GetBucketLocationResult
from oss2.models import ListBucketCnameResult
from oss2.models import RequestResult
from oss2.models import PutObjectResult
from oss2.models import PartInfo
from long_utils.request import Request

class AliyumOss(OssBase):
    """
    阿里云OSS对象存储
    文档：
        https://help.aliyun.com/document_detail/32026.html?spm=a2c4g.11186623.6.994.4aff196bVJxXwO
    """

    def __init__(self, config: SSconfig, address=None):
        super(AliyumOss, self).__init__(config=config)
        self.address = address
        endpoint_host, endpoint_sec = config.bucket_url.split('//')
        self.endpoint_host = endpoint_host  # http:
        object_image_url = f"{config.bucket_name}.{endpoint_sec}"
        self.object_image_url = object_image_url
        self.request = Request(max_retries=3)

    def multipart_upload_file(self, key, file, parent=None, limit_file_size=1024 * 1024 * 20, progress_callback=None):
        """

        :param key: 对象key
        :param file: 要上传的本地文件
        :param parent: parent.running 控制是否暂停, parent.running=False时暂停
        :param limit_file_size: 分片大小
        :param progress_callback: 回调函数
        :return:
        """
        total_size = os.path.getsize(file)
        upload_id = self.bucket.init_multipart_upload(key).upload_id
        part_size = determine_part_size(total_size, preferred_size=limit_file_size)
        parts = []
        is_completed = True
        # 逐个上传分片。
        with open(file, 'rb') as fileobj:
            part_number = 1
            offset = 0
            while offset < total_size:
                if parent and not getattr(parent, 'running', True):
                    is_completed = False
                    break
                num_to_upload = min(part_size, total_size - offset)
                # 调用SizedFileAdapter(fileobj, size)方法会生成一个新的文件对象，重新计算起始追加位置。
                result = self.bucket.upload_part(
                    key=key,
                    upload_id=upload_id,
                    part_number=part_number,
                    data=SizedFileAdapter(fileobj, num_to_upload)
                )
                parts.append(PartInfo(part_number, result.etag))
                offset += num_to_upload
                part_number += 1
                if progress_callback:
                    progress_callback(offset, total_size)
        if is_completed:
            # 完成分片上传
            self.bucket.complete_multipart_upload(key, upload_id, parts)
        else:
            self.bucket.abort_multipart_upload(key, upload_id)

    def object_exists(self, key) -> bool:
        """
        判断一个文件是否存在于oss
        @param key: 文件 key
        @return: bool
        """
        # 返回值为true表示文件存在，false表示文件不存在。
        return self.bucket.object_exists(key)

    def check_bucket_location(self):
        result: 'GetBucketLocationResult' = self.bucket.get_bucket_location()
        if not result.location in self.bucket_url:
            raise Exception('选择的地域与存储空间所处地域不一致!')
        return result

    def put_object(self, key: str, data: str):
        self.bucket.put_object(key, data)

    def upload_file_str(self, key, content: str, headers=None, progress_callback=None):
        """
        功能：上传字符串
        文档：
            https://help.aliyun.com/document_detail/88426.html?spm=a2c4g.11186623.6.1018.1913bc51aVHPz6
        :param key:
        :param content:
        :param headers:
        :param progress_callback:
        :return:
        """
        result = self.bucket.put_object(key=key, data=content, headers=headers, progress_callback=progress_callback)
        # HTTP返回码。
        if result.status == 200:
            return key

    def check_bucket_name(self):
        """检查存储空间是否存在"""
        list_bucket_cname: 'ListBucketCnameResult' = self.bucket.list_bucket_cname()
        return list_bucket_cname.status

    def upload_local_file(self, key, local_file, headers=None, progress_callback=None):
        """
        上传一个本地文件到OSS的普通文件。
        :param str key: 上传到OSS的文件名
        :param str local_file: 本地文件名，需要有可读权限

        :param headers: 用户指定的HTTP头部。可以指定Content-Type、Content-MD5、x-oss-meta-开头的头部等
        :type headers: 可以是dict，建议是oss2.CaseInsensitiveDict

        :param progress_callback: 用户指定的进度回调函数。参考 :ref:`progress_callback`

        :return: : key
        """
        result: 'oss2.models.PutObjectResult' = self.bucket.put_object_from_file(
            key=key,
            filename=local_file,
            headers=headers,
            progress_callback=progress_callback
        )
        if result.status == 200:
            return key

    def set_key_acl(self, key, flag="public", headers=None):
        """管理文件访问权限"""
        permission = oss2.OBJECT_ACL_PUBLIC_READ
        if flag == "private":
            permission = oss2.OBJECT_ACL_PRIVATE
        self.bucket.put_object_acl(key, permission, headers=headers)

    def upload_image(self, file, progress_callback=None):
        """
        上传图片到oss上
        flag=file表示本地文件，或者file就对应bytes
        """
        if isinstance(file, str):
            content_type, _ = mimetypes.guess_type(file)
            img_suffix = mimetypes.guess_extension(content_type)
            with open(file, 'rb') as fp:
                data = fp.read()
        else:
            data = file
            img_suffix = ".jpg"
        file_name = f"{str_to_md5(content=data)}{img_suffix}"
        key = f'images/{time.strftime("%Y", time.localtime())}'
        key += f"/{time.strftime('%Y%m', time.localtime())}/{file_name}"
        headers = CaseInsensitiveDict()
        headers['content-disposition'] = 'inline'
        result = self.bucket.put_object(
            key=key,
            data=data,
            headers=headers,
            progress_callback=progress_callback
        )
        # HTTP返回码。
        if result.status == 200:
            return file_name, key

    def get_sign_url(self, key, expires=3600, headers=None, params=None, slash_safe=False, additional_headers=None):
        """生成下载文件的签名URL，有效时间为60秒。
        常见的用法是生成加签的URL以供授信用户下载，如为log.jpg生成一个5分钟后过期的下载链接::

            >>> bucket.sign_url('GET', 'log.jpg', 5 * 60)
            r'http://your-bucket.oss-cn-hangzhou.aliyuncs.com/logo.jpg?OSSAccessKeyId=YourAccessKeyId\&Expires=1447178011&Signature=UJfeJgvcypWq6Q%2Bm3IJcSHbvSak%3D'

        :param key: 文件名
        :param expires: 过期时间（单位：秒），链接在当前时间再过expires秒后过期

        :param headers: 需要签名的HTTP头部，如名称以x-oss-meta-开头的头部（作为用户自定义元数据）、
            Content-Type头部等。对于下载，不需要填。
        :type headers: 可以是dict，建议是oss2.CaseInsensitiveDict

        :param params: 需要签名的HTTP查询参数

        :param slash_safe: 是否开启key名称中的‘/’转义保护，如果不开启'/'将会转义成%2F
        :type slash_safe: bool

        :param additional_headers: 额外的需要签名的HTTP头

        :return: 签名URL。
        """
        # 指定Header。
        if not headers:
            headers = dict()
            # 如果您希望实现浏览器访问时自动下载文件，并自定义下载后的文件名称，配置文件HTTP头中的Content-Disposition为attachment
            # headers['Content-Disposition'] = 'attachment'
            # 如果您希望直接在浏览器中预览文件，配置文件HTTP头中的Content-Disposition为inline并使用Bucket绑定的自定义域名进行访问。
            headers['content-disposition'] = 'inline'

        # 生成下载文件的签名URL，有效时间为60秒。
        # 生成签名URL时，OSS默认会对Object完整路径中的正斜线（/）进行转义，从而导致生成的签名URL无法直接使用。
        # 设置slash_safe为True，OSS不会对Object完整路径中的正斜线（/）进行转义，此时生成的签名URL可以直接使用。
        url = self.bucket.sign_url('GET', key,
                                   expires=expires,
                                   slash_safe=slash_safe,
                                   headers=headers,
                                   params=params,
                                   additional_headers=additional_headers
                                   )
        if self.address:
            url = url.replace('https://', 'http://')
            url = url.replace(self.object_image_url, self.address)
        return url

    def download_to_file(self, key, local_file):
        """
        功能：
            oss 下载到本地文件
        @param key: 文件 key
        @param local_file: 本地文件
        @return: 返回本地文件路径
        """
        # 下载OSS文件到本地文件。如果指定的本地文件存在会覆盖，不存在则新建。
        #  <yourLocalFile>由本地文件路径加文件名包括后缀组成，例如/users/local/myfile.txt。
        #  <yourObjectName>表示下载的OSS文件的完整名称，即包含文件后缀在内的完整路径，例如abc/efg/123.jpg。
        # 如果是下载到本地存在多级目录的话，需要自行创建目录，如：2020/12/06/dmeo.json 这种的话就要自行创建 2020/12/06 目录。
        res = self.bucket.get_object_to_file(key, local_file)
        if res.status == 200:
            return key

    def get_content(self, key, result_flag='str'):
        """
        修改成通过服务器请求内网的oss内容，节省流量
        @param key:
        @param result_flag:
        @return:
        """
        try:
            if self.address:
                url = self.get_sign_url(key=key)
                response = self.request.session.get(url=url, timeout=120)
                return response.content.decode() if result_flag == 'str' else response.content
            res = self.bucket.get_object(key=key)
            if res:
                return res.read().decode() if result_flag == 'str' else res.read()
        except Exception as e:
            raise Exception(e)

    def del_key(self, key) -> bool:
        """
        删除 key
        @param key:
        @return: bool
        """
        result: RequestResult = self.bucket.delete_object(key=key)
        if result.status == 204:
            return True
        return False

    def move_object(self, source_key: str, target_key: str, is_del_old_key=False)->bool:
        """
        将 一个文件 移动到 另一个文件中
        @param source_key: 源文件名
        @param target_key: 目标文件名
        @param is_del_old_key: 是否需要删除旧的 key
        @return:
        """
        put_result: 'PutObjectResult' = self.bucket.copy_object(self.bucket_name, source_key, target_key)
        if put_result.status == 200:
            if is_del_old_key:
                is_del = self.del_key(key=source_key)
                if is_del:
                    return True
            return True
        return False

    def resumable_download(self, key, local_file, progress_callback=None, timeout=600)->bool:
        """
        下载文件
        :param key:
        :param local_file: 本地文件路径
        :param progress_callback:
        :param timeout: 针对内网地址下载时有用 , 默认为 600秒 超时
        :return: bool
        """
        if self.address:
            url = self.get_sign_url(key=key)
            response = self.request.session.get(url=url, timeout=600)
            with open(local_file, 'wb', encoding='utf-8') as fp:
                fp.write(response.content)
            return True
        oss2.resumable_download(
            self.bucket,
            key=key,
            filename=local_file,
            progress_callback=progress_callback
        )
        return True
