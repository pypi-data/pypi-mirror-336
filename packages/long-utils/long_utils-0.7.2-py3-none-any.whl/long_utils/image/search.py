import typing
import cv2
import numpy as np


class ImgFindImg(object):
    """
    图中找图，从原图中找小图
    """

    def __init__(self, img_source, img_search):
        """
        :param img_source: 原图，路径或流式图片
        :param img_search: 原图中的小图，路径或流式图片
        """
        self._img_source = img_source
        self._img_search = img_search

    def find_template(self, im_source: typing.Union[str, bytes], im_search: typing.Union[str, bytes], threshold=0.5, rgb=False, bgremove=False):
        result = self.find_all_template(im_source, im_search, threshold, 1, rgb, bgremove)
        return result[0] if result else None

    def find_coord(
            self,
            threshold=0.95,
            max_count=0,
            is_debug=False,
            debug_local_file='local_debug.png',
            rgb=False,
            bgremove=False
    ):
        """
        获取坐标和相似值
        :param threshold: 阈值，当相识度小于该阈值的时候，就忽略掉
        :param max_count:
        :param is_debug: 是否使用debug模式，该模式下会生成本地图片。带上标注的坐标位置。
        :param debug_local_file: debug模式下才会使用该值
        :param rgb:
        :param bgremove:
        :return:
            [
                {'result': (539.0, 21.5), 'rectangle': ((524, 10), (524, 33), (554, 10), (554, 33)), 'confidence': 0.9999780058860779}
            ]
        """
        im_source = self._img_source
        im_search = self._img_search
        if isinstance(im_source, str):
            im_source = cv2.imread(im_source, cv2.IMREAD_COLOR)
        if isinstance(im_search, str):
            im_search = cv2.imread(im_search, cv2.IMREAD_COLOR)
        method = cv2.TM_CCOEFF_NORMED
        if rgb:
            s_bgr = cv2.split(im_search)  # Blue Green Red
            i_bgr = cv2.split(im_source)
            weight = (0.3, 0.3, 0.4)
            resbgr = [0, 0, 0]
            for i in range(3):  # bgr
                resbgr[i] = cv2.matchTemplate(i_bgr[i], s_bgr[i], method)
            res = resbgr[0] * weight[0] + resbgr[1] * weight[1] + resbgr[2] * weight[2]
        else:
            s_gray = cv2.cvtColor(im_search, cv2.COLOR_BGR2GRAY)
            i_gray = cv2.cvtColor(im_source, cv2.COLOR_BGR2GRAY)
            # 边界提取(来实现背景去除的功能)
            if bgremove:
                s_gray = cv2.Canny(s_gray, 100, 200)
                i_gray = cv2.Canny(i_gray, 100, 200)

            res = cv2.matchTemplate(i_gray, s_gray, method)
        w, h = im_search.shape[1], im_search.shape[0]

        result = []
        while True:
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
                top_left = min_loc
            else:
                top_left = max_loc
            if max_val < threshold:
                break
            # calculator middle point
            middle_point = (top_left[0] + w / 2, top_left[1] + h / 2)
            result.append(dict(
                result=middle_point,
                rectangle=(top_left, (top_left[0], top_left[1] + h), (top_left[0] + w, top_left[1]),
                           (top_left[0] + w, top_left[1] + h)),
                confidence=round(max_val, 3)
            ))
            if max_count and len(result) >= max_count:
                break
            # floodfill the already found area
            cv2.floodFill(res, None, max_loc, (-1000,), max_val - threshold + 0.1, 1, flags=cv2.FLOODFILL_FIXED_RANGE)
        if is_debug:
            for i in result:
                x, y, x1, y1 = list(i['rectangle'])
                cv2.line(im_source, x, x1, (0, 255, 0))
                cv2.line(im_source, x, y, (0, 255, 0))
                cv2.line(im_source, x1, y1, (0, 255, 0))
                cv2.line(im_source, y, y1, (0, 255, 0))
            cv2.imwrite(debug_local_file, im_source)
        else:
            return result

    @staticmethod
    def imread(bytes_content):
        """
        :param bytes_content: 图片的字节内容
        :return:
        """
        im = cv2.imdecode(np.frombuffer(bytes_content, np.uint8), cv2.IMREAD_COLOR)
        return im

    def run(self):
        f = open('big.png', 'rb')
        source_bytes = f.read()
        f.close()
        print(type(source_bytes))

        # 目标图片
        f1 = open('small.png', 'rb')
        target_bytes = f1.read()
        f1.close()

        source = self.imread(source_bytes)
        target = self.imread(target_bytes)
        match_result = self.find_all_template(source, target, threshold=0.95)

        # 把目标的区域画出来
        img = self.imread(source_bytes)
        for i in match_result:
            x, y, x1, y1 = list(i['rectangle'])
            cv2.line(img, x, x1, (0, 255, 0))
            cv2.line(img, x, y, (0, 255, 0))
            cv2.line(img, x1, y1, (0, 255, 0))
            cv2.line(img, y, y1, (0, 255, 0))
        cv2.imwrite('aaa.png', img)


if __name__ == '__main__':
    find_img = ImgFindImg()
    find_img.run()
