import logging
from typing import Dict
from pymongo import MongoClient
from .constant import ZCBOT_PUBLIC_MONGO_URL, ZCBOT_PUBLIC_MONGO_DATABASE, ZCBOT_PUBLIC_MONGO_COLLECTION_IMAGE_THUMB_CONFIG
from .utils import singleton


@singleton
class ImageThumbConfig(object):
    """
    缩略图尺寸配置
    """
    logger = logging.getLogger(__name__)

    def __init__(self, mongo_url: str = None, mongo_database: str = None, mongo_collection_image_thumb_config: str = None):
        self.mongo_url = mongo_url or ZCBOT_PUBLIC_MONGO_URL
        self.mongo_database = mongo_database or ZCBOT_PUBLIC_MONGO_DATABASE
        self.mongo_collection_image_thumb_config = mongo_collection_image_thumb_config or ZCBOT_PUBLIC_MONGO_COLLECTION_IMAGE_THUMB_CONFIG

        self.config_map = dict()
        self._init_rule_map()
        self.logger.info(f'===================')
        self.logger.info(f'缩略图尺寸配置规则: {len(self.config_map)}条')
        self.logger.info(f'===================')

    def get_thumbs(self, config_key: str) -> Dict:
        if config_key and config_key in self.config_map:
            return self.config_map.get(config_key).get('thumbs', {}) or {}
        return {}

    def _init_rule_map(self):
        client = MongoClient(self.mongo_url)
        try:
            rs = client.get_database(self.mongo_database).get_collection(self.mongo_collection_image_thumb_config).find({})
            if rs:
                for row in list(rs):
                    self.config_map[row.get('_id')] = row
        except Exception as e:
            print(e)
        finally:
            try:
                client.close()
            except Exception as e:
                self.logger.error(e)
