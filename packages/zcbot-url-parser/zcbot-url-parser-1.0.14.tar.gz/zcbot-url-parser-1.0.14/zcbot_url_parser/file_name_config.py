import logging
from typing import Union
from pymongo import MongoClient
from .constant import ZCBOT_PUBLIC_MONGO_URL, ZCBOT_PUBLIC_MONGO_DATABASE, ZCBOT_PUBLIC_MONGO_COLLECTION_FILE_NAME_CONFIG
from .utils import singleton


@singleton
class FileNameFormatter(object):
    """
    文件命名格式配置
    """
    logger = logging.getLogger(__name__)

    def __init__(self, mongo_url: str = None, mongo_database: str = None, mongo_collection_file_name_config: str = None):
        self.mongo_url = mongo_url or ZCBOT_PUBLIC_MONGO_URL
        self.mongo_database = mongo_database or ZCBOT_PUBLIC_MONGO_DATABASE
        self.mongo_collection_file_name_config = mongo_collection_file_name_config or ZCBOT_PUBLIC_MONGO_COLLECTION_FILE_NAME_CONFIG

        self.config_map = dict()
        self._init_rule_map()
        self.logger.info(f'===================')
        self.logger.info(f'有效文件名规则: {len(self.config_map)}条')
        self.logger.info(f'===================')

    def format_name(self, config_key: str, sn: str, row_id: str, index: str, sort: str, padding_index: str, padding_sort: str, image_type: str) -> Union[str, tuple]:
        _format = None
        if config_key:
            file_name_config = self.config_map.get(config_key) or {}
            # 1、优先按index读取mapper的配置
            mapper = file_name_config.get(f'{image_type}_mapper', {}) or file_name_config.get('mapper', {}) or {}
            _format = mapper.get(str(index), None) or mapper.get('ALL') or None
            # 2、如果mapper无对应index的配置（或无mapper），读取default字段
            if not _format:
                _format = file_name_config.get('default', None) or None
        # 3、如以上配置均无，使用固定默认格式
        if not _format:
            _format = '%(row_id)s-%(sort)s'

        return _format % {'sn': sn, 'row_id': row_id, 'index': index, 'sort': sort, 'padding_index': padding_index, 'padding_sort': padding_sort}

    def _init_rule_map(self):
        client = MongoClient(self.mongo_url)
        try:
            rs = client.get_database(self.mongo_database).get_collection(self.mongo_collection_file_name_config).find({})
            if rs:
                for row in list(rs):
                    self.config_map[row.get('_id')] = row
        except Exception as e:
            self.logger.error(e)
        finally:
            try:
                client.close()
            except Exception as e:
                self.logger.error(e)
