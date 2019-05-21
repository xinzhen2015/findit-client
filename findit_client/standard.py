# -*- coding:utf-8 -*-
from findit_client.base import FindItBaseClient
import warnings
import contextlib
import tempfile
import os

try:
    import cv2
except ImportError:
    warnings.warn('opencv-python is not found on your device. It is better to use the mini client only.')


@contextlib.contextmanager
def cv2file(pic_object):
    """ save cv object to file, and return its path """
    temp_pic_file_object = tempfile.NamedTemporaryFile(mode='wb+', suffix='.png', delete=False)
    temp_pic_file_object_path = temp_pic_file_object.name
    cv2.imwrite(temp_pic_file_object_path, pic_object)
    temp_pic_file_object.close()
    yield temp_pic_file_object_path
    os.remove(temp_pic_file_object_path)


class FindItStandardClient(FindItBaseClient):
    """
    powerful client, with all functions of findit. (need opencv installed)
    """
    def analyse_with_object(self, target_pic_object, template_pic_name):
        with cv2file(target_pic_object) as file_path:
            return self.analyse_with_path(file_path, template_pic_name)


if __name__ == '__main__':
    cli = FindItStandardClient(host='172.17.204.2', port=29412)
    assert cli.heartbeat()
    result = cli.analyse_with_path(u'../tests/pics/screen.png', u'desktop/wechat_logo.png')
    print(result)
