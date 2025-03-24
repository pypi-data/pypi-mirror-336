import base64
import math
import random
import string
import time


def list_with_page(result, page_num, page_len=10):
    data_sum = len(result)
    page_sum = math.ceil(data_sum / page_len)

    page_num = int(page_num) if page_num else 1
    page_list = result[page_len * (page_num - 1): page_len * page_num]
    return page_list, page_sum, data_sum


def set_login_token(expire=7200):
    """token简单加密"""
    token = '{}:{}'.format(get_random_str(8), str(time.time() + expire))
    b64_token = base64.b64encode(token.encode())
    str_token = str(b64_token, encoding='utf-8')
    return str_token


def get_login_token(b64_token):
    """token简单解密"""
    try:
        token = base64.b64decode(b64_token).decode()
    except:
        return ''
    return token


def get_random_str(str_len):
    return ''.join(random.sample(string.ascii_letters + string.digits, str_len))
