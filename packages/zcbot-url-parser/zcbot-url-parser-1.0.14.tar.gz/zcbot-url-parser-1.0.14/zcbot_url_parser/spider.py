import re
import logging
import urllib.parse as parser
from typing import List, Union
from pymongo import MongoClient
from .constant import ZCBOT_PUBLIC_MONGO_URL, ZCBOT_PUBLIC_MONGO_DATABASE, ZCBOT_PUBLIC_MONGO_COLLECTION_SPIDERS, ZCBOT_PUBLIC_MONGO_COLLECTION_RULES
from .parser import _parse_sku_by_param, _parse_sku_by_path
from .utils import singleton, clean_url

LOGGER = logging.getLogger(__name__)


@singleton
class SpiderUrlParser(object):
    """
    常见电商平台商品编码解析规则
    """
    logger = logging.getLogger(__name__)

    def __init__(self, spider_id: Union[str, List], mongo_url: str = None, mongo_database: str = None, mongo_collection_spiders: str = None, mongo_collection_rules: str = None):
        self.spider_id = spider_id
        self.mongo_url = mongo_url or ZCBOT_PUBLIC_MONGO_URL
        self.mongo_database = mongo_database or ZCBOT_PUBLIC_MONGO_DATABASE
        self.mongo_collection_spiders = mongo_collection_spiders or ZCBOT_PUBLIC_MONGO_COLLECTION_SPIDERS
        self.mongo_collection_rules = mongo_collection_rules or ZCBOT_PUBLIC_MONGO_COLLECTION_RULES

        self.rule_map = dict()
        self._init_rule_map()
        self.logger.info(f'===================')
        self.logger.info(f'有效链接解析规则: {len(self.rule_map)}条')
        self.logger.info(f'===================')

    def parse(self, url) -> Union[str, tuple]:
        ec_sku_id = ''
        _url = clean_url(url)
        if _url:
            host = parser.urlparse(_url).hostname
            rule = self.rule_map.get(host)
            if host and rule:
                sku_param = rule.get('sku_param', [])
                if sku_param:
                    ec_sku_id = _parse_sku_by_param(_url, sku_param, None)
                patterns = rule.get('patterns', [])
                if patterns and not ec_sku_id:
                    ec_sku_id = _parse_sku_by_path(_url, patterns, None)

        return ec_sku_id

    def _init_rule_map(self):
        client = MongoClient(self.mongo_url)
        try:
            if isinstance(self.spider_id, list):
                match = {'$in': self.spider_id}
            else:
                match = self.spider_id
            rs = client.get_database(self.mongo_database).get_collection(self.mongo_collection_spiders).aggregate([
                {'$lookup': {'from': self.mongo_collection_rules, 'localField': 'patterns', 'foreignField': '_id', 'as': 'rules'}},
                {'$match': {'_id': match}},
                {'$project': {'rules': 1}}
            ])

            rs = list(rs)
            if rs:
                rows = rs[0].get('rules')
                for row in rows:
                    patterns = []
                    regex_list = row.get('regex', [])
                    for regex in regex_list:
                        try:
                            patterns.append(re.compile(regex))
                        except re.error:
                            LOGGER.error(f'错误规则: regex={regex}, row={row}')

                    plat_code = row.get('plat_code')
                    self.rule_map[row.get('_id')] = {
                        'plat_code': plat_code,
                        'sku_param': row.get('params', []),
                        'patterns': [
                            re.compile(x) for x in row.get('regex', [])
                        ],
                    }
        except Exception as e:
            self.logger.error(e)
        finally:
            try:
                client.close()
            except Exception as e:
                self.logger.error(e)
