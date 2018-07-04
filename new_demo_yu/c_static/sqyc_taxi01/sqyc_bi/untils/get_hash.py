from hashlib import  sha1


def get_hash(str, salt =None):
    '''
    字符串散列值设置
    :param str:
    :param salt:
    :return:
    '''
    str = '!@#'+str+'$%^'

    if salt:
        str =str +salt

    sh = sha1()
    sh.update(str.encode('utf-8'))

    return  sh.hexdigest()
