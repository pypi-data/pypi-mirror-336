import os

# ZCBOT_PUBLIC_MONGO_URL = os.getenv('ZCBOT_PUBLIC_MONGO_URL') or 'mongodb://public_read:public_read_zsodata@zcbot-inner.mongodb.rds.aliyuncs.com:3717'
ZCBOT_PUBLIC_MONGO_URL = os.getenv('ZCBOT_PUBLIC_MONGO_URL') or 'mongodb://public_read:public_read_zsodata@mongo.zcbot.cn:3717'
ZCBOT_PUBLIC_MONGO_DATABASE = os.getenv('ZCBOT_PUBLIC_MONGO_DATABASE') or 'zcbot_pool'

ZCBOT_PUBLIC_MONGO_COLLECTION_SPIDERS = os.getenv('ZCBOT_PUBLIC_MONGO_COLLECTION_SPIDERS') or 'zcbot_spider'
ZCBOT_PUBLIC_MONGO_COLLECTION_PLATFORMS = os.getenv('ZCBOT_PUBLIC_MONGO_COLLECTION_PLATFORMS') or 'zcbot_platforms'
ZCBOT_PUBLIC_MONGO_COLLECTION_RULES = os.getenv('ZCBOT_PUBLIC_MONGO_COLLECTION_RULES') or 'zcbot_url_parse_rule_v2'
ZCBOT_PUBLIC_MONGO_COLLECTION_FILE_NAME_CONFIG = os.getenv('ZCBOT_PUBLIC_MONGO_COLLECTION_FILE_NAME_CONFIG') or 'zcbot_file_name_config'
ZCBOT_PUBLIC_MONGO_COLLECTION_IMAGE_THUMB_CONFIG = os.getenv('ZCBOT_PUBLIC_MONGO_COLLECTION_IMAGE_THUMB_CONFIG') or 'zcbot_image_thumb_config'
