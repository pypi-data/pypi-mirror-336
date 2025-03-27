import re
import logging
from pymongo import MongoClient
from .constant import ZCBOT_PUBLIC_MONGO_URL, ZCBOT_PUBLIC_MONGO_DATABASE, ZCBOT_PUBLIC_MONGO_COLLECTION_PLATFORMS, ZCBOT_PUBLIC_MONGO_COLLECTION_RULES
from .utils import singleton


@singleton
class RuleHolder(object):
    """
    常见电商平台商品编码解析规则
    """
    logger = logging.getLogger(__name__)
    rule_map = {}

    def __init__(self, mongo_url: str = None, mongo_database: str = None, mongo_collection_platforms: str = None, mongo_collection_rules: str = None):
        self.mongo_url = mongo_url or ZCBOT_PUBLIC_MONGO_URL
        self.mongo_database = mongo_database or ZCBOT_PUBLIC_MONGO_DATABASE
        self.mongo_collection_platforms = mongo_collection_platforms or ZCBOT_PUBLIC_MONGO_COLLECTION_PLATFORMS
        self.mongo_collection_rules = mongo_collection_rules or ZCBOT_PUBLIC_MONGO_COLLECTION_RULES
        self.reload()

    def get_rule(self, host):
        return self.rule_map.get(host)

    def reload(self):
        """
        加载最新规则，可挂到定时任务上定期更新
        :return:
        """
        plats = self._fetch_platforms()
        plat_map = {}
        for plat in plats:
            plat_map[plat.get('_id')] = plat.get('name')

        rows = self._fetch_url_rules()
        for row in rows:
            regex_list = row.get('regex', [])
            patterns = []
            for regex in regex_list:
                try:
                    patterns.append(re.compile(regex))
                except re.error:
                    self.logger.error(f'错误规则: regex={regex}, row={row}')

            plat_code = row.get('plat_code')
            plat_name = row.get('plat_name', None) or plat_map.get(plat_code) or plat_code
            self.rule_map[row.get('_id')] = {
                'plat_code': plat_code,
                'plat_name': plat_name,
                'sku_param': row.get('params', []),
                'patterns': [
                    re.compile(x) for x in row.get('regex', [])
                ],
            }
        self.logger.info(f'更新链接分拣规则: {len(self.rule_map)}条')

    def _fetch_platforms(self):
        try:
            client = MongoClient(self.mongo_url)
            rs = client.get_database(self.mongo_database).get_collection(self.mongo_collection_platforms).find()
            rows = list(rs)
            client.close()
            return rows
        except Exception as e:
            self.logger.error(e)

        return []

    def _fetch_url_rules(self):
        try:
            client = MongoClient(self.mongo_url)
            rs = client.get_database(self.mongo_database).get_collection(self.mongo_collection_rules).find()
            rows = list(rs)
            client.close()
            return rows
        except Exception as e:
            self.logger.error(e)

        return []
