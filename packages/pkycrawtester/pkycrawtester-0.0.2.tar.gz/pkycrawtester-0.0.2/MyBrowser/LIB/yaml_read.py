# -*- coding: utf-8 -*-
# ================================================
# 제목 : config 파일로 YAML 사용
# 날짜 : 2021.09.24
# 버전 : V0.1
# 설명 : Config 파일로 YAML 사용하기
# ================================================
import yaml
import logging

# 로거 설정
log = logging.getLogger('TEST')
log.debug("Logging Started... {}".format(__name__))

class Config(object):

    def __init__(self, config_file):

        config_file = config_file

    @staticmethod
    def read_yaml(yaml_file):
        """
            yaml file을 읽고 dictionery 리턴

            input: none
            output: dict()
        """

        with open(yaml_file, encoding='utf-8') as file:
            # The FullLoader parameter handles the conversion from YAML
            # scalar values to Python the dictionary format
            dict_data = yaml.load(file, Loader=yaml.FullLoader)

        return dict_data

    @staticmethod
    def write_yaml(dict_data, yaml_file):
        """
            yaml 파일에 데이타 쓰기 (dict --> yaml)
        """
        with open(yaml_file, 'w', encoding='utf-8') as file:
            yaml.dump(dict_data, file)


if __name__ == '__main__':

    import random

    cfg = Config('../example.yaml')
    data = cfg.read_yaml()
    print('Return Value =', data)
    print(len(data['email_list']))
    print(data['email_list'][0][0])
    random_number = random.randint(0, 1)
    user = data['email_list'][random_number]
    print('USER ({}) = {}'.format(random_number, user))
    for item, doc in data.items():
        print(item, ":", doc)

    print('dictionary data to yaml')
    cfg.write_yaml(data, 'zz.yaml')

    cfg1 = Config('example.yaml')
    data = cfg.read_yaml()
    print('Return Value =', data)
